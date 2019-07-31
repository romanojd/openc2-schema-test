import os
import json
import pprint
from validator import Validator


if __name__ == '__main__':
	# specify schema
	# schema_filename = 'oc2ls-v1.0.json'
	schema_filename = 'profile-base.json'
	# schema_filename = 'profile-restrict-actions.json'
	# schema_filename = 'profile-restrict-targets.json'
	# schema_filename = 'profile-extend-targets.json'
	# schema_filename = 'profile-define-actuator.json'
	# schema_filename = 'profile-extend-args.json'
	# schema_filename = 'profile-restrict-pairs-dependency.json'
	# schema_filename = 'profile-restrict-pairs-conditional.json'


	# specify message files
	source_files = ['command-pass.json', 'command-fail.json']	

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
