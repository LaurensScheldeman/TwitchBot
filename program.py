#!/usr/bin/env python

from src.santaBot import SantaBot
from src.config.config import config

bot = SantaBot(config).run()
