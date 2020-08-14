#!/usr/bin/env python3

# import libraries
import psycopg2
import os

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
	# print connection properties
	print(f'postgres connection info: {db_conn.get_dsn_parameters()}')