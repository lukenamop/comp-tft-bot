#!/usr/bin/env python3

# import libraries
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
# flair_mod_stream error overflow limit
OVERFLOW = 5

# riot API token
RIOT_API_TOKEN = os.environ['RIOT_API_TOKEN']
# custom flair character limit
CUSTOM_FLAIR_CHAR_LIM = 30
# auto-updater sleep time between flair updates (seconds)
AUTO_UPDATE_SLEEP_TIME = 15
# dict of all ranked tiers
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

# verification message links
START_VERIF_MSG_LINK = f'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification&message=Please%20type%20your%20Summoner%20Name%20below%20between%20the%20percent%20symbols%3A%0A%0A%25SUMMONER%20NAME%25%0A%0APlease%20type%20your%20Region%20below%20between%20the%20percent%20symbols.%20Your%20region%20must%20be%20one%20of%20these%20options%3A%20BR%20%2F%20EUN%20%2F%20EUW%20%2F%20JP%20%2F%20KR%20%2F%20LA%20%2F%20NA%20%2F%20OC%20%2F%20RU%20%2F%20TR%0A%0A%25REGION%25%0A%0APlease%20type%20your%20preferred%20Custom%20Flair%2C%20up%20to%20{CUSTOM_FLAIR_CHAR_LIM}%20characters%20%28it%20will%20appear%20like%20this%3A%20Grandmaster%20%7C%20Custom%20Flair%29%2C%20below%20between%20the%20percent%20symbols%3A%0A%0A%25CUSTOM%20FLAIR%25'
FINISH_VERIF_MSG_LINK = 'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification%20-%20Part%202&message=Click%20the%20%22send%22%20button%20to%20complete%20your%20verification%21'