import typing
from worlds.generic.Rules import add_rule, set_rule
from .Locations import stage_locations

def set_rules(world, options, player):
    for stage_name in stage_locations:
        base_name = stage_name.replace(" Complete", "")
        if base_name != "Underground World":  # Underground is always open
            access_item = f"{base_name} Access"
            set_rule(world.menu_entrances[base_name],
                     lambda state, item=access_item: state.has(item, player))
    
    # Extra Jump Power-Up requirement for certain worlds 
    # Map 1 requires Jump for these worlds which means the whole region gets gated behind it
    jump_locked_stages = ["Space World", "Fire Hydrent World", "Mars"]
    for stage in jump_locked_stages:
        add_rule(world.menu_entrances[stage],
                 lambda state: state.has("Jump Power-Up", player))

    # The rest of Clouds Requirements
    set_rule(world.get_location("Above the Clouds Complete", player),
             lambda state: state.has("Jump Power-Up", player))

    # Secret exit requirements
    set_rule(world.get_location("Dirty World Secret Exit", player),
             lambda state: state.has("Jump Power-Up", player))
    set_rule(world.get_location("Jungle World Secret Exit", player),
             lambda state: state.has("Jump Power-Up", player) and state.has("Key", player))
    set_rule(world.get_location("Maze World Secret Exit", player),
             lambda state: state.has("Key", player))
    # set_rule(world.get_location("The Jungle Inferno Secret Exit", player),
    #          lambda state: state.has("Jump Power-Up", player))

    # House cleaned requirements
    set_rule(world.get_location("House Cleaned", player),
             lambda state: state.has("Hose", player))

    # Victory
    goal = getattr(options, "goal")

    if goal == 0:  # House Cleaned only
        world.completion_condition[player] = lambda state: state.has("House Cleaned", player)

    elif goal == 1:  # Tyler Defeated only
        world.completion_condition[player] = lambda state: state.has("Tyler Defeated", player)

    elif goal == 2:  # Both
        world.completion_condition[player] = lambda state: (
            state.has("House Cleaned", player) and state.has("Tyler Defeated", player)
        )

    # DEBUG
    #debug_reachability(world, player)


def debug_reachability(world, player):
    print("\n--- Reachability Debug ---")
    state = world.get_all_state(False)  # initial state, no items collected
    for entrance_name, entrance in world.menu_entrances.items():
        print(f"{entrance_name}: {'reachable' if entrance.can_reach(state) else 'locked'}")
    print("--------------------------\n")
