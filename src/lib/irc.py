import socket
import string

import src.lib.fileHandler as fileHandler

class irc:

    def __init__(self, config):
        self.__config = config
        self.__socket = socket.socket()
        self.__read_data = ""
        self.__message_buffer = []

    def get_socket(self):
        return self.__socket

    def join_channel(self):
        self.__open_socket()

        read_data = ""
        loading = True
        while loading:
            read_data = read_data + self.__socket.recv(self.__config['socket_buffer_size'])
            temp = string.split(read_data, "\n")
            read_data = temp.pop()

            for line in temp:
                loading = (False if "End of /NAMES list" in line else True)
                if self.__config['debug']:
                    print(line)

        self.send_message(self.__config['entering_message'])

    def send_message(self, message):
        self.__socket.send("PRIVMSG #" + self.__config['channel'] + " :" + message + "\r\n")
        if self.__config['save_log']:
            fileHandler.append_to_file(self.__config['save_log_filepath'], self.__config['username'] + ": " + message, use_time=True)
        if self.__config['debug']:
            print("-- Sent: " + message)

    def read_message(self):
        if not self.__message_buffer:
            self.__add_buffer()
        line = self.__message_buffer.pop(0)

        if self.__check_for_ping(line):
            return "PING", "PONG"

        temp = line.split(":",2)
        user = u'%s' % temp[1].split("!", 1)[0]
        message = u'%s' % temp[2].split("\r",1)[0]
        return user, message

    def check_ping_message(self, user, message):
        return (True if (user == "PING") and (message == "PONG") else False)

    def __open_socket(self):
        self.__socket.connect((self.__config['server'], self.__config['port']))
        self.__socket.send("PASS " + self.__config['oauth_password'] + "\r\n")
        self.__socket.send("NICK " + self.__config['username'] + "\r\n")
        self.__socket.send("JOIN #" + self.__config['channel'] + "\r\n")

    def __add_buffer(self):
        self.__read_data += self.__socket.recv(self.__config['socket_buffer_size'])
        self.__message_buffer = string.split(self.__read_data, "\n")
        self.__read_data = self.__message_buffer.pop()

    def __check_for_ping(self, line):
        if "PING" in line:
            self.__socket.send(line.replace("PING", "PONG") + "\r\n")
            return True
        return False
