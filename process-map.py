#!/usr/bin/env python
import sys

message_queue = []

for line in sys.stdin:
	my_lib = __import__("pagerank-map")

	tokens = my_lib.tok(line)
	msg_type = int(tokens[0])


	if msg_type >= 0:
		m = my_lib.MESSAGE(msg_type)
		m.set_contrib(float(tokens[1]))
		m.set_tag("$")
		message_queue.append(m)
		continue

	if msg_type == -101:
		target_node = int(tokens[1])
		m = my_lib.MESSAGE(target_node)
		m.set_contrib(float(tokens[2]))
		m.set_tag("*")
		message_queue.append(m)
		continue

	if msg_type == -100:
		target_node = int(tokens[1])
		m = my_lib.MESSAGE(target_node)
		m.set_contrib(-1.0)


		outnodes = []
		for u in range(2, len(tokens)):
			m.add_tag_list(int(tokens[u]))
			outnodes.append(int(u))

		m.set_tag("{")
		message_queue.append(m)
		continue
	
	## for other types
	sys.stdout.write(line)


for msg in message_queue:
	sys.stdout.write(msg.__str__(True))
