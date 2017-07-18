# Twitchbot santaBot
This is a simple twitch chat/irc bot written in python.

# Requirements
As this twitchbot is written in python, python is needed to execute the program. I recommend to use anaconda [https://www.continuum.io/downloads] as python program. This twitchbot is written in python 2.7, so if you download it, I recommend this version of the software.

# Connect to your channel
To connect to your channel you need to set the configuration to connect to your server, and channel. Inside the GUI tab `Botsettings` there is a section `IRC configuration`. There are the settings to connect to your channel. You will also find a section `Save log` to enable debug mode, so it gives some extra information into the console [recommended]. Also, it will save a version of your console to a .txt file by default. You can disable this with the `save chat and debug to file` parameter, as wel as the `Show debug in command prompt`.

# Adding new commands
To add basic commands, go to the tab `Commands`. There are examples of pre-made commands in there as examples, and some gambling games. The cooldown parameter is the amount of times inbetween the command can be used in seconds, if you don't want a limit, don't put in the cooldown parameter, or set it to 0.

If your command is only going to return a string, ex - `!ping` returns `!pong`, you will have to place the string you wish to be returned to the user in the `Response text` parameter. For example, if you wanted to create a command such as this and limit it to being used ever 30 seconds, you would add in:

```python
Command name: !ping
Cooldown (sec): 30
Return type: Simple text response
Response text: !pong
```

However, if your command has to have some logic implemented and if the command is just going to return whatever a function returns, set the `return` parameter on the command to `command`. If your command is going to take arguments, ex `!hello <name>`, set argc to `1` or however many arguments the command is going to take in. If you don't need any arguments, set the `argc` parameter to 0, or don't include it (It defaults to 0).

You're going to need to know basic Python if you want to add advanced commands. Make a new file in `src/commands/` and give the filename `command.py` where command is the command name (without the explanation point `!`). Add a new function `command` and set the only function parameter to `args`. Args will contain a list of whatever arguments were passed to the command. Remember, the args will be strings, so you will need to convert them into your desired type.

This command will contain whatever logic needs to be carried out. You should validate the arguments in there. After you have the response that you want a user to see, just `return` it.

Let's say we want to add a command which will take two arguments, we will call it `!randomNumber` and it will take a `minimum` and `maximum` argument. We will limit this command to be allowed to be called every 20 seconds.

Add the following command to the GUI:

```python
Command name: !randomNumber
Cooldown (sec): 20
Return type: Command response
Number of arguments: 2
Command usage: Please use the command correctly: !randomNumber [min] [max]
```

And then add the file `src/commands/randomNumber.py` , write the following:

```python
import random
from datetime import datetime, timedelta

def randomNumber(args):
    try:
        min_ = int(args[0])
        max_ = int(args[1])
    except ValueError:
        return "Please use the command correctly: !randomNumber [min] [max]"

    if min_ > max_:
        # Swap min_ and max_
        min_ += max_
        max_ = min_ - max_
        min_ -= max_

    elif min_ == max_:
        return str(min_)

    seed = int((datetime.now() - datetime(1970,1,1)).total_seconds())
    random.seed(seed)
    return str(random.randint(min_, max_))
```

And now if somebody types `!randomNumber 5 10` into the chat, the bot will respond with a pseudo-random number between 5 and 10 if the command is not on cooldown.
