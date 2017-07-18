import time
from datetime import datetime
import string

import src.lib.fileHandler as fileHandler
from src.lib.variables import global_variables

import importlib

def is_valid_command(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    return command in commands.keys()

def get_command_last_used(command):
    try:
        return global_variables['commands'][command]['last_used']
    except KeyError:
        global_variables['commands'][command]['last_used'] = (datetime(1970,1,1)-datetime(1970,1,1)).total_seconds()
        return global_variables['commands'][command]['last_used']

def get_argc(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    try:
        return commands[command]['argc']
    except KeyError:
        return 0

def get_usage(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    return commands[command]['usage']

def get_command_cooldown(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    try:
        return commands[command]['cooldown']
    except KeyError:
        return 0

def get_cooldown_remaining(command):
    return int(round(get_command_cooldown(command) - (((datetime.now() - datetime(1970,1,1)).total_seconds()) - get_command_last_used(command))))

def get_return(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    return commands[command]['return']

def is_on_cooldown(command):
    return get_cooldown_remaining(command) > 0

def check_has_args(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    try:
        return commands[command]['argc']
    except KeyError:
        return 0

def check_pass_username_arg(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    try:
        return commands[command]['arg_username']
    except KeyError:
        return False

def check_has_correct_args(message, command):
    message = message.split(' ')
    try:
        return len(message) - 1 >= get_argc(command)
    except KeyError:
        return True # argc = 0

def check_returns_function(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    return True if 'return' in commands[command].keys() and commands[command]['return'] == 'command' else False

def check_has_return(command):
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    return True if commands[command]['return'] and commands[command]['return'] != 'command' else False

def update_last_used(command):
    global_variables['commands'][command]['last_used'] = (datetime.now() - datetime(1970,1,1)).total_seconds()

def pass_to_function(command, args):
    command = command.replace('!', '')

    module = importlib.import_module('src.commands.%s' % command)
    function = getattr(module, command)

    return function(args)
