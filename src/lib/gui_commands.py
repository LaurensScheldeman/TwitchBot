import string

import Tkinter as tk
import ttk

import src.lib.fileHandler as fileHandler
from src.lib.variables import global_variables

class Commands(ttk.Frame):
    def __init__(self, parent):
        '''
        Construction of the commands tab
        '''
        ttk.Frame.__init__(self, parent)
        self.__parent = parent
        #self.__config = fileHandler.read_json('data/SantaBot/config.json')

        self.__initialize()

        #self.save()

    def save(self):
        commands = {}
        if not 'commands' in global_variables.keys():
            global_variables['commands'] = {}

        for cmd in self.__commands.get_children():
            command = self.__commands.item(cmd)['text']
            commands[command] = {}

            cooldown = self.__commands.item(cmd)['values'][0]
            if cooldown > 0:
                commands[command]['cooldown'] = cooldown

            return_value = self.__commands.item(cmd)['values'][1]
            if return_value == 'command':
                commands[command]['return'] = 'command'

                argc = self.__commands.item(cmd)['values'][2]
                if argc > 0:
                    commands[command]['argc'] = argc

                if self.__commands.item(cmd)['values'][3] == 'True':
                    commands[command]['arg_username'] = True

                usage = self.__commands.item(cmd)['values'][4]
                if len(usage):
                    commands[command]['usage'] = usage
            else:
                commands[command]['return'] = return_value

            if not command in global_variables['commands'].keys():
                global_variables['commands'][command] = {}

        fileHandler.write_json('data/SantaBot/config_commands.json', commands)


    def __add_command(self, command, cooldown, return_value, argc='', arg_username='', usage=''):
        values=(
            cooldown,
            return_value,
            argc,
            '' if arg_username == '' else ('True' if arg_username == 'True' else 'False'),
            usage)
        self.__commands.insert('', 'end', text=command, values=values)

    def __edit_command(self, command_index, command, cooldown, return_value, argc='', arg_username='', usage=''):
        values=(
            cooldown,
            return_value,
            argc,
            '' if arg_username == '' else ('True' if arg_username else 'False'),
            usage)
        self.__commands.insert('', self.__commands.index(command_index), text=command, values=values)
        self.__commands.delete(command_index)

    def __delete_command(self, command_index):
        self.__commands.delete(command_index)

    def __initialize(self):
        self.__parent.add(self, text='Commands')

        # Groupings
        command_view = tk.LabelFrame(self, text='Configured commands', labelanchor='n')
        command_view.grid(row=0, column=0, sticky='wens', padx=5, pady=5, ipadx=3, ipady=2)

        self.__init_current_commands(command_view)

    def __init_current_commands(self, command_frame):
        self.__commands = ttk.Treeview(command_frame)
        self.__commands['columns']=('1','2','3','4','5')
        #tree['show'] = 'headings'
        self.__commands.column('1', width=100)
        self.__commands.column('2', width=338)
        self.__commands.column('3', width=100)
        self.__commands.column('4', width=100)
        self.__commands.column('5', width=250)
        self.__commands.heading('1', text='Cooldown')
        self.__commands.heading('2', text='Return value')
        self.__commands.heading('3', text='Arguments')
        self.__commands.heading('4', text='Pass user')
        self.__commands.heading('5', text='Usage')
        self.__commands.grid(row=0, column=0, columnspan=10, padx=5, pady=(3,5))

        #self.__commands.insert('', 0, text='!test', values=('col1','col2'))

        def new_command_entry(*args):
            self.__add_button['state'] = 'disabled'
            self.__edit_button['state'] = 'disabled'
            self.__delete_button['state'] = 'disabled'

            def new_command_quit():
                self.__new_command_window.destroy()
            def add_new_command():
                try:
                    return_type = self.__return_type.get()
                    if return_type==1:
                        # Simple text return
                        self.__add_command(
                            self.__command.get(),
                            self.__cooldown.get(),
                            self.__return_text.get())
                    else:
                        # Command
                        self.__add_command(
                            self.__command.get(),
                            self.__cooldown.get(),
                            'command',
                            self.__command_argc.get(),
                            self.__command_username.get()==1,
                            self.__command_usage.get())
                    new_command_quit()
                except ValueError:
                    pass
            self.__new_command_window = tk.Toplevel()
            self.__new_command_window.wm_title('Add new command')
            self.__new_command_window.iconbitmap('src/images/santaBot_icon.ico')
            self.__new_command_window.protocol("WM_DELETE_WINDOW", new_command_quit)

            new_command_frame = ttk.Frame(self.__new_command_window)
            new_command_frame.pack(padx=10, pady=10)

            # Command name
            self.__command = tk.StringVar()
            self.__command.set('!command')
            tk.Label(new_command_frame, text='Command name', padx=10).grid(row=0, column=0, sticky='e')
            tk.Entry(new_command_frame, textvariable=self.__command).grid(row=0, column=1)

            # Cooldown
            self.__cooldown = tk.IntVar()
            self.__cooldown.set(0)
            tk.Label(new_command_frame, text='Cooldown (sec)', padx=10).grid(row=1, column=0, sticky='e')
            tk.Entry(new_command_frame, textvariable=self.__cooldown).grid(row=1, column=1)

            def changing_return_type():
                if self.__return_type.get()==1:
                    # Simple text return
                    self.__return_text_entry['state'] = 'normal'
                    self.__command_argc_entry['state'] = 'disabled'
                    self.__command_username_entry['state'] = 'disabled'
                    self.__command_usage_entry['state'] = 'disabled'
                else:
                    # Command returning
                    self.__return_text_entry['state'] = 'disabled'
                    self.__command_argc_entry['state'] = 'normal'
                    self.__command_username_entry['state'] = 'normal'
                    self.__command_usage_entry['state'] = 'normal'

            # Return type
            self.__return_type = tk.IntVar()
            self.__return_type.set(1)
            tk.Label(new_command_frame, text='Return type', padx=10).grid(row=2, column=0, sticky='e', rowspan=2)
            tk.Radiobutton(new_command_frame, text='Simple text response', variable=self.__return_type,\
                value=1, command=changing_return_type).grid(row=2, column=1, sticky='w')
            tk.Radiobutton(new_command_frame, text='Command response', variable=self.__return_type,\
                value=2, command=changing_return_type).grid(row=3, column=1, sticky='w')

            # Simple return text
            self.__return_text = tk.StringVar()
            tk.Label(new_command_frame, text='Response text', padx=10).grid(row=4, column=0, sticky='e')
            self.__return_text_entry = tk.Entry(new_command_frame, textvariable=self.__return_text)
            self.__return_text_entry.grid(row=4, column=1)

            # Number of arguments to pass
            self.__command_argc = tk.IntVar()
            tk.Label(new_command_frame, text='Number of arguments', padx=10).grid(row=5, column=0, sticky='e')
            self.__command_argc_entry = tk.Entry(new_command_frame, textvariable=self.__command_argc)
            self.__command_argc_entry.grid(row=5, column=1)

            # Pass username as extra arguments
            self.__command_username = tk.IntVar()
            self.__command_username_entry = tk.Checkbutton(
                new_command_frame,
                text='Pass username as extra argument',
                variable=self.__command_username)
            self.__command_username_entry.grid(row=6, column=0, columnspan=2, sticky='e')

            # Usage of command
            self.__command_usage = tk.StringVar()
            tk.Label(new_command_frame, text='Command usage', padx=10).grid(row=7, column=0, sticky='e')
            self.__command_usage_entry = tk.Entry(new_command_frame, textvariable=self.__command_usage)
            self.__command_usage_entry.grid(row=7, column=1)

            changing_return_type() # Initial state

            self.__confirm_new_command_button = tk.Button(
                new_command_frame,
                text='Add',
                command=add_new_command,
                width=10,
                padx=10)
            self.__confirm_new_command_button.grid(row=8, column=0, padx=10)

            self.__cancel_new_command_button = tk.Button(
                new_command_frame,
                text='Cancel',
                command=new_command_quit,
                width=10,
                padx=10)
            self.__cancel_new_command_button.grid(row=8, column=1, padx=10)

            self.__add_button['state'] = 'normal'
            self.__edit_button['state'] = 'normal'
            self.__delete_button['state'] = 'normal'

        self.__add_button = tk.Button(
            command_frame,
            text='Add',
            command=new_command_entry,
            width=10,
            padx=10)
        self.__add_button.grid(row=1, column=7, padx=10)

        def edit_command_entry(*args):
            command = self.__commands.focus()
            if command:
                self.__add_button['state'] = 'disabled'
                self.__edit_button['state'] = 'disabled'
                self.__delete_button['state'] = 'disabled'

                def edit_command_quit():
                    self.__edit_command_window.destroy()
                def add_edit_command():
                    try:
                        return_type = self.__return_type.get()
                        if return_type==1:
                            # Simple text return
                            self.__edit_command(
                                command,
                                self.__command.get(),
                                self.__cooldown.get(),
                                self.__return_text.get())
                        else:
                            # Command
                            self.__edit_command(
                                command,
                                self.__command.get(),
                                self.__cooldown.get(),
                                'command',
                                self.__command_argc.get(),
                                self.__command_username.get()==1,
                                self.__command_usage.get())
                        edit_command_quit()
                    except ValueError:
                        pass
                self.__edit_command_window = tk.Toplevel()
                self.__edit_command_window.wm_title('Add new command')
                self.__edit_command_window.iconbitmap('src/images/santaBot_icon.ico')
                self.__edit_command_window.protocol("WM_DELETE_WINDOW", edit_command_quit)

                edit_command_frame = ttk.Frame(self.__edit_command_window)
                edit_command_frame.pack(padx=10, pady=10)

                # Command name
                self.__command = tk.StringVar()
                self.__command.set(self.__commands.item(command)['text'])
                tk.Label(edit_command_frame, text='Command name', padx=10).grid(row=0, column=0, sticky='e')
                tk.Entry(edit_command_frame, textvariable=self.__command).grid(row=0, column=1)

                # Cooldown
                self.__cooldown = tk.IntVar()
                self.__cooldown.set(self.__commands.item(command)['values'][0])
                tk.Label(edit_command_frame, text='Cooldown (sec)', padx=10).grid(row=1, column=0, sticky='e')
                tk.Entry(edit_command_frame, textvariable=self.__cooldown).grid(row=1, column=1)

                def changing_return_type():
                    if self.__return_type.get()==1:
                        # Simple text return
                        self.__return_text_entry['state'] = 'normal'
                        self.__command_argc_entry['state'] = 'disabled'
                        self.__command_username_entry['state'] = 'disabled'
                        self.__command_usage_entry['state'] = 'disabled'
                    else:
                        # Command returning
                        self.__return_text_entry['state'] = 'disabled'
                        self.__command_argc_entry['state'] = 'normal'
                        self.__command_username_entry['state'] = 'normal'
                        self.__command_usage_entry['state'] = 'normal'

                return_text = self.__commands.item(command)['values'][1]
                # Return type
                self.__return_type = tk.IntVar()
                self.__return_type.set(2 if return_text=='command' else 1)
                tk.Label(edit_command_frame, text='Return type', padx=10).grid(row=2, column=0, sticky='e', rowspan=2)
                tk.Radiobutton(edit_command_frame, text='Simple text response', variable=self.__return_type,\
                    value=1, command=changing_return_type).grid(row=2, column=1, sticky='w')
                tk.Radiobutton(edit_command_frame, text='Command response', variable=self.__return_type,\
                    value=2, command=changing_return_type).grid(row=3, column=1, sticky='w')

                # Simple return text
                self.__return_text = tk.StringVar()
                self.__return_text.set('' if return_text=='command' else return_text)
                tk.Label(edit_command_frame, text='Response text', padx=10).grid(row=4, column=0, sticky='e')
                self.__return_text_entry = tk.Entry(edit_command_frame, textvariable=self.__return_text)
                self.__return_text_entry.grid(row=4, column=1)

                # Number of arguments to pass
                self.__command_argc = tk.IntVar()
                self.__command_argc.set(self.__commands.item(command)['values'][2])
                tk.Label(edit_command_frame, text='Number of arguments', padx=10).grid(row=5, column=0, sticky='e')
                self.__command_argc_entry = tk.Entry(edit_command_frame, textvariable=self.__command_argc)
                self.__command_argc_entry.grid(row=5, column=1)

                # Pass username as extra arguments
                self.__command_username = tk.IntVar()
                self.__command_username.set(1 if self.__commands.item(command)['values'][3]=='True' else 0)
                self.__command_username_entry = tk.Checkbutton(
                    edit_command_frame,
                    text='Pass username as extra argument',
                    variable=self.__command_username)
                self.__command_username_entry.grid(row=6, column=0, columnspan=2, sticky='e')

                # Usage of command
                self.__command_usage = tk.StringVar()
                self.__command_usage.set(self.__commands.item(command)['values'][4])
                tk.Label(edit_command_frame, text='Command usage', padx=10).grid(row=7, column=0, sticky='e')
                self.__command_usage_entry = tk.Entry(edit_command_frame, textvariable=self.__command_usage)
                self.__command_usage_entry.grid(row=7, column=1)

                changing_return_type() # Initial state

                self.__confirm_new_command_button = tk.Button(
                    edit_command_frame,
                    text='Edit',
                    command=add_edit_command,
                    width=10,
                    padx=10)
                self.__confirm_new_command_button.grid(row=8, column=0, padx=10)

                self.__cancel_new_command_button = tk.Button(
                    edit_command_frame,
                    text='Cancel',
                    command=edit_command_quit,
                    width=10,
                    padx=10)
                self.__cancel_new_command_button.grid(row=8, column=1, padx=10)

                self.__add_button['state'] = 'normal'
                self.__edit_button['state'] = 'normal'
                self.__delete_button['state'] = 'normal'

        self.__edit_button = tk.Button(
            command_frame,
            text='Edit',
            command=edit_command_entry,
            width=10,
            padx=10)
        self.__edit_button.grid(row=1, column=8, padx=10)

        def delete_command_entry(*args):
            command = self.__commands.focus()
            if command:
                self.__delete_command(command)

        self.__delete_button = tk.Button(
            command_frame,
            text='Delete',
            command=delete_command_entry,
            width=10,
            padx=10)
        self.__delete_button.grid(row=1, column=9, padx=10)

        # Add commands out of config file
        if fileHandler.check_file_exist('data/SantaBot/config_commands.json'):
            commands = fileHandler.read_json('data/SantaBot/config_commands.json')

            for command in commands:
                if commands[command]['return'] == 'command':
                    # Command
                    self.__add_command(
                        command,
                        commands[command]['cooldown'] if 'cooldown' in commands[command].keys() else 0,
                        'command',
                        commands[command]['argc'] if 'argc' in commands[command].keys() else 0,
                        'True' if (('arg_username' in commands[command].keys()) and commands[command]['arg_username']) else 'False',
                        commands[command]['usage'] if 'usage' in commands[command].keys() else '')
                else:
                    # Simple text return
                    self.__add_command(
                        command,
                        commands[command]['cooldown'] if 'cooldown' in commands[command].keys() else 0,
                        commands[command]['return'])
