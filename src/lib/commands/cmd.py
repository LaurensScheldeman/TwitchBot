import string

from src.config.config_commands import commands_config

def cmd():
    msg = 'Active channel commands: '
    for key in commands_config.keys():
        msg += key[1:] + ', '
    return msg[:-2]
