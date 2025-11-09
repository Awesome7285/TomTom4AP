from typing import List, Dict, Tuple
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Items import TomTom4Item, stage_items, other_items, filler_items, all_items, starting_items, item_table as item_name_to_id
from .Locations import TomTom4Location, stage_locations, extra_locations, location_table as location_name_to_id
from .Regions import create_regions
from .Rules import set_rules
from .Options import TomTom4Options

from BaseClasses import Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld


def run_client():
    from .Client import main as client_main
    launch_subprocess(client_main)

components.append(Component("TomTom 4 Client", func=run_client, component_type=Type.CLIENT))


class TomTom4World(World):
    """ 
    TomTom Adventures Flaming Special game description.
    """

    game: str = "TomTom Adventures Flaming Special"
    topology_present = False
    # web = KTANEWeb()

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    required_client_version: Tuple[int, int, int] = (0, 0, 1)

    options_dataclass = TomTom4Options

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_item(self, name: str) -> Item:
        classification = ItemClassification.progression
        if name in filler_items:
            classification = ItemClassification.filler
        # elif name in stage_items:
        #     classification = ItemClassification.progression_skip_balancing
        return TomTom4Item(name, classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        item_pool: List[TomTom4Item] = []
        #print([i.name for i in self.multiworld.get_locations()])

        # Add Underground World Access to starting items
        for item in starting_items:
            self.multiworld.push_precollected(self.create_item(item))

        # Add victory items
        goal = getattr(self.options, "goal")
        if goal == 1 or goal == 2:
            self.multiworld.get_location("The End Complete", self.player).place_locked_item(self.create_item("Tyler Defeated"))
        if goal == 0 or goal == 2:
            self.multiworld.get_location("House Cleaned", self.player).place_locked_item(self.create_item("House Cleaned"))

        # Add all access keys
        item_pool += [self.create_item(item) for item in stage_items]

        # Add all misc items
        item_pool += [self.create_item(item) for item in other_items]

        # Fill any empty locations with filler items.
        while len(item_pool) < len(self.multiworld.get_unfilled_locations(player=self.player)):
            item_pool.append(self.create_item(filler_items[0])) # self.get_filler_item_name()

        self.multiworld.itempool += item_pool

    def generate_basic(self):
        pass

    def generate_early(self):
        pass

    def fill_slot_data(self):
        slot_data: Dict[str, object] = {
            "goal": self.options.goal.value,
            "DeathLink": self.options.death_link.value == True,
        }

        return slot_data