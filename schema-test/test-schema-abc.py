import os
import json
import pprint
from validator import Validator


if __name__ == '__main__':
	# specify schema
	# schema_filename = 'schema-a.json'
	# schema_filename = 'schema-b.json'
	schema_filename = 'schema-c1.json'

	# specify message files
	source_files = ['test-pass.json', 'test-fail.json']	

	# instantiate validator
	v = Validator(schema_filename)

	# read and process each message
	source_path = '..\\messages'
	for source_filename in source_files:
		with open(os.path.join(source_path, source_filename), 'r') as json_message_file:
			message = json.load(json_message_file)

		# print the message
		print('Message:')
		pprint.pprint(message)

		# validate the source message
		error_message = v.validate(message)
		if not error_message:
			print(f'Schema "{schema_filename}": PASS\n')
		else:
			print(f'Schema "{schema_filename}": FAIL\n{error_message}\n')
