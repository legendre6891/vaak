#!/usr/bin/env python

import sys
import re


"""
Currently, messages come in these types:
	CONTRIB;	key = natural number, value = float;
	ITER; 		key = -1; value = int;
	IGNORE; 	key = -2; value = int
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
	

message_queue = []
alpha = 0.85
alpha_bar = 1-alpha
ignore_set = set([])
regex = re.compile(".*:([0-9]+).*")

def tok(string):
	"""@todo: Docstring for tok

	:string: @todo
	:returns: @todo

	"""
	res = string.strip()
	return res.split('\t')

def getNumber(string):
	"""@todo: Docstring for getNumber

	:string: @todo
	:returns: @todo

	"""
	global regex
	r = regex.search(string)
	regex.match(string)

	return int(r.groups()[0])

def getType(string):
	"""@todo: Docstring for getType

	:string: @todo
	:returns: @todo

	"""
	if string == "ITER":
		return -1
	if string == 'IGNORE':
		return -2
	else:
		return getNumber(string)

for line in sys.stdin:
	tokens = tok(line)
	msg_type = getType(tokens[0])
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
		m.set_prev(previous_rank)
		message_queue.append(m)



		d = len(outnode_list)
		if d > 0:
			fraction = 1.0/float(d)
			for outnode in outnode_list:
				m = MESSAGE(outnode) # a contribution for outnode
				m.set_contrib(fraction * alpha * current_rank)
				message_queue.append(m)
		else:
			m = MESSAGE(msg_type)
			m.set_contrib(alpha * current_rank)
			message_queue.append(m)

		## add the contribution of G
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
		m.set_ignore(int(tokens[1]))
		message_queue.append(m)

		ignore_set.add(int(tokens[1]))
		continue

for msg in message_queue:
	sys.stdout.write(str(msg))
