#!/usr/bin/env python

import sys
keyword_list = ["IGNORE", "ITERATION"]

#
# This program simply represents the identity function.
#

class PR_Reduce_Struct:
	def __init__(self, node):
		"""@todo: Docstring for __init__
		:returns: @todo

		"""
		self.sum = 0.0
		self.id = node
		self.innodes = []	
		self.previous_rank = 0.0

	def set_prev_rank(self, pr):
		"""@todo: Docstring for set_prev_rank

		:pr: @todo
		:returns: @todo

		"""
		self.previous_rank = pr

	def contribute(self, ct):
		"""@todo: Docstring for contribute

		:ct: @todo
		:returns: @todo

		"""
		self.sum += ct
	
	def add_in(self, node_id):
		"""@todo: Docstring for add_in

		:node_id: @todo
		:returns: @todo

		"""
		self.innodes.append(node_id)
	
	def __str__(self):
		"""@todo: Docstring for __str__
		:returns: @todo

		"""
		return str(self.id) + '\t' + str(self.sum) + '\t' + \
	str(self.innodes) + '\t' + str(self.previous_rank) + '\n'

def processMap(line):
	"""
	process a line printed by processMap into a list as follows:

	[node j, contribution/node k to j, node k, previous rank of
		node j]

	:line: line given by pagerank-map
	:returns: list

	"""
	line = line.strip()
	line = line.split('\t')

	if (int(line[0]) == -10):
		return [int(line[0]), int(line[1])]

	return [int(line[0]), float(line[1]), int(line[2]), float(line[3])]



last_node = -1
list_of_structs = []
counter = -1

for line in sys.stdin:
	old_line = line
	line = processMap(line)

	if (line[0] == -10):
		sys.stdout.write(old_line)
		continue

	if line[0] != last_node:
		if last_node != -1:
			 sys.stdout.write(str(list_of_structs[counter]))
		list_of_structs.append(PR_Reduce_Struct(line[0]))

		counter += 1
		last_node = line[0]

	
	list_of_structs[counter].contribute(line[1])

	if line[2] != -11 and line[2] != -1:
		list_of_structs[counter].add_in(line[2])

	if line[2] == -1:
		list_of_structs[counter].set_prev_rank(line[3])

sys.stdout.write(str(list_of_structs[counter]))
