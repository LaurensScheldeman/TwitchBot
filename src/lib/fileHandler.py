import os
from datetime import datetime
import string

def create_empty_file(filepath):
    # Creates an empty file, override the file if it already exists
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, "w"):
        pass

def rename_file(filepath, new_filename):
    if check_file_exist(filepath):
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
    return os.path.exists(filepath)
