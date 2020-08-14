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


##### REDDIT MODERATION FUNCTIONS #####

def inbox_reply_stream(mp_lock, reddit, iteration=1):
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
			respond_to_message = True
			if message.created_utc < (time.time() - 60 * 30):
				respond_to_message = False

			if respond_to_message:
				# mark any new message as read
				reddit.inbox.mark_read([message])

				# start the verification process for a new user
				if message.subject == 'r/CompetitiveTFT Ranked Flair Verification':
					# generate random 6 character string excluding unwanted_chars
					unwanted_chars = ["0", "O", "l", "I"]
					char_choices = [char for char in string.ascii_letters if char not in unwanted_chars] + [char for char in string.digits if char not in unwanted_chars]
					verification_string = ''.join(random.choices(char_choices, k=6))
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

	# create a multiprocessing lock
	mp_lock = Lock()

	# start the inbox reply stream
	inbox_reply_stream_process = Process(target=inbox_reply_stream, args=(mp_lock, reddit,))
	inbox_reply_stream_process.start()

if __name__ == '__main__':
	main()