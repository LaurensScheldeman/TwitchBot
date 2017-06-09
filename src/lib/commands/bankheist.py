import string

from src.lib.timers import InfiniteTimer
import src.lib.irc as irc_

from src.config.config import config as config
from src.config.config_bankheist import bankheist_config as bankheist_config


def bankheist(args):
    # User wants to join a bankheist
    user = args[0]
    try:
        user_bet = int(args[1])
    except ValueError: # Invalid bet
        user_bet = 0

    init_bankheist()

    if bankheist_config['cooldown_timer'].is_running:
        # Bankheist on cooldown
        config['irc'].send_message(decode_message(bankheist_config['cooldown_message'], user))

    elif bankheist_config['in_progress_timer'].is_running:
        # Bankheist in progress
        config['irc'].send_message(decode_message(bankheist_config['late_entery'], user))

    elif ((user_bet > 0) or ((bankheist_config['max_bet'] == 0) and (user_bet <= bankheist_config['max_bet']))):
        # Able to join, will only join if user placed a valid bet
        bankheist_config['enteries'][user] = user_bet

        current_enteries = len(bankheist_config['enteries'])
        if current_enteries == 1: # First entery
            message = bankheist_config['entery_message_1'] + ' ' + bankheist_config['entery_instructions']
            if bankheist_config['max_bet'] > 0:
                message += ' ' + bankheist_config['max_entery_message']
            config['irc'].send_message(decode_message(message, user))
            bankheist_config['entery_timer'].start()
            if config['debug']:
                print('-- heist_entery_timer started. (' + str(bankheist_config['entery_timer'].seconds) + ' seconds)')

        elif current_enteries == (bankheist_config['level_1_max_users'] + 1):
            config['irc'].send_message(decode_message(bankheist_config['entery_message_2'], user))

        elif current_enteries == (bankheist_config['level_2_max_users'] + 1):
            config['irc'].send_message(decode_message(bankheist_config['entery_message_3'], user))

        elif current_enteries == (bankheist_config['level_3_max_users'] + 1):
            config['irc'].send_message(decode_message(bankheist_config['entery_message_4'], user))

        elif current_enteries == (bankheist_config['level_4_max_users'] + 1):
            config['irc'].send_message(decode_message(bankheist_config['entery_message_5'], user))

    return ''

def decode_message(message, user = None):
    split_message = message.split('@', message.count('@'))
    result = split_message.pop(0)

    while len(split_message):
        key = split_message.pop(0)

        if key == 'user' and user:
            result += user

        elif key == 'bankname':
            number_of_enteries = len(bankheist_config['enteries'])
            if number_of_enteries <= bankheist_config['level_1_max_users']:
                result += bankheist_config['level_1_bank_name']
            elif number_of_enteries <= bankheist_config['level_2_max_users']:
                result += bankheist_config['level_2_bank_name']
            elif number_of_enteries <= bankheist_config['level_3_max_users']:
                result += bankheist_config['level_3_bank_name']
            elif number_of_enteries <= bankheist_config['level_4_max_users']:
                result += bankheist_config['level_4_bank_name']
            else:
                result += bankheist_config['level_5_bank_name']

        elif key in bankheist_config:
            result += str(bankheist_config[key])

        else: # unknown key
            result += ('@' + key + '@')

        if len(split_message):
            result += split_message.pop(0)

    return result

def init_bankheist():
    # initialize the bankheist (only happens first time)
    if not check_init_status():
        bankheist_config['entery_timer'] = InfiniteTimer(bankheist_config['time_to_enter'], bankheist_in_progress)
        bankheist_config['in_progress_timer'] = InfiniteTimer(30, bankheist_outcome)
        bankheist_config['cooldown_timer'] = InfiniteTimer(bankheist_config['cooldown_time'] * 60, bankheist_end_of_cooldown)
        bankheist_config.pop('enteries', None) # Delete all enteries of current heist
        bankheist_config['enteries'] = {} # Empty dictionary
        bankheist_config['init_status'] = True

def check_init_status():
    try:
        return bankheist_config['init_status']
    except KeyError:
        bankheist_config['init_status'] = False
        return False

def bankheist_in_progress():
    # Start of the heist
    bankheist_config['entery_timer'].stop()
    bankheist_config['in_progress_timer'].start()
    if config['debug']:
        print('-- heist_entery_timer stopped.')
        print('-- heist_in_progress_timer started. (' + str(bankheist_config['in_progress_timer'].seconds) + ' seconds)')
    config['irc'].send_message(decode_message(bankheist_config['heist_start']))

def bankheist_outcome():
    # End of the heist
    a=1

def bankheist_end_of_cooldown():
    # End of cooldown
    a=1
