"""
Simple IRC Bot for Twitch.tv

Developed by Laurens Scheldeman <laurens.scheldeman@gmail.com>
"""
import lib.irc as irc_


class SantaBot:

    def __init__(self, config):
        self.__config = config
        self.__irc = irc_.irc(config)
        self.__socket = self.__irc.get_socket()


    def run(self):
        self.__irc.join_channel()

        while True:
            user, message = self.__irc.read_message()

            if (user != "PING") and (message != "PONG"):
                if self.__config['debug']:
                    print(user + ": " + message)
