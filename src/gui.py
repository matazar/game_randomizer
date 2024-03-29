import tkinter as tk
import PIL.Image
import PIL.ImageTk
import os
import random
import time
import subprocess
import platform
from pkg_resources import resource_filename


README = """
Game Randomizer
===============

A simple GUI app for selecting a random game
based on a JSON file of games.

"""


class GUI(object):
    """
    Base class for shared GUI functionality.
    """

    TITLE = "Window Title"
    WIDTH = 200
    HEIGHT = 200
    BACKGROUND = 'grey25'
    LOGO = None

    def __init__(self):
        """
        Create the main app window/frame.
        """
        # Create the main app window
        self.root_window()
        self.frames = {}
        self.mainframe = self.frame_init()
        self.frame_layout()

    def __call__(self):
        """
        Run the GUI.
        """
        self.root.mainloop()

    def root_window(self):
        """
        Set up the root window.
        """
        self.root = tk.Tk()
        self.root.title(self.title)
        # Only include a logo if one is specified.
        if self.default_img:
            ico = tk.PhotoImage(file=self.default_img)
            self.root.iconphoto(False, ico)
        self.root.configure(background=self.background_colour)
        self.root.geometry('%sx%s' % (self.window_width, self.window_height))
        self.root.resizable(False, False)

    def frame_init(self):
        """
        Creates a frame based on our default settings.
        """
        frame = tk.Frame(self.root, width=self.window_width,
                         height=self.window_height,
                         background=self.background_colour)
        frame.grid(column=0, row=0, sticky="nsew",)
        return frame

    def frame_layout(self):
        """
        Sets the frame layout.
        """
        pass

    def apply_settings(self):
        """
        Apple the class settings to the GUI.
        """
        # Set the title
        self.title = self.TITLE
        # Set up the main window
        self.default_img = self.LOGO
        self.window_height = self.HEIGHT
        self.window_width = self.WIDTH
        self.background_colour = self.BACKGROUND


class JSONGUI(GUI):
    """
    GUI client for selecting a .json file.
    """

    TITLE = "Select Game List"
    WIDTH = 340
    HEIGHT = 180
    BACKGROUND = 'grey25'

    def __init__(self):
        """
        Create some variables and set up the GUI.
        """
        self.selected = None
        # Retrieve list of .json files in the directory
        self.assets_dir = resource_filename('game_randomizer', 'assets')
        self.json_files = [f[:-5] for f in os.listdir(self.assets_dir)
                           if f.endswith('.json')]
        # Apply class specific settings.
        self.apply_settings()
        # Do the normal GUI setup
        super().__init__()

    def __call__(self):
        """
        Run the GUI, return the selected .json file.
        """
        super().__call__()
        return self.selected

    def frame_layout(self):
        """
        Sets the frame layout.
        """
        # Label for json dropdown selector
        self.label_dropdown = tk.Label(self.mainframe, text="Select Games: ",
                                       background=self.background_colour,
                                       font=("Arial", 12), fg="white")
        self.label_dropdown.grid(row=1, column=0, columnspan=2,
                                 padx=10, pady=(20, 10))
        # Variable to hold the selected file.
        self.selected_file = tk.StringVar(self.mainframe)
        # Default to jackbox games if it exists, otherwise first in list.
        if self.json_files:
            if 'jackbox_games' in self.json_files:
                self.selected_file.set('jackbox_games')
            else:
                self.selected_file.set(self.json_files[0])
        else:
            self.selected_file.set("No .json files found")
            self.json_files = ["No .json files found"]
        # Set up the dropdown menu.
        self.dropdown = tk.OptionMenu(self.mainframe, self.selected_file,
                                      *self.json_files)
        self.dropdown.configure(background=self.background_colour,
                                highlightcolor=self.background_colour,
                                highlightthickness=0, width=15,
                                font=("Arial", 12), fg="white")
        self.dropdown.grid(row=1, column=2, columnspan=3)

        # Label for assets folder.
        self.label_open_folder = tk.Label(self.mainframe,
                                          text="Browse Game Data: ",
                                          background=self.background_colour,
                                          font=("Arial", 12), fg="white",
                                          height=3)
        self.label_open_folder.grid(row=2, column=0, columnspan=3, padx=10)
        # Open assets folder button.
        self.open_folder_btn = tk.Button(self.mainframe, text='\U0001F4C1',
                                         command=self.open_folder,
                                         font=("Arial", 12), fg="white")
        self.open_folder_btn.configure(background=self.background_colour,
                                       highlightcolor=self.background_colour,
                                       highlightthickness=0)
        self.open_folder_btn.grid(row=2, column=3)
        # Load button
        self.load_btn = tk.Button(self.mainframe, text="Load",
                                  command=self.select,
                                  font=("Arial", 12), fg="white")
        self.load_btn.configure(background=self.background_colour,
                                highlightcolor=self.background_colour,
                                highlightthickness=0)
        self.load_btn.grid(row=3, column=1, pady=15)
        # Exit button
        self.exit_btn = tk.Button(self.mainframe, text="Exit",
                                  command=self.exit,
                                  font=("Arial", 12), fg="white")
        self.exit_btn.configure(background=self.background_colour,
                                highlightcolor=self.background_colour,
                                highlightthickness=0)
        self.exit_btn.grid(row=3, column=3)

    def open_folder(self):
        """
        Opens the folder containing the .json files.
        """
        if platform.system() == "Windows":
            os.startfile(self.assets_dir)
        elif platform.system() == "Darwin":  # for MacOS
            subprocess.Popen(["open", self.assets_dir])
        else:  # assumed to be Linux/Unix
            subprocess.Popen(["xdg-open", self.assets_dir])

    def select(self):
        """
        Get the selected .json file and exit the GUI.
        """
        self.selected = self.selected_file.get()
        return self.exit()

    def exit(self):
        """
        Exit the GUI.
        """
        self.root.destroy()
        return self.selected


class RandomGUI(GUI):
    """
    GUI client for the game randomizer.
    """

    TITLE = "Game Randomizer"
    WIDTH = 480
    HEIGHT = 620
    BACKGROUND = 'grey25'

    def __init__(self, randomizer):
        """
        Set up some basic variables for the GUI
        """
        # Set randomize variable.
        self.randomizer = randomizer
        # Get our settings.
        self.game_setting = randomizer.settings()
        self.default_subheader = 'Number of players: '
        self.default_description = ' '
        # Set player info
        self.default_players = self.game_setting['Default_Players']
        self.max_players = self.game_setting['Max_Players']
        # Number of random games to display before the actual pick.
        self.pretty_roll_count = 75
        # Set size/background
        self.apply_settings()
        # Set the title based off the json file.
        self.title = self.game_setting['Title']
        # Set up logo path.
        self.default_img = \
            resource_filename('game_randomizer',
                              os.path.join(
                                  'assets',
                                  self.game_setting['Image_Directory'],
                                  self.game_setting['Logo']))
        # Do the normal GUI setup
        super().__init__()

    def frame_layout(self):
        """
        Sets the frame layout.
        """
        # Image
        img = PIL.Image.open(self.default_img)
        img = img.resize((420, 192), PIL.Image.Resampling.LANCZOS)
        photo = PIL.ImageTk.PhotoImage(img)
        self.banner = tk.Label(self.mainframe, image=photo,
                               background=self.background_colour)
        self.banner.image = photo
        self.banner.grid(row=0, column=0, pady=20, padx=25, columnspan=3)
        # Header
        self.header = tk.StringVar()
        self.header.set(self.title)
        header = tk.Label(self.mainframe, textvariable=self.header,
                          font=('Arial', 18),
                          background=self.background_colour)
        header.grid(row=1, column=0, pady=0, columnspan=3)
        # Subheader
        self.subheader = tk.StringVar()
        self.subheader.set(self.default_subheader)
        self.subheader_label = tk.Label(self.mainframe,
                                        textvariable=self.subheader,
                                        font=('Arial', 10),
                                        background=self.background_colour)
        self.subheader_label.grid(row=2, column=0, pady=0, columnspan=2)
        self.players = tk.IntVar(self.mainframe)
        self.players.set(self.default_players)  # default players
        player_options = list(range(2, self.max_players + 1))
        self.player_prompt = tk.OptionMenu(self.mainframe, self.players,
                                           *player_options)
        self.player_prompt.configure(background=self.background_colour,
                                     highlightcolor=self.background_colour,
                                     highlightthickness=0)
        self.player_prompt['menu'].configure(background=self.background_colour,
                                             activeborderwidth=0,
                                             borderwidth=0)
        self.player_prompt.grid(row=2, column=2, pady=20,
                                columnspan=1, sticky='w')
        # Description
        self.description = tk.StringVar()
        self.description.set(self.default_description)
        self.desc_label = tk.Label(self.mainframe,
                                   textvariable=self.description,
                                   font=('Arial', 10),
                                   wraplength=420, height=5,
                                   background=self.background_colour)
        # Options
        self.enable_pretty_roll = tk.IntVar(value=1)
        self.proll_check = tk.Checkbutton(self.mainframe,
                                          text='Pizzazz',
                                          variable=self.enable_pretty_roll,
                                          foreground='black',
                                          background=self.background_colour)
        self.proll_check.grid(row=4, column=0, pady=0, columnspan=3)
        self.repeat_option = tk.IntVar(value=1)
        self.repeat_check = tk.Checkbutton(self.mainframe,
                                           text='Exclude last game played',
                                           variable=self.repeat_option,
                                           foreground='black',
                                           background=self.background_colour)
        self.repeat_check.grid(row=5, column=0, pady=0, columnspan=3)
        # Occurrences
        self.occurrences = tk.StringVar()
        self.occurrences.set('')
        self.occurrences_label = tk.Label(self.mainframe,
                                          textvariable=self.occurrences,
                                          font=('Arial', 10),
                                          height=1,
                                          background=self.background_colour)
        # Empty row for keeping things spaced correctly
        self.blank_label = tk.Label(self.mainframe, text="",
                                    background=self.background_colour)
        self.blank_label.grid(row=6, column=0, pady=(10, 0), columnspan=3)
        # Random Selection Button
        roll_img = PIL.Image.open(
            resource_filename('game_randomizer',
                              os.path.join(
                                  'assets',
                                  'rollv2.png')))
        roll = PIL.ImageTk.PhotoImage(roll_img)
        roll_button = tk.Button(self.mainframe, image=roll,
                                command=self.rollGame,
                                background=self.background_colour)
        roll_button.image = roll
        roll_button.grid(row=7, column=0, pady=30, columnspan=3)
        # Control Buttons
        self.setup_button = tk.Button(self.mainframe, text='Setup',
                                      command=self.settings, anchor='sw',
                                      state=tk.DISABLED,
                                      background=self.background_colour)
        self.setup_button.grid(row=8, column=0, pady=30)
        about_button = tk.Button(self.mainframe, text='About',
                                 command=self.about, anchor='s',
                                 background=self.background_colour)
        about_button.grid(row=8, column=1, pady=30)
        exit_button = tk.Button(self.mainframe, text='Exit',
                                command=self.quit, anchor='se',
                                background=self.background_colour)
        exit_button.grid(row=8, column=2, pady=30)

    def pretty_roll(self):
        """
        Shows random game banners over a short delay to make
        the roll process more satisfying.
        """
        i = 0
        # Get the number of games in the list
        games = self.randomizer.games_list()
        games_list = list(games.keys())
        # Loop through random banners for a short time
        while i <= self.pretty_roll_count:
            # Pick a game at random
            game = random.choice(games_list)
            # Get the game info to display
            game_info = games[game]
            # Set the banner image
            img = PIL.Image.open(
                resource_filename('game_randomizer',
                                  os.path.join(
                                      'assets',
                                      self.game_setting['Image_Directory'],
                                      game_info['image'])))
            img = img.resize((420, 192), PIL.Image.Resampling.LANCZOS)
            banner = PIL.ImageTk.PhotoImage(img)
            self.banner.configure(image=banner)
            self.banner.image = banner
            # Set the game info
            self.header.set(game)
            self.subheader.set(game_info['pack'])
            self.description.set(game_info['description'])
            self.occurrences.set('Occurrences: %s' % (self.stats[game]))
            # Update the window
            self.mainframe.update()
            # Sleep
            time.sleep(i*0.001)
            i += 1

    def rollGame(self):
        """
        Performs the roll process to select a random game.
        """
        # Change widget state
        self.setup_button.config(state=tk.NORMAL)
        self.desc_label.grid(row=4, column=0, pady=10, columnspan=3)
        self.occurrences_label.grid(row=5, column=0, pady=5,
                                    columnspan=3, rowspan=2)
        self.subheader_label.grid(row=2, column=0, pady=0, columnspan=3)
        self.player_prompt.grid_forget()
        self.repeat_check.grid_forget()
        self.proll_check.grid_forget()
        self.blank_label.grid_forget()
        # Get a copy of the current occurrences.
        self.stats = self.randomizer.view_stats()
        # Check if user doesn't want to play the same game twice.
        if self.repeat_option.get():
            last_game = self.header.get()
        else:
            last_game = False
        # Show random banners if Pizza is enabled
        if self.enable_pretty_roll.get():
            self.pretty_roll()
        # Select the random game
        game, game_info = self.randomizer.pick_game(self.players.get(),
                                                    last_game)
        # Update the screen
        img = PIL.Image.open(
            resource_filename('game_randomizer',
                              os.path.join(
                                  'assets',
                                  self.game_setting['Image_Directory'],
                                  game_info['image'])))
        img = img.resize((420, 192), PIL.Image.Resampling.LANCZOS)
        banner = PIL.ImageTk.PhotoImage(img)
        self.banner.configure(image=banner)
        self.banner.image = banner
        self.header.set(game)
        self.subheader.set(game_info['pack'])
        self.description.set(game_info['description'])
        # Stats are updated before display, so remove 1.
        self.occurrences.set('Occurrences: %s' % (self.stats[game]-1))

    def settings(self):
        """
        Switch back to the setup/settings window.
        """
        # Disable setup button
        self.setup_button.config(state=tk.DISABLED)
        self.desc_label.grid_forget()
        self.occurrences_label.grid_forget()
        self.subheader_label.grid(row=2, column=0, pady=0, columnspan=2)
        self.player_prompt.grid(row=2, column=2, pady=20, columnspan=1,
                                sticky='w')
        self.repeat_check.grid(row=5, column=0, pady=0, columnspan=3)
        self.proll_check.grid(row=4, column=0, pady=0, columnspan=3)
        self.blank_label.grid(row=6, column=0, pady=(14, 0), columnspan=3)
        # Reset
        img = PIL.Image.open(self.default_img)
        img = img.resize((420, 192), PIL.Image.Resampling.LANCZOS)
        banner = PIL.ImageTk.PhotoImage(img)
        self.banner.configure(image=banner)
        self.banner.image = banner
        self.header.set(self.title)
        self.subheader.set(self.default_subheader)
        self.description.set(self.default_description)

    def about(self):
        """
        Displays some information about the app in a new frame.
        """
        # Set the window
        self.popup = tk.Tk()
        self.popup.title("About")
        self.popup.geometry("200x210")
        # Set the text
        label = tk.Label(self.popup, text=README, wraplength=200)
        label.pack(side="top", fill="x", pady=5)
        # Set up an OK button for closing the pop-up.
        B1 = tk.Button(self.popup, text="OK", command=self.popup.destroy)
        B1.pack()

        # Run the pop-up
        self.popup.mainloop()

    def quit(self):
        """
        Allows the user to quit the app.
        """
        # Destory the window.
        self.root.destroy()
        # Attempt to destory the about window.
        try:
            self.popup.destroy()
        # Window opened and closed before quit.
        except tk._tkinter.TclError:
            pass
        # Window not opened at all.
        except AttributeError:
            pass
