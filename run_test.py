#!/usr/bin/env python

from sys import *
from subprocess import *
import os
import re
def main():
	"""@todo: Docstring for main
	:returns: @todo

	"""

	stat = call('./pagerank-map.py < 0 | sort -k 1,1 | ./pagerank-reduce.py | ./process-map.py | sort -k 1,1 | ./process-reduce.py > output', shell=True)
	stat = call('rm log.txt', shell=True)

	count = 1

	while stat == 0 and count < int(argv[1]):
		call('cp output input', shell=True)
		print count
		count += 1
		stat = call('./pagerank-map.py < input | sort -k 1,1 | ./pagerank-reduce.py | ./process-map.py | sort -k 1,1 | ./process-reduce.py > output', shell=True)

	call('cat output', shell=True)

if __name__ == '__main__':
	main()
