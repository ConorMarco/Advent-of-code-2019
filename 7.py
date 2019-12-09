#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator

from queue import Queue 
from intcode import *


# This is a template file for Advent of Code 2019. It handles basic input and reading files,
# as well as providing a usage string and unit tests.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="This is a template file. Please copy for individual problems for the 2019 Advent of Code.")

# Uncomment this lne for file input
parser.add_argument("file", help="An intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------

def main():
	global inputs_so_far
	global last_out
	global queue

	code = get_input_file_numbers()
	best = 0

	# Part 1
	for perm in itertools.permutations(range(5)):
		amps = setup(perm, code, 0)
		for amp in amps:
			amp.run_intcode()
		result = amps[0].io_handler.in_queue.get()
		best = max(best, result)
	print_result(best, 1)


	# Part 2
	for perm in itertools.permutations(range(5, 10)):
		amps = setup(perm, code, 0)
		run_concurrently(amps)
		result = amps[0].io_handler.in_queue.get()
		best = max(best, result)
	print_result(best, 2)


def setup(phases, code, initial):
	queues = [Queue() for _ in range(5)]
	io_handlers = [QueueIoHandler(queues[i % 5], queues[(i+1) % 5]) for i in range(5)]
	for i in range(5):
		queues[i].put(phases[i])
	queues[0].put(initial)
	return [IntcodeComputer(code.copy(), io_handlers[i]) for i in range(5)]

def run_concurrently(amps):
	return None




#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_trivial(self):
		self.assertTrue(True)


	# Test cleanup
	def tearDown(self):
		return None


#----------------------------------------------END TEST CODE---------------------------------------------------


# Read a filename in from arguments and give the contents of the file as a list of lines
def get_input_file():
	filename = args.file
	try:
		file = open(filename, 'r')
		return file.readlines()
	except:
		print("There has been a file reading error with file " + filename + ":")
		exit()

def tokenize_input_file_by_line(delimeter=','):
	return list(map(lambda x: x.split(delimeter), get_input_file()))

def get_input_file_tokens(delimeter=','):
	return functools.reduce(operator.iconcat, tokenize_input_file_by_line(delimeter), [])

def get_input_file_numbers(delimeter=','):
	return list(map(int, get_input_file_tokens(delimeter)))

def print_result(message, part):
	if not args.part or args.part == part:
		print("Part " + str(part) + ": " + str(message))



parser.add_argument("-t", "--test", help="run all tests", action="store_true")
parser.add_argument("-p", "--part", help="only print results for the given part", type=int, choices=[1, 2])

# Hack to get around positional arguments still being required even for test runs:
if "-t" in sys.argv or "--test" in sys.argv:
	# Remove command line arguments for test run
	unittest.main(argv = [sys.argv[0]])
else:
	args = parser.parse_args()
	main()
