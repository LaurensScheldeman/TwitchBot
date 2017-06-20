import string

from src.lib.timers import InfiniteTimer
import src.lib.fileHandler as fileHandler

from src.config.config import config
from src.config.config_userdata import userdata_config
from src.config.config_roulette import roulette_config

def roulette(args):
    if not roulette_config['enable_roulette']:
        return ''
    if args[1] == 'help':
        return roulette_config['usage_help']

    # User wants to join roulette
    user = args[0]
    try:
        user_bet = int(args[1])
    except ValueError: # Invalid bet
        return ''
    bet_option = args[2]

    init_roulette()

    if roulette_config['in_progress_timer'].is_running:
        return decode_message(message=roulette_config['late_entery'], user=user)

    elif ((user_bet > 0) and ((roulette_config['max_bet'] == 0) or (user_bet <= roulette_config['max_bet']))):

        users_dict = fileHandler.read_json(userdata_config['userdata_filename'])
        if not ((user in users_dict.keys()) and (users_dict[user]['points'] >= user_bet)):
            if config['debug']:
                print('-- ' + user + 'cannot join roulette with that amount (' + str(user_bet) + ')')
            return '' # Not enough points to bet that much

        # Able to join, will only join if user placed a valid bet
        bet_type = check_bet_type(bet_option)
        if bet_type == 'Invalid':
            if config['debug']:
                print('-- invalid bet')
            return ''
        if bet_type == 'Number':
            bet_option = int(bet_option)
        roulette_config['enteries'][user] = {
            'bet_type': bet_type,
            'placed_bet': bet_option,
            'bet_amount': user_bet
        }
        if config['debug']:
            print('-- ' + user + 'entered the roulette with a bet of ' + \
                int_to_string(roulette_config['enteries'][user]['bet_amount']) + \
                ' ' + roulette_config['currency_name'] + ' on ' + roulette_config['enteries'][user]['bet_type'] + \
                ' ' + roulette_config['enteries'][user]['placed_bet'])
        if len(roulette_config['enteries']) == 1:
            roulette_config['entery_timer'].start()
            if config['debug']:
                print('-- roulette entery timer started'


    return '' # No message to return

def roulette_in_progress():
    a=1

def roulette_outcome():
    a=1

def decode_message(message, user=None):
    split_message = message.split('@', message.count('@'))
    result = split_message.pop(0)

    while len(split_message):
        key = split_message.pop(0)

        if key == 'user' and user:
            result += user

        elif key in roulette_config:
            result_to_add = roulette_config[key]
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

def init_roulette():
    # initialize the bankheist (only happens first time)
    if not check_init_status():
        roulette_config['entery_timer'] = InfiniteTimer(roulette_config['time_to_enter'], roulette_in_progress)
        roulette_config['in_progress_timer'] = InfiniteTimer(300, roulette_outcome)
        roulette_config.pop('enteries', None) # Delete all enteries of current heist
        roulette_config['enteries'] = {} # Empty dictionary
        roulette_config['init_status'] = True

def check_init_status():
    try:
        return roulette_config['init_status']
    except KeyError:
        roulette_config['init_status'] = False
        return False

def check_bet_type(bet_option): # Returns 'Number', 'Numbertype', 'Colortype' or 'Invalid'
    if (bet_option == 'even' or bet_option == 'odd'):
        return 'Numbertype'
    elif (bet_option == 'red' or bet_option == 'black' or bet_option == 'green'):
        return 'Colortype'
    else:
        try:
            number = int(bet_option)
            return 'Number' if (number >= 0 and number <= 36) else 'Invalid'
        except ValueError:
            return 'Invalid'

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
