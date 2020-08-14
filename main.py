#!/usr/bin/env python3

# import libraries
import math
import praw
import prawcore
import random
import requests
import time
from multiprocessing import Process, Lock
from unidecode import unidecode

# import additional files
import config
import connect
from sql_functions import execute_sql

def initialize_reddit(client_id=config.R_CLIENT_ID,client_secret=config.R_CLIENT_SECRET,password=config.R_PASSWORD,username=config.R_USERNAME,user_agent=config.R_USER_AGENT):
	reddit = praw.Reddit(client_id=client_id,
		client_secret=client_secret,
		password=password,
		username=username,
		user_agent=user_agent)
	print('reddit object initialized')
	return reddit

def prepare_request_headers(riot_token=config.RIOT_API_TOKEN):
	request_headers = {'User-Agent': 'r/CompetitiveTFT Ranked Flair Bot', 'Accept-Language': 'en-US,en;q=0.9', 'Accept-Charset': 'utf-8', 'X-Riot-Token': riot_token}
	return request_headers


##### REDDIT MODERATION FUNCTIONS #####

def inbox_reply_stream(mp_lock, reddit, request_headers, iteration=1):
	print('inbox_reply_stream started')

	# connect to the database
	connect.db_connect('inbox reply stream')
	connect.db_stats()

	subreddit = reddit.subreddit(config.HOME_SUBREDDIT)
	try:
		messages = reddit.inbox.messages
		# iterate through all mentions, indefinitely
		for message in praw.models.util.stream_generator(messages, skip_existing=True):
			# make sure the message is actually new
			check_message = True
			if message.created_utc < (time.time() - 60 * 30):
				check_message = False

			if check_message:
				# mark any new message as read
				reddit.inbox.mark_read([message])

				# start the verification process for a new user
				if message.subject == 'r/CompetitiveTFT Ranked Flair Verification':
					# check to see if the message template was followed
					try:
						riot_summoner_name = unidecode(message.body.split('%')[1].split('%')[0])
						riot_region = unidecode(message.body.split('%')[3].split('%')[0])
						print(f'rsn: {riot_summoner_name}\nrr: {riot_region}')
					except IndexError:
						print(f'message from u/{message.author.name} did not follow verification template')
						check_message = False

					if check_message:
						pass

	except prawcore.exceptions.ServerError as error:
		print(f'skipping message due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.RequestException as error:
		print(f'skipping message due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.ResponseException as error:
		print(f'skipping message due to PRAW error: {type(error)}: {error}')
	except Exception as error:
		print(f'skipping message due to unknown error: {type(error)}: {error}')

	iteration += 1
	if iteration <= config.OVERFLOW:
		inbox_reply_stream(mp_lock, reddit, iteration)
	else:
		print(f'killing inbox reply stream, >{config.OVERFLOW} skipped logs')


##### CODE TO RUN AT LAUNCH #####

def main():
	# initialize a reddit object
	reddit = initialize_reddit()

	# initialize request headers
	request_headers = prepare_request_headers()

	# create a multiprocessing lock
	mp_lock = Lock()

	# start the inbox reply stream
	inbox_reply_stream_process = Process(target=inbox_reply_stream, args=(mp_lock, reddit, request_headers,))
	inbox_reply_stream_process.start()

if __name__ == '__main__':
	main()