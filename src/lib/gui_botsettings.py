import string
from datetime import datetime
import webbrowser
import socket

import Tkinter as tk
import ttk
import tkFont

import src.lib.fileHandler as fileHandler
import src.lib.twitchHandler as twitchHandler

from src.lib.irc import irc as irc_
from src.lib.variables import global_variables



class Botsettings(ttk.Frame):
    def __init__(self, parent):
        '''
        Construction of the botsettings tab
        '''
        ttk.Frame.__init__(self, parent)
        self.__parent = parent
        self.__config = fileHandler.read_json('data/SantaBot/config.json')

        self.__initialize()

        #self.save()

    def save(self):
        '''
        Save settings to config.json
        '''
        # IRC config
        self.__config['server'] = self.__server.get()
        self.__config['port'] = self.__port.get()
        self.__config['botname'] = self.__botname.get()
        self.__config['botoauth'] = self.__botoauth.get()
        self.__config['channel'] = self.__channel.get()
        self.__config['entering_message'] = self.__entering_message.get()

        if not 'socket_buffer_size' in self.__config.keys():
            self.__config['socket_buffer_size'] = 1024

        # Stream config
        self.__config['clientID'] = self.__clientID.get()
        self.__config['clientoauth'] = self.__clientoauth.get()

        # Save_log
        if self.__save_chat.get():
            self.__config['save_log'] = True
        else:
            self.__config['save_log'] = False

        # debug
        if self.__debug.get():
            self.__config['debug'] = True
        else:
            self.__config['debug'] = False

        fileHandler.write_json('data/SantaBot/config.json', self.__config)

    def add_chatmessage(self, user, message):
        time = datetime.now().time()
        timestamp = ('0' if time.hour < 10 else '') + str(time.hour)
        timestamp += (':0' if time.minute < 10 else ':') + str(time.minute)
        text_to_append = '[' + timestamp + '] <' + user + '> : ' + message + '\n'

        self.__chat['state']='normal'
        self.__chat.insert('end', text_to_append)
        self.__chat.see(tk.END)
        self.__chat['state']='disabled'

    def __initialize(self):
        self.__parent.add(self, text='Botsettings')

        # Groupings
        irc_config = tk.LabelFrame(self, text='IRC configuration', labelanchor='n')
        irc_config.grid(row=0, column=0, columnspan=3, sticky='wens', padx=5, pady=5, ipady=3)

        connection_status = tk.LabelFrame(self, text='Status', labelanchor='n')
        connection_status.grid(row=0, column=3, sticky='wens', padx=5, pady=5)

        stream_config = tk.LabelFrame(self, text='Twitch channel configuration', labelanchor='n')
        stream_config.grid(row=1, column=0, rowspan=2, columnspan=2, sticky='wens', padx=5, pady=5, ipady=3)

        chat = tk.LabelFrame(self, text='Chat', labelanchor='n')
        chat.grid(row=3, column=0, columnspan=2, sticky='wens', padx=5, pady=5)

        logs = tk.LabelFrame(self, text='Save log', labelanchor='n')
        logs.grid(row=1, column=2, columnspan=2, sticky='wens', padx=5, pady=5)

        viewers = tk.LabelFrame(self, text='Viewers', labelanchor='n')
        viewers.grid(row=2, column=2, rowspan=2, columnspan=2, sticky='wens', padx=5, pady=5)

        # Init logging settings
        self.__init_logging(logs)
        # Init irc_config and connection_status
        self.__init_frame_ircconfig_connectionstatus(irc_config, connection_status)
        # Init stream_config
        self.__init_frame_streamconfig(stream_config)
        # Chat
        self.__chat = tk.Text(
            chat,
            relief = 'flat',
            state = 'disabled',
            font = tkFont.Font(family="anonymous pro", size=9))
        self.__chat.grid(padx=10, pady=10, sticky='wen')

    def __init_logging(self, logging_frame):
        # Save chat
        self.__save_chat = tk.IntVar()
        tk.Checkbutton(
            logging_frame,
            text='Save chat and debug to file (recommended)',
            variable=self.__save_chat
        ).grid(row=0, column=0, sticky='w')
        if 'save_log' in self.__config.keys():
            self.__save_chat.set(1 if self.__config['save_log'] else 0)
        else:
            self.__save_chat.set(1)
            self.__config['save_log']=True

        # Debug
        self.__debug = tk.IntVar()
        tk.Checkbutton(
            logging_frame,
            text='Show debug in command prompt (recommended)',
            variable=self.__debug
        ).grid(row=1, column=0, sticky='w')
        if 'debug' in self.__config.keys():
            self.__debug.set(1 if self.__config['debug'] else 0)
        else:
            self.__debug.set(1)
            self.__config['debug']=True

    def __init_frame_ircconfig_connectionstatus(self, ircconfig_frame, connectionstatus_frame):
        # Server
        self.__server = tk.StringVar()
        tk.Label(ircconfig_frame, text='Server', padx=10).grid(row=0, column=2, sticky='e')
        self.__server_entry = tk.Entry(ircconfig_frame, textvariable=self.__server)
        self.__server_entry.grid(row=0, column=3)
        if 'server' in self.__config.keys():
            self.__server.set(self.__config['server'])
        else:
            self.__config['server']=''

        # Port
        self.__port = tk.IntVar()
        tk.Label(ircconfig_frame, text='Port', padx=10).grid(row=1, column=2, sticky='e')
        self.__port_entry = tk.Entry(ircconfig_frame, textvariable=self.__port)
        self.__port_entry.grid(row=1, column=3)
        if 'port' in self.__config.keys():
            self.__port.set(self.__config['port'])
        else:
            self.__config['port']=''

        # Botname
        self.__botname = tk.StringVar()
        tk.Label(ircconfig_frame, text='Bot Login Name', padx=10).grid(row=0, column=0, sticky='e')
        self.__botname_entry = tk.Entry(ircconfig_frame, textvariable=self.__botname)
        self.__botname_entry.grid(row=0, column=1)
        if 'botname' in self.__config.keys():
            self.__botname.set(self.__config['botname'])
        else:
            self.__config['botname']=''

        # BotOAuth
        def OAuthGen(event):
            webbrowser.open_new(r'https://twitchapps.com/tmi/')

        self.__botoauth = tk.StringVar()
        botoauth_label = tk.Label(ircconfig_frame, text='Bot OAuth Token', fg='blue', cursor='hand2', padx=10)
        botoauth_label.bind("<Button-1>", OAuthGen)
        botoauth_label.grid(row=1, column=0, sticky='e')
        self.__botoauth_entry = tk.Entry(ircconfig_frame, textvariable=self.__botoauth, show='*')
        self.__botoauth_entry.grid(row=1, column=1)
        if 'botoauth' in self.__config.keys():
            self.__botoauth.set(self.__config['botoauth'])
        else:
            self.__config['botoauth']=''

        # Channel
        self.__channel = tk.StringVar()
        tk.Label(ircconfig_frame, text='Channel', padx=10).grid(row=0, column=4, sticky='e')
        self.__channel_entry = tk.Entry(ircconfig_frame, textvariable=self.__channel)
        self.__channel_entry.grid(row=0, column=5)
        if 'channel' in self.__config.keys():
            self.__channel.set(self.__config['channel'])
        else:
            self.__config['channel']=''

        # Entering message
        self.__entering_message = tk.StringVar()
        tk.Label(ircconfig_frame, text='Entering message', padx=10).grid(row=1, column=4, sticky='e')
        self.__entring_message_entry = tk.Entry(ircconfig_frame, textvariable=self.__entering_message)
        self.__entring_message_entry.grid(row=1, column=5)
        if 'entering_message' in self.__config.keys():
            self.__entering_message.set(self.__config['entering_message'])
        else:
            self.__config['entering_message']=''

        # Connecting button + status indicator
        self.__image_offline = tk.PhotoImage(file='src/images/offline.gif')
        self.__image_online = tk.PhotoImage(file='src/images/online.gif')

        self.__connection_status = tk.Label(connectionstatus_frame, image=self.__image_offline)
        self.__connection_status.pack(anchor='center', expand=True)
        self.irc_connection = False

        def set_status_indicator(status): # True  = connected
            if status:                    # False = disconnected
                self.__connection_status['image'] = self.__image_online
                self.irc_connection = True
            else:
                self.__connection_status['image'] = self.__image_offline
                self.irc_connection = False

        def connect_button_action():
            def joinIRC():
                global_variables['irc'] = irc_(self.__config)
                global_variables['irc'].join_channel()

            def set_irc_entry_state(state):
                self.__server_entry['state'] = state
                self.__port_entry['state'] = state
                self.__botname_entry['state'] = state
                self.__botoauth_entry['state'] = state
                self.__channel_entry['state'] = state
                self.__entring_message_entry['state'] = state

            if (self.__connect_button['text'] == 'Connect'):
                # Attempt to connect
                self.__connect_button['text'] = 'Connecting...'
                set_irc_entry_state('disabled')

                self.save()

                self.update()

                try:
                    joinIRC()
                except socket.timeout:
                    self.__connect_button['text'] = 'Connect'
                    set_irc_entry_state('normal')

                set_status_indicator(True)
                self.__connect_button['text'] = 'Disconnect'

            else:
                # Disconnecting
                self.__connect_button['text'] = 'Connect'
                set_status_indicator(False)
                set_irc_entry_state('normal')

        self.__connect_button = tk.Button(
            ircconfig_frame,
            text='Connect',
            command=connect_button_action,
            width=10,
            padx=10)
        self.__connect_button.grid(row=0, column=6, padx=10, rowspan=2)

        def connect_button_state(*args):
            try:
                if (self.__server.get() and self.__port.get() and self.__botname.get() \
                    and self.__botoauth.get() and self.__channel.get() and self.__entering_message.get()):
                    self.__connect_button['state']='normal'
                else:
                    self.__connect_button['state']='disabled'
            except ValueError:
                self.__connect_button['state']='disabled'

        self.__server.trace('w', connect_button_state)
        self.__port.trace('w', connect_button_state)
        self.__botname.trace('w', connect_button_state)
        self.__botoauth.trace('w', connect_button_state)
        self.__channel.trace('w', connect_button_state)
        self.__entering_message.trace('w', connect_button_state)
        connect_button_state() # Initial state

    def __init_frame_streamconfig(self, streamconfig_frame):
        # Client-ID
        self.__clientID = tk.StringVar()
        tk.Label(streamconfig_frame, text='Client-ID', padx=10).grid(row=0, column=0, sticky='e')
        self.__clientID_entry = tk.Entry(streamconfig_frame, textvariable=self.__clientID, show='*')
        self.__clientID_entry.grid(row=0, column=1)
        if 'clientID' in self.__config.keys():
            self.__clientID.set(self.__config['clientID'])
        else:
            self.__config['clientID']=''

        # Client-OAuth
        self.__clientoauth = tk.StringVar()
        tk.Label(streamconfig_frame, text='Client-OAuth', padx=10).grid(row=1, column=0, sticky='e')
        self.__clientoauth_entry = tk.Entry(streamconfig_frame, textvariable=self.__clientoauth, show='*')
        self.__clientoauth_entry.grid(row=1, column=1)
        if 'clientoauth' in self.__config.keys():
            self.__clientoauth.set(self.__config['clientoauth'])
        else:
            self.__config['clientoauth']=''

        # Title of the stream
        self.__streamtitle = tk.StringVar()
        tk.Label(streamconfig_frame, text='Stream title', padx=10).grid(row=0, column=3, sticky='e')
        self.__streamtitle_entry = tk.Entry(streamconfig_frame, textvariable=self.__streamtitle)
        self.__streamtitle_entry.grid(row=0, column=4)
        if 'streamtitle' in self.__config.keys():
            self.__streamtitle.set(self.__config['streamtitle'])
        else:
            self.__config['streamtitle']=''

        # Game of the stream
        self.__streamgame = tk.StringVar()
        tk.Label(streamconfig_frame, text='Stream game', padx=10).grid(row=1, column=3, sticky='e')
        self.__streamgame_entry = tk.Entry(streamconfig_frame, textvariable=self.__streamgame)
        self.__streamgame_entry.grid(row=1, column=4)
        if 'streamgame' in self.__config.keys():
            self.__streamtitle.set(self.__config['streamgame'])
        else:
            self.__config['streamgame']=''

        def client_update_button():
            self.__client_update_button['text'] = 'Updating...'
            self.__client_update_button['state'] = 'disabled'
            self.update()
            twitchHandler.update_title(self.__channel.get(), self.__clientoauth.get(), self.__streamtitle.get())
            twitchHandler.update_game(self.__channel.get(), self.__clientoauth.get(), self.__streamgame.get())
            self.__client_update_button['text'] = 'Update'
            self.__client_update_button['state'] = 'normal'

        self.__client_update_button = tk.Button(
            streamconfig_frame,
            text='Update',
            command=client_update_button,
            width=10,
            padx=10)
        self.__client_update_button.grid(row=2, column=4, padx=5)

        # Client check
        self.__red_x = tk.PhotoImage(file='src/images/red_x.gif')
        self.__green_v = tk.PhotoImage(file='src/images/green_v.gif')

        self.__client_status = tk.Label(streamconfig_frame, image=self.__red_x)
        self.__client_status.grid(row=0, column=2, rowspan=2, sticky='wens')

        def check_client_state(*args):
            self.__client_state = twitchHandler.check_valid_client_token(self.__clientID.get(), self.__clientoauth.get())

            if self.__client_state:
                self.__client_status['image'] = self.__green_v
                self.__config['streamtitle'] = twitchHandler.get_title(self.__clientoauth.get())
                self.__streamtitle.set(self.__config['streamtitle'])
                self.__config['streamgame'] = twitchHandler.get_game(self.__clientoauth.get())
                self.__streamgame.set(self.__config['streamgame'])
                self.__streamtitle_entry['state'] = 'normal'
                self.__streamgame_entry['state'] = 'normal'
                self.__client_update_button['state'] = 'normal'
            else:
                self.__client_status['image'] = self.__red_x
                self.__config['streamtitle'] = ''
                self.__config['streamgame'] = ''
                self.__streamtitle_entry['state'] = 'disabled'
                self.__streamgame_entry['state'] = 'disabled'
                self.__client_update_button['state'] = 'disabled'

        check_client_state() # Initial state

        def client_check_button():
            self.__client_check_button['text'] = 'Checking...'
            self.__client_check_button['state'] = 'disabled'
            self.update()

            check_client_state()

            self.__client_check_button['text'] = 'Check'
            self.__client_check_button['state'] = 'normal'

        self.__client_check_button = tk.Button(
            streamconfig_frame,
            text='Check',
            command=client_check_button,
            width=10,
            padx=10)
        self.__client_check_button.grid(row=2, column=1, columnspan=3, padx=5)

        def client_quit_help():
            self.__client_help.destroy()

        def client_give_help():
            self.__client_help = tk.Toplevel()
            self.__client_help.wm_title('How to get client-ID and OAuth')
            self.__client_help.iconbitmap('src/images/santaBot_icon.ico')
            self.__client_help.protocol("WM_DELETE_WINDOW", client_quit_help)

            client_help_ok = tk.Button(
                self.__client_help,
                text='OK',
                command=client_quit_help,
                width=10,
                padx=10)
            client_help_ok.grid(row=1,column=1, sticky='w')

            def help_text_hyperlink(event):
                event_tag = event.widget.tag_names('current')
                if event_tag[0] == 'sel':
                    webbrowser.open_new(event_tag[2])
                else:
                    webbrowser.open_new(event_tag[1])
            help_text=tk.Text(
                self.__client_help,
                font='Arial 10',
                padx=10)
            help_text.grid(row=0, column=0, columnspan=2)
            help_text.tag_config('link', foreground='blue', underline=1)
            help_text.tag_config('input', font='Monaco')
            help_text.config(cursor='arrow')
            help_text.tag_bind('link', '<Button-1>', help_text_hyperlink)
            help_text.insert('end', 'Part 1: Authorize bot to use your twitch\n')
            help_text.insert('end', 'To get your client ID, you need to go to your ')
            help_text.insert('end', 'twitch connection settings', ('link', 'https://www.twitch.tv/settings/connections'))
            help_text.insert('end',  '.\nAt the bottom select enable for development, and click the button to register a new application.\n\n')
            help_text.insert('end', 'Give your application a name (E.g. ')
            help_text.insert('end', 'santaBot', 'input')
            help_text.insert('end', ') and as redirect URI type  ')
            help_text.insert('end', 'http://localhost\n', 'input')
            help_text.insert('end', 'also select the category chat bot and accept the the terms to register.\n')
            help_text.insert('end', 'if everything went will you will get a client ID in return.\n\n')
            help_text.insert('end', 'Part 2: Get the oauth token for your client ID.\n')
            help_text.insert('end', 'To get access to your client you need to go to your internet browser and insert next link:\n')
            help_text.insert('end', 'https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&scope=channel_editor+channel_read&redirect_uri=http://localhost&client_id=\n', 'input')
            help_text.insert('end', 'and at the end (afther the \'=\') you insert your client ID.\nIt will redirect you to a page that says it couldn\'t find localhost.\n')
            help_text.insert('end', 'If you look at the URL of the page, you will see it contains a #access_token.\n')
            help_text.insert('end', 'That\'s the OAuth for your client ID. Make sure to check if it\'s correct.')
            help_text['state']='disabled'

        # Client help button
        self.__client_help_button = tk.Button(
            streamconfig_frame,
            text='Help',
            command=client_give_help,
            width=10,
            padx=10)
        self.__client_help_button.grid(row=2, column=0, padx=5)
