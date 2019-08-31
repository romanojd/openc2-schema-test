import os
import json
import pprint
from validator import Validator

show_error_message = True

if __name__ == '__main__':
	# specify schema
	# schema_filename = 'oc2ls-v1.0.json'
	schema_filename = 'command.json'
	# schema_filename = 'response.json'

	# specify message files
	source_files = [
	  '..\\messages\\fail\\bberliner\\commands\\empty_object.json', 
	  '..\\messages\\fail\\bberliner\\commands\\empty_array.json'
	]	

	# instantiate validator
	v = Validator(schema_filename)

	# read and process each message
	for source_filepath in source_files:
		error_message = None

		# load the message
		with open(source_filepath, 'r') as json_message_file:
			try:
				message = json.load(json_message_file)
			except json.decoder.JSONDecodeError:
				message = None
				error_message = 'JSON Decode Error'

		# print the message
		print('Message:')
		pprint.pprint(message)

		# validate the source file
		if message and v:
			error_message = v.validate(message)

		# report results
		if error_message:
			print(f'[FAIL] {source_filepath}')
			if show_error_message:
				print(f'{error_message}\n')

		else:
			print(f'[PASS] {source_filepath}')
