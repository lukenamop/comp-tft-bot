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
HOME_SUBREDDIT = 'CompetitiveTFT'
# reddit command prefix
R_CMD_PREFIX = '!'
# flair_mod_stream error overflow limit
OVERFLOW = 5

# riot API token
RIOT_API_TOKEN = os.environ['RIOT_API_TOKEN']
# custom flair character limit
CUSTOM_FLAIR_CHAR_LIM = 30
# auto-updater sleep time between flair updates (seconds)
AUTO_UPDATE_SLEEP_TIME = 15
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
# dict of all ranked flair template IDs
RANKED_TIER_FLAIR_DICT = {
	'Unranked': None,
	'Iron': '80c0cc06-74ef-11ea-9d33-0eba2ee63b05',
	'Bronze': '897d9e82-74ef-11ea-9046-0e1e5f6d96db',
	'Silver': '9032ee12-74ef-11ea-88ec-0e377b41a0af',
	'Gold': '92d2d04c-74ef-11ea-874f-0ecf395933d7',
	'Platinum': '968bb0be-74ef-11ea-8d72-0e7b9a34f76f',
	'Diamond': '99461b00-74ef-11ea-8c0b-0e77129c2301',
	'Master': 'f9c10fec-dea5-11ea-b61c-0e68680acae9',
	'Grandmaster': '15e31148-dea6-11ea-9f4b-0e1ba84af911',
	'Challenger': '23277cc2-dea6-11ea-8216-0ef1c84efa99'
}
# dict of all regions
REGION_DICT = {
	'br': 'br1',
	'eun': 'eun1',
	'euw': 'euw1',
	'jp': 'jp1',
	'kr': 'kr',
	'la': 'la',
	'las': 'la',
	'lan': 'la',
	'na': 'na1',
	'oc': 'oc1',
	'ru': 'ru',
	'tr': 'tr1'
}

# verification message links
START_VERIF_MSG_LINK = f'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification&message=To%20verify%20your%20account%2C%20please%20type%20your%20Summoner%20Name%2C%20Region%2C%20and%20an%20optional%20Custom%20Flair%20below%20between%20the%20dashes.%20Region%20must%20be%20one%20of%20BR%20%2F%20EUN%20%2F%20EUW%20%2F%20JP%20%2F%20KR%20%2F%20LA%20%2F%20NA%20%2F%20OC%20%2F%20RU%20%2F%20TR.%20Custom%20Flair%20must%20be%20{CUSTOM_FLAIR_CHAR_LIM}%20characters%20or%20less%20and%20will%20display%20like%20this%3A%20Grandmaster%20%7C%20Custom%20Flair%20%28if%20you%20don%27t%20want%20a%20custom%20flair%2C%20leave%20CUSTOM%20FLAIR%20as-is%29.%20%20%20%20%20%20%20%20--SUMMONER%20NAME--%20%20%20%20%20%20%20%20--REGION--%20%20%20%20%20%20%20%20--CUSTOM%20FLAIR--'
FINISH_VERIF_MSG_LINK = 'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification%20-%20Part%202&message=Click%20the%20%22send%22%20button%20to%20complete%20your%20verification%21'

# pushshift guide search config
GUIDE_LIMIT = 10