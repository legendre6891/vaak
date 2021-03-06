#!/usr/bin/env python


import sys
#from math import fabs
#
# This program simply represents the identity function.
#

class PROCESS_Reduce_Struct:
	def __init__(self, node):
		"""@todo: Docstring for __init__

		:node: @todo
		:returns: @todo

		"""
		self.outnodes = []
		self.id = node 
		self.previous_rank = 0.0
		self.current_rank = -1
	
	def add_out(self, out):
		"""@todo: Docstring for add_out

		:out: @todo
		:returns: @todo

		"""
		self.outnodes.append(out)
	
	def set_curr_rank(self, cr):
		"""@todo: Docstring for set_curr_rank

		:cr: @todo
		:returns: @todo

		"""
		self.current_rank = cr

	def set_prev_rank(self, pr):
		"""@todo: Docstring for set_prev_rank

		:pr: @todo
		:returns: @todo

		"""
		self.previous_rank = pr

	def __str__(self):
		"""@todo: Docstring for __str__
		:returns: @todo

		"""
		result =  "NodeId:" + str(self.id) + '\t' + str(self.current_rank) + \
				',' + str(self.previous_rank) 

		if len(self.outnodes) == 0:
			return result + '\n'
		else:
			for s in self.outnodes:
				result += ',' + str(s)
			return result + '\n'


def stoppingCriterion(minimum_digress, maximum, count_iteration):
	"""@todo: Docstring for stoppingCriterion

	:minimum_digress: @todo
	:maximum: @todo
	:returns: @todo

	"""
	if count_iteration >= 200:
		return True
	if (minimum_digress / maximum < .01):
		return True
	else:
		return False

def fabs(f):
	if f < 0:
		return -f
	else:
		return f

def process_processMap(line):
	"""@todo: Docstring for processMap

	:line: @todo
	:returns: @todo

	"""
	line = line.strip()
	line = line.split('\t')

	return line

def calculate_digression(list_of_structs):
	"""@todo: Docstring for calculate_digression

	:list_of_structs: @todo
	:returns: @todo

	"""
	min_d = 0 
	for struct in list_of_structs:
		if fabs(struct.current_rank - struct.previous_rank) > min_d:
			min_d = fabs(struct.current_rank - struct.previous_rank)
	return min_d

def calculate_maximum(list_of_structs):
	"""@todo: Docstring for calculate_maximum

	:list_of_structs: @todo
	:returns: @todo

	"""
	maximum = 0 
	for struct in list_of_structs:
		if struct.current_rank > maximum:
			maximum = struct.current_rank
	return maximum


def findTenBiggest(list_of_structs):
	"""@todo: Docstring for findTenBiggest

	:list_of_structs: @todo
	:returns: @todo

	"""
	found_indices = [[0,0] for i in range(10)]
	for st in list_of_structs:
		if (st.current_rank > found_indices[0][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = found_indices[1]
			found_indices[1] = found_indices[0]
			found_indices[0] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[1][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = found_indices[1]
			found_indices[1] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[2][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[3][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[4][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[5][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[6][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[7][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[8][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = [st.id, st.current_rank]
			continue
		if (st.current_rank > found_indices[9][1]):
			found_indices[9] = [st.id, st.current_rank]
			continue
	
	return found_indices

last_node = -1
list_of_structs = []
counter = -1
list_to_write = []
count_iteration = 0

for line in sys.stdin:
	line = process_processMap(line)

	if (int(line[0]) == -10):
		count_iteration = int(line[1])
		continue

	if line[0] != last_node:
		if last_node != -1:
			list_to_write.append(str(list_of_structs[counter]))
		list_of_structs.append(PROCESS_Reduce_Struct(line[0]))

		counter += 1
		last_node = line[0]

	if len(line) == 2:
		list_of_structs[counter].add_out(int(line[1]))
	else:
		if line[2] == '!':
			list_of_structs[counter].set_prev_rank(float(line[1]))
		if line[2] == '#':
			list_of_structs[counter].set_curr_rank(float(line[1]))

		
list_to_write.append(str(list_of_structs[counter]))
list_to_write.append("ITERATION" + '\t' + str(count_iteration + 1) + '\n')

minimum_digress = calculate_digression(list_of_structs)
maximum = calculate_maximum(list_of_structs)

if stoppingCriterion(minimum_digress, maximum, count_iteration):
	top_ten = findTenBiggest(list_of_structs)
	for i in range(10):
		sys.stdout.write("FinalRank:" + str(top_ten[i][1]) + '\t' + str(top_ten[i][0]) + '\n')
	#sys.stdout.write("minimum_digress = " + str(minimum_digress) + '\n')
	#sys.stdout.write("iteration = " + str(count_iteration) + '\n')
	#sys.exit(33)
else:
	for u in list_to_write:
		sys.stdout.write(u)
	#sys.exit(0)

