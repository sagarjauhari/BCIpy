import csv
import os

def make_passage_list (file, col):
	passage_list = []
	with open(file, 'rb') as inFile:
		fi = csv.reader(inFile)
		for row in fi:
			passage_list.append(row[col])
	passage_list.sort()
	return passage_list

def assign_id (passage_list):
	passage_id = {}
	index = 0;
	for item in passage_list:
		if item in passage_id:
			pass
		passage_id[item] = index
		index = index + 1
	return passage_id


def word_data(file, col1, col2):
	word_info = {}
	with open(file, 'rb') as reader:
		fi = csv.reader(reader)
		for row in fi:
			key = row[col1]
			if key in word_info:
				pass
			word_info[key] = row[col2]
	return word_info

def string_data(word_info, text):
	string_info = []
	#print text
	for word in text.split():
		if word in word_info:
			string_info.append(word_info[word])
	#print text, string_info
	return string_info

def passage_data(passage_id, word_info):
	passage_info = {}
	for k, v in passage_id.iteritems():
		if v in passage_info:
			pass
		passage_info[v] = string_data(word_info, k)
	return passage_info

def get_dict(passage_id, file, col1, col2):
	word_info = word_data(file, col1, col2)
	passage_info = passage_data(passage_id, word_info)
	return passage_info



passage_file = r"C:\Users\Vinaya\Desktop\test.csv"
passage_col =  4
passage_dif = 9
passage_list = make_passage_list(passage_file, passage_col)
passage_id = assign_id(passage_list)

passage_diff = get_dict(passage_id, passage_file, passage_col, passage_dif)

aoa_file = r"C:\Users\Vinaya\Desktop\aoa-data.csv"
aoa_word_col = 0
aoa_col = 10
aoa_dict = get_dict(passage_id, aoa_file, aoa_word_col, aoa_col)

frequency_file = r"C:\Users\Vinaya\Desktop\frequency.csv"
frequency_word_col = 1
frequency_col =0
frequency_dict = get_dict(passage_id, frequency_file, frequency_word_col, frequency_col)

output_file = r"C:\Users\Vinaya\Desktop\classifiers.csv"
with open (output_file, 'w+') as output:
	out = csv.writer(output)
	out.writerow(["id", "passage", "difficulty", "aoa", "frequency"])
	for k, v in passage_id.iteritems():
		out.writerow([v, k, passage_diff[v], aoa_dict[v], frequency_dict[v]])

#print "done"

#for k, v in passage_id.iteritems():
		#print v, k, passage_difficulty[v], aoa_dict[v], frequency_dict[v]


