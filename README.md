# Game Randomizer
Tired of picking the next game to play? I certainly was after running a weekley Jackbox Games night since the start of the pandemic. So I made this little GUI game picker to make the process easier.

This app takes a list of games provided in a JSON file and selects them at random using either the GUI or CLI interface. The games are weighted by user ranking within the JSON file and the app attempts to play all games somewhat equally. The randomizer will only pick games that support the current number of players. By default, it will not repeat the same game during a single session. Play stats are saved to a file to keep track of how many times each game has been played.

# Install
To run the application, you first need to ensure Python 3 is installed on your system, then you can either clone the repo or install the package using pip. 

## GIT Clone
To install a copy of the application from Github:

1. Clone the repository to your computer  
```git clone git@github.com:matazar/game_randomizer.git game_randomizer```
2. Change to the game_randomizer directory  
```cd game_randomizer```
3. Install the game randomizer application  
```python3 setup.py install```

## PIP
To install the application using pip:

1. Download the latest release from the (releases)[https://github.com/matazar/game_randomizer/releases] page
2. Install using pip:
```pip3 install game_randomizer-<version>.tar.gz```

# Games Lists
There are currenty two game lists available:  

1. jackbox_games - Which contains all the online multiplayer games from the Jackbox Party Pack series.
2. boardgames - Which contains a selection of board games I own.

The json files and banner images are currently stored in the python package assets folder found under game_randomizer/assets folder found under the python site-packages. It's possible to add additional game lists by adding a json file to the folder and banner images to a subfolder within. Future releases should allow for custom game lists to be stored in a different location.

# Usage
You can run the game application in GUI or CLI mode by running the following commands with in the command prompt or terminal.

GUI:  
```game_randomizer jackbox_games```  
CLI:   
```game_randomizer -c jackbox_games```  

# License
Code in this project is MIT licensed.
