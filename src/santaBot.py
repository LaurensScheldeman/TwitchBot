"""
Simple IRC Bot for Twitch.tv

Developed by Laurens Scheldeman <laurens.scheldeman@gmail.com>
"""
import string

import src.lib.irc as irc_
import src.lib.fileHandler as fileHandler
from src.lib.userHandler import userHandler
import src.lib.commands_functions as commands
from src.config.config_userdata import userdata_config


class SantaBot:

    def __init__(self, config):
        self.__config = config

        # Prepare file to save log
        if self.__config['save_log']:
            if fileHandler.check_file_exist(self.__config['save_log_filepath']):
                fileHandler.rename_file(self.__config['save_log_filepath'], self.__config['save_prevlog_filename'])
            else:
                fileHandler.create_empty_file(self.__config['save_log_filepath'])

        self.__irc = irc_.irc(config)
        self.__config['irc'] = self.__irc

        userHandler(userdata_config)

    def run(self):
        self.__irc.join_channel()

        while True:
            user, message = self.__irc.read_message()

            if self.__config['save_log']:
                fileHandler.append_to_file(self.__config['save_log_filepath'], '\n' + user + ": " + message, use_time=True)
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
                            fileHandler.append_to_file(self.__config['save_log_filepath'], debug_message, use_time=True)
                else: # No cooldown
                    if self.__config['debug']:
                        debug_message = "-- Command is not on cooldown."
                        print(debug_message)
                        if self.__config['save_log']:
                            fileHandler.append_to_file(self.__config['save_log_filepath'], debug_message, use_time=True)

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
                                self.__irc.send_message(result)

                        else:
                            self.__irc.send_message("Please use command correctly: " + commands.get_usage(command.split(' ')[0]))

                    # check if the command has a return that is not a function
                    elif commands.check_has_return(command):
                        result = commands.get_return(command)
                        commands.update_last_used(command)

                        if result and type(result) is str:
                            self.__irc.send_message(result)
