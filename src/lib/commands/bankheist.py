import string

from src.lib.timers import InfiniteTimer
import src.lib.irc as irc_

from src.config.config import config as config
from src.config.config_bankheist import bankheist_config as bankheist


def bankheist(args):
    # User wants to join a heist
    user = args[0]
    try:
        user_bet = int(args[1])
    except ValueError:
        user_bet = 0

    initBankheist()

    if bankheist['cooldown_timer'].is_running():
        # Bankheist on cooldown
        config['irc'].send_message(decode_message(user, bankheist['cooldown_message']))

    elif bankheist['in_progress_timer'].is_running():
        # Bankheist in progress
        config['irc'].send_message(decode_message(user, bankheist['late_entery']))

    elif ((user_bet > 0) or ((bankheist['max_bet'] == 0) and (user_bet <= bankheist['max_bet']))):
        # Able to join, will only join if user placed a valid bet
        bankheist['enteries'][user] = user_bet

        if len(bankhiest['enteries']) == 1: # First entery
            message = bankheist['entery_message_1'] + bankheist['entery_instructions']
            if bankheist['max_bet'] > 0:
                message += bankheist['max_entery_message']
            config['irc'].send_message(decode_message(user, message))

        elif len(bankhiest['enteries']) == (bankheist['level_1_max_users'] + 1):
            config['irc'].send_message(decode_message(user, bankheist['entery_message_2']))

        elif len(bankhiest['enteries']) == (bankheist['level_2_max_users'] + 1):
            config['irc'].send_message(decode_message(user, bankheist['entery_message_3']))

        elif len(bankhiest['enteries']) == (bankheist['level_3_max_users'] + 1):
            config['irc'].send_message(decode_message(user, bankheist['entery_message_4']))

        elif len(bankhiest['enteries']) == (bankheist['level_4_max_users'] + 1):
            config['irc'].send_message(decode_message(user, bankheist['entery_message_5']))

    return ''

def decode_message(user, message):
    split_message = message.split('@', message.count('@'))
    result = split_message.pop(0)

    while len(split_message):
        key = split_message.pop(0)
        if key == 'user':
            result += user
        elif key in bankheist:
            result += bankheist[key]
        else:
            result += ('@' + key + '@')

        if len(split_message):
            result += split_message.pop(0)

    return result

def initBankheist():
    # initialize the bankheist (only happens first time)
    if not check_init_status():
        bankheist['entery_timer'] = InfiniteTimer(bankheist['time_to_enter'], bankheist_in_progress)
        bankheist['in_progress_timer'] = InfiniteTimer(3, bankheist_result)
        bankheist['cooldown_timer'] = InfiniteTimer(bankheist['cooldown_time'] * 60, new_bankheist)
        bankheist.pop('enteries', None) # Delete all enteries of current heist
        bankheist['init_status'] = True

def check_init_status():
    try:
        return bankheist['init_status']
    except KeyError:
        bankheist['init_status'] = False
        return False

def bankheist_in_progress():
    # Start of the heist
    a=1

def bankheist_result():
    # End of the heist
    a=1

def new_bankheist():
    # End of cooldown
    a=1
