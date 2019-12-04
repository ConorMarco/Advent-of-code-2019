#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# I liked this one. It was cute.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 4. Takes in two numbers and tests everything in the range between them.")


parser.add_argument("start", help="the start of the range to test", type=int)
parser.add_argument("end", help="the end of the range to test", type=int)


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	print_result(test_range(args.start, args.end, first_criterion), 1)
	print_result(test_range(args.start, args.end, second_criterion), 2)


def test_range(a, b, test):
	return len(list(filter(test, range(a, b+1))))


def first_criterion(n):
	return never_decreasing(n) and has_double(n)

def second_criterion(n):
	return has_lonely_double(n) and first_criterion(n)



def never_decreasing(n):
	while n >= 10:
		if n % 10 < (n % 100) // 10:
			return False
		n //= 10
	return True
	return False

def has_double(n):
	while n >= 10:
		if n % 10 == (n % 100) // 10:
			return True
		n //= 10
	return False


# Check if there is a double that is not a part of a larger sequence
def has_lonely_double(n):
	prev = None
	count = 0

	# Iterate through the digits of n from least to greatest, keeping track of how many we've seen in a row
	while n >= 1:
		if n % 10 == prev:
			count += 1
		else:
			# We've hit the end of a streak of the same number
			if count == 2:
				return True
			prev = n % 10
			count = 1

		# Move on to the next digit
		n //= 10
	return count == 2

#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_never_decreasing(self):
		self.assertTrue(never_decreasing(123478))
		self.assertTrue(never_decreasing(111177))
		self.assertFalse(never_decreasing(123460))

	def test_has_double(self):
		self.assertTrue(has_double(123345))
		self.assertTrue(has_double(111177))
		self.assertFalse(has_double(123460))

	def test_has_lonely_double(self):
		self.assertTrue(has_lonely_double(123345))
		self.assertTrue(has_lonely_double(111177))
		self.assertFalse(has_lonely_double(111178))


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
