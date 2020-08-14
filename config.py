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

# start verification message link
START_VERIF_MSG_LINK = 'https://www.reddit.com/message/compose/?to=CompetitiveTFTBot&subject=r%2FCompetitiveTFT%20Ranked%20Flair%20Verification&message=Please%20type%20your%20**Summoner%20Name**%20below%20**between%20the%20percent%20symbols**%3A%0A%0A%25SUMMONER%20NAME%25%0A%0APlease%20type%20your%20**Region**%20below%20**between%20the%20percent%20symbols**.%20Your%20region%20must%20be%20one%20of%20these%20options%3A%20BR%20%2F%20EUN%20%2F%20EUW%20%2F%20JP%20%2F%20KR%20%2F%20LA%20%2F%20NA%20%2F%20OC%20%2F%20RU%20%2F%20TR%0A%0A%25REGION%25'