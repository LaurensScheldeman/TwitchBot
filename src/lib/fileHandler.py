import os
from datetime import datetime
import string

def create_empty_file(path):
    # Creates an empty file, override the file if it already exists
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w"):
        pass

def append_to_file(path, text_to_append, use_date=False, use_time=False):
    if use_date or use_time:
        time = datetime.now().time()
        date = datetime.now().date()
        stamp = ""
        if use_date:
            stamp += str(date.day)+"/"+str(date.month)+"/"+str(date.year)
        if use_date and use_time:
            stamp += " "
        if use_time:
            stamp += str(time.hour)+":"+str(time.minute)
        text_to_append = "[" + stamp + "] " + text_to_append

    with open(path, 'a') as file:
        file.write(text_to_append)
