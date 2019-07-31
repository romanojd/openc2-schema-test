import os
import json
import jsonschema

class Validator:
	def __init__(self, schema_filename):
		self.schema = None
		self.schema_filename = schema_filename
		self.schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schemas'))
		if schema_filename:
			self.load_schema()

	def load_schema(self):
		self.schema_filepath = os.path.join(self.schema_path, self.schema_filename)
		with open(self.schema_filepath, 'r') as json_schema_file:
			self.schema = json.load(json_schema_file)

		# create validator
		resolver = jsonschema.RefResolver(
			base_uri='file:///{}/'.format(self.schema_path),
			referrer=self.schema
		)
		self.validator = jsonschema.Draft7Validator(self.schema, resolver=resolver)

	def validate(self, message):
		error_list = []
		error_message = None

		try:
			self.validator.validate(instance=message)

		except jsonschema.exceptions.ValidationError:
			errors = sorted(self.validator.iter_errors(instance=message), key=lambda e: e.path)
			for error in errors:
				if error.context:
					for suberror in sorted(error.context, key=lambda e: e.schema_path):
						error_list.append('{}, {}'.format(list(suberror.schema_path), suberror.message))
				else:
					error_list.append('{}, {}'.format(list(error.schema_path), error.message))

			error_message = '\n'.join(error_list)

		except jsonschema.exceptions.SchemaError:
			error_message = 'SchemaError'

		except jsonschema.exceptions.RefResolutionError:
			error_message = 'HTTP Error 404: Not Found'

		return error_message
