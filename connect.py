#!/usr/bin/env python3

# import libraries
import os
import psycopg2

# import additional files
import config

def db_connect(connection_name):
	# establish database connection
	global db_conn
	db_conn = psycopg2.connect(config.DB_URL)
	global db_crsr
	db_crsr = db_conn.cursor()
	print(f'database connected: {connection_name}')

	return True

def db_stats():
	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = False""")
	unverified_redditors = db_crsr.fetchone()[0]

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True""")
	verified_redditors = db_crsr.fetchone()[0]

	# print connection properties
	print(f'postgres connection info: {db_conn.get_dsn_parameters()}'
		+ f'\nunverified redditors: {unverified_redditors}'
		+ f'\nverified redditors: {verified_redditors}')

# TABLE flaired_redditors
# db_id SERIAL PRIMARY KEY
# reddit_username VARCHAR(30) NOT NULL
# riot_region VARCHAR(6) NOT NULL
# riot_summoner_name VARCHAR(30) NOT NULL
# riot_summoner_id VARCHAR(100) DEFAULT NULL
# riot_verification_key VARCHAR(6) NOT NULL
# riot_verified BOOLEAN DEFAULT False
# riot_verified_rank VARCHAR(40) DEFAULT NULL
# custom_flair VARCHAR(60) DEFAULT NULL