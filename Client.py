import subprocess, os, sys, Utils, asyncio, configparser, multiprocessing, json
import colorama
from pathlib import Path
from collections import Counter

from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser, logger, ClientStatus
from .Items import item_table, BASE_ID
from .Locations import location_table, stage_locations

# CONFIG filename (stored in user home)
CONFIG_FILENAME = Path(os.path.join(Utils.user_path(), ".tomtom4_client_config.json"))
EXPECTED_EXE_NAMES = ["TomTom Flaming Special Archipelago.exe"]  # tolerate variations

def load_saved_game_dir():
    """Return saved directory Path or None."""
    try:
        if CONFIG_FILENAME.exists():
            data = json.loads(CONFIG_FILENAME.read_text(encoding="utf-8"))
            p = Path(data.get("game_dir", ""))
            if p.exists() and p.is_dir():
                return p
    except Exception:
        print("yes: ", CONFIG_FILENAME)
        pass
    return None

def save_game_dir(game_dir: Path):
    """Persist the chosen game_dir for next runs."""
    try:
        CONFIG_FILENAME.write_text(json.dumps({"game_dir": str(game_dir)}), encoding="utf-8")
    except Exception as e:
        print("Warning: failed to save tomtom4 client config:", e)

def _is_valid_game_exe(path: Path):
    """Simple heuristic: path is file and name matches expected exe name or contains 'tomtom'."""
    if not path.exists() or not path.is_file():
        return False
    name = path.name.lower()
    if any(exe.lower() == name for exe in EXPECTED_EXE_NAMES):
        return True
    return False

def prompt_for_exe_via_gui(initialdir=None):
    """Open a Tk file dialog to pick the executable. Returns Path or None."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    root = tk.Tk()
    root.withdraw()  # hide main window
    root.attributes("-topmost", True)  # bring dialog to front on Windows
    filetypes = [("Executable", "*.exe"), ("All files", "*.*")]
    try:
        selected = filedialog.askopenfilename(title="Select TomTom4 executable",
                                              initialdir=initialdir or str(Path.home()),
                                              filetypes=filetypes)
    finally:
        try:
            root.destroy()
        except Exception:
            pass

    if not selected:
        return None
    return Path(selected)

def prompt_for_exe_via_console(initialdir=None):
    """Fallback: ask user to paste the full path in the console."""
    prompt = "Enter full path to TomTom4 executable (or blank to cancel): "
    if initialdir:
        print("Please select TomTom4 executable. Suggested dir:", initialdir)
    val = input(prompt).strip()
    if not val:
        return None
    return Path(val)

def ask_user_for_game_exe():
    """
    Try GUI picker first, then console. Validate selection and return (exe_path, game_dir) or (None, None).
    """
    # Try GUI
    exe_path = prompt_for_exe_via_gui()
    if exe_path and _is_valid_game_exe(exe_path):
        return exe_path.resolve(), exe_path.parent.resolve()

    # GUI either cancelled or picked invalid file. Ask via console (if interactive).
    if sys.stdin and sys.stdin.isatty():
        exe_path = prompt_for_exe_via_console()
        if exe_path and _is_valid_game_exe(exe_path):
            return exe_path.resolve(), exe_path.parent.resolve()

    # last attempt: search current directory and parent for likely exe
    cwd = Path.cwd()
    for candidate in cwd.iterdir():
        if candidate.is_file() and _is_valid_game_exe(candidate):
            return candidate.resolve(), candidate.parent.resolve()

    return None, None

def ensure_game_dir():
    """
    Return Path to game directory. Load saved config or prompt user. Save result.
    """
    saved = load_saved_game_dir()
    if saved:
        # quick sanity check: the exe must exist in that dir
        for name in EXPECTED_EXE_NAMES:
            candidate = saved / name
            if candidate.exists() and candidate.is_file():
                return saved
        # if saved dir no longer valid, fall through to prompt

    exe_path, game_dir = ask_user_for_game_exe()
    if exe_path and game_dir:
        save_game_dir(game_dir)
        return game_dir

    return None

def launch_game(exe_path: Path = None, game_dir: Path = None):
    """
    Launch the game exe with working directory set to game_dir (or exe parent).
    exe_path optional; if omitted the function will try to find an exe inside game_dir.
    """
    if game_dir is None and exe_path is None:
        raise ValueError("Either exe_path or game_dir must be provided")
    if game_dir is None:
        game_dir = exe_path.parent
    if exe_path is None:
        # try to find an exe inside game_dir
        for name in EXPECTED_EXE_NAMES:
            candidate = game_dir / name
            if candidate.exists():
                exe_path = candidate
                break
        if exe_path is None:
            # choose any .exe in folder
            candidates = list(game_dir.glob("*.exe"))
            exe_path = candidates[0] if candidates else None
    if not exe_path or not exe_path.exists():
        raise FileNotFoundError(f"Could not find executable in {game_dir}")

    # Launch and return Popen object
    popen = subprocess.Popen([str(exe_path)], cwd=str(game_dir))
    return popen

def clear_ini(ini_dir):
    if os.path.exists(ini_dir):
        os.remove(ini_dir)
    config = configparser.ConfigParser()
    config.add_section("Items")
    config.add_section("Locations")
    with open(ini_dir, "w") as f:
        config.write(f)

def read_ini_section(ini_dir, section):
    config = configparser.ConfigParser()
    config.read(ini_dir)
    return dict(config[section]) if section in config else {}

def write_ini(ini_dir, section, key, value):
    config = configparser.ConfigParser()
    if os.path.exists(ini_dir):
        config.read(ini_dir)
    if section not in config:
        config[section] = {}
    config[section][key] = str(value).lower()

    tmp = ini_dir + ".tmp"
    with open(tmp, "w") as f:
        config.write(f)
    os.replace(tmp, ini_dir)

class TomTom4Context(CommonContext):
    game = "TomTom Adventures Flaming Special"
    items_handling = 0b111
    game_dir = None
    ini_file = "tomtom4_ap.ini"
    ini_dir = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.checked_locations = set()
        self.is_connected = False
        self.options = None

        self.all_location_ids = None
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.previous_location_checked = None
        self.location_mapping = None

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"TomTom 4 Client"
        return ui

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        """
        Manage the package received from the server
        """
        
        if cmd == "Connected":
            self.previous_location_checked = args['checked_locations']
            self.all_location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.options = args["slot_data"] # Yaml Options
            self.is_connected = True

            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["TomTom Adventures Flaming Special"]}]))
            clear_ini(self.ini_dir)
            asyncio.create_task(self.update_checked_locations(self.previous_location_checked))

        if cmd == "ReceivedItems":
            print("got:", args["items"])
            asyncio.create_task(self.update_received_items(args["items"]))

        elif cmd == "DataPackage":
            if not self.all_location_ids:
                # Connected package not received yet, wait for datapackage request after connected package
                return
            self.location_name_to_ap_id = args["data"]["games"]["TomTom Adventures Flaming Special"]["location_name_to_id"]
            self.location_name_to_ap_id = {
                name: loc_id for name, loc_id in
                self.location_name_to_ap_id.items() if loc_id in self.all_location_ids
            }
            self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
            self.item_name_to_ap_id = args["data"]["games"]["TomTom Adventures Flaming Special"]["item_name_to_id"]
            self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}

            print(self.location_name_to_ap_id)
            print(self.location_ap_id_to_name)
            print(self.item_name_to_ap_id)
            print(self.item_ap_id_to_name)

            asyncio.create_task(self.check_for_locations_loop())

    def update_ini_file(self) -> None:
        """Updates the INI file directory"""
        self.ini_dir = os.path.join(self.game_dir, self.ini_file)

    async def update_checked_locations(self, locations):
        """Updates the locations already completed from initial datapackage"""
        print(locations)
        for loc in locations:
            write_ini(self.ini_dir, "Locations", str(loc-BASE_ID+1), 1)
    
    async def update_received_items(self, items):
        """Updates items received to the INI"""
        new_items = [item.item-BASE_ID+1 for item in items]
        received = dict(Counter(new_items))
        for item_id, amount in received.items():
            write_ini(self.ini_dir, "Items", str(item_id), amount)

        # Check for victory
        if self.item_name_to_ap_id:
            received_ids = {item.item for item in self.items_received}
            if self.options["goal"] == 0:
                if self.item_name_to_ap_id["House Cleaned"] in received_ids:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            if self.options["goal"] == 1:
                if self.item_name_to_ap_id["Tyler Defeated"] in received_ids:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            if self.options["goal"] == 2:
                if self.item_name_to_ap_id["Tyler Defeated"] in received_ids and self.item_name_to_ap_id["House Cleaned"] in received_ids:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    
    async def check_for_locations_loop(self):
        """Permanent Loop that checks the users ini file for new locations to send"""
        while True:
            await asyncio.sleep(1.3)
            new_locations = []
            written_locations = read_ini_section(self.ini_dir, "Locations")
            for loc_id, obtained in written_locations.items():
                actual_id = int(loc_id)+BASE_ID-1
                if obtained == "1" and actual_id not in self.previous_location_checked:
                    new_locations.append(actual_id)

            if new_locations:
                self.previous_location_checked = self.previous_location_checked + new_locations
                await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])


def main():
    Utils.init_logging("TomTom 4 Client")
    parser = get_base_parser()
    args = sys.argv[1:]
    if "TomTom 4 Client" in args:
        args.remove("TomTom 4 Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()
        ctx = TomTom4Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        
        game_dir = ensure_game_dir()
        if not game_dir:
            print("No TomTom4 executable selected. Client will not auto-launch game.")
        else:
            try:
                popen = launch_game(game_dir=game_dir)
                print("Launched game from:", game_dir)
            except Exception as e:
                print("Failed to launch game:", e)
        ctx.game_dir = str(game_dir) if game_dir else None
        ctx.update_ini_file()

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

    colorama.init()
    asyncio.run(_main())
    colorama.deinit()

    

if __name__ == "__main__":
    main()