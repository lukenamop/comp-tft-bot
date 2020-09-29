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
	unverified_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True""")
	verified_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'br1'""")
	br1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'eun1'""")
	eun1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'euw1'""")
	euw1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'jp1'""")
	jp1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'kr'""")
	kr_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'la1'""")
	la1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'la2'""")
	la2_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'na1'""")
	na1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'oc1'""")
	oc1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'ru'""")
	ru_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM flaired_redditors WHERE riot_verified = True AND riot_region = 'tr1'""")
	tr1_redditors = int(db_crsr.fetchone()[0])

	db_crsr.execute("""SELECT COUNT(*) FROM guide_submissions""")
	guide_submissions = int(db_crsr.fetchone()[0])

	# print connection properties
	print(f'postgres connection info: {db_conn.get_dsn_parameters()}'
		+ f'\nunverified redditors: {unverified_redditors}'
		+ f'\nverified redditors: {verified_redditors}'
		+ f'\nbr1: {br1_redditors}'
		+ f'\neun1: {eun1_redditors}'
		+ f'\neuw1: {euw1_redditors}'
		+ f'\njp1: {jp1_redditors}'
		+ f'\nkr: {kr_redditors}'
		+ f'\nla1: {la1_redditors}'
		+ f'\nla2: {la2_redditors}'
		+ f'\nna1: {na1_redditors}'
		+ f'\noc1: {oc1_redditors}'
		+ f'\nru: {ru_redditors}'
		+ f'\ntr1: {tr1_redditors}'
		+ f'\nguide submissions: {guide_submissions}')

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

# TABLE guide_submissions
# db_id SERIAL PRIMARY KEY
# reddit_id VARCHAR(7) NOT NULL
# title VARCHAR(300) NOT NULL
# author VARCHAR(30) NOT NULL
# full_selftext VARCHAR(40000) NOT NULL
# created_utc NUMERIC(10) NOT NULL
# keyword_1 VARCHAR(50) DEFAULT NULL
# keyword_2 VARCHAR(50) DEFAULT NULL
# keyword_3 VARCHAR(50) DEFAULT NULL
# keyword_4 VARCHAR(50) DEFAULT NULL
# keyword_5 VARCHAR(50) DEFAULT NULL