#!/usr/bin/env python

from src.chatbot import ChatBot
from src.config.config import config

bot = ChatBot(config).run()
