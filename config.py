#!/usr/bin/env python3

# import libraries
import datetime
import os

##### connect.py stuff
# POSTGRESQL credentials
DB_URL = os.environ['DATABASE_URL']

##### main.py stuff
# PRAW credentials for u/CompetitiveTFTBot
R_CLIENT_ID = os.environ['R_CLIENT_ID']
R_CLIENT_SECRET = os.environ['R_CLIENT_SECRET']
R_PASSWORD = os.environ['R_PASSWORD']
R_USERNAME = os.environ['R_USERNAME']
R_USER_AGENT = 'heroku:comp-tft-bot (by /u/lukenamop)'
# subreddit the bot will act on
HOME_SUBREDDIT = 'CompetitiveTFTTestSub'
# reddit command prefix
R_CMD_PREFIX = '!'
# flair_mod_stream error overflow limit
OVERFLOW = 5

# riot API token
RIOT_API_TOKEN = os.environ['RIOT_API_TOKEN']
# custom flair character limit
CUSTOM_FLAIR_CHAR_LIM = 30
# auto-updater sleep time between flair updates (seconds)
AUTO_UPDATE_SLEEP_TIME = 60
# auto-updater flair decay lockout start (epoch timestamp)
AUTO_UPDATE_LOCKOUT_START = 1600153200
# auto-updater flair decay lockout duration (days)
AUTO_UPDATE_LOCKOUT_DAYS = 30
# auto-updater flair decay lockout start and end datetime objects
AUTO_UPDATE_LOCKOUT_START_DATETIME = datetime.datetime.fromtimestamp(AUTO_UPDATE_LOCKOUT_START)
AUTO_UPDATE_LOCKOUT_END_DATETIME = AUTO_UPDATE_LOCKOUT_START_DATETIME + datetime.timedelta(days=AUTO_UPDATE_LOCKOUT_DAYS)
# dict of all ranked tiers and divisions
RANKED_TIER_DICT = {
	'Unranked': 0,
	'Iron': 1,
	'Bronze': 2,
	'Silver': 3,
	'Gold': 4,
	'Platinum': 5,
	'Diamond': 6,
	'Master': 7,
	'Grandmaster': 8,
	'Challenger': 9
}
RANKED_DIV_DICT = {
	'IV': 0,
	'III': 1,
	'II': 2,
	'I': 3
}
RANKED_TIER_FLAIR_DICT = {
	'Unranked': None,
	'Iron': '02ffc88c-de8d-11ea-b61c-0e68680acae9',
	'Bronze': '0c755e18-de8d-11ea-bbc0-0ec8330c3f45',
	'Silver': '0e2281fa-de8d-11ea-b1b5-0e924619d27b',
	'Gold': '10e74358-de8d-11ea-958d-0e6b190ecc7b',
	'Platinum': '13fd6a4a-de8d-11ea-928c-0e8484cf5443',
	'Diamond': '16723b66-de8d-11ea-9ce7-0e3953cf8987',
	'Master': '48b9e132-de8d-11ea-a71f-0e762dd480fb',
	'Grandmaster': '4c638c7a-de8d-11ea-b264-0ef6b978cbfb',
	'Challenger': '4f4a4d5c-de8d-11ea-b610-0efb666e413f'
}
REGION_DICT = {
	'br': 'br1',
	'eun': 'eun1',
	'euw': 'euw1',
	'jp': 'jp1',
	'kr': 'kr',
	'la': 'la',
	'na': 'na1',
	'oc': 'oc1',
	'ru': 'ru',
	'tr': 'tr1'
}

# verification message links
START_VERIF_MSG_LINK = f'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification&message=Please%20type%20your%20Summoner%20Name%20below%20between%20the%20percent%20symbols%3A%0A%0A%25SUMMONER%20NAME%25%0A%0APlease%20type%20your%20Region%20below%20between%20the%20percent%20symbols.%20Your%20region%20must%20be%20one%20of%20these%20options%3A%20BR%20%2F%20EUN%20%2F%20EUW%20%2F%20JP%20%2F%20KR%20%2F%20LA%20%2F%20NA%20%2F%20OC%20%2F%20RU%20%2F%20TR%0A%0A%25REGION%25%0A%0APlease%20type%20your%20preferred%20Custom%20Flair%2C%20up%20to%20{CUSTOM_FLAIR_CHAR_LIM}%20characters%20%28it%20will%20appear%20like%20this%3A%20Grandmaster%20%7C%20Custom%20Flair%29%2C%20below%20between%20the%20percent%20symbols%3A%0A%0A%25CUSTOM%20FLAIR%25'
FINISH_VERIF_MSG_LINK = 'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification%20-%20Part%202&message=Click%20the%20%22send%22%20button%20to%20complete%20your%20verification%21'