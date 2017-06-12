import socket
import string

import src.lib.fileHandler as fileHandler

class irc:

    def __init__(self, config):
        self.__config = config
        self.__socket = None
        self.__read_data = ""
        self.__message_buffer = []

    def get_socket(self):
        return self.__socket

    def join_channel(self):
        self.__open_socket_connection()
        self.__socket.settimeout(None)

        self.__socket.send("PASS " + self.__config['oauth_password'] + "\r\n")
        self.__socket.send("NICK " + self.__config['username'] + "\r\n")
        self.__socket.send("JOIN #" + self.__config['channel'] + "\r\n")

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
                    if self.__config['save_log']:
                        fileHandler.append_to_file(self.__config['save_log_filepath'], line, use_time=True)

        self.send_message(self.__config['entering_message'])

    def send_message(self, message):
        self.__socket.send("PRIVMSG #" + self.__config['channel'] + " :" + message + "\r\n")
        if self.__config['save_log']:
            fileHandler.append_to_file(self.__config['save_log_filepath'], self.__config['username'] + ": " + message, use_time=True)
        if self.__config['debug']:
            print("-- Sent: " + message)

    def read_message(self):
        while not self.__message_buffer:
            self.__read_data += self.__socket.recv(self.__config['socket_buffer_size'])
            self.__message_buffer = string.split(self.__read_data, "\n")
            self.__read_data = self.__message_buffer.pop()
        line = self.__message_buffer.pop(0)

        if line[:4] == "PING": # Check for PING
            self.__socket.send(line.replace("PING", "PONG") + "\r\n")
            return self.read_message()

        temp = line.split(":",2)
        user = unicode(temp[1].split("!", 1)[0], errors='ignore')
        message = unicode(temp[2].split("\r",1)[0], errors='ignore')

        return user, message

    def __open_socket_connection(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(10)

        try:
            self.__socket.connect((self.__config['server'], self.__config['port']))
        except:
            if self.__config['debug']:
                print('-- Cannot connect to server (%s:%s).' % (self.__config['server'], self.__config['port']))
                if self.__config['save_log']:
                    fileHandler.append_to_file(self.__config['save_log_filepath'], \
                        '-- Cannot connect to server (%s:%s).' % (self.__config['server'], self.__config['port']), use_time=True)
