#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

def str_to_list(string):
	"""@todo: Docstring for str_to_list

	:string: @todo
	:returns: @todo

	"""
	if string == '[]':
		return []
	return [int(s.strip()) for s in string[1:-1].split(',')]

def process_pagerank_reduce(line):
	"""
	Processes a line returned by page-rank-reduce into the list:
	[ 	node k, 
		page_rank of node k (did not incldue the [1] matrix yet),
		a list of nodes that POINTS **TO** k,
		previous rank of k
	]

	:line: @todo
	:returns: @todo

	"""
	line = line.strip()
	line = line.split('\t')

	if (int(line[0]) == -10):
		return [int(line[0]), int(line[1])]

	return [int(line[0]), float(line[1]), str_to_list(line[2]),
			float(line[3])]
	

for line in sys.stdin:
	old_line = line
	line = process_pagerank_reduce(line)

	if (line[0] == -10):
		sys.stdout.write(old_line)
		continue
		

	for innode in line[2]:
		sys.stdout.write(str(innode) + '\t' + str(line[0]) + '\n')

	sys.stdout.write(str(line[0]) + '\t' + str(line[1]) + '\t' + '#' + \
			'\n')
	sys.stdout.write(str(line[0]) + '\t' + str(line[3]) + '\t' + '!' + \
			'\n')
