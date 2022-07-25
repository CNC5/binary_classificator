import time
loglevel = 0 #0-3 Error-Debug


def log(message, level):
	if level <= loglevel:
		t = time.time()
		print(f'[{t:<20}]', message)

def debug(message):
	log('(DBG) '+message, 3)

def info(message):
	log('(INF) '+message, 2)

def warning(message):
	log('(WRN) '+message, 1)

def error(message):
	log('(ERR) '+message, 0)