#!/usr/bin/env python
import sys


def fabs(f):
	if f < 0:
		return -f
	else:
		return f

def getMaxDigressionRatio(node_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if fabs(data[0] - data[1])/data[1] > m:
			m = fabs(data[0] - data[1])/data[1]
	
	return m

def getMaxDigression(node_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if fabs(data[0] - data[1]) > m:
			m = fabs(data[0] - data[1])
	
	return m


def getMaxRank(node_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if data[1] > m:
			m = data[1]
	
	return m

def getMaxDelta(node_dict):
	"""@todo: Docstring for getMaxDelta

	:node_dict: @todo
	:returns: @todo

	"""
	m = 0.0
	for node,data in node_dict.iteritems():
		if fabs(data[0] - data[1])/data[1] > m: 
			m = fabs(data[0] - data[1])/data[1]
	
	return m

def stoppingCriterion(node_dict, message_dict, top_ten):
	"""@todo: Docstring for stoppingCriterion

	:node_dict: @todo
	:count_iteration: @todo
	:returns: @todo

	"""
	count_iteration = message_dict['ITER']
	ten_nodes = message_dict['TEN']

	if len(ten_nodes) == 10:
		print >> sys.stderr, ten_nodes
		print >> sys.stderr, [top_ten[i][0] for i in range(10)]
		changed = False
		for i in range(10):
			if ten_nodes[i] != top_ten[i][0]:
				changed = True
				break
		
		if changed == False:
			message_dict['SAME'] += 1
			print >> sys.stderr, "SAME!", message_dict['SAME']
			if message_dict['SAME'] * count_iteration > 35:
				return True
		else:
			message_dict['SAME'] = 0
			print >> sys.stderr, "NOT SAME!", message_dict['SAME']

	
	if (count_iteration > 100000):
		return True

	#dig = getMaxDigression(node_dict)
	#ma = getMaxRank(node_dict)
	
	#if (dig/ma < 0.001):
		#return True

	#rat = getMaxDigressionRatio(node_dict)
	#if (rat < 0.001):
		#return True
	else:
		return False

def findTenBiggest(node_dict):
	"""@todo: Docstring for findTenBiggest

	:list_of_structs: @todo
	:returns: @todo

	"""
	found_indices = [[0,0] for i in range(10)]
	for node,data in node_dict.iteritems():
		if (data[0] > found_indices[0][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = found_indices[1]
			found_indices[1] = found_indices[0]
			found_indices[0] = [node, data[0]]
			continue
		if (data[0] > found_indices[1][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = found_indices[1]
			found_indices[1] = [node, data[0]]
			continue
		if (data[0] > found_indices[2][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = found_indices[2]
			found_indices[2] = [node, data[0]]
			continue
		if (data[0] > found_indices[3][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = found_indices[3]
			found_indices[3] = [node, data[0]]
			continue
		if (data[0] > found_indices[4][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = found_indices[4]
			found_indices[4] = [node, data[0]]
			continue
		if (data[0] > found_indices[5][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = found_indices[5]
			found_indices[5] = [node, data[0]]
			continue
		if (data[0] > found_indices[6][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = found_indices[6]
			found_indices[6] = [node, data[0]]
			continue
		if (data[0] > found_indices[7][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = found_indices[7]
			found_indices[7] = [node, data[0]]
			continue
		if (data[0] > found_indices[8][1]):
			found_indices[9] = found_indices[8]
			found_indices[8] = [node, data[0]]
			continue
		if (data[0] > found_indices[9][1]):
			found_indices[9] = [node, data[0]]
			continue
	
	return found_indices


def fancystring(message):
	"""@todo: Docstring for fancystring

	:message: @todo
	:returns: @todo

	"""
	msg_type = message.get_type()
	if (msg_type == -1):
		return 'ITER' + '\t' + str(1+ message.data) + '\n'
	if (msg_type == -2):
		return 'KEEP' + '\t' + str(message.data) + '\n'



def message_entry_to_string(msg_type, data):
	"""@todo: Docstring for message_entry_to_string

	:msg_type: @todo
	:data: @todo
	:returns: @todo

	"""
	if msg_type == 'ITER':
		return msg_type + '\t' + str(data) + '\n'
	
	if msg_type == 'KEEP':
		string = ''
		for ignored_node in data:
			string += msg_type + '\t' + str(ignored_node) + '\n'
		return string

	if msg_type == 'TEN':
		string = 'TEN'
		for node in data:
			string += '\t' + str(node)
		string += '\n'
		return string

	if msg_type == 'SAME':
		return msg_type + '\t' + str(data) + '\n'

def PERFORM_OPTIMIZATIONS(node_dict, message_dict):
	"""@todo: Docstring for PERFORM_OPTIMIZATIONS

	:node_dict: @todo
	:message_dict: @todo
	:returns: @todo

	"""
	#return
	count_iteration = message_dict['ITER']
	count_nodes = len(node_dict)
	#change_threshold= 10**(-float(count_iteration)/5.00 - 1) \
			#* (0.000206897*count_nodes + 0.17931) 
	#change_threshold= 10**(-float(count_iteration)/5.00 - 1) \
			#* 0.6
	#change_threshold = 0.003 * count_iteration + 0.000
	#change_threshold = 0.01
	#max_allowed = 0.0SAME
	change_threshold = 0.01 + (0.001 - 5*1.0/float(count_nodes))*count_iteration

	#change_threshold = 0
	#if change_threshold > max_allowed:
		#change_threshold = max_allowed



	for node, data in node_dict.iteritems():
		if (node not in message_dict['KEEP']) and fabs(data[1] -\
				data[0])/(data[1]) < change_threshold:
			f_file = open('log.txt', 'a')
			print >> f_file, 'keeping', node, '(curr, prev) =', data[1], \
			data[0], "at iteration", count_iteration
			message_dict['KEEP'].add(node)

def main():
	my_lib = __import__("pagerank-map")
	message_queue = []

	node_dict = {}


	message_dict = {}
	message_dict['ITER'] = 0
	message_dict['KEEP'] = set([])
	message_dict['TEN'] = []
	message_dict['SAME'] = 0

	hasIter = False

	for line in sys.stdin:
		tokens = my_lib.tok(line)

		if int(tokens[0]) < 0:
			if int(tokens[0]) == -1:
				hasIter = True
				count_iteration = int(tokens[1])

			m = my_lib.MakeMessage(tokens)
			
			if m.form == -1:
				message_dict['ITER'] = m.data + 1
			elif m.form == -2:
				message_dict['KEEP'].add(m.data)
			elif m.form == -3:
				message_dict['TEN'] = m.data2
			elif m.form == -4:
				message_dict['SAME'] = m.data


			message_queue.append(m)
		else:
			target_node = int(tokens[0])
			if target_node in node_dict:
				if tokens[2] == '{':
					for u in range(3, len(tokens)):
						node_dict[target_node][2].append(int(tokens[u]))
				elif tokens[2] == '$':
					next_rank = float(tokens[1])
					node_dict[target_node][0] = next_rank
				elif tokens[2] == '*':
					prev_rank = float(tokens[1])
					node_dict[target_node][1] = prev_rank
			else:
				node_dict[target_node] = [0,0,[]]
				if tokens[2] == '{':
					for u in range(3, len(tokens)):
						node_dict[target_node][2].append(int(tokens[u]))
				elif tokens[2] == '$':
					next_rank = float(tokens[1])
					node_dict[target_node][0] = next_rank
				elif tokens[2] == '*':
					prev_rank = float(tokens[1])
					node_dict[target_node][1] = prev_rank


	PERFORM_OPTIMIZATIONS(node_dict, message_dict)
	
	top_ten = findTenBiggest(node_dict)

	if stoppingCriterion(node_dict, message_dict, top_ten):
		for i in range(10):
			sys.stdout.write("FinalRank:" + str(top_ten[i][1]) + '\t' +
					str(top_ten[i][0]) + '\n')
		sys.exit(33)
	else:

		m = my_lib.MESSAGE(-3)
		for u in range(10):
			m.add_to_ten(top_ten[u][0])
		
		message_dict['TEN'] = m.data2
		
		for msg_type, data in message_dict.iteritems():
			string = message_entry_to_string(msg_type, data)
			sys.stdout.write(string)

		for node, data in node_dict.iteritems():
			sys.stdout.write("NodeId:" + str(node) + '\t' + str(data[0]) + ',' \
					+ str(data[1]))
			for outnode in data[2]:
				sys.stdout.write(',' + str(outnode))
			sys.stdout.write('\n')
		


		sys.exit(0)
	
	
if __name__ == '__main__':
	main()
