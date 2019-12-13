#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# This is a template file for Advent of Code 2019. It handles basic input and reading files,
# as well as providing a usage string and unit tests.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="This is a template file. Please copy for individual problems for the 2019 Advent of Code.")

# Uncomment this lne for file input
# parser.add_argument("file", help="An intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	# Write main code here.
	return None


# Other functions can be defined here.
z

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
