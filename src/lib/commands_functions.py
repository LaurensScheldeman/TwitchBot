import time
import string

from src.config.config_commands import commands_config as commands

import importlib

def is_valid_command(command):
    return command in commands.keys()

def get_command_last_used(command):
    try:
        return commands[command]['last_used']
    except KeyError:
        commands[command]['last_used'] = 0
        return 0

def get_argc(command):
    try:
        return commands[command]['argc']
    except KeyError:
        commands[command]['argc'] = 0
        return 0

def get_usage(command):
    return commands[command]['usage']

def get_command_cooldown(command):
    try:
        return commands[command]['cooldown']
    except KeyError:
        commands[command]['cooldown'] = 0
        return 0

def get_cooldown_remaining(command):
	return int(round(get_command_cooldown(command) - (time.time() - get_command_last_used(command))))

def get_return(command):
    return commands[command]['return']

def is_on_cooldown(command):
    return True if time.time() -  get_command_last_used(command) < get_command_cooldown(command) else False

def check_has_args(command):
    try:
        return commands[command]['argc']
    except KeyError:
        commands[command]['argc'] = 0
        return 0

def check_pass_username_arg(command):
    try:
        return commands[command]['arg_username']
    except KeyError:
        commands[command]['arg_username'] = False
        return False

def check_has_correct_args(message, command):
    message = message.split(' ')
    try:
        return len(message) - 1 >= commands[command]['argc']
    except KeyError:
        commands[command]['argc'] = 0
        return len(message) - 1 >= commands[command]['argc']

def check_returns_function(command):
	return True if 'return' in commands[command].keys() and commands[command]['return'] == 'command' else False

def check_has_return(command):
    return True if commands[command]['return'] and commands[command]['return'] != 'command' else False

def update_last_used(command):
    commands[command]['last_used'] = time.time()

def pass_to_function(command, args):
	command = command.replace('!', '')

	module = importlib.import_module('src.lib.commands.%s' % command)
	function = getattr(module, command)

	if args:
		# need to reference to src.lib.commands.<command.py>
		return function(args)
	else:
		# need to reference to src.lib.commands.<command.py>
		return function()
