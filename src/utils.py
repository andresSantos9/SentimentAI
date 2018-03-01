# Created by Sinclert Perez (Sinclert@hotmail.com)


import json
import os
import pickle
import random
import re


project_paths = {
	'dataset': ['resources', 'datasets'],
	'model': ['models'],
	'profile_p': ['profiles', 'predicting'],
	'profile_t': ['profiles', 'training'],
	'stopwords': ['resources', 'stopwords']
}


default_filters = [
	{
		'pattern': 'http\S+',
		'replace': '',
		'prob': 100
	},
	{
		'pattern': '(^|\s)@\w+',
		'replace': ' -USER-',
		'prob': 100
	},
	{
		'pattern': '#',
		'replace': '',
		'prob': 100
	},
	{
		'pattern': '&\w+;',
		'replace': '',
		'prob': 100
	},
	{
		'pattern':
			'[\U00002600-\U000027B0'
			'\U0001F300-\U0001F64F'
			'\U0001F680-\U0001F6FF'
			'\U0001F910-\U0001F919]+',
		'replace': '',
		'prob': 100
	},
	{
		'pattern': '\s+',
		'replace': ' ',
		'prob': 100
	},
]




def append_text(file_name, min_length = 0):

	""" Coroutine that appends the received text at the end of a file

	Arguments:
	----------
		file_name:
			type: string
			info: appendable file name

		min_length:
			type: int (optional)
			info: minimum length to append a text to the file

	Yield:
	----------
		text:
			type: string
			info: text to append in the file
	"""

	file_path = compute_path(file_name, 'dataset')

	file_dir = file_path.replace(file_name, '')
	os.makedirs(file_dir, exist_ok = True)

	try:
		file = open(file_path, 'a', encoding = 'utf-8')

		try:
			while True:
				text = yield
				if len(text) >= min_length: file.write(text + '\n')

		finally:
			file.close()

	except IOError:
		exit('The file ' + file_path + ' cannot be opened')




def build_filters(words, words_prob):

	""" Builds a list of probabilistic filters

		Arguments:
		----------
			words:
				type: list
				info: words to subtract given a probability

			words_prob:
				type: int
				info: probability in which the words are subtracted

	Returns:
	----------
		filters:
			type: list
			info: contains the probabilistic filters
	"""

	prob_filters = []

	for word in words:
		prob_filters.append({
			'pattern': '(^|\s)' + word + '(\W|$)',
			'replace': ' ',
			'prob': words_prob
		})

	return prob_filters




def check_keys(keys, data_struct, error):

	""" Checks if all the keys are present in the data structure

	Arguments:
	----------
		keys:
			type: list
			info: elements which must be in the data structure

		data_struct:
			type: set / dictionary
			info: data structure to check existence

		error:
			type: string
			info: error message to print
	"""

	if not all(k in data_struct for k in keys):
		exit(error)




def clean_text(text, filters = default_filters):

	""" Cleans the text applying regex substitution specified by the filters

	Arguments:
	----------
		text:
			type: string
			info: lowercase text where the regex substitutions will be applied

		filters:
			type: list (optional)
			info: list containing dictionaries with the following keys:
				- pattern (regex)
				- replace (string)
				- prob (int)

	Returns:
	----------
		text:
			type: string
			info: lowercase cleaned text
	"""

	try:
		for f in filters:

			# In case the replacement must be performed
			if (f['prob'] == 100) or ((random.random() * 100) < f['prob']):
				text = re.sub(f['pattern'], f['replace'], text)

		return text.strip()

	except KeyError:
		exit('The filters do not have the correct format')




def compute_path(file_name, file_type):

	""" Builds the absolute path to the desired file given its file type

	Arguments:
	----------
		file_name:
			type: string
			info: desired file name

		file_type:
			type: string
			info: {'dataset', 'model', 'profile_p', 'profile_t', 'stopwords'}

	Returns:
	----------
		path:
			type: string
			info: absolute path to the desired file
	"""

	try:
		project_root = str(os.path.dirname(os.getcwd()))

		path = [project_root]
		path = path + project_paths[file_type]
		path = path + [file_name]

		return os.path.join(*path)

	except KeyError:
		exit('The file type "' + file_type + '" is not defined')




def load_object(file_name, file_type):

	""" Loads an object from the specified file

	Arguments:
		----------
		file_name:
			type: string
			info: saved object file name

		file_type:
			type: string
			info: used to determine the proper path

	Returns:
	----------
		obj:
			type: dict
			info: dictionary containing the object information
	"""

	file_path = compute_path(file_name, file_type)

	try:
		file = open(file_path, 'rb')
		obj = pickle.load(file)
		file.close()

		return obj

	except IOError:
		exit('The object could not be loaded from ' + file_path)




def save_object(obj, file_name, file_type):

	""" Saves an object in the specified path

	Arguments:
	----------
		obj:
			type: object
			info: instance of a class that will be serialized

		file_name:
			type: string
			info: saved object file name

		file_type:
			type: string
			info: used to determine the proper path
	"""

	file_path = compute_path(file_name, file_type)

	file_dir = file_path.replace(file_name, '')
	os.makedirs(file_dir, exist_ok = True)

	try:
		file = open(file_path, 'wb')
		pickle.dump(obj.__dict__, file)
		file.close()

	except IOError:
		exit('The object could not be saved in ' + file_path)




def read_json(file_name, file_type):

	""" Reads a JSON file and returns it as a dictionary

	Arguments:
	----------
		file_name:
			type: string
			info: readable file name

		file_type:
			type: string
			info: used to determine the proper path

	Returns:
	----------
		json_dict:
			type: dict
			info: dictionary containing the parsed JSON file
	"""

	file_path = compute_path(file_name, file_type)

	try:
		file = open(file_path, 'r', encoding = 'utf-8')
		json_dict = json.load(file)
		file.close()

		return json_dict

	except IOError:
		exit('The file ' + file_name + ' cannot be opened')




def read_lines(file_name, file_type):

	""" Reads the lines of a file and returns them inside a list

	Arguments:
	----------
		file_name:
			type: string
			info: readable file name

		file_type:
			type: string
			info: used to determine the proper path

	Returns:
	----------
		lines:
			type: list
			info: file lines (separated by the new line character)
	"""

	file_path = compute_path(file_name, file_type)

	try:
		file = open(file_path, 'r', encoding = 'utf-8')
		lines = file.read().splitlines()
		file.close()

		return lines

	except IOError:
		exit('The file ' + file_name + ' cannot be opened')
