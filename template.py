#!/usr/bin/python

import sys
import unittest


# This is a template file for Advent of Code 2019. It handles basic input and reading files,
# as well as providing a usage string and unit tests.

USAGE_MESSAGE = '''This is a template file. Please copy for individual problems for the 2019 Advent of Code.'''


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	# Write main code here.
	return None


# Other functions can be defined here.


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

# Input methods:

# Read a filename in from arguments and give the contents of the file as a list of lines
def get_input_file():
	filename = sys.argv[1]


	# else:
	# 	print("There has been a file reading error with file " + filename + ":")
	# 	print(error)

def get_input_string():
	return sys.argv[1]

def get_input_int():
	return int(sys.argv[1])


def print_usage():
	print(USAGE_MESSAGE)


if len(sys.argv) == 1 or sys.argv[1] == "-h":
	print_usage()
elif sys.argv[1] == "-t":
	# Remove command line arguments for test run
	unittest.main(argv = [sys.argv[0]])
else:
	main()
