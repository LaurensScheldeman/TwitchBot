"""
Simple IRC Bot for Twitch.tv

Developed by Laurens Scheldeman <laurens.scheldeman@gmail.com>
"""
import string

import src.lib.fileHandler as fileHandler
import src.lib.twitchHandler as twitchHandler
import src.lib.commands_functions as commands

from src.lib.gui import GUI

from src.lib.variables import global_variables



class SantaBot:

    def __init__(self):
        # Check for debug settings
        if fileHandler.check_file_exist('data/SantaBot/config.json'):
            filedata = fileHandler.read_json('data/SantaBot/config.json')
            debug = filedata['debug']
            save_log = filedata['save_log']
        else:
            debug = False
            save_log = True
            filedata = {
                'debug': False,
                'save_log': True
            }
            fileHandler.write_json('data/SantaBot/config.json',filedata)

        # Prepare file to save log
        if save_log:
            if fileHandler.check_file_exist('data/SantaBot/current_log.txt'):
                fileHandler.rename_file('data/SantaBot/current_log.txt', 'previous_log.txt')
            else:
                fileHandler.create_empty_file('data/SantaBot/current_log.txt')

        print('\n\n\n   Welcome to SantaBot!'+\
              '\n\n   This window is the terminal of SantaBot, you can minimize this while using the bot, but you cannot close it.'+\
              '\n   You can close it when you stop using SantaBot if it doesn\'t close automaticly.\n\n\n')
        global_variables['gui'] = GUI()
        global_variables['gui'].update()

    def run(self):
        while(global_variables['gui'].check_active()):

            global_variables['gui'].update()
            if global_variables['gui'].get_irc_connection_status():
                user, message = global_variables['irc'].read_message()

                if len(message):
                    global_variables['gui'].add_chatmessage(user,message)
                    self.__config = fileHandler.read_json('data/SantaBot/config.json')

                    if self.__config['save_log']:
                        fileHandler.append_to_file('data/SantaBot/current_log.txt', user + ": " + message, use_time=True)
                    if self.__config['debug']:
                        print('\n' + user + ': ' + message)

                    # check if message is a command
                    if commands.is_valid_command(message.split(' ')[0]):
                        command = message.split(' ')[0]
                        # check if command is on cooldown
                        if commands.is_on_cooldown(command):
                            if self.__config['debug']:
                                debug_message = "-- Command is on cooldown. (" + \
                                    str(commands.get_cooldown_remaining(command)) + "s remaining)"
                                print(debug_message)
                                if self.__config['save_log']:
                                    fileHandler.append_to_file('data/SantaBot/current_log.txt', debug_message, use_time=True)
                        else: # No cooldown
                            if self.__config['debug']:
                                debug_message = "-- Command is not on cooldown."
                                print(debug_message)
                                if self.__config['save_log']:
                                    fileHandler.append_to_file('data/SantaBot/current_log.txt', debug_message, use_time=True)

                            # check if the command returns a function
                            if commands.check_returns_function(command):
                                if commands.check_has_correct_args(message, command):
                                    args = message.split(' ')

                                    while len(args) > (commands.get_argc(command) + 1):
                                        del args[len(args)-1]

                                    # args[0] is the command, change it to user if needed, delete otherwise
                                    if commands.check_pass_username_arg(command):
                                        args[0] = user
                                    else:
                                        del args[0]

                                    result = commands.pass_to_function(command, args)
                                    commands.update_last_used(command)

                                    if result:
                                        global_variables['irc'].send_message(result)

                                else:
                                    global_variables['irc'].send_message("Please use command correctly: " + commands.get_usage(command.split(' ')[0]))

                            # check if the command has a return that is not a function
                            elif commands.check_has_return(command):
                                result = commands.get_return(command)
                                commands.update_last_used(command)

                                if len(result):
                                    global_variables['irc'].send_message(result)
