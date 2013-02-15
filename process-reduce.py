#!/usr/bin/env python
import sys
import re
from time import time
from sys import stderr


"""
Currently, messages come in these types:
	CONTRIB;	key = natural number, value = float;
	ITER; 		key = -1; value = int;
	KEEP; 		key = -2; value = int
	TEN: 		key = -3; value = [list of 10 ints]
	SAME: 		key = -4; value = int
	IGNORE; 	key = -3; value = int
	CHAIN; 		key = -100; value = [int] [int .... int]
	PREV; 		key = -101; value = [int] float

Furthermore, all messages end in a
	tag
and
	tag_list

These two values can be *ANY STRING*. Use them for your convenience.
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

	def add_to_ten(self, node):
		"""@todo: Docstring for add_to_ten

		:node: @todo
		:returns: @todo

		"""
		if self.form == -3:
			self.data2.append(node)
		else:
			print "NOT TEN"

	def set_same(self, s):
		"""@todo: Docstring for set_same

		:s: @todo
		:returns: @todo

		"""
		if self.form == -4:
			self.data = s
		else:
			print "NOT SAME"

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


def getNumber(string, regex, makePositive=True):
	"""@todo: Docstring for getNumber

	:string: @todo
	:returns: @todo

	"""
	r = regex.search(string)
	regex.match(string)

	if makePositive:
		return abs(int(r.groups()[0]))
	else:
		return int(r.groups()[0])

def getType(string, regex):
	"""@todo: Docstring for getType

	:string: @todo
	:returns: @todo

	"""
	if string == "ITER":
		return [-1, 0]
	if string == 'KEEP':
		return [-2, 0]
	if string == 'TEN':
		return [-3, 0]
	if string == 'SAME':
		return [-4, 0]
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
	if msg_type == -3:
		for u in range(2, len(tokens)):
			m.add_to_ten(int(tokens[u]))
		return m
	if msg_type == -4:
		m.set_same(int(tokens[1]))
		return m
	if msg_type == -1:
		m.set_same(int(tokens[1]))
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
# PREPEND ABOVE
# ---------------------

def fabs(f):
	if f < 0:
		return -f
	else:
		return f

def getMaxDigressionRatio(node_dict, message_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if node in message_dict['KEEP']:
			continue
		if fabs(data[0] - data[1])/data[1] > m:
			m = fabs(data[0] - data[1])/data[1]

	return m

def getMaxDigression(node_dict, message_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if node in message_dict['KEEP']:
			continue
		if fabs(data[0] - data[1]) > m:
			m = fabs(data[0] - data[1])

	return m


def getMaxRank(node_dict):

	m = 0.0
	for node,data in node_dict.iteritems():
		if data[1] > m:
			m = data[1]

	return m

def getMaxDelta(node_dict, message_dict):
	"""@todo: Docstring for getMaxDelta

	:node_dict: @todo
	:returns: @todo

	"""
	m = 0.0
	for node,data in node_dict.iteritems():
		if node in message_dict['KEEP']:
			continue
		if fabs(data[0] - data[1])/data[1] > m:
			m = fabs(data[0] - data[1])/data[1]

	return m

def stoppingCriterion(node_dict, message_dict, top_ten):
	"""@todo: Docstring for stoppingCriterion

	:node_dict: @todo
	:count_iteration: @todo
	:returns: @todo

	"""
	ti = time()
	count_iteration = message_dict['ITER']
	ten_nodes = message_dict['TEN']
	if len(ten_nodes) == 10: #print >> sys.stderr, ten_nodes
		#print >> sys.stderr, [top_ten[i][0] for i in range(10)]
		changed = False
		for i in range(10):
			if ten_nodes[i] != top_ten[i][0]:
				changed = True
				break

		if changed == False:
			message_dict['SAME'] += 1
			#print >> sys.stderr, "SAME!", message_dict['SAME']
			if message_dict['SAME'] * count_iteration > 150:
				pass
				return True
		else:
			message_dict['SAME'] = 0
			#print >> sys.stderr, "NOT SAME!", message_dict['SAME']


	if (count_iteration > 40):
		return True

	dig = getMaxDigression(node_dict, message_dict)
	ma = getMaxRank(node_dict)

	if (dig/ma < 0.001):
		return True

	#rat = getMaxDigressionRatio(node_dict)
	#if (rat < 0.00001):
		#return True
	#else:
		#return False
	
	tf = time()
	print >> stderr, "stoppingCriterion TOOK:", float(tf-ti)
	return False

def findKBiggest(node_dict, k):
	ti = time()
	topk = [[0,-1] for i in range(k)]

	for node,data in node_dict.iteritems():
		for u in range(k):
			if data[0] > topk[u][1]:
				for v in range(k-1, u,-1):
					topk[v] = topk[v-1]
				topk[u] = [node, data[0]]
				break
	
	tf = time()
	print >> stderr, "findKBiggest TOOK:", float(tf-ti)

	return topk
				


def findTenBiggest(node_dict):
	"""@todo: Docstring for findTenBiggest

	:list_of_structs: @todo
	:returns: @todo

	"""
	return findKBiggest(node_dict, 10)


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

def PERFORM_OPTIMIZATIONS(node_dict, message_dict, topk):
	"""@todo: Docstring for PERFORM_OPTIMIZATIONS

	:node_dict: @todo
	:message_dict: @todo
	:returns: @todo

	"""
	ti = time()
	count_iteration = message_dict['ITER']
	count_nodes = len(node_dict)
	#change_threshold= 10**(-float(count_iteration)/5.00 - 1) \
			#* (0.000206897*count_nodes + 0.17931)
	#change_threshold= 10**(-float(count_iteration)/5.00 - 1) \
			#* 0.8
	change_threshold = 0.01
	#change_threshold = 0.003 * count_iteration + 0.000
	#change_threshold = 0.01
	#max_allowed = 0.0
	#change_threshold = 0.01 + (0.001 - 5*1.0/float(count_nodes))*count_iteration

	#change_threshold = 0
	#if change_threshold > max_allowed:
		#change_threshold = max_allowed


	topk_nodes = [topk[i][0] for i in range(len(topk))]
	topnode_set = set(topk_nodes)

	#if count_iteration >= 15:
		#return

	for node, data in node_dict.iteritems():
		if (node not in message_dict['KEEP']) and fabs(data[1] -\
				data[0])/(data[1]) < change_threshold:
			#f_file = open('log.txt', 'a')
			#print >> f_file, 'keeping', node, '(curr, prev) =', data[1], \
			#data[0], "at iteration", count_iteration
			message_dict['KEEP'].add(node)

		if (node not in message_dict['KEEP'] and \
				(not topnode_set & set(data[2])) and \
				count_iteration >= 5 and \
				node not in topnode_set):
			pass
			#message_dict['KEEP'].add(node)
		
	tf = time()

	print >> stderr, "PERFORM_OPTIMIZATION TOOK:", float(tf-ti)


def main():

	node_dict = {}


	message_dict = {}
	message_dict['ITER'] = 0
	message_dict['KEEP'] = set([])
	message_dict['TEN'] = []
	message_dict['SAME'] = 0

	hasIter = False

	for line in sys.stdin:
		tokens = tok(line)

		if int(tokens[0]) < 0:
			if int(tokens[0]) == -1:
				hasIter = True
				count_iteration = int(tokens[1])

			m = MakeMessage(tokens)

			if m.form == -1:
				message_dict['ITER'] = m.data + 1
			elif m.form == -2:
				message_dict['KEEP'].add(m.data)
			elif m.form == -3:
				message_dict['TEN'] = m.data2
			elif m.form == -4:
				message_dict['SAME'] = m.data


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


	topk = findKBiggest(node_dict, 15)
	#top_ten = findTenBiggest(node_dict)
	top_ten = [topk[i] for i in range(10)]

	PERFORM_OPTIMIZATIONS(node_dict, message_dict, topk)


	if stoppingCriterion(node_dict, message_dict, top_ten):
		for i in range(10):
			sys.stdout.write("FinalRank:" + str(top_ten[i][1]) + '\t' +
					str(top_ten[i][0]) + '\n')
		#sys.exit(33)
	else:
		m = MESSAGE(-3)
		for u in range(10):
			m.add_to_ten(top_ten[u][0])

		message_dict['TEN'] = m.data2

		for msg_type, data in message_dict.iteritems():
			string = message_entry_to_string(msg_type, data)
			sys.stdout.write(string)

		for node, data in node_dict.iteritems():
			if node in message_dict['KEEP']:
				sys.stdout.write("NodeId:" + str(-node) + '\t' + str(data[0]) + ',' \
						+ str(data[1]))
				for outnode in data[2]:
					if outnode not in message_dict['KEEP']:
						sys.stdout.write(',' + str(outnode))
					else:
						sys.stdout.write(',' + str(-outnode))

				sys.stdout.write('\n')
			else:
				sys.stdout.write("NodeId:" + str(node) + '\t' + str(data[0]) + ',' \
						+ str(data[1]))
				for outnode in data[2]:
					if outnode not in message_dict['KEEP']:
						sys.stdout.write(',' + str(outnode))
					else:
						sys.stdout.write(',' + str(-outnode))
				sys.stdout.write('\n')



		#sys.exit(0)


if __name__ == '__main__':
	main()
