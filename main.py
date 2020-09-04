#!/usr/bin/env python3

# import libraries
import datetime
import json
import math
import praw
import prawcore
import random
import requests
import string
import time
from multiprocessing import Process, Lock
from sklearn.feature_extraction.text import TfidfVectorizer
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
		# iterate through all mentions indefinitely
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
					fail_message = None
					try:
						riot_summoner_name = unidecode(message.body.split('%')[1].split('%')[0]).strip()
						if len(riot_summoner_name) > 30:
							fail_message = message.reply(f"""There was an error fetching your summoner profile.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
						riot_region = unidecode(message.body.split('%')[3].split('%')[0]).lower().strip()
						custom_flair = unidecode(message.body.split('%')[5].split('%')[0]).strip()
						if len(custom_flair) > config.CUSTOM_FLAIR_CHAR_LIM:
							fail_message = message.reply(f"""Your custom flair `{custom_flair}` was too long, it cannot be longer than 30 characters.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
					except IndexError:
						fail_message = message.reply(f"""It doesn't look like you followed the message template.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
						print(f'did not follow verification template: u/{message.author.name}')

					if fail_message is None:
						# strip numbers off of the provided region
						riot_region = riot_region.translate(str.maketrans('', '', '0123456789'))

						# make sure the provided region matches one of the options
						if riot_region not in config.REGION_DICT.keys():
							fail_message = message.reply(f"""The region you provided, `{riot_region.upper()}`, was not valid.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
							print(f'invalid region: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}')
						else:
							riot_region = config.REGION_DICT[riot_region]
						
					if fail_message is None:
						riot_summoner_id = None

						# first check both 'la' regions
						if riot_region == 'la':
							try_riot_region = 'la1'
							# request the summoner from riot
							summoner_json = requests.get(f"""https://{try_riot_region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{riot_summoner_name}""", headers=request_headers).json()
							try:
								riot_summoner_id = summoner_json['id']
								riot_region = try_riot_region
							except KeyError:
								try_riot_region = 'la2'
								# request the summoner from riot
								summoner_json = requests.get(f"""https://{try_riot_region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{riot_summoner_name}""", headers=request_headers).json()
								try:
									riot_summoner_id = summoner_json['id']
									riot_region = try_riot_region
								except KeyError:
									try:
										fail_message = message.reply(f"""There was an error fetching your summoner profile: `{summoner_json['status']['message']}`\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
										print(f"""{summoner_json['status']['status_code']} error fetching summoner: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}: {summoner_json['status']['message']}""")
									except KeyError:
										fail_message = message.reply(f"""There was an unknown error fetching your summoner profile. If this issue continues, please contact u/lukenamop.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
										print(f'unknown error fetching summoner: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}')
						
						# then check all other regions
						if fail_message is None and riot_region not in ['la', 'la1', 'la2']:
							# request the summoner from riot
							summoner_json = requests.get(f"""https://{riot_region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{riot_summoner_name}""", headers=request_headers).json()
							try:
								riot_summoner_id = summoner_json['id']
							except KeyError:
								try:
									fail_message = message.reply(f"""There was an error fetching your summoner profile: `{summoner_json['status']['message']}`\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
									print(f"""{summoner_json['status']['status_code']} error fetching summoner: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}: {summoner_json['status']['message']}""")
								except KeyError:
									fail_message = message.reply(f"""There was an unknown error fetching your summoner profile. If this issue continues, please contact u/lukenamop.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
									print(f'unknown error fetching summoner: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}')

					if fail_message is None:
						# parse the custom flair
						if custom_flair in ['CUSTOM FLAIR', '']:
							custom_flair = None

						# generate random 6 character string excluding unwanted_chars
						unwanted_chars = ["0", "O", "l", "I"]
						char_choices = [char for char in string.ascii_letters if char not in unwanted_chars] + [char for char in string.digits if char not in unwanted_chars]
						riot_verification_key = ''.join(random.choices(char_choices, k=6))

						# see if the redditor exists in the database
						redditor_exists = False
						query = 'SELECT db_id, custom_flair FROM flaired_redditors WHERE reddit_username = %s'
						q_args = [message.author.name]
						execute_sql(query, q_args)
						if connect.db_crsr.fetchone() is not None:
							redditor_exists = True

						# if the redditor doesn't exist, add them to the database
						if not redditor_exists:
							query = 'INSERT INTO flaired_redditors (reddit_username, riot_region, riot_summoner_name, riot_summoner_id, riot_verification_key, custom_flair) VALUES (%s, %s, %s, %s, %s, %s)'
							q_args = [message.author.name, riot_region, riot_summoner_name, riot_summoner_id, riot_verification_key, custom_flair]
							execute_sql(query, q_args)
							connect.db_conn.commit()
						# if the redditor exists, update them in the database
						else:
							query = 'UPDATE flaired_redditors SET riot_region = %s, riot_summoner_name = %s, riot_summoner_id = %s, riot_verification_key = %s, custom_flair = %s WHERE reddit_username = %s'
							q_args = [riot_region, riot_summoner_name, riot_summoner_id, riot_verification_key, custom_flair, message.author.name]
							execute_sql(query, q_args)
							connect.db_conn.commit()

						# send the redditor instructions to complete verification
						message.reply(f'Your unique verification key is `{riot_verification_key}`. To complete verification, follow these steps:'
							+ '\n\n1. Open the **League of Legends** client'
							+ '\n2. Click the **Settings** cog in the top right'
							+ '\n3. On the left-hand side, scroll all the way down to the **Verification** tab'
							+ f'\n4. Enter your unique verification key (`{riot_verification_key}`)'
							+ '\n5. Click **Save**'
							+ f'\n6. [Click here and then click "send" to complete your verification!]({config.FINISH_VERIF_MSG_LINK})')
						print(f"""verification key sent to u/{message.author.name}""")

				# attempt to complete a user's verification
				if message.subject == 'r/CompetitiveTFT Ranked Flair Verification - Part 2':
					# search for the redditor in the database
					fail_message = None
					query = 'SELECT db_id, riot_region, riot_summoner_name, riot_summoner_id, riot_verification_key, custom_flair FROM flaired_redditors WHERE reddit_username = %s'
					q_args = [message.author.name]
					execute_sql(query, q_args)
					result = connect.db_crsr.fetchone()
					if result is None:
						fail_message = message.reply(f"""It looks like you haven't completed the first step of verification.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")

					if fail_message is None:
						db_id, riot_region, riot_summoner_name, riot_summoner_id, riot_verification_key, custom_flair = result
						# request the summoner's third party code from riot
						third_party_code = requests.get(f"""https://{riot_region}.api.riotgames.com/lol/platform/v4/third-party-code/by-summoner/{riot_summoner_id}""", headers=request_headers).text.strip('"')

						# check the summoner's third party code against their verification key in the database
						if third_party_code != riot_verification_key:
							fail_message = message.reply(f"""Your verification key was incorrect.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")

					if fail_message is None:
						# request the summoner's ranked info from riot
						ranked_json = requests.get(f"""https://{riot_region}.api.riotgames.com/tft/league/v1/entries/by-summoner/{riot_summoner_id}""", headers=request_headers).json()
						try:
							riot_verified_rank_tier = ranked_json[0]['tier'].capitalize()
							riot_verified_rank_division = ranked_json[0]['rank']
							riot_verified_rank = f'{riot_verified_rank_tier} {riot_verified_rank_division}'
						except KeyError:
							try:
								fail_message = message.reply(f"""There was an error fetching your ranked info: `{ranked_json['status']['message']}`\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
								print(f"""{ranked_json['status']['status_code']} error fetching ranked info: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}: {ranked_json['status']['message']}""")
							except KeyError:
								fail_message = message.reply(f"""There was an unknown error fetching your ranked info. If this issue continues, please contact u/lukenamop.\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
								print(f'unknown error fetching summoner: u/{message.author.name} -- {riot_summoner_name} -- {riot_region}')
						except IndexError:
							# send the redditor a message
							fail_message = message.reply(f"""Your verified summoner account `{riot_summoner_name}` is currently `Unranked`. Your flair on r/{config.HOME_SUBREDDIT} has not been updated, please get ranked to update your flair!\n\nIf you'd like to try again, [please click here]({config.START_VERIF_MSG_LINK}).""")
							print(f'ranked flair not updated for u/{message.author.name}')

							# update the redditor in the database
							query = 'UPDATE flaired_redditors SET riot_verified = True, riot_verified_rank = %s, custom_flair = %s WHERE reddit_username = %s'
							q_args = ['Unranked', custom_flair, message.author.name]
							execute_sql(query, q_args)
							connect.db_conn.commit()

					if fail_message is None:
						# find the flair template ID for the summoner's ranked tier
						flair_template_id = config.RANKED_TIER_FLAIR_DICT[riot_verified_rank_tier]
						if riot_verified_rank_tier in ['Master', 'Grandmaster', 'Challenger']:
							riot_verified_rank = riot_verified_rank_tier

						# prepare the redditor's ranked flair
						flair_prefix = riot_verified_rank
						flair_suffix = ''
						if custom_flair is not None:
							flair_suffix = f' | {custom_flair}'

						# update the redditor's flair in the subreddit
						subreddit.flair.set(message.author.name, text=f':{riot_verified_rank_tier.lower()[:4]}: {riot_verified_rank}{flair_suffix}', flair_template_id=flair_template_id)

						# send the redditor a confirmation message
						message.reply(f"""Your verified summoner account `{riot_summoner_name}` is currently `{riot_verified_rank}`. Your flair on r/{config.HOME_SUBREDDIT} has been updated!\n\nIf you want to make any changes you can [click here]({config.START_VERIF_MSG_LINK}) to start over.""")

						# update the redditor in the database
						query = 'UPDATE flaired_redditors SET riot_verified = True, riot_verified_rank = %s, custom_flair = %s WHERE reddit_username = %s'
						q_args = [riot_verified_rank, custom_flair, message.author.name]
						execute_sql(query, q_args)
						connect.db_conn.commit()
						print(f'ranked flair updated for u/{message.author.name}: {riot_verified_rank}{flair_suffix}')

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
		inbox_reply_stream(mp_lock, reddit, request_headers, iteration)
	else:
		print(f'killing inbox reply stream, >{config.OVERFLOW} skipped messages')

def ranked_flair_updater(mp_lock, reddit, request_headers, iteration=1):
	print('ranked_flair_updater started')

	# connect to the database
	connect.db_connect('ranked flair update')

	subreddit = reddit.subreddit(config.HOME_SUBREDDIT)

	# check to see if the auto-updater flair decay lockout is active
	decay_lockout = False
	datetime_now = datetime.datetime.now()
	if datetime_now > config.AUTO_UPDATE_LOCKOUT_START_DATETIME and datetime_now < config.AUTO_UPDATE_LOCKOUT_END_DATETIME:
		decay_lockout = True
		print('auto-updater flair decay lockout is active')

	try:
		# fetch all flaired redditors from the database
		query = 'SELECT reddit_username, riot_region, riot_summoner_name, riot_summoner_id, riot_verified_rank, custom_flair FROM flaired_redditors WHERE riot_verified = True ORDER BY reddit_username ASC'
		execute_sql(query)
		results = connect.db_crsr.fetchall()
		redditors_to_update = len(results)
		# iterate through all flaired redditors
		for redditor in results:
			redditors_to_update -= 1
			fail_message = None
			reddit_username, riot_region, riot_summoner_name, riot_summoner_id, riot_verified_rank, custom_flair = redditor
			# request the summoner's ranked info from riot
			ranked_json = requests.get(f"""https://{riot_region}.api.riotgames.com/tft/league/v1/entries/by-summoner/{riot_summoner_id}""", headers=request_headers).json()
			try:
				new_riot_verified_rank_tier = ranked_json[0]['tier'].capitalize()
				new_riot_verified_rank_division = ranked_json[0]['rank']
				new_riot_verified_rank = f'{new_riot_verified_rank_tier} {new_riot_verified_rank_division}'
			except KeyError:
				try:
					print(f"""auto-updater {ranked_json['status']['status_code']} error fetching ranked info: u/{reddit_username} -- {riot_summoner_name} -- {riot_region}: {ranked_json['status']['message']}""")
					fail_message = ''
				except KeyError:
					print(f'auto-updater unknown error fetching summoner: u/{reddit_username} -- {riot_summoner_name} -- {riot_region}')
					fail_message = ''
			except IndexError:
				# print(f'auto-updater skipped u/{reddit_username}, Unranked')
				fail_message = ''
				# if not locked out of decay, update the redditor in the database
				if not decay_lockout:
					query = 'UPDATE flaired_redditors SET riot_verified_rank = %s, custom_flair = %s WHERE reddit_username = %s'
					q_args = ['Unranked', custom_flair, reddit_username]
					execute_sql(query, q_args)
					connect.db_conn.commit()

			if fail_message is None:
				update_flair = True
				# if locked out of decay, compare the redditor's old flair to the updated flair
				if decay_lockout:
					old_riot_verified_rank_tier = riot_verified_rank.split()[0]
					try:
						old_riot_verified_rank_division = riot_verified_rank.split()[1]
					except IndexError:
						old_riot_verified_rank_division = 'I'

					update_flair = False
					if config.RANKED_TIER_DICT[new_riot_verified_rank_tier] > config.RANKED_TIER_DICT[old_riot_verified_rank_tier]:
						update_flair = True
					elif config.RANKED_TIER_DICT[new_riot_verified_rank_tier] == config.RANKED_TIER_DICT[old_riot_verified_rank_tier]:
						if config.RANKED_DIV_DICT[new_riot_verified_rank_division] > config.RANKED_DIV_DICT[old_riot_verified_rank_division]:
							update_flair = True

				if not update_flair:
					# print(f'auto-updater skipped u/{reddit_username}, flair decay lockout')
					pass
				else:
					# find the flair template ID for the summoner's ranked tier
					flair_template_id = config.RANKED_TIER_FLAIR_DICT[new_riot_verified_rank_tier]
					if new_riot_verified_rank_tier in ['Master', 'Grandmaster', 'Challenger']:
						new_riot_verified_rank = new_riot_verified_rank_tier

					# prepare the redditor's ranked flair
					flair_prefix = new_riot_verified_rank
					flair_suffix = ''
					if custom_flair is not None:
						flair_suffix = f' | {custom_flair}'

					# find the redditor's existing flair
					current_sub_flair = reddit.subreddit(config.HOME_SUBREDDIT).flair(redditor=reddit_username, limit=1)
					current_redditor_flair = None
					for flair in current_sub_flair:
						current_redditor_flair = flair['flair_text']

					# if it has changed, update the redditor's flair in the subreddit
					if current_redditor_flair != f':{new_riot_verified_rank_tier.lower()[:4]}: {new_riot_verified_rank}{flair_suffix}':
						subreddit.flair.set(reddit_username, text=f':{new_riot_verified_rank_tier.lower()[:4]}: {new_riot_verified_rank}{flair_suffix}', flair_template_id=flair_template_id)
						print(f'auto-updater triggered for u/{reddit_username}: {new_riot_verified_rank}{flair_suffix}')
					else:
						# print(f'auto-updater skipped u/{reddit_username}, no change in flair')
						pass

					# update the redditor in the database
					query = 'UPDATE flaired_redditors SET riot_verified_rank = %s, custom_flair = %s WHERE reddit_username = %s'
					q_args = [riot_verified_rank, custom_flair, reddit_username]
					execute_sql(query, q_args)
					connect.db_conn.commit()

			# sleep for a few seconds before updating the next redditor
			time.sleep(config.AUTO_UPDATE_SLEEP_TIME)

	except prawcore.exceptions.ServerError as error:
		print(f'skipping auto-update due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.RequestException as error:
		print(f'skipping auto-update due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.ResponseException as error:
		print(f'skipping auto-update due to PRAW error: {type(error)}: {error}')
	except Exception as error:
		print(f'skipping auto-update due to unknown error: {type(error)}: {error}')

	# if the loop completes instead of erroring out, don't add an iteration towards the overflow limit
	if redditors_to_update > 0:
		iteration += 1

	if iteration <= config.OVERFLOW:
		ranked_flair_updater(mp_lock, reddit, request_headers, iteration)
	else:
		print(f'killing ranked flair updater, >{config.OVERFLOW} skipped auto-update')


##### OTHER REDDIT FUNCTIONS #####

def maintain_guide_index(reddit):
	print('index guides started')

	# connect to the database
	connect.db_connect('maintain guide index')

	# pull all guide submission IDs from the database
	query = 'SELECT db_id, reddit_id FROM guide_submissions'
	execute_sql(query)
	results = connect.db_crsr.fetchall()
	print(f're-indexing {len(results)} guides...')
	# iterate through guide submissions
	for guide_submission in results:
		# fetch the submission object from reddit
		submission = reddit.submission(id=guide_submission[1])

		# remove any submissions that have been deleted or removed
		remove_from_db = False
		if submission is None:
			remove_from_db = True
		else:
			if submission.author is None or submission.selftext in [None, '', '[deleted]', '[removed]']:
				remove_from_db = True
		if remove_from_db:
			query = 'DELETE FROM guide_submissions WHERE db_id = %s'
			q_args = [guide_submission[0]]
			execute_sql(query, q_args)
	connect.db_conn.commit()
	print('done re-indexing')

	# pull all guide submission selftexts from the database
	query = 'SELECT db_id, full_selftext FROM guide_submissions'
	execute_sql(query)
	results = connect.db_crsr.fetchall()
	print(f'vectorizing {len(results)} guides...')
	# iterate through guide submissions
	guide_submission_texts = []
	guide_submission_db_ids = []
	for guide_submission in results:
		guide_submission_texts.append(guide_submission[1])
		guide_submission_db_ids.append(guide_submission[0])

	# create a TFIDF vectorizer with all guide submission texts
	vectorizer = TfidfVectorizer(stop_words='english')
	dense_vector_list = vectorizer.fit_transform(guide_submission_texts).todense().tolist()
	feature_names = vectorizer.get_feature_names()

	# iterate through all guide submissions and find the most relevant vectors
	g_i = 0
	for guide_submission_db_id in guide_submission_db_ids:
		v_i = 0
		vector_1 = {'num': 0, 'index': 0}
		vector_2 = {'num': 0, 'index': 0}
		vector_3 = {'num': 0, 'index': 0}
		vector_4 = {'num': 0, 'index': 0}
		vector_5 = {'num': 0, 'index': 0}
		for vector_num in dense_vector_list[g_i]:
			if vector_num > vector_1['num']:
				vector_1 = {'num': vector_num, 'index': v_i}
			elif vector_num > vector_2['num']:
				vector_2 = {'num': vector_num, 'index': v_i}
			elif vector_num > vector_3['num']:
				vector_3 = {'num': vector_num, 'index': v_i}
			elif vector_num > vector_4['num']:
				vector_4 = {'num': vector_num, 'index': v_i}
			elif vector_num > vector_5['num']:
				vector_5 = {'num': vector_num, 'index': v_i}
			v_i += 1
		g_i += 1

		# find keywords via relevant vectors
		keyword_1 = feature_names[vector_1['index']] if vector_1['num'] != 0 else None
		keyword_2 = feature_names[vector_2['index']] if vector_2['num'] != 0 else None
		keyword_3 = feature_names[vector_3['index']] if vector_3['num'] != 0 else None
		keyword_4 = feature_names[vector_4['index']] if vector_4['num'] != 0 else None
		keyword_5 = feature_names[vector_5['index']] if vector_5['num'] != 0 else None

		# update the database with the most relevant keywords
		query = 'UPDATE guide_submissions SET keyword_1 = %s, keyword_2 = %s, keyword_3 = %s, keyword_4 = %s, keyword_5 = %s WHERE db_id = %s'
		q_args = [keyword_1, keyword_2, keyword_3, keyword_4, keyword_5, guide_submission_db_id]
		execute_sql(query, q_args)
	connect.db_conn.commit()
	print('done vectorizing')
	return

def submission_reply_stream(mp_lock, reddit, iteration=1):
	print('submission reply stream started')

	# connect to the database
	connect.db_connect('submission reply stream')

	subreddit = reddit.subreddit(config.HOME_SUBREDDIT)

	try:
		# iterate through all new submissions indefinitely
		for submission in subreddit.stream.submissions(skip_existing=True):
			respond_to_submission = False

			# only comment on submissions with specific flair
			if hasattr(submission, 'link_flair_text'):
				if submission.link_flair_text == 'GUIDE':
					respond_to_submission = True

			# make sure the submission is actually new
			if submission.created_utc < (time.time() - 60 * 30):
				respond_to_submission = False

			# only respond to each submission once
			submission.comment_sort = 'top'
			submission.comments.replace_more(limit=0)
			comments_list = submission.comments.list()
			if len(comments_list) > 0:
				top_comment = comments_list[0]
				if top_comment.author.name == 'CompetitiveTFTBot':
					respond_to_submission = False

			if respond_to_submission:
				# # submit a comment reply
				# reply = submission.reply(f"""Thank you for your guide submission! We've added it to our guide submission index. You can search for other guides by replying to this comment with `{config.R_CMD_PREFIX}guide <timeframe (days)> <keyword>`\n\n^^What&nbsp;do&nbsp;you&nbsp;think&nbsp;of&nbsp;this&nbsp;new&nbsp;feature? ^^[Let&nbsp;the&nbsp;mod&nbsp;team&nbsp;know!](https://reddit.com/message/compose?to=/r/CompetitiveTFT&subject=My%20thoughts%20on%20the%20new%20sub%20bot)""")
				# # distinguish and sticky the comment reply
				# reply.mod.distinguish(how='yes', sticky=True)
				# print(f"""guide submission from u/{submission.author.name}""")

				# index guide submission in database
				if submission.selftext not in [None, '']:
					query = 'SELECT db_id FROM guide_submissions WHERE reddit_id = %s'
					q_args = [submission.id]
					execute_sql(query, q_args)
					if connect.db_crsr.fetchone() is None:
						query = 'INSERT INTO guide_submissions (reddit_id, title, author, full_selftext, created_utc) VALUES (%s, %s, %s, %s, %s)'
						q_args = [submission.id, submission.title, submission.author.name, submission.selftext, submission.created_utc]
						execute_sql(query, q_args)
					print('added new guide submission to the index')
				maintain_guide_index(reddit)

	except prawcore.exceptions.ServerError as error:
		print(f'skipping submission reply due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.RequestException as error:
		print(f'skipping submission reply due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.ResponseException as error:
		print(f'skipping submission reply due to PRAW error: {type(error)}: {error}')
	except Exception as error:
		print(f'skipping submission reply due to unknown error: {type(error)}: {error}')

	iteration += 1
	if iteration <= config.OVERFLOW:
		submission_reply_stream(mp_lock, reddit, iteration)
	else:
		print(f'killing submission reply stream, >{config.OVERFLOW} skipped comments')

def comment_reply_stream(mp_lock, reddit, iteration=1):
	print('comment reply stream started')

	# connect to the database
	connect.db_connect('comment reply stream')

	subreddit = reddit.subreddit(config.HOME_SUBREDDIT)

	try:
		# iterate through all comment replies indefinitely
		reply_function = reddit.inbox.comment_replies
		for comment in praw.models.util.stream_generator(reply_function, skip_existing=True):
			# mark all new comments as read
			reddit.inbox.mark_read([comment])

			if comment.body.startswith(config.R_CMD_PREFIX):
				# parse commands from comment replies
				comment_body = comment.body.lstrip(config.R_CMD_PREFIX)
				command = comment_body.split()[0].lower()
				args = comment_body.split()[1:]
				# guide search command
				if command in ['guide', 'search']:
					run_search = False
					try:
						# pull the search timeframe and keywords from the arg list
						search_days = int(args[0].rstrip('d'))
						search_timestamp = int(time.time()) - (60 * 60 * 24 * search_days)
						search_keyword = args[1]
						run_search = True
					except ValueError:
						response = f"""There was an error executing this command. Be sure to use this format: `{config.R_CMD_PREFIX}guide <timeframe (days)> <keyword>`, for example `{config.R_CMD_PREFIX}guide 30 viktor`"""
						response_print = f"""attempted guide search from u/{comment.author.name}: {' '.join(args)}"""

					if run_search:
						# search the database index
						query = 'SELECT db_id, keyword_1, keyword_2, keyword_3, keyword_4, keyword_5, title, author, reddit_id FROM guide_submissions WHERE created_utc > %s ORDER BY db_id DESC'
						q_args = [search_timestamp]
						execute_sql(query, q_args)
						results = connect.db_crsr.fetchall()
						if results not in [None, []]:
							# iterate through guide submissions to find relevant guides
							search_results = []
							keyword_num = 1
							while keyword_num <= 5:
								for guide_submission in results:
									# if the keywords match, add a result to the list
									if guide_submission[keyword_num] == search_keyword:
										search_results.append({'title': guide_submission[6], 'author': guide_submission[7], 'reddit_id': guide_submission[8]})
										# stop when the limit of relevant guides has been found
										if len(search_results) >= config.GUIDE_LIMIT:
											break
								keyword_num += 1

						# build a comment response
						if len(search_results) == 0:
							# if no search results were found, inform the user
							response = f"""Unfortunately no guides were found from the past {search_days} days when searching for `{search_keyword}`. Please try again."""
						else:
							# list all search results
							response = f"""Top {len(search_results)} `{search_keyword}` guides from the past {search_days} days:\n"""
							for search_result in search_results:
								response += f"""\n- [{search_result['title']}](https://redd.it/{search_result['reddit_id']}/) from u/{search_result['author']}"""
						response_print = f"""guide search from u/{comment.author.name}, {len(search_results)} results: {' '.join(args)}"""

					# reply to the command
					reply = comment.reply(response)
					# distinguish the comment reply
					reply.mod.distinguish(how='yes')
					print(response_print)

	except prawcore.exceptions.ServerError as error:
		print(f'skipping comment reply due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.RequestException as error:
		print(f'skipping comment reply due to PRAW error: {type(error)}: {error}')
	except prawcore.exceptions.ResponseException as error:
		print(f'skipping comment reply due to PRAW error: {type(error)}: {error}')
	# except Exception as error:
	# 	print(f'skipping comment reply due to unknown error: {type(error)}: {error}')

	iteration += 1
	if iteration <= config.OVERFLOW:
		comment_reply_stream(mp_lock, reddit, iteration)
	else:
		print(f'killing comment reply stream, >{config.OVERFLOW} skipped comments')

def ranked_flair_index(mp_lock, reddit):
	print('ranked flair index started')

	# connect to the database
	connect.db_connect('ranked flair index')

	subreddit = reddit.subreddit(config.HOME_SUBREDDIT)

	try:
		# iterate through all subreddit flairs
		rioters = []
		for flair in subreddit.flair(limit=None):
			if flair['flair_text'] is not None:
				if 'challenger' in flair['flair_text'].lower():
					print(flair)
					rioters.append(flair['user'].name)
		print('done iterating challenger flair!')
		print(rioters)

	except prawcore.exceptions.Forbidden as error:
		print(f'stopping ranked flair index due to PRAW error: {type(error)}: {error}')

##### CODE TO RUN AT LAUNCH #####

def main():
	# initialize a reddit object
	reddit = initialize_reddit()

	# initialize request headers
	request_headers = prepare_request_headers()

	# create a multiprocessing lock
	mp_lock = Lock()

	# # start the inbox reply stream
	# inbox_reply_stream_process = Process(target=inbox_reply_stream, args=(mp_lock, reddit, request_headers,))
	# inbox_reply_stream_process.start()

	# # start the comment reply stream
	# comment_reply_stream_process = Process(target=comment_reply_stream, args=(mp_lock, reddit,))
	# comment_reply_stream_process.start()

	# start the submission reply stream
	submission_reply_stream_process = Process(target=submission_reply_stream, args=(mp_lock, reddit,))
	submission_reply_stream_process.start()

	# # start the ranked flair updater
	# ranked_flair_updater_process = Process(target=ranked_flair_updater, args=(mp_lock, reddit, request_headers,))
	# ranked_flair_updater_process.start()

	# start the ranked flair index
	ranked_flair_index_process = Process(target=ranked_flair_index, args=(mp_lock, reddit,))
	ranked_flair_index_process.start()

	# start the function to maintain guide index
	maintain_guide_index(reddit)

if __name__ == '__main__':
	main()