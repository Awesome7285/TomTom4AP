# TomTom Flaming Special MultiWorld Setup Guide

## Required Software



## Configuring a YAML File

### What is a YAML and why do I need one?

The [basic multiworld setup guide](https://archipelago.gg/tutorial/Archipelago/setup/en) explains the use of a YAML and
the way they are used.

### How do I get a YAML for Keep Talking and Nobody Explodes?

Since this game isn't fully released yet, the only way to get a YAML template is to generate it from the Archipelago
Software.

1. Install the [latest version of Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Remember where 
the installation folder is, because it will be needed.
2. In your Archipelago folder, navigate to the "custom_worlds" folder and add ktane.apworld. If you have a previous 
version of ktane.apworld installed in the "lib/worlds" directory, you will need to remove it.
3. Navigate back to your Archipelago folder and launch ArchipelagoLauncher.exe. A window should appear. In this window,
on the left, click on "Generate Template Options". It will open a window with a lot of .yaml files.
4. Locate the one that's named "Keep Talking and Nobody Explodes.yaml". This is your base template. You can create a 
copy of it.

## Generating a Randomized Playthrough

Since Keep Talking and Nobody Explodes isn't fully released yet, the only way to generate a seed containing the game
must be locally.

1. Follow steps 1 and 2 from the previous section to add the .apworld to the generation list.
2. In your Archipelago folder, navigate to the "Players" folder. In this folder, add all the YAMLs that will be used to
generate the MultiWorld randomized seed.
3. Navigate back to your Archipelago folder and launch ArchipelagoGenerate.exe. The program will execute and create a 
new seed with all the YAML files present in the "Players" folder. The generated seed will be in the "output" folder.

Please note that the generation may fail. If it fails because of invalid placement, please try again and it should work.

## Hosting a Game on a Server

The seed must be hosted on a server to be playable. The easiest possibilities are using the website or running a local 
server.

### Using the Archipelago Website to host a seed

Once the seed is generated:
1. On the Archipelago website, go under the [Host Game](https://archipelago.gg/uploads) tab.
2. Click the "Upload File" button and select your seed.
3. Create a new room. This room will give the ip, port (usually archipelago.gg:XXXXX) and slot name to connect to it.

### Running a local server to host a seed
Once the seed is generated:
1. In your Archipelago folder, launch ArchipelagoServer.exe. A command prompt will open.
2. A file prompt will also open. Select your seed.
3. The server is now open. The slot names will be the same as the YAMLs' name and the ip will be your computer ip. By
default, the port should be 38281, but it will be shown in the command prompt window.

Please remember the 2 following things:
1. If you are not on the same network, the port will need to be forwarded by your router.
2. Never share your personal computer ip with a stranger.

## Joining a MultiWorld Game

Since this game is based for a defuser and an expert, they have two different ways of joining a game.

