import string

import src.lib.fileHandler as fileHandler

from src.config.config_pointsystem import pointsystem_config
from src.config.config_userdata import userdata_config

def shreckles(args):
    try:
        user = args[0].decode('utf-8').lower()
    except:
        return ''

    users_dict = fileHandler.read_json(userdata_config['userdata_filename'])

    if user in users_dict.keys():
        return decode_message(pointsystem_config['check_balance_message'], users_dict[user]['points'], user)
    else:
        return 'You haven\'t been long enough in this channel to use this command. Please try again in ' + \
            str(userdata_config['updata_interval']) + 'minutes.'

def decode_message(message, user_points_amount, user=None):
    split_message = message.split('@', message.count('@'))
    result = split_message.pop(0)

    while len(split_message):
        key = split_message.pop(0)

        if key == 'user' and user:
            result += user

        elif key == 'amount':
            result += int_to_string(user_points_amount)

        elif key in pointsystem_config:
            result_to_add = pointsystem_config[key]
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
