import string

import src.lib.fileHandler as fileHandler

from src.config.config_pointsystem import pointsystem_config
from src.config.config_commands import commands_config
from src.config.config_userdata import userdata_config

def give(args):
    try:
        user_giving = args[0].decode('utf-8').lower()
        user_receiving = args[1].decode('utf-8').lower()
        giving_amount = int(args[2])
    except:
        return 'Please use command correctly: ' + commands_config[pointsystem_config['transfer_command']]['usage']

    if giving_amount <= 0:
        return 'Transfer amount must be greather than zero.'

    if user_giving == user_receiving:
        return user_giving + ', think you are funny? I\'m not that stupid...'

    users_dict = fileHandler.read_json(userdata_config['userdata_filename'])

    if not (user_giving in users_dict.keys()):
        return 'You haven\'t been long enough in this channel to use this command. Please try again afther more than' + \
            str(userdata_config['updata_interval']) + 'minutes.'

    if not (user_receiving in users_dict.keys()):
        return 'Can\'t find user \'' + user_receiving + '\'.'

    if users_dict[user_giving]['points'] < giving_amount:
        if users_dict[user_giving]['authorisation'] != 'moderator':
            return user_giving + ', you don\'t have enough ' + pointsystem_config['currency_name'] + '.'
        else:
            users_dict[user_giving]['points'] = giving_amount

    users_dict[user_giving]['points'] -= giving_amount
    users_dict[user_receiving]['points'] += giving_amount

    fileHandler.write_json(userdata_config['userdata_filename'], users_dict)

    return 'Transfered ' + str(giving_amount) + ' ' + pointsystem_config['currency_name'] + \
        ' from ' + user_giving + ' to ' + user_receiving + '.'
