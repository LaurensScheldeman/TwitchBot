import string
from datetime import datetime

import Tkinter as tk
import ttk
import tkFont

import webbrowser
import socket


import src.lib.fileHandler as fileHandler
import src.lib.twitchHandler as twitchHandler

from src.lib.irc import irc as irc_
from src.lib.variables import global_variables

from src.lib.gui_botsettings import Botsettings
from src.lib.gui_commands import Commands



class GUI():

    def __init__(self):
        # GUI
        self.__ROOT = tk.Tk()
        self.__ROOT.withdraw() # Makes gui invisible

        # Loading window
        loading = tk.Tk()
        loading.wm_title(' ')
        loading.iconbitmap('src/images/santaBot_icon.ico')
        tk.Label(loading, text='Loading SantaBot...', padx=20, pady=10).grid(row=1,column=0)
        loading.update()

        self.__ROOT.wm_title('SantaBot v0.2.0')
        self.__ROOT.iconbitmap('src/images/santaBot_icon.ico')
        self.__active = True
        self.__ROOT.protocol("WM_DELETE_WINDOW", self.__quit)

        self.__notebook = ttk.Notebook(self.__ROOT, width=1120, height=690)
        # Tab1: Botsettings
        self.__botsettings = Botsettings(self.__notebook)
        self.__config = fileHandler.read_json('data/SantaBot/config.json')
        # Tab2: commands
        self.__commands = Commands(self.__notebook)

        self.__notebook.grid(row=1, column=0, columnspan=10, sticky='wen', padx=15, pady=15)

        # Buttons
        button_frame = tk.Frame(self.__ROOT)
        button_frame.grid(row=2, column = 9)
        tk.Button(button_frame, text='Save changes', command=self.__save, width=13).grid(row=0, column=0, padx=5, pady=(0,20))
        tk.Button(button_frame, text='Quit', command=self.__quit, width=13).grid(row=0, column=1, padx=5, pady=(0,20))

        # Save initial state
        self.__save()

        self.__ROOT.deiconify() # Makes gui visible
        loading.destroy() # Delete loading window

    def update(self):
        self.__ROOT.update() # Update the GUI itself

    def check_active(self):
        return self.__active

    def add_chatmessage(self, user, message):
        self.__botsettings.add_chatmessage(user, message)

    def get_irc_connection_status(self):
        return self.__botsettings.irc_connection

    def __save(self):
        # config.json
        self.__botsettings.save()
        # config_commands.json
        self.__commands.save()

    def __quit(self):
        self.__active = False
        self.__ROOT.destroy()
