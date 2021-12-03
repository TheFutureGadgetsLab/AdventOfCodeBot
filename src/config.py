import pytz
import logging

YEAR           = 2020
SESSION_COOKIE = ""
LEADERBOARD    = ""
URL            = f"https://adventofcode.com/{YEAR}/leaderboard/private/view/{LEADERBOARD}.json"
DISCORD_TOKEN  = ''
COMMAND_PREFIX = '!'
UTC = pytz.timezone('UTC')
EST = pytz.timezone('US/Eastern')

logging.basicConfig(level=logging.DEBUG)