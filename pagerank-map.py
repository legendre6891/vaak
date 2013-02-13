#!/usr/bin/env python

import sys
import re
from subprocess import *

keyword_list = ["IGNORE", "ITERATION"]
"""
IGNORE will output a -99 as the node receiving the input 
ITERATION ########## -10 ##########
#################### -1 #### comes from G
#################### -11 ### comes from self, when no outnodes
"""

logfile_name = "data_log.txt"
watch_nodes = [89,793]

def processLine(line):
	"""This processes a input line of the form 
	NodeId:k 	rank, rank',a,b,c,d,e, ....

	:line: a string of the format above.
	:returns: returns a list
	[node id, current rank, previous rank, \
			[list of outnodes]]

	"""
	
	line = line.strip()
	line = line.split('\t')
	if line[0] in keyword_list:
		return [line[0], int(line[1])]


	regex = re.compile(".*:([0-9]+).*")
	r = regex.search(line[0])
	regex.match(line[0])

	node_id = int(r.groups()[0])

	numberlist = line[1].split(',')
	current_rank = float(numberlist[0])
	previous_rank = float(numberlist[1])

	outnode_list = []
	for u in range(2, len(numberlist)):
		outnode_list.append(int(numberlist[u]))

	return [node_id, current_rank, previous_rank, outnode_list]


page_rank_map_output = []
alpha = 0.85
alpha_bar = 1-alpha
list_of_line_structs = []
total_sum = 0.0
total_nodes = 0

ignore_set = set([])

for line in sys.stdin:
	line = processLine(line)
	list_of_line_structs.append(line)
n_nodes = len(list_of_line_structs)


for u in range(n_nodes):
	r = list_of_line_structs[u]

	if (r[0] == "ITERATION"):
		page_rank_map_output.append(str(-10) + '\t' + str(r[1]) + '\n')
		continue

	if (r[0] == "IGNORE"):
		ignore_set.add(r[1])
		continue

	if len(r[3]) > 0:
		fraction = 1.0/len(r[3])
		for outnode in r[3]:
			contribution = r[1] * fraction * alpha
			inc = r[1] * fraction * alpha


			"""
			If something is in the ignore_set, then there is no need to
			recompute its page rank. To do this, we do not any outnodes that
			are in the ignore list.


			Finally, at the VERY END, we simulate a contribution from every
			member of the ignore list, to itself. To make sure that its
			rating is preserved.
			"""
			if outnode not in ignore_set:
				page_rank_map_output.append(str(outnode) + '\t' + str(contribution) + \
						'\t' + str(r[0]) + '\t' + str(691.0) + '\n')
			"""
			string is the the form:
				<node j to add the contribution to>,
				<the contribution amount>
				<node k the contribution came from>
				<reserved for passing along the previous rank>
			"""
	else:
		if outnode not in ignore_set:
			page_rank_map_output.append(str(r[0]) + '\t' + str(r[1]*alpha) +
					'\t' + str(-11) + '\t' + \
					str(691.0) + '\n')
	
	"""
	We need to account for the matrix G.
	In here, EVERY NODE contributes to EVERY NODE (even itself).
	"""
	#for v in range(n_nodes):
		#G_contribution = list_of_line_structs[v][1] * 1.0/n_nodes * (1-alpha)

		#page_rank_map_output.append(str(r[0]) + '\t' + \
				#str(G_contribution) + '\t' + \
				#'-1' + '\t' + \
				#str(r[2]) + '\n')
	#G_contribution = (1-alpha)*total_sum * n_nodes
	page_rank_map_output.append(str(r[0]) + '\t' + \
			str(1-alpha) + '\t' + \
			str(-1) + '\t' + \
			str(r[1]) + '\n')
	#page_rank_map_output.append(str(r[0]) + '\t' + \
			#str((1-alpha)*total_sum/total_nodes) + '\t' + \
			#'-1' + '\t' + \
			#str(r[1]) + '\n')

for s in page_rank_map_output:
	sys.stdout.write(s)
