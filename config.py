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