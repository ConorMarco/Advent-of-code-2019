#!/usr/bin/python

import sys
import unittest
import argparse
import functools
import itertools
import operator
import math


# Day 3. Starting to get slightly more challenging now. Enjoying the Jingle Jam today and occasionally coding.
# Not my most elegant solution, but then again, not the most elegant problem either.

#------------------------------------------------ARGUMENTS-----------------------------------------------------

parser = argparse.ArgumentParser(description="Day 3 of Advent of Code 2019")

# Uncomment this lne for file input
parser.add_argument("file", help="a file containing two lines of comma-separated wire segment descriptions.")


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	codes_list = tokenize_input_file_by_line()
	segments1 = convert_codes_to_segments(codes_list[0])
	segments2 = convert_codes_to_segments(codes_list[1])

	print_result(find_closest_intersection(segments1, segments2), 1)

	print_result(find_closest_intersection_by_wire_length(segments1, segments2), 2)


def find_closest_intersection(segments1, segments2):
	intersections = []
	for s1, s2 in itertools.product(segments1, segments2):
		intersections += simple_segment_intersections(s1, s2)
	return min(map(manhattan, intersections))

def find_closest_intersection_by_wire_length(segments1, segments2):
	best_score = math.inf
	base_score_1 = 0
	base_score_2 = 0

	for s1 in segments1:
		for s2 in segments2:
			if base_score_1 + base_score_2 < best_score:
				intersections = simple_segment_intersections(s1, s2)
				if intersections:
					score1 = base_score_1 + point_distance(intersections[0], s1[0]) + 1 + base_score_2 + point_distance(intersections[0], s2[0]) + 1
					score2 = base_score_1 + point_distance(intersections[-1], s1[0]) + 1 + base_score_2 + point_distance(intersections[-1], s2[0]) + 1
					best_score = min(score1, score2, best_score)
			else:
				break

			base_score_2 += segment_length(s2)

		base_score_2 = 0
		base_score_1 += segment_length(s1)

	return best_score


# Processing input

def convert_codes_to_segments(codes):
	segments = []
	starting_point = (0,0)

	for code in codes:
		segment = make_one_segment(starting_point, code)
		segments.append(segment)
		_, starting_point = segment

	return segments

def make_one_segment(starting_point, next_code):
	direction = get_dir_from_char(next_code[0])
	length = int(next_code[1:])

	close_endpoint = point_add(starting_point, direction)
	far_endpoint = point_add(starting_point, point_scale(direction, length))
	return close_endpoint,far_endpoint

# Other functions can be defined here.
def get_dir_from_char(c):
	if c == 'U':
		return (0,1)
	elif c == 'D':
		return (0,-1)
	elif c == 'R':
		return (1,0)
	elif c == 'L':
		return (-1,0)
	else:
		# error
		print(c + " is not a valid direction!")


# Geometry section

# Checks for lattice intersections of horizontal and vertical segments
def simple_segment_intersections(segment1, segment2):
	(x1,y1),(x2,y2) = segment1
	(a1,b1),(a2,b2) = segment2

	if x1 > x2:
		x1,x2 = x2,x1
	if y1 > y2:
		y1,y2 = y2,y1
	if a1 > a2:
		a1,a2 = a2,a1
	if b1 > b2:
		b1,b2 = b2,b1

	return segment_intersections_by_coords(x1, y1, x2, y2, a1, b1, a2, b2)

# First 4 coords are for first segment. z1 <= z2 for all variables z
def segment_intersections_by_coords(x1, y1, x2, y2, a1, b1, a2, b2):
	# Both horizontal
	if y1 == y2 and b1 == b2:
		if y1 == b1:
			[(x, y1) for x in range(max(x1, a1), min(x2, a2) + 1)]
		else:
			return []
	# Both vertical
	if x1 == x2 and a1 == a2:
		if x1 == a1:
			[(x1, y) for y in range(max(y1, b1), min(y2, b2) + 1)]
		else:
			return []

	# Perpendicular
	if a1 <= x1 <= a2:
		x_coord = x1
	elif x1 <= a1 <= x2:
		x_coord = a1
	else:
		return []

	if b1 <= y1 <= b2:
		y_coord = y1
	elif y1 <= b1 <= y2:
		y_coord = b1
	else:
		return []

	# That was a mess, but no easy way around it
	return [(x_coord, y_coord)]


# Point utility functions

def point_add(p1, p2):
	x1,y1 = p1
	x2,y2 = p2
	return (x1 + x2, y1 + y2)

def point_scale(p1, s):
	x1,y1 = p1
	return (s*x1, s*y1)

def manhattan(p1):
	x1,y1 = p1
	return abs(x1) + abs(y1)

def point_distance(p1, p2):
	return manhattan(point_add(p1, point_scale(p2, -1)))

def segment_length(s):
	return point_distance(*s) + 1

#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# segment_length relies on all the other point functions, so it's a good indicator that everything is working properly.
	def test_point_functions(self):
		self.assertEqual(segment_length(((2, 28), (2, -100))), 129)

	def test_closest_intersection(self):
		left = convert_codes_to_segments("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','))
		right = convert_codes_to_segments("U62,R66,U55,R34,D71,R55,D58,R83".split(','))
		self.assertEqual(find_closest_intersection(left, right), 159)

		left = convert_codes_to_segments("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','))
		right = convert_codes_to_segments("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(','))
		self.assertEqual(find_closest_intersection(left, right), 135)

	def test_closest_intersection_length(self):
		left = convert_codes_to_segments("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','))
		right = convert_codes_to_segments("U62,R66,U55,R34,D71,R55,D58,R83".split(','))
		self.assertEqual(find_closest_intersection_by_wire_length(left, right), 610)

		left = convert_codes_to_segments("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','))
		right = convert_codes_to_segments("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(','))
		self.assertEqual(find_closest_intersection_by_wire_length(left, right), 410)


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
