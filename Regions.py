from BaseClasses import MultiWorld, Region, Entrance
from .Locations import TomTom4Location, stage_locations, extra_locations, location_table

def create_regions(world: MultiWorld, player: int):
    # Menu region
    menu = Region("Menu", player, world)
    world.regions.append(menu)

    # Store all entrances from Menu for use in Rules.py
    world.menu_entrances = {}

    # Create each world region and connect it from Menu
    for stage_name in stage_locations:
        base_name = stage_name.replace(" Complete", "")
        region = Region(base_name, player, world)

        # Add the "Complete" location
        region.locations.append(
            TomTom4Location(player, stage_name, location_table[stage_name], region)
        )

        # Add any extra locations for this world
        if base_name in extra_locations:
            for loc_name in extra_locations[base_name]:
                region.locations.append(
                    TomTom4Location(player, loc_name, location_table[loc_name], region)
                )

        # Add region to the world
        world.regions.append(region)

        # Create an entrance from Menu to this stage
        entrance = Entrance(player, f"To {base_name}", menu)
        menu.exits.append(entrance)
        entrance.connect(region)

        # Save the entrance for Rules.py
        world.menu_entrances[base_name] = entrance
