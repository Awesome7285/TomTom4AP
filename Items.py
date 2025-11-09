from BaseClasses import Item

BASE_ID = 2247201

class TomTom4Item(Item):
    game: str = "TomTom Adventures Flaming Special"

stage_items = [
    "Dirty World Access",
    "Desert World Access",
    "School Access",
    "Above the Clouds Access",
    "Snow World Access",
    "Space World Access",
    "Condensed Milk World Access",
    "Rumi's Palace Access",
    "Fire Hydrent World Access",
    "Maze World Access",
    "Mars Access",
    "Jungle World Access",
    "Tetris World Access",
    "Christmas World Access",
    "The Jungle Inferno Access",
    "Mexico Access",
    "Pythag World Access",
    "Lava World Access",
    "Purple Abyss Access",
    "The End Access",
    "Bridge World Access"
]

starting_items = [
    "Underground World Access"
]

other_items = [
    "Jump Power-Up",
    "Key",
    "Hose"
]

victory_items = [
    "Tyler Defeated",
    "House Cleaned"
]

filler_items = [
    "Life",
    "Declan Power-Up"
]

all_items = starting_items + stage_items + other_items + victory_items + filler_items

item_table = {name: id for id, name in enumerate(all_items, BASE_ID)}

item_table = {
    "Underground World Access": BASE_ID,
    "Dirty World Access": BASE_ID+1,
    "Desert World Access": BASE_ID+2,
    "School Access": BASE_ID+3,
    "Above the Clouds Access": BASE_ID+4,
    "Snow World Access": BASE_ID+5,
    "Space World Access": BASE_ID+6,
    "Condensed Milk World Access": BASE_ID+7,
    "Rumi's Palace Access": BASE_ID+8,
    "Fire Hydrent World Access": BASE_ID+9,
    "Maze World Access": BASE_ID+10,
    "Mars Access": BASE_ID+11,
    "Jungle World Access": BASE_ID+12,
    "Tetris World Access": BASE_ID+13,
    "Christmas World Access": BASE_ID+14,
    "The Jungle Inferno Access": BASE_ID+15,
    "Mexico Access": BASE_ID+16,
    "Pythag World Access": BASE_ID+17,
    "Lava World Access": BASE_ID+18,
    "Purple Abyss Access": BASE_ID+19,
    "The End Access": BASE_ID+20,
    "Bridge World Access": BASE_ID+21,
    "Jump Power-Up": BASE_ID+22,
    "Key": BASE_ID+23,
    "Hose": BASE_ID+24,
    "Tyler Defeated": BASE_ID+25,
    "House Cleaned": BASE_ID+26,
    "Life": BASE_ID+27,
    "Declan Power-Up": BASE_ID+28,
}