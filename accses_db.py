import os

from config import Config



db = Database(Config.MONGODB_URI, Config.BOT_USERNAME)
