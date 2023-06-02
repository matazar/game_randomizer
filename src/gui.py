import tkinter as tk
import PIL.Image
import PIL.ImageTk
import os
import random
import time
from pkg_resources import resource_filename


README = """
Game Randomizer
===============

A simple GUI app for selecting a random game
based on a JSON file of games.

"""


class GUI(object):
    """
    GUI client for the game randomizer.
    """
    def __init__(self, randomizer, verbose):
        """
        Set up some basic variables for the GUI
        """
        # Set up the variables we need.
        self.verbose = verbose
        self.randomizer = randomizer
        # Get our settings.
        self.game_setting = randomizer.settings()
        # Set the title based off the json file.
        self.title = self.game_setting['Title']
        # Set up the window size.
        self.window_height = 600
        self.window_width = 480
        # Set up logo path.
        self.default_img = \
            resource_filename('game_randomizer',
                              os.path.join(
                                  'assets',
                                  self.game_setting['Image_Directory'],
                                  self.game_setting['Logo']))
        self.default_subheader = 'Number of players: '
        self.default_description = ' '
        # Set player info
        self.default_players = self.game_setting['Default_Players']
        self.max_players = self.game_setting['Max_Players']
        self.background_colour = "grey25"
        # Number of random games to display before the actual pick.
        self.pretty_roll_count = 75
        # Creat the root app window.
        self.rootWindow()
        self.frames = {}
        # Setup/config window
        self.mainframe = self.frameInit()
        self.frameLayout()

    def __call__(self):
        """
        Run the GUI.
        """
        self.root.mainloop()

    def rootWindow(self):
        """
        Set up the root window.
        """
        self.root = tk.Tk()
        self.root.title(self.title)
        ico = tk.PhotoImage(file=self.default_img)
        self.root.iconphoto(False, ico)
        self.root.configure(background=self.background_colour)
        self.root.geometry('%sx%s' % (self.window_width, self.window_height))

    def frameInit(self):
        """
        Creates a frame based on our default settings.
        """
        frame = tk.Frame(self.root, width=self.window_width,
                         height=self.window_height,
                         background=self.background_colour)
        frame.grid(column=0, row=0, sticky="nsew",)
        return frame

    def frameLayout(self):
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
                                   wraplength=420, height=3,
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
        if self.verbose:
            print(f'Random game selection is "{game}"')
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
