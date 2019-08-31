import os
import json
import pprint
from validator import Validator

show_error_message = True

if __name__ == '__main__':
	# get the list of files
	source_path = '..\\messages'
	source_files = []
	for dirpath, dirname_list, filename_list in os.walk(source_path):
		source_files.extend([os.path.join(dirpath, filename) for filename in filename_list])
		# print(f'dirpath: {dirpath}\ndirnames: {dirname_list}\nfilenames: {filename_list}\n')

	# process each file
	for source_filepath in source_files:
		error_message = None

		# load the message
		with open(source_filepath, 'r') as json_message_file:
			try:
				message = json.load(json_message_file)
			except json.decoder.JSONDecodeError:
				message = None
				error_message = 'JSON Decode Error'

		# set the validator
		if source_filepath.find('commands') > -1:
			v = Validator('command.json')
		elif source_filepath.find('responses') > -1:
			v = Validator('response.json')
		else:
			v = None

		# validate the source file
		if message and v:
			error_message = v.validate(message)

		# report invalid/pass
		if error_message:
			if source_filepath.startswith('..\\messages\\pass'):
				print(f'[FAIL] {source_filepath}')
				if show_error_message:
					print(f'{error_message}\n')

		# report valid/fail
		else:
			if source_filepath.startswith('..\\messages\\fail'):
				print(f'[PASS] {source_filepath}')
