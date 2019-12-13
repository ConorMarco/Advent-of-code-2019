#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator

from intcode import *


# The Intcode continues!

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 9 or Advent of Code 2019")

# Uncomment this lne for file input
parser.add_argument("file", help="An intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	code = get_input_file_numbers()
	comp = IntcodeComputer(code)
	comp.run_intcode()

	# Part 1
	if should_show_part(1):
		_,outputs = run_intcode_statically(code, [1])
		print_result(outputs[0], 1)

	# Part 2
	if should_show_part(2):
		_,outputs = run_intcode_statically(code, [2])
		print_result(outputs[0], 2)

# Other functions can be defined here.


#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_intcode_1(self):
		code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
		io_handler = QueueIoHandler()
		comp = IntcodeComputer(code.copy(), io_handler)
		comp.run_intcode()
		self.assertEqual(code, list(io_handler.out_queue.queue))

	def test_intcode_2(self):
		code = [1102,34915192,34915192,7,4,7,99,0]
		io_handler = QueueIoHandler()
		comp = IntcodeComputer(code.copy(), io_handler)
		comp.run_intcode()

		result = io_handler.out_queue.get()
		self.assertEqual(len(str(result)), 16)

	def test_intcode_3(self):
		code = [104,1125899906842624,99]
		io_handler = QueueIoHandler()
		comp = IntcodeComputer(code.copy(), io_handler)
		comp.run_intcode()

		result = io_handler.out_queue.get()
		self.assertEqual(result, 1125899906842624)


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


def should_show_part(part):
	return not args.part or args.part == part

def print_result(message, part):
	if should_show_part(part):
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
