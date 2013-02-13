#!/usr/bin/env python

import sys
import re


"""
Currently, messages come in these types:
	CONTRIB;	key = natural number, value = float;
	ITER; 		key = -1; value = int;
	KEEP; 	key = -2; value = int
	CHAIN; 		key = -100; value = [int] [int .... int]
	PREV; 		key = -101; value = [int] float
"""


"""
To add a new kind, the following must be done:
	* Add something in the MESSAGE class to set elements.
	* Add support into getType
	* Add a handler after getType
"""

class MESSAGE:
	def __init__(self, msg_type):
		"""@todo: Docstring for __init__

		:type: @todo
		:returns: @todo

		"""
		self.form = msg_type 
		self.data = None
		self.data2 = []
		self.tag = None
		self.taglist = []
		

	def set_tag(self, t):
		"""@todo: Docstring for set_tag

		:t: @todo
		:returns: @todo

		"""
		self.tag = t
	
	def add_tag_list(self, thing):
		"""@todo: Docstring for add_tag_list

		:thing: @todo
		:returns: @todo

		"""
		self.taglist.append(thing)

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
	
	def set_keep(self, ig):
		"""@todo: Docstring for set_keep

		:ig: @todo
		:returns: @todo

		"""
		if self.form == -2:
			self.data = ig
		else:
			print "NOT KEEP"
	
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
			self.data2.append(pr)
		else:
			print "NOT PREV"
	
	def set_prev_parent(self, node):
		"""@todo: Docstring for set_chain_parent

		:node: @todo
		:returns: @todo

		"""
		if self.form == -101:
			self.data = node
		else:
			print "NOT PREV (parent)"
	
	def __str__(self, displayTag = False):
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

		if displayTag:
			result += '\t'
			result += str(self.tag)

			for thing in self.taglist:
				result += '\t'
				result += str(thing)

		result += '\n'

		return result
	


def tok(string):
	"""@todo: Docstring for tok

	:string: @todo
	:returns: @todo

	"""
	res = string.strip()
	return res.split('\t')

def getNumber(string, regex):
	"""@todo: Docstring for getNumber

	:string: @todo
	:returns: @todo

	"""
	r = regex.search(string)
	regex.match(string)

	return int(r.groups()[0])

def getType(string, regex):
	"""@todo: Docstring for getType

	:string: @todo
	:returns: @todo

	"""
	if string == "ITER":
		return -1
	if string == 'KEEP':
		return -2
	else:
		return getNumber(string, regex)

def CreatePageRankMessage(node, rank):
	m = MESSAGE(node)
	m.set_contrib(rank)
	return m

def MakeMessage(tokens, hasTag = False):
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
		m.set_keep(int(tokens[1]))
		return m
	if msg_type == -100:
		m.set_chain_parent(int(tokens[1]))
		for u in range(2, len(tokens)):
			m.add_to_chain(int(tokens[u]))
		return m

	if msg_type == -101:
		m.set_prev_parent(int(tokens[1]))
		m.set_prev(float(tokens[2]))
		return m

def main():
	message_queue = []
	alpha = 0.85
	keep_set = set([])
	regex = re.compile(".*:([0-9]+).*")
	
	for line in sys.stdin:
		tokens = tok(line)

		msg_type = getType(tokens[0], regex)
		if msg_type >= 0:
			numberlist = tokens[1].split(',')
			current_rank = float(numberlist[0])
			previous_rank = float(numberlist[1])


			## Add the CHAIN
			m = MESSAGE(-100)
			m.set_chain_parent(msg_type)

			outnode_list = []
			for u in range(2, len(numberlist)):
				outnode_list.append(int(numberlist[u]))
				m.add_to_chain(int(numberlist[u]))

			message_queue.append(m)

			m = MESSAGE(-101)
			m.set_prev(current_rank)
			m.set_prev_parent(msg_type)
			message_queue.append(m)

			if msg_type in keep_set:
				m = MESSAGE(msg_type)
				m.set_contrib(current_rank)
				message_queue.append(m)


			d = len(outnode_list)
			if d > 0:
				fraction = 1.0/float(d)
				for outnode in outnode_list:
					if outnode not in keep_set:
						m = MESSAGE(outnode) # a contribution for outnode
						m.set_contrib(fraction * alpha * current_rank)
						message_queue.append(m)
			else:
				if outnode not in keep_set:
					m = MESSAGE(msg_type)
					m.set_contrib(alpha * current_rank)
					message_queue.append(m)

			## add the contribution of G
			if msg_type not in keep_set:
				m = MESSAGE(msg_type)
				m.set_contrib(1-alpha)
				message_queue.append(m)

			continue ## continue to the next line

		if msg_type == -1:
			m = MESSAGE(msg_type)
			m.set_iter(int(tokens[1]))
			message_queue.append(m)
			
			continue

		if msg_type == -2:
			m = MESSAGE(msg_type)
			m.set_keep(int(tokens[1]))
			message_queue.append(m)

			keep_set.add(int(tokens[1]))
			continue

	for msg in message_queue:
		sys.stdout.write(str(msg))

if __name__ == '__main__':
	main()
