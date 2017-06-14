
from src.config.config_bankheist import bankheist_config
from src.config.config_roulette import roulette_config
from src.config.config_pointsystem import pointsystem_config

# To add a command:
#
#   '!<command>': {
#       'return': <return type, type a string if plain text, type function if there is logic to it>,
#       'cooldown': <cooldown time in seconds, if not defined, no cooldown is set>,
#       'argc': <number of arguments taken by the command, only if return type is command,
#                   default 0, don't count arg_username as a argument>,
#       'arg_username': <True/False, if true, will pass the username as first argument, default False>,
#       'usage': <short description about how to send the arguments of a command>
#   }
#
# If 'return' == 'command' you need to add a file src/lib/commands/<command>.py
#   with the logic to determin the return and logic of the command

commands_config = {
    # Example commands
    '!ping': {
        'return': '!pong',
        'cooldown': 30
    },
    '!randomNumber': {
        'usage': '!randomNumber [min] [max] (only full integers)',
        'return': 'command',
        'cooldown': 30,
        'argc': 2
    },

    # Custom commands
    '!bots': {
        'return': 'I\'m here BloodTrail ',
        'cooldown': 30
    },

    # Bankheist
    bankheist_config['activation_command']: {
        'usage': bankheist_config['activation_command_usage'],
        'return': 'command',
        'argc': 1,
        'arg_username': True
    },

    # Roulette
    roulette_config['activation_command']: {
        'usage': roulette_config['activation_command_usage'],
        'return': 'command',
        'argc': 2,
        'arg_username': True
    },

    # Pointsystem
    pointsystem_config['check_balance_command']: {
        'return': 'command',
        'cooldown': pointsystem_config['check_balance_cooldown'],
        'arg_username': True,
    },
    pointsystem_config['transfer_command']: {
        'usage': pointsystem_config['transfer_command'] + ' [username] + [amount]',
        'return': 'command',
        'argc': 2,
        'arg_username': True
    }



} # End of commands
