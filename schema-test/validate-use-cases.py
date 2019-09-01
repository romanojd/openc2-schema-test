import os
import re
import json
from validator import Validator

show_error_message = True

def get_file_list(rootpath):
	# initialize list of files
	file_list = []

	# walk through the root path
	for dirpath, dirnames, filenames in os.walk(rootpath):
		# remove hidden folders
		for dirname in dirnames:
			if dirname.startswith('.'):
				dirnames.remove(dirname)

		# build file list with markdown files
		for filename in filenames:
			if filename.endswith('.md'):
				file_list.append(os.path.join(dirpath, filename))

	# return list of files
	return file_list

if __name__ == '__main__':
	# specify schema
	schema_filename = 'oc2ls-v1.0.json'
	# schema_filename = 'command.json'
	# schema_filename = 'response.json'

	# specify message files
	# this is the relative path to a local clone of the openc2-usecases repository
	rootpath = '..\\..\\openc2-usecases'
	source_file_list = get_file_list(rootpath)

	# instantiate validator
	v = Validator(schema_filename)

	# read and process each message
	total_code_blocks = 0
	for source_filepath in source_file_list:
		error_message = None

		# load the message
		with open(source_filepath, 'r') as source_file:
			try:
				source = source_file.read()
			except UnicodeDecodeError as err:
				print(f'[FAIL] {source_filepath}: SOURCE FILE')
				if show_error_message:
					print(f"'{err.encoding}' codec can't decode byte {err.object[err.start: err.end]} in position {err.start}: {err.reason}\n")
			else:
				# find code blocks
				regex = re.compile(r'```([^`]+)```')
				code_list = regex.findall(source)

				# process each code block
				code_num = 0
				for code_num, code_block in enumerate(code_list, 1):
					# reinitalize variables
					error_message = None

					m = re.search(r'\{.*\}', code_block, re.MULTILINE | re.DOTALL)
					code = m.group(0) if m else None

					try:
						message = json.loads(code) if code else None
					except json.decoder.JSONDecodeError as err:
						message = None
						print(f'[FAIL] {source_filepath}: CODE BLOCK #{code_num}')
						if show_error_message:
							print(f'Invalid JSON, {err.msg}: line {err.lineno} column {err.colno} (char {err.pos})\n')
						# print(message)
					else:				
						# validate the source file
						if message and v:
							error_message = v.validate(message)

					# report results
					if error_message:
						print(f'[FAIL] {source_filepath}: CODE BLOCK #{code_num}')
						if show_error_message:
							print(f'{error_message}\n')

					else:
						print(f'[PASS] {source_filepath}: CODE BLOCK #{code_num}')

				# report number of code blocks
				total_code_blocks += code_num

	print(f'Total code blocks: {total_code_blocks}')





