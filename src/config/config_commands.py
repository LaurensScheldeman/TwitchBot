
from src.config.config_bankheist import bankheist_config

# To add a command:
#
#   '!<command>': {
#       'cooldown': <cooldown time in seconds, type zero if none>,
#       'return': <return type, type a string if plain text, type function if there is logic to it>,
#       'argc': <number of arguments taken by the command, only if return type is command>,
#       'arg_username': <True/False, if true, will pass the username as first argument>,
#       'usage': <short description about how to send the arguments of a command>
#   }
#
# If 'return' == 'command' you need to add a file src/lib/commands/<command>.py
#   with the logic to determin the return and logic of the command

commands_config = {

    '!ping': {
        'cooldown': 30,
        'return': '!pong'
    },

    '!randomNumber': {
        'cooldown': 10,
        'return': 'command',
        'argc': 2,
        'arg_username': False,
        'usage': '!randomNumber [min] [max] (only full integers)'
    },

    # Bankheist
    bankheist_config['activation_command']: {
        'cooldown': 0, # Time between two persons that enter, should be zero.
        'return': 'command',
        'argc': 1,
        'arg_username': True,
        'usage': '!bankheist [bet] (full integer)'
    }

} # End of commands
