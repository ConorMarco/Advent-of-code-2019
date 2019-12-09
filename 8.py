#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator


# Last one was hard, but this looks like a breeze.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 8 of Advent of Code.")

# Uncomment this lne for file input
parser.add_argument("file", help="A file with an image in Digital Sending Network format.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

def main():
	raw = get_input_file()[0].strip()
	chunk_size = IMAGE_WIDTH * IMAGE_HEIGHT
	layers = split_into_chunks(raw, chunk_size)

	# Part 1
	best_layer = min(layers, key=lambda s: s.count('0'))
	print_result(best_layer.count('1') * best_layer.count('2'), 1)

	# Part 2
	msg = ""
	for i in range(chunk_size):
		msg += highest_matching_layer(layers, lambda x: x[i] != '2')[i]
	if should_show_part(2):
		print("Part 2")
		pretty_print_rectangle(msg, IMAGE_WIDTH, IMAGE_HEIGHT)


def split_into_chunks(s, chunk_size):
	return [s[i : i+chunk_size] for i in range(0, len(s), chunk_size)]

def highest_matching_layer(layers, predicate):
	for layer in layers:
		if predicate(layer):
			return layer
	else:
		return layer[-1]

def pretty_print_rectangle(s, width, height):
	for line in split_into_chunks(s.replace('0', ' '), width):
		print(line)


#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_split_into_chunks(self):
		self.assertEqual(split_into_chunks("ABCDEFABCGHIABCJKL", 3), ["ABC", "DEF", "ABC", "GHI", "ABC", "JKL"])

	def test_transparent_layers(self):
		layers = split_into_chunks("0222112222120000", 4)
		msg = ""
		for i in range(4):
			msg += highest_matching_layer(layers, lambda x: x[i] != '2')[i]
		self.assertEqual(msg, "0110")


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
