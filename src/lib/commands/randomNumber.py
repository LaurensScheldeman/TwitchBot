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
