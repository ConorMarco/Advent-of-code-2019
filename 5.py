#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# The intcode computer returns! I rewrote it with a dispatch table like I probably should have on day 2.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 5 o Advent of Code 2019")

# Uncomment this lne for file input
parser.add_argument("file", help="an intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	code = get_input_file_numbers()
	run_intcode(code)



# Other functions can be defined here.
def run_intcode(code):
	pointer = 0
	while pointer < len(code):
		instruction = code[pointer]
		op = instruction % 100
		num_parameters,func = dispatch_table[op]

		if pointer + num_parameters >= len(code):
			intcode_error("Not enough parameters for instruction at memory value " + str(pointer))

		# Get parameters with modes
		parameters = []
		instruction //= 100
		for i in range(1, num_parameters+1):
			mode = instruction % 10
			instruction //= 10

			val = code[pointer + i]
			parameters.append((val, mode))

		result = func(code, *parameters)
		if result == -1:
			# Halt program
			return code
		elif result != None:
			pointer = result
		else:
			pointer += 1 + num_parameters

	intcode_error("Ran out of instructions before halting")


def memory_get(code, addr):
	val, mode = addr
	if mode == 0:
		return code[val]
	elif mode == 1:
		return val
	else:
		intcode_error("Invalid read parameter mode")

def memory_set(code, addr, new_val):
	val, mode = addr
	if mode == 0:
		code[val] = new_val
	else:
		intcode_error("Invalid write parameter mode")

# If a function takes two inouts and has an otput, write it more easily with this
def intcode_standard_instr(code, a, b, out, f):
	result = f(memory_get(code, a), memory_get(code, b))
	memory_set(code, out, result)

def intcode_add(code, a, b, out):
	intcode_standard_instr(code, a, b, out, operator.add)

def intcode_mult(code, a, b, out):
	intcode_standard_instr(code, a, b, out, operator.mul)

def intcode_input(code, out):
	try:
		x = int(input("Intcode input: "))
	except ValueError:
		intcode_error("A non-integer was input")
	memory_set(code, out, x)

def intcode_ouput(code, x):
	print(memory_get(code, x))

def intcode_jump_true(code, nonzero, next_instr):
	if memory_get(code, nonzero) != 0:
		return memory_get(code, next_instr)

def intcode_jump_false(code, zero, next_instr):
	if memory_get(code, zero) == 0:
		return memory_get(code, next_instr)

def intcode_less_than(code, a, b, out):
	intcode_standard_instr(code, a, b, out, operator.lt)

def intcode_equals(code, a, b, out):
	intcode_standard_instr(code, a, b, out, operator.eq)

def intcode_halt(code):
	return -1

# Dispatch table contains the opcode, the number of parameters to the operation, and the function to perform.
# Functions should return -1 if the program should halt after their completion.
# Nonnegative returns signify the next value for the instruction pointer.
dispatch_table = {
	1: (3, intcode_add),
	2: (3, intcode_mult),
	3: (1, intcode_input),
	4: (1, intcode_ouput),
	5: (2, intcode_jump_true),
	6: (2, intcode_jump_false),
	7: (3, intcode_less_than),
	8: (3, intcode_equals),
	99: (0, intcode_halt),
}

def intcode_error(error):
	print(error)


#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_modes(self):
		self.assertEqual(run_intcode([1002,4,3,4,33]), [1002,4,3,4,99])
		self.assertEqual(run_intcode([1101,100,-1,4,0]), [1101,100,-1,4,99])


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
