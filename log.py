import time
loglevel = 3 #0-3 Error-Debug


def log(message, level):
	if level <= loglevel:
		print(f'[{time.time()}]', message)

def debug(message):
	log(message, 3)

def info(message):
	log(message, 2)

def warning(message):
	log(message, 1)

def error(message):
	log(message, 0)