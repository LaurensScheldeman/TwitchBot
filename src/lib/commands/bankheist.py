import string
import random
import time
from datetime import datetime, timedelta

from src.lib.timers import InfiniteTimer
import src.lib.fileHandler as fileHandler
import src.lib.irc as irc_

from src.config.config import config
from src.config.config_userdata import userdata_config
from src.config.config_bankheist import bankheist_config


def bankheist(args):
    if not bankheist_config['enable_bankheist']:
        return ''

    # User wants to join a bankheist
    user = args[0]
    try:
        user_bet = int(args[1])
    except ValueError: # Invalid bet
        return ''

    init_bankheist()

    if bankheist_config['cooldown_timer'].is_running:
        # Bankheist on cooldown
        return decode_message(message=bankheist_config['cooldown_message'], user=user)

    elif bankheist_config['in_progress_timer'].is_running:
        # Bankheist in progress
        return decode_message(message=bankheist_config['late_entery'], user=user)

    elif ((user_bet > 0) and ((bankheist_config['max_bet'] == 0) or (user_bet <= bankheist_config['max_bet']))):

        users_dict = fileHandler.read_json(userdata_config['userdata_filename'])
        if not ((user in users_dict.keys()) and (users_dict[user]['points'] >= user_bet)):
            return '' # Not enough points to bet that much

        # Able to join, will only join if user placed a valid bet
        bankheist_config['enteries'][user] = user_bet
        if config['debug']:
            print('-- ' + user + 'entered the heist with a bet of ' + \
                int_to_string(bankheist_config['enteries'][user]) + ' ' + bankheist_config['currency_name'] + '.')

        current_enteries = len(bankheist_config['enteries'])
        if current_enteries == 1: # First entery
            message = bankheist_config['entery_message_1'] + ' ' + bankheist_config['entery_instructions']
            if bankheist_config['max_bet'] > 0:
                message += ' ' + bankheist_config['max_entery_message']

            bankheist_config['entery_timer'].start()
            if config['debug']:
                print('-- heist_entery_timer started. (' + str(bankheist_config['entery_timer'].seconds) + ' seconds)')

            return decode_message(message=message, user=user)

        elif current_enteries == (bankheist_config['level_1_max_users'] + 1):
            return decode_message(message=bankheist_config['entery_message_2'], user=user)

        elif current_enteries == (bankheist_config['level_2_max_users'] + 1):
            return decode_message(message=bankheist_config['entery_message_3'], user=user)

        elif current_enteries == (bankheist_config['level_3_max_users'] + 1):
            return decode_message(message=bankheist_config['entery_message_4'], user=user)

        elif current_enteries == (bankheist_config['level_4_max_users'] + 1):
            return decode_message(message=bankheist_config['entery_message_5'], user=user)
    return '' # No message to return

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
    bankheist_config['in_progress_timer'].stop()
    print('-- heist_in_progress_timer stopped.')

    seed = int((datetime.now() - datetime(1970,1,1)).total_seconds())
    random.seed(seed)

    # Chance of winning and winning multiplier
    number_of_enteries = len(bankheist_config['enteries'])
    if number_of_enteries <= bankheist_config['level_1_max_users']:
        succes_chance = bankheist_config['level_1_win']
        succes_multiplier = bankheist_config['level_1_win_multiplier']
    elif number_of_enteries <= bankheist_config['level_2_max_users']:
        succes_chance = bankheist_config['level_2_win']
        succes_multiplier = bankheist_config['level_2_win_multiplier']
    elif number_of_enteries <= bankheist_config['level_3_max_users']:
        succes_chance = bankheist_config['level_3_win']
        succes_multiplier = bankheist_config['level_3_win_multiplier']
    elif number_of_enteries <= bankheist_config['level_4_max_users']:
        succes_chance = bankheist_config['level_4_win']
        succes_multiplier = bankheist_config['level_4_win_multiplier']
    else:
        succes_chance = bankheist_config['level_5_win']
        succes_multiplier = bankheist_config['level_5_win_multiplier']

    stolen_amount = 0 # Total amount stolen out of the bank
    souls_survived = 0 # Souls that survived the heist

    users_dict = fileHandler.read_json(userdata_config['userdata_filename'])
    for user in bankheist_config['enteries'].keys():
        if (random.randint(0, 999999)%10000) < int(succes_chance * 100):
            # succes
            users_dict[user]['points'] += bankheist_config['enteries'][user] * (succes_multiplier - 1)
            bankheist_config['enteries'][user] *= succes_multiplier
            stolen_amount += bankheist_config['enteries'][user]
            souls_survived += 1
        else:
            # lose
            users_dict[user]['points'] -= bankheist_config['enteries'][user]
            bankheist_config['enteries'][user] *= -1
    fileHandler.write_json(userdata_config['userdata_filename'], users_dict)

    if len(bankheist_config['enteries']) == 1: # Single user heist
        if souls_survived == 1:
            config['irc'].send_message(decode_message(message=bankheist_config['single_succes'], \
                user=next(iter(bankheist_config['enteries'])), totalwinamount=stolen_amount))
        else:
            config['irc'].send_message(decode_message(message=bankheist_config['single_fail'], \
                user=next(iter(bankheist_config['enteries']))))
    else: # Multiple user heist
        win_rate = (1.*souls_survived)/len(bankheist_config['enteries'])
        if win_rate == 0:
            config['irc'].send_message(decode_message(bankheist_config['multi_fail']))
        else:
            if win_rate == 1:
                config['irc'].send_message(decode_message(message=bankheist_config['multi_succes_100'], totalwinamount=stolen_amount))
            elif win_rate > (2./3):
                config['irc'].send_message(decode_message(message=bankheist_config['multi_succes_34-99%'], totalwinamount=stolen_amount))
            else:
                config['irc'].send_message(decode_message(message=bankheist_config['multi_succes_1-33%'], totalwinamount=stolen_amount))

            message = bankheist_config['heist_outcome']
            for user in bankheist_config['enteries'].keys():
                win_amount = bankheist_config['enteries'][user]
                if win_amount > 0:
                    message += ' '+user+": "+int_to_string(win_amount)+' ('+int_to_string(win_amount/succes_multiplier)+') -'
            time.sleep(3) # Otherwise it sends it too fast
            config['irc'].send_message(message[:-2])

    bankheist_config.pop('enteries', None) # Delete all enteries of current heist
    bankheist_config['enteries'] = {} # Empty dictionary
    bankheist_config['cooldown_timer_starttime'] = datetime.now()
    if bankheist_config['cooldown_time'] > 0:
        bankheist_config['cooldown_timer'].start()
        if config['debug']:
            print('-- heist_cooldown_timer started. (' + str(bankheist_config['cooldown_timer'].seconds) + ' seconds)')

def bankheist_end_of_cooldown():
    # End of cooldown
    bankheist_config['cooldown_timer'].stop()
    if config['debug']:
        print('-- heist_cooldown_timer stopped.')
    config['irc'].send_message(decode_message(bankheist_config['cooldown_over_message']))

def init_bankheist():
    # initialize the bankheist (only happens first time)
    if not check_init_status():
        bankheist_config['entery_timer'] = InfiniteTimer(bankheist_config['time_to_enter'], bankheist_in_progress)
        bankheist_config['in_progress_timer'] = InfiniteTimer(30, bankheist_outcome)
        if bankheist_config['cooldown_time'] > 0:
            bankheist_config['cooldown_timer'] = InfiniteTimer(bankheist_config['cooldown_time'] * 60, bankheist_end_of_cooldown)
        bankheist_config.pop('enteries', None) # Delete all enteries of current heist
        bankheist_config['enteries'] = {} # Empty dictionary
        bankheist_config['init_status'] = True

def decode_message(message, user=None, totalwinamount=0):
    split_message = message.split('@', message.count('@'))
    result = split_message.pop(0)

    while len(split_message):
        key = split_message.pop(0)

        if key == 'user' and user:
            result += user

        elif key == 'totalwinamount':
            result += int_to_string(totalwinamount)

        elif key == 'cooldown_time_left':
            result += str(bankheist_config['cooldown_time'] - int(round((datetime.now() - bankheist_config['cooldown_timer_starttime']).total_seconds()/60)))

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
            result_to_add = bankheist_config[key]
            if type(result_to_add) in [type(0), type(0L)]:
                result += int_to_string(result_to_add)
            else:
                result += result_to_add

        else: # unknown key
            result += ('@' + key + '@')

        if len(split_message):
            # text between two keys, even if only a space
            result += split_message.pop(0)

    return result

def check_init_status():
    try:
        return bankheist_config['init_status']
    except KeyError:
        bankheist_config['init_status'] = False
        return False

def int_to_string(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)
