#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# Could've used a proper tree class but it was kinda fun to try to make it work with dicts instead,
# and it continues the tradition of not using problem-specific indepenedent libraries.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 6 of Advent of Code")

# Uncomment this lne for file input
parser.add_argument("file", help="a file containing one orbit per line, where an orbit is of the form A)B meaning B orbits A")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------

ROOT_ID = "COM"
PLAYER_ID = "YOU"
SANTA_ID = "SAN"


def main():
	orbit_lists = tokenize_input_file_by_line(')')

	orbit_tree = make_orbit_tree(orbit_lists)
	orbital_depths = make_orbital_depths(orbit_tree)

	print_result(get_total_orbits(orbital_depths), 1)
	print_result(orbital_transfers_to_match_orbit(orbit_tree, PLAYER_ID, SANTA_ID, orbital_depths), 2)


# Takes in a list of two-element lists, each containing a larger object and a satellite
# Returns a tree stored as a dict, with children as keys and parents as values
def make_orbit_tree(orbits):
	orbit_tree = {}
	for item in orbits:
		orbit_tree[item[1]] = item[0]
	return orbit_tree


def make_orbital_depths(orbit_tree):
	orbital_objects = set(orbit_tree.keys()).union(set(orbit_tree.values()))

	orbital_depths = {ROOT_ID: 0}
	for obj in orbital_objects:
		get_orbital_depth(obj, orbital_depths, orbit_tree)

	return orbital_depths

def get_orbital_depth(obj, orbital_depths, orbit_tree):
	if obj not in orbital_depths:
		orbital_depths[obj] = get_orbital_depth(orbit_tree[obj], orbital_depths, orbit_tree) + 1
	return orbital_depths[obj]


def get_total_orbits(orbital_depths):
	return sum(orbital_depths.values())


# Note that this is not the number of transfers from orbit a to b, but from parent a to parent b
# (as if a was moving orbits to match b's orbit)
def orbital_transfers_to_match_orbit(orbit_tree, a, b, orbital_depths=None):
	if orbital_depths == None:
		orbital_depths = make_orbital_depths(orbit_tree)

	common_ancestor = get_common_ancestor(orbit_tree, a, b, orbital_depths)

	# (orbital_depths[a] - orbital_depths[common_ancestor] - 1) + (orbital_depths[b] - orbital_depths[common_ancestor] - 1)
	return orbital_depths[a] + orbital_depths[b] - 2*orbital_depths[common_ancestor] - 2


def parent(orbit_tree, child):
	return orbit_tree[child]

def get_common_ancestor(orbit_tree, a, b, orbital_depths):
	# Get a and b to the same orbital depth level
	while orbital_depths[a] > orbital_depths[b]:
		a = parent(orbit_tree, a)
	while orbital_depths[b] > orbital_depths[a]:
		b = parent(orbit_tree, b)

	# Now just traverse up the tree from both targets simultaneously until we hit a common root
	while a != b:
		a = parent(orbit_tree, a)
		b = parent(orbit_tree, b)
	
	return a


#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_total_orbit_count(self):
		raw_test_data = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''

		test_data = list(map(lambda x: x.strip().split(')'), raw_test_data.split("\n")))
		tree = make_orbit_tree(test_data)
		depths = make_orbital_depths(tree)
		self.assertEqual(get_total_orbits(depths), 42)

	def test_orbital_transfers_count(self):
		raw_test_data = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''
		test_data = list(map(lambda x: x.strip().split(')'), raw_test_data.split("\n")))
		tree = make_orbit_tree(test_data)
		self.assertEqual(orbital_transfers_to_match_orbit(tree, "YOU", "SAN"), 4)


	# Test cleanup
	def tearDown(self):
		return None


#----------------------------------------------END TEST CODE---------------------------------------------------


# Read a filename in from arguments and give the contents of the file as a list of lines
def get_input_file():
	filename = args.file
	try:
		file = open(filename, 'r')
		return list(map(lambda x: x.strip(), file.readlines()))
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
