import os
import json

import string
from datetime import datetime

from src.config.config import config

def create_empty_file(filepath):
    # Creates an empty file, override the file if it already exists
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, "w"):
        pass

def rename_file(filepath, new_filename):
    if check_file_exist(filepath):
        if check_file_exist(os.path.dirname(filepath) + '/' + new_filename):
            os.remove(os.path.dirname(filepath) + '/' + new_filename)
        os.rename(filepath, os.path.dirname(filepath) + '/' + new_filename)

def append_to_file(filepath, text_to_append, use_date=False, use_time=False):
    # Add text to the end of a file
    if not check_file_exist(filepath):
        create_empty_file(filepath)

    if use_date or use_time:
        time = datetime.now().time()
        date = datetime.now().date()

        stamp = ""
        if use_date:
            stamp += ("0" if date.month < 10 else "") + str(date.month) \
                     + ("/0" if date.day < 10 else "/") + str(date.day) \
                     + "/"+str(date.year)
            if use_time:
                stamp += " "
        if use_time:
            stamp += ("0" if time.hour < 10 else "") + str(time.hour) \
                     +(":0" if time.minute < 10 else ":") + str(time.minute)
        text_to_append = "[" + stamp + "] " + text_to_append + "\n"

    with open(filepath, 'a') as file:
        file.write(text_to_append)

def check_file_exist(filepath):
    return (os.path.isfile(filepath) and os.access(filepath, os.R_OK))

def write_json(filepath, data):
    if check_file_exist(filepath):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
    else:
        create_empty_file(filepath)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

def read_json(filepath):
    if check_file_exist(filepath):
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except ValueError, e:
                if e.message != "No JSON object could be decoded":
                    raise ValueError, e
                else:
                    if config['debug']:
                        message = '-- Invalid json file: ' + filepath
                        print(message)
                        if config['save_log']:
                            append_to_file(config['save_log_filepath'], message, use_time=True)
                    data = {}
    else:
        data = {}
    return data
