#!/usr/bin/env python

import sys
class MESSAGE:
	def __init__(self, msg_type):
		"""@todo: Docstring for __init__

		:type: @todo
		:returns: @todo

		"""
		self.form = msg_type 
		self.data = None
		self.data2 = []
	def get_type(self):
		"""@todo: Docstring for get_type
		:returns: @todo

		"""
		return self.form
	def set_contrib(self, ctr):
		"""@todo: Docstring for set_contrib

		:ctr: @todo
		:returns: @todo

		"""
		if self.form >= 0:
			self.data = ctr
		else:
			print "NOT CONTRIB"
	def set_iter(self, it):
		"""@todo: Docstring for set_iter

		:it: @todo
		:returns: @todo

		"""
		if self.form == -1:
			self.data = it
		else:
			print "NOT ITER"
	
	def set_ignore(self, ig):
		"""@todo: Docstring for set_ignore

		:ig: @todo
		:returns: @todo

		"""
		if self.form == -2:
			self.data = ig
		else:
			print "NOT IGNORE"
	
	def set_chain_parent(self, chain_pt):
		"""@todo: Docstring for set_chain_parent

		:chain_pt: @todo
		:returns: @todo

		"""
		if self.form == -100:
			self.data = chain_pt
		else:
			print "NOT CHAIN"
	
	def add_to_chain(self, node_id):
		"""@todo: Docstring for add_to_chain

		:node_id: @todo
		:returns: @todo

		"""
		if self.form == -100:
			self.data2.append(node_id)
		else:
			print "NOT CHAIN"
	
	def set_prev(self, pr):
		"""@todo: Docstring for set_prev

		:pr: @todo
		:returns: @todo

		"""
		if self.form == -101:
			self.data = pr
		else:
			print "NOT PREV"
	
	def __str__(self):
		"""@todo: Docstring for __str__
		:returns: @todo

		"""
		result = ''
		result += str(self.form)
		result += '\t'

		result += str(self.data)

		for thing in self.data2:
			result += '\t'
			result += str(thing)

		result += '\n'

		return result

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



def tok(string):
	"""@todo: Docstring for tok

	:string: @todo
	:returns: @todo

	"""
	res = string.strip()
	return res.split('\t')

def CreatePageRankMessage(node, rank):
	m = MESSAGE(node)
	m.set_contrib(rank)
	return m

def MakeMessage(tokens):
	"""@todo: Docstring for MakeMessage

	:tokens: @todo
	:returns: @todo

	"""
	msg_type = int(tokens[0])
	m = MESSAGE(msg_type)

	if msg_type >= 0:
		m.set_contrib(float(tokens[1]))
		return m
	if msg_type == -1:
		m.set_iter(int(tokens[1]))
		return m
	if msg_type == -2:
		m.set_ignore(int(tokens[1]))
		return m
	if msg_type == -100:
		m.set_chain_parent(int(tokens[1]))
		for u in range(2, len(tokens)):
			m.add_to_chain(int(tokens[u]))
		return m
	if msg_type == -101:
		m.set_prev(float(tokens[1]))
		return m


message_queue = []
pagerank_dict = {}

for line in sys.stdin:
	tokens = tok(line)
	if int(tokens[0]) < 0:
		message_queue.append(MakeMessage(tokens))
	else:
		target_node = int(tokens[0])
		if target_node in pagerank_dict:
			# add the contributions
			pagerank_dict[target_node] += float(tokens[1]) 
		else:
			pagerank_dict[target_node] = 0.0

for node, rank in pagerank_dict.iteritems():
	m = CreatePageRankMessage(node, rank)
	message_queue.append(m)

for msg in message_queue:
	sys.stdout.write(str(msg))
