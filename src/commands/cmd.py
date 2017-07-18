import string

import src.lib.fileHandler as fileHandler

def cmd(args):
    msg = 'Active channel commands: '
    commands = fileHandler.read_json('data/SantaBot/config_commands.json')
    for command in commands.keys():
        msg += command[1:] + ', '
    return msg[:-2]
