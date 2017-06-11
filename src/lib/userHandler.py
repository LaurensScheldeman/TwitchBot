
import urllib2
import ast
from datetime import datetime

import src.lib.fileHandler as fileHandler
from src.lib.timers import InfiniteTimer

from src.config.config import config
from src.config.config_pointsystem import pointsystem_config

class userHandler:
    def __init__(self, userdata_config):
        self.__userdata_config = userdata_config

        if self.__userdata_config['updata_interval'] > 0:
            self.__userdata_config['updata_timer'] = InfiniteTimer(self.__userdata_config['updata_interval'] * 60, self.update_userdata)
            self.__userdata_config['updata_timer'].start()

    def update_userdata(self):
        if config['debug']:
            message = '-- Updating userdata, this can take a second.'
            print(message)
            if config['save_log']:
                fileHandler.append_to_file(config['save_log_filepath'], message, use_time=True)

        users_dict = self.__get_users_from_savefile()

        user_count, users = self.__get_users_from_channel()
        for user_type in users.keys():
            authorisation_type = self.__get_authorisation_type(user_type)

            for user in users[user_type]: # Iterate over all active users in the channel
                user = user.decode('utf-8').lower()
                if user in users_dict.keys():
                    users_dict[user]['authorisation'] = authorisation_type
                    users_dict[user]['last_seen'] = datetime.now().strftime('%m/%d/%Y %H:%M')
                    users_dict[user]['points'] += int(pointsystem_config['points_over_time']*self.__userdata_config['updata_interval']*(1./60))
                else:
                    users_dict[user] = self.__add_new_user(user, authorisation_type)

        self.__save_users_to_savefile(users_dict)

        if config['debug']:
            message = '-- Done updating userdata.'
            print(message)
            if config['save_log']:
                fileHandler.append_to_file(config['save_log_filepath'], message, use_time=True)

    def __get_users_from_savefile(self):
        return fileHandler.read_json(self.__userdata_config['userdata_filename'])

    def __save_users_to_savefile(self, users_dict):
        fileHandler.write_json(self.__userdata_config['userdata_filename'], users_dict)

    def __add_new_user(self, username, authorisation):
        userdata = {
            'username': username,
            'points': 0,
            'authorisation': authorisation, # empty, mod, global_mod, admin or staff

            'join_data': datetime.now().strftime('%m/%d/%Y %H:%M'),
            'last_seen': datetime.now().strftime('%m/%d/%Y %H:%M'),
        }
        return userdata

    def __get_users_from_channel(self):
        request = 'http://tmi.twitch.tv/group/user/' + config['channel'] + '/chatters'
        response = urllib2.urlopen(request).read()
        chatters = ast.literal_eval(response)
        return chatters['chatter_count'], chatters['chatters']

    def __get_authorisation_type(self, user_type):
        if user_type == 'viewers':
            return 'empty'
        elif user_type == 'moderators':
            return 'moderator'
        elif user_type == 'global_mods':
            return 'global_moderator'
        elif user_type == 'admins':
            return 'admin'
        elif user_type == 'staff':
            return 'staff'
        else:
            return 'unknown'
