#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# Apparently the two problems each day are related, so I'm switching to just having one file.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Advent of Code day 2.")
parser.add_argument("file", help="An intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------

PART_1_INPUT = (12,2)
PART_2_DESIRED_OUTPUT = 19690720

def main():
	original_code = get_input_file_numbers()

	# Part 1
	a, b = PART_1_INPUT
	print_result(run_updated_intcode(original_code, a, b), 1)

	# Part 2
	for i in range(100):
		for j in range(100):
			if run_updated_intcode(original_code, i, j) == PART_2_DESIRED_OUTPUT:
				print_result(i*100+j, 2)
				break

# Other functions can be defined here.
def run_intcode(code):
	pointer = 0

	while pointer + 4 <= len(code):
		op = code[pointer]
		src1_addr = code[pointer + 1]
		src2_addr = code[pointer + 2]
		dest_addr = code[pointer + 3]

		src1 = code[src1_addr]
		src2 = code[src2_addr]


		if op == 1:
			result = src1 + src2
		elif op == 2:
			result = src1 * src2
		else:
			break

		code[dest_addr] = result
		pointer += 4

	return code

def run_updated_intcode(original_code, a, b):
	code = original_code.copy()
	code[1] = a
	code[2] = b
	return run_intcode(code)[0]

#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_run_intcode(self):
		self.assertEqual(run_intcode([1,0,0,0,99]), [2,0,0,0,99])
		self.assertEqual(run_intcode([2,3,0,3,99]), [2,3,0,6,99])
		self.assertEqual(run_intcode([2,4,4,5,99,0]), [2,4,4,5,99,9801])
		self.assertEqual(run_intcode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])


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

def get_input_file_numbers(delimeter=','):
	list_of_lists = list(map(lambda x: x.split(delimeter), get_input_file()))
	return list(map(int, functools.reduce(operator.iconcat, list_of_lists, [])))

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
