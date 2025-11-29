import os, Utils, json, sys, subprocess, pkgutil
from pathlib import Path


### GAME DIRECTORY STUFF

CONFIG_FILENAME = Path(os.path.join(Utils.user_path(), ".tomtom4_client_config.json"))
EXPECTED_EXE_NAMES = ["TomTom Flaming Special Archipelago.exe", "TomTomAdventures4AP.exe"]  # tolerate variations
VERSION = None

def determine_version():
    global VERSION
    data = json.loads(pkgutil.get_data(__name__, "archipelago.json").decode())
    VERSION = data["world_version"]

determine_version()

def load_saved_game_dir():
    """Return saved directory Path or None."""
    try:
        if CONFIG_FILENAME.exists():
            data = json.loads(CONFIG_FILENAME.read_text(encoding="utf-8"))
            p = Path(data.get("game_dir", ""))
            v = data.get("version", None)
            if p.exists() and p.is_dir() and v == VERSION:
                return p
    except Exception:
        print("yes: ", CONFIG_FILENAME)
        pass
    return None

def save_game_dir(game_dir: Path):
    """Persist the chosen game_dir for next runs."""
    try:
        CONFIG_FILENAME.write_text(json.dumps({"game_dir": str(game_dir), "version": VERSION}), encoding="utf-8")
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