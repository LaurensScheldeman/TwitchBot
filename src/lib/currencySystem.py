import datetime.datetime as datetime

import src.lib.fileHandler as fileHandler

from src.config.config_pointsystem import pointsystem_config

def add_new_user(username):
    users_dict = fileHandler.read_json(pointsystem_config['userdata_filename'])
    userdata = {
        'username': username,
        'points': 0,
        'mod_level': 0, # 0 = user, 1 = moderator, 2 = owner

        'join_data': datetime.now(),
        'last_seen': datetime.now(),

        'vip': False,
        'vip_expire': None
    }
    users_dict[username] = userdata
    fileHandler.write_json(pointsystem_config['userdata_filename'], users_dict)

def update_user(username):
    a=1
