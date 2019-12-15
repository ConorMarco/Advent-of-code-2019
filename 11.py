#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator

from intcode import *
from collections import defaultdict


# Intcode returns yet again for a turtle program.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 11 of the 2019 Advent of Code.")

# Uncomment this lne for file input
parser.add_argument("file", help="An intcode file consisting of integers separated by commas.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	code = get_input_file_numbers()
	painter = Painter(code)
	painter.run()
	print_result(len(painter.grid), 1)

	if should_show_part(2):
		grid = defaultdict(lambda: 0)
		grid[(0,0)] = 1
		painter = Painter(code, grid)
		painter.run()

		print("Part 2:")
		painter.print_grid()


# This can function as an I/O handler for the intcode computer
class Painter:
	def __init__(self, code, grid=defaultdict(lambda: 0)):
		self.grid = grid

		self.code = code.copy()
		self.comp = IntcodeComputer(self.code, self)

		self.position = (0, 0)
		self.direction = (0, 1)
		self.move_flag = False


	def grid_access(self, pos, write=None):
		if write == None:
			return self.grid[pos]
		else:
			self.grid[pos] = write

	def print_grid(self):
		# Min values make the offsets so that we can have a rectangle with origin 0,0
		offset_x = -min(self.grid.keys(), key=lambda x:x[0])[0]
		offset_y = -min(self.grid.keys(), key=lambda x:x[1])[1]

		max_x = max(self.grid.keys(), key=lambda x:x[0])[0]
		max_y = max(self.grid.keys(), key=lambda x:x[1])[1]

		width = offset_x + max_x + 1
		height = offset_y + max_y + 1

		visual = [[' '] * width for _ in range(height)]

		for ((x,y), color) in self.grid.items():
			if color == 1:
				visual[-(y + offset_y) - 1][x + offset_x] = '#'

		for line in visual:
			print("".join(line))


	def get_input(self):
		return self.grid_access(self.position)


	def send_output(self, m):
		if self.move_flag:
			self.move(m)
		else:
			self.paint_panel(m)
		# Alternate between paint and move instructions
		self.move_flag = not self.move_flag


	def paint_panel(self, color):
		self.grid_access(self.position, color)


	def move(self, m):
		# Turn
		if m == 0:
			self.turn_left()
		elif m == 1:
			self.turn_right()

		# Move forward
		self.position = pt_add(self.position, self.direction)

	def turn_left(self):
		x,y = self.direction
		self.direction = -y,x

	def turn_right(self):
		x,y = self.direction
		self.direction = y,-x


	def error(self, e):
		print("Error running intcode: " + e)


	def run(self):
		self.comp.run_intcode()



def pt_add(a, b):
	return (a[0] + b[0], a[1] + b[1])


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
