#!/usr/bin/env python
import sys

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
	count_interation = -1

	for line in sys.stdin:
		tokens = my_lib.tok(line)

		if int(tokens[0]) < 0:
			if int(tokens[0]) == -1:
				hasIter = True
				interation = int(tokens[1])


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
	
if __name__ == '__main__':
	main()
