
import requests

import src.lib.fileHandler as fileHandler

def check_valid_client_token(client_ID, client_OAuth):
    if len(client_ID) and len(client_OAuth):
        r = requests.get('https://api.twitch.tv/kraken?oauth_token=' + client_OAuth)
        if r.status_code == requests.codes.ok:
            data = r.json()
            if data['identified'] and data['token']['valid'] and data['token']['client_id']==client_ID:
                return True
    return False

def get_title(client_oAuth):
    r = requests.get('https://api.twitch.tv/kraken/channel?oauth_token=' + client_oAuth)
    if r.status_code == requests.codes.ok:
        data = r.json()
        if 'status' in data.keys():
            return data['status']
    return ''

def update_title(channel, client_oAuth, channel_title):
    if len(channel_title):
        r = requests.put('https://api.twitch.tv/kraken/channels/' + channel +\
            '?oauth_token=' + client_oAuth + '&_method=put&channel[status]=' + channel_title)
        if r.status_code == requests.codes.ok:
            return True
    return False

def get_game(client_oAuth):
    r = requests.get('https://api.twitch.tv/kraken/channel?oauth_token=' + client_oAuth)
    if r.status_code == requests.codes.ok:
        data = r.json()
        if 'game' in data.keys():
            return data['game']
    return ''

def update_game(channel, client_oAuth, channel_game):
    if len(channel_game):
        r = requests.put('https://api.twitch.tv/kraken/channels/' + channel +\
            '?oauth_token=' + client_oAuth + '&_method=put&channel[game]=' + channel_game)
        if r.status_code == requests.codes.ok:
            return True
    return False
