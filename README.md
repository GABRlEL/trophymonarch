<br/>
<div align="center">
<h3 align="center">Trophy Monarch</h3>
<p align="center">
A Python-based Mario Kart Wii save game editor
for Time Trials trophies in Pulsar mod distributions
<br/>
</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Features](#features)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Example usage](#example-usage)
- [How this tool could be improved](#how-this-tool-could-be-improved)
  - [Known issues](#known-issues)
  - [Improvement ideas](#improvement-ideas)
- [License](#license)
- [Contact](#contact)

## About The Project

Trophy Monarch is a tool, which allows the user to edit the trophy values their leaderboard files (ldb.pul) in the Ghosts folder and update the TROP section in the settings file (usually settings.pul) accordingly. The primary purpose of this is, to recover trophies lost caused by Pulsars design choice of storing ghosts in the settings file, which is overwritten when a Pulsar packs settings or tracks are updated. Additionally it can be used, to recover the trophy state from a lost Ghosts folder.

The tools saves the user from tediously editing the hex manually and checking all leaderboard files manually, prevents human error and serves as a future-proof way for packs with regular updates.

### Features

- Loading and editing trophy 1-4 in the leaderboards (ldb.pul) of a Pulsar pack Ghosts folder
- Set all features for all 4 trophies
- Resolving track IDs by loading a FolderToTrackList (translation) file
- Dynamically updating the settings.pul file
- Display current trophy count based on the checkmarks set in the tool
- Remove trophies and check count of unrecognized tracks based on translation file

### Built With

This project was built with:

- Python
- Tkinter
- ChatGPT o4-mini-high
- GitHub Copilot

Note: The code in this script was authored by AI. I only did prompting, testing and function designing.

## Getting Started

This is a Python script which was tested on Windows 11, Python 3.13.2 & Arch Linux, Python 3.13.3.
To get a local copy up and running follow these simple example steps (installation instructions are Windows-only since I&#39;m not familiar with Linux).

### Prerequisites

This project requires Python and Tkinter to be installed in your system. If you don&#39;t have it installed, you can follow these steps:

- Install [Python](https://www.python.org/downloads/)

- Verify that Python has been installed on your machine by running the following command in your terminal:

  ```
  py --version
  ```
  If Python has been installed correctly, your terminal should display the version of Python installed on your machine.

- Make sure that Tkinter is available by running the following command in your terminal:

  ```
  py -m tkinter
  ```
  If Tkinter is available, a small window should open.

Now you are ready to use the tool!

### Setup

Please follow the following steps for successful usage:

1. **Download the Python file:** Get started by downloading trophymonarch.py, either by pressing on the file in the repository and clicking "Download raw file", or via the link:
   https://github.com/GABRlEL/trophymonarch/raw/refs/heads/main/trophymonarch.py

2. **Run the file:** Either run the file by double-clicking (untested), or by executing the following script trophymonarch.cmd (recommended, provides error output):

   ```
   @echo off
   title Trophymonarch Debug Output
   py trophymonarch.py
   ```
   Script with data above: https://github.com/GABRlEL/trophymonarch/raw/refs/heads/main/trophymonarch.cmd

   Alternatively you can of course open a terminal by right-clicking the folder the script is in and just typing ```py trophymonarch.py```
   
   This sets the title and shows any error output, in case there's issues with the tool.
   In general, any way of running the Python script should do the job.

### Example usage

0. Backup your Ghosts folder and settings.pul (RRSettings.pul for Retro Rewind) before using the tool in the following steps!

1. Open your Ghosts folder

   This can either be found on Dolphin in:
   ```
   Dolphin Emulator\Wii\shared2\Pulsar\PACKNAME\Ghosts
   ```
   Dolphin Emulator folder can be found in either: Documents, %appdata% or in the User folder of your Dolphin install when using portable

   or on Wii:
   ```
   SD Card\PACKNAME\Ghosts
   ```
   You should see lots of entries with IDs now.

3. Open your FolderToTrackName.txt to resolve track names

   This can either be found when using WheelWizard (Retro Rewind) in:
   ```
   Dolphin Emulator\Load\Riivolution\WheelWizard\RetroRewind6\Ghosts\FolderToTrackName.txt
   ```
   Dolphin Emulator folder can be found in either: Documents, %appdata% or in the User folder of your Dolphin install when using portable

   When using Riivolution patches in Dolphin:
   ```
   PACKFOLDER\Ghosts\FolderToTrackName.txt
   ```   

   or on Wii:
   ```
   SD Card\PACKNAME\Ghosts\FolderToTrackName.txt
   ```
   If you can't see track names after loading translations, please verify that the FolderToTrackName.txt file used is correct and current. Contact your pack distributor when in doubt.

4. (Optional next steps) Edit your trophies to your liking. The game modes for the trophy 1-4 are usually in order like they are ingame.

   - **Retro Rewind:** Trophy 1 = 150cc, Trophy 2 = 200cc, Trophy 3 = unused, Trophy 4 = unused
   - **IKW:** Trophy 1 = 150cc, Trophy 2 = 200cc, Trophy 3 = 150cc Feather, Trophy 4 = 200cc Feather

   You can use the Tools menu in the top menu bar for additional functions.
   - "Show Current Trophy Count": This displays how many trophies would be applied in total, if you would modify the settings file with the currently set checkboxes.
   - "Show Unrecognized Tracks": This displays how many tracks couldn't be resolved with the FolderToTrackName.txt
   - "Uncheck Unrecognized Tracks": This removes any checkmarks for tracks which names couldn't be resolved. This feature is useful to not inflate or falsify the total trophy count.
   Make sure to click "Save Changes", if you made any changes to the trophies.
  
5. Open the Tools menu in the top menu bar and click "Update settings file". This feature will update your settings file, to make sure your total trophies and per track trophies are properly displayed. Select your settings.pul (RRSettings.pul for Retro Rewind) and save the changes.

   This can either be found on Dolphin in:
   ```
   Dolphin Emulator\Wii\shared2\Pulsar\PACKNAME\
   ```
   Dolphin Emulator folder can be found in either: Documents, %appdata% or in the User folder of your Dolphin install when using portable

   or on Wii:
   ```
   SD Card\PACKNAME\
   ```

6. Verify, that your trophies are back ingame. If it didn't work, please revert to the backup from Step 0 and try again, to make sure that you don't play with a corrupted settings file.


## How this tool could be improved

### Known issues
- The tool severely lacks error handling. Behaviour outside of the intended usage or scenarios is untested, unrecommended and possibly unsafe to data.
- This tool uses hex 47 50 00 00 00 00 00 01 as a terminator. Therefore any track with the track ID 47 50 00 00 will likely make the tool completely unusable. In this case, please contact your pack distributor to get the ID changed. This terminator usage might be wrong or unsafe but has been tested and is known to work on RR and IKW as of May 2025. As of now, I'm unsure whether this track ID is a) possible and b) if a Pulsar pack would even properly survive saving trophies if this track ID is present.
- Window sizing is jank.
- Paths in the message box don't display properly. This doesn't affect the function of the program.

### Improvement ideas

I don't plan on improving this tool further - I don't mind forks though.

- Add error handling in all places
- Make the entire thing look better
- Add feature to remove outdated track folders entirely
- Resolve outdated track folder names by reading the ldb.pul
- Add drag-and-drop (would require dnd and therefore a dependency to be installed)
- Provide compiled EXE to remove the requirement of running the Python script
- Add better guidance in the tool
- Fix the 47 50 00 00 kill screen

Unless there's something fundamentally broken with this, I personally don't plan to make any changes unless they're easy and I still have the motivation to do it.

## License

I will not provide an actual license for this product, as I'm unsure of the situation with AI generated code. What I can say is, that I don't mind if this tool is forked and improved upon, as long as it stays open-source. I would appreciate if you could atleast credit me for the idea in your project. If the AI code situation wasn't there, this would probably be GPLv3.

## Contact

If you have any questions or suggestions, feel free to reach out at any of my socials at:

- All my socials: [Solo @Gab](https://solo.to/Gab)

This ReadMe was inspired from [makeread.me](https://www.makeread.me/) 🚀
