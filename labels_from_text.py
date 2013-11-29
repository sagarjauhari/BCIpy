import csv
import os
import sys

def make_passage_list (file, col, delimiter="\t"):
	"Given a file and a column, extract column as a sorted list"
	# TODO deduplicate, probably using a set
	# TODO trim whitespace
	passage_list = []
	with open(file, 'rb') as inFile:
		fi = csv.reader(inFile, delimiter=delimiter)
		for row in fi:
			passage_list.append(row[col])
	passage_list.sort()
	return passage_list

def assign_id (passage_list):
	"Assign a unique ID to every item in a list"
	passage_id = {}
	index = 0;
	for item in passage_list:
		if item in passage_id:
			pass
		passage_id[item] = index
		index = index + 1
	return passage_id


def word_data(file, col1, col2, delimiter=','):
	word_info = {}
	with open(file, 'rb') as reader:
		fi = csv.reader(reader, delimiter=delimiter)
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

def get_dict(passage_id, file, col1, col2, delimiter=','):
	word_info = word_data(file, col1, col2, delimiter=delimiter)
	passage_info = passage_data(passage_id, word_info)
	return passage_info


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "usage: %s [aoa.csv] [tasks.csv] [out.csv]" % (sys.argv[0])
		sys.exit()

	aoa_file, passage_file, output_file = sys.argv[1:]

	passage_col =  4
	passage_list = make_passage_list(passage_file, passage_col)
	passage_id = assign_id(passage_list)

	passage_diff = get_dict(passage_id, passage_file, passage_col, 9, delimiter='\t')
	aoa_dict = get_dict(passage_id, aoa_file, 0, 10)
	frequency_dict = get_dict(passage_id, aoa_file, 0, 2)

	with open (output_file, 'w+') as output:
		out = csv.writer(output)
		out.writerow(["id", "passage", "difficulty", "aoa", "frequency"])
		for k, v in passage_id.iteritems():
			out.writerow([v, k, passage_diff[v], aoa_dict[v], frequency_dict[v]])
