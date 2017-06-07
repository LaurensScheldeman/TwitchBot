global config

SantaBot_config = {

    # Details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'lovely_santa',
    'oauth_password': 'oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # get this from http://twitchapps.com/tmi/

    # Channel to join
    'channel': 'lovely_santa',
    'entering_message': '<santaBot> succesfully joined the channel.',

    # If set to true will display any debug data in console
    'debug': True,

    # Maximum amout of bytes to receive from socket (1024-4096)
    'socket_buffer_size': 1024,

} # End of Config
