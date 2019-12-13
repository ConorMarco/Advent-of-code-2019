#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator
import math


# This problem wasn't really fun enough to write tests for.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 10 of the 2019 Advent of Code.")

# Uncomment this lne for file input
parser.add_argument("file", help="A file of an asteroid map written with asteroids as #")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------

PART_2_INDEX = 199


def main():
	grid = convert_map_to_booleans(get_input_file())

	station = max(asteroids_list(grid), key=lambda a: num_asteroids_detectable(a, grid))
	print_result(num_asteroids_detectable(station, grid), 1)

	winner = create_asteroid_destroy_list(station, grid)[PART_2_INDEX]
	print_result(winner[0] * 100 + winner[1], 2)

	pretty_print(create_asteroid_destroy_list(station, grid), station, grid)

def pretty_print(order, station, grid):
	chars = [['    '] * len(grid[0]) for _ in range(len(grid))]

	for i, (x,y) in enumerate(order):
		chars[y][x] = str(i+1).ljust(4)
	a,b = station
	chars[b][a] = '0   '

	for line in chars:
		print(functools.reduce(operator.iconcat, line, ''))


def convert_map_to_booleans(m):
	m = list(map(lambda s: s.strip(), m))
	return list(map(lambda s: list(map(lambda c: c == '#', s)), m)) 


def asteroids_list(grid):
	results = []
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			if grid[y][x]:
				results.append((x,y))
	return results

def other_asteroids(origin, grid):
	results = asteroids_list(grid)
	if origin in results:
		results.remove(origin)
	return results


def num_asteroids_detectable(src, grid):
	count = 0
	for other in other_asteroids(src, grid):
		if can_see(src, other, grid):
			count += 1
	return count

def num_asteroids_between(a,b, x,y, grid):
	delta_x = x - a
	delta_y = y - b

	g = math.gcd(delta_x, delta_y)
	reduced_x, reduced_y = delta_x // g, delta_y // g

	count = 0
	for scalar in range(1, g):
		if grid[b + scalar * reduced_y][a + scalar * reduced_x]:
			count += 1
	return count

def can_see(src, dest, grid):
	return num_asteroids_between(*src, *dest, grid) == 0


def create_asteroid_destroy_list(station, grid):
	passes = [[] for i in range(max(len(grid), len(grid[0])))]

	for asteroid in other_asteroids(station, grid):
		passes[num_asteroids_between(*station, *asteroid, grid)].append(asteroid)

	for p in passes:
		p.sort(key=lambda x: aster_angle(station, x))

	# Concatenate list of lists
	return functools.reduce(operator.iconcat, passes, [])

def aster_angle(src, dest):
	a,b = src
	x,y = dest
	return math.atan2(x-a, b-y)

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
