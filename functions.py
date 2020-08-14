#!/usr/bin/env python3

# import libraries
import math

# function to translate seconds into hours/minutes/seconds
def time_string(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	if d > 0:
		if h > 0:
			return f'{int(d)}d {int(h)}h'
		else:
			return f'{int(d)}d'
	elif h > 0:
		if m > 0:
			return f'{int(h)}h {int(m)}m'
		else:
			return f'{int(h)}h'
	elif m > 0:
		if s > 0:
			return f'{int(m)}m {int(s)}s'
		else:
			return f'{int(m)}m'
	elif s > 0:
		return f'{int(s)}s'
	else:
		return 'invalid'

# function to translate milliseconds into seconds/milliseconds
def ms_string(milliseconds):
	if milliseconds < 500:
		return f'{round(milliseconds, 2)}ms'
	elif milliseconds >= 500:
		return f'{round(milliseconds / 1000, 3)}s'
	return 'invalid'