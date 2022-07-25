import numpy as np
import os
import subprocess
from . import log


def get_creds():
	if not(os.path.isfile('.env')):
		print('\nLogin information file not found, creating one for you.')
		login = input('Enter gmail box login(will be saved for further use)(example: example@gmail.com): ')
		atoken = input('Enter access token: ')
		spec_mail = input('Specify email to accept samples from(necessary): ')
		with open('.env','w') as env_file:
			env_file.write(login+'\n'+spec_mail+'\n'+atoken)
	elif os.path.isfile('.env'):
		with open('.env','r') as env_file:
			creds = env_file.read().split('\n')
			if '' in creds:
				creds.remove('')
			login, spec_mail, atoken = creds
	return [login, atoken, spec_mail]

if __name__ == '__main__':
	print(get_creds())
