import os
import json
import pprint
from validator import Validator


if __name__ == '__main__':
	# schema_filename = 'oc2ls-v1.0.json'
	schema_filename = 'oc2slpf-v1.0.json'

	# instantiate validator
	v = Validator(schema_filename)

	# read the source file
	source_path = '..\\messages'
	source_files = ['oc2slpf-example_a2.json', 'oc2slpf-example_a12.json']	
	# source_files = ['command-pass.json', 'command-fail.json']

	for source_filename in source_files:
		with open(os.path.join(source_path, source_filename), 'r') as json_message_file:
			message = json.load(json_message_file)

		# print the message
		print('Message:')
		pprint.pprint(message)

		# validate the source file
		error_message = v.validate(message)
		if not error_message:
			print(f'Schema "{schema_filename}": PASS\n')
		else:
			print(f'Schema "{schema_filename}": FAIL\n{error_message}\n')
