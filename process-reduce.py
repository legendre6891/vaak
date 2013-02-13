#!/usr/bin/env python
import sys

def stoppingCriterion(node_dict, count_iteration):
	"""@todo: Docstring for stoppingCriterion

	:node_dict: @todo
	:count_iteration: @todo
	:returns: @todo

	"""
	if (count_iteration > 50):
		return True
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
		return 'IGNORE' + '\t' + str(message.data) + '\n'



def main():
	my_lib = __import__("pagerank-map")
	message_queue = []
	node_dict = {}
	hasIter = False
	count_iteration = -1

	for line in sys.stdin:
		tokens = my_lib.tok(line)

		if int(tokens[0]) < 0:
			if int(tokens[0]) == -1:
				hasIter = True
				count_iteration = int(tokens[1])


			message_queue.append(my_lib.MakeMessage(tokens))
		else:
			target_node = int(tokens[0])
			if target_node in node_dict:
				if tokens[2] == '{':
					for u in range(3, len(tokens)):
						node_dict[target_node][2].append(int(tokens[u]))
				if tokens[2] == '$':
					next_rank = float(tokens[1])
					node_dict[target_node][0] = next_rank
				if tokens[2] == '*':
					prev_rank = float(tokens[1])
					node_dict[target_node][1] = prev_rank
			else:
				node_dict[target_node] = [0,0,[]]
				if tokens[2] == '{':
					for u in range(3, len(tokens)):
						node_dict[target_node][2].append(int(tokens[u]))
				if tokens[2] == '$':
					next_rank = float(tokens[1])
					node_dict[target_node][0] = next_rank
				if tokens[2] == '*':
					prev_rank = float(tokens[1])
					node_dict[target_node][1] = prev_rank


	if stoppingCriterion(node_dict, count_iteration):
		top_ten = findTenBiggest(node_dict)
		for i in range(10):
			sys.stdout.write("FinalRank:" + str(top_ten[i][1]) + '\t' +
					str(top_ten[i][0]) + '\n')
		sys.exit(33)
	else:
		for node, data in node_dict.iteritems():
			sys.stdout.write("NodeId:" + str(node) + '\t' + str(data[0]) + ',' \
					+ str(data[1]))
			for outnode in data[2]:
				sys.stdout.write(',' + str(outnode))
			sys.stdout.write('\n')
		

		for msg in message_queue:
			string = fancystring(msg)
			sys.stdout.write(string)

		if hasIter == False:
			m = my_lib.MESSAGE(-1)
			m.set_iter(0)
			string = fancystring(m)
			sys.stdout.write(string)

		sys.exit(0)
	
	
if __name__ == '__main__':
	main()
