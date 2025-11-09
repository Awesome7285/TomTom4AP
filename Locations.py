from BaseClasses import Location
from .Items import BASE_ID

class TomTom4Location(Location):
    game: str = "TomTom Adventures Flaming Special"

# Stage completion locations
stage_locations = [
    "Underground World Complete",
    "Dirty World Complete",
    "Desert World Complete",
    "School Complete",
    "Above the Clouds Complete",
    "Snow World Complete",
    "Space World Complete",
    "Condensed Milk World Complete",
    "Rumi's Palace Complete",
    "Fire Hydrent World Complete",
    "Maze World Complete",
    "Mars Complete",
    "Jungle World Complete",
    "Tetris World Complete",
    "Christmas World Complete",
    "The Jungle Inferno Complete",
    "Mexico Complete",
    "Pythag World Complete",
    "Lava World Complete",
    "Purple Abyss Complete",
    "The End Complete",
    "Bridge World Complete"
]

# Extra locations tied to their respective worlds
extra_locations = {
    "Dirty World": ["Dirty World Secret Exit"],
    "Maze World": ["Maze World Secret Exit"],
    "Jungle World": ["Jungle World Secret Exit"],
    "The Jungle Inferno": ["The Jungle Inferno Secret Exit"],
    "Above the Clouds": ["Jump Power-Up Switch"],
    "Rumi's Palace": ["Rumi's Palace Key", "Life from Rumi"],
    "The End": ["The End Hose"],
    "Underground World": ["House Cleaned"]
}


# Build the full ordered location list
all_locations = []
for stage in stage_locations:
    all_locations.append(stage)
    base_name = stage.replace(" Complete", "")
    if base_name in extra_locations:
        all_locations.extend(extra_locations[base_name])

# Assign location IDs
location_table = {name: id for id, name in enumerate(all_locations, BASE_ID)}

location_table = {
    "Underground World Complete": BASE_ID,
    "Dirty World Complete": BASE_ID+1,
    "Desert World Complete": BASE_ID+2,
    "School Complete": BASE_ID+3,
    "Above the Clouds Complete": BASE_ID+4,
    "Snow World Complete": BASE_ID+5,
    "Space World Complete": BASE_ID+6,
    "Condensed Milk World Complete": BASE_ID+7,
    "Rumi's Palace Complete": BASE_ID+8,
    "Fire Hydrent World Complete": BASE_ID+9,
    "Maze World Complete": BASE_ID+10,
    "Mars Complete": BASE_ID+11,
    "Jungle World Complete": BASE_ID+12,
    "Tetris World Complete": BASE_ID+13,
    "Christmas World Complete": BASE_ID+14,
    "The Jungle Inferno Complete": BASE_ID+15,
    "Mexico Complete": BASE_ID+16,
    "Pythag World Complete": BASE_ID+17,
    "Lava World Complete": BASE_ID+18,
    "Purple Abyss Complete": BASE_ID+19,
    "The End Complete": BASE_ID+20,
    "Bridge World Complete": BASE_ID+21,
    "Dirty World Secret Exit": BASE_ID+22,
    "Maze World Secret Exit": BASE_ID+23,
    "Jungle World Secret Exit": BASE_ID+24,
    "The Jungle Inferno Secret Exit": BASE_ID+25,
    "Jump Power-Up Switch": BASE_ID+26,
    "Rumi's Palace Key": BASE_ID+27,
    "The End Hose": BASE_ID+28,
    "House Cleaned": BASE_ID+29,
    "Life from Rumi": BASE_ID+30
}