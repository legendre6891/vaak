#!/usr/bin/env python

import sys

def main():
	my_lib = __import__("pagerank-map")

	message_queue = []
	pagerank_dict = {}

	for line in sys.stdin:
		tokens = my_lib.tok(line)
		if int(tokens[0]) < 0:
			message_queue.append(my_lib.MakeMessage(tokens))
		else:
			target_node = int(tokens[0])
			if target_node in pagerank_dict:
				pagerank_dict[target_node] += float(tokens[1]) 
			else:
				pagerank_dict[target_node] = 0.0
				pagerank_dict[target_node] += float(tokens[1]) 

	for node, rank in pagerank_dict.iteritems():
		m = my_lib.CreatePageRankMessage(node, rank)
		message_queue.append(m)

	for msg in message_queue:
		sys.stdout.write(str(msg))

if __name__ == '__main__':
	main()
