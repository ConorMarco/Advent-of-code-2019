#!/usr/bin/python

import sys
import unittest


# Starting out easy, huh?

USAGE_MESSAGE = '''Problem 1a. Please give the name to a file with a list of masses, one per line.'''


#-------------------------------------------BEGIN SOLUTION CODE------------------------------------------------


def main():
	print(sum(map(fuel_from_mass, get_input_file_numbers())))


# Other functions can be defined here.
def fuel_from_mass(mass):
	return mass // 3 - 2


#--------------------------------------------END SOLUTION CODE-------------------------------------------------
#---------------------------------------------BEGIN TEST CODE--------------------------------------------------


class TestMethods(unittest.TestCase):
	# Test setup
	def setUp(self):
		return None


	# Define testing functions here.
	def test_fuel_from_mass(self):
		self.assertEqual(fuel_from_mass(12), 2)
		self.assertEqual(fuel_from_mass(14), 2)
		self.assertEqual(fuel_from_mass(1969), 654)
		self.assertEqual(fuel_from_mass(100756), 33583)


	# Test cleanup
	def tearDown(self):
		return None


#----------------------------------------------END TEST CODE---------------------------------------------------

# Input methods:

# Make sure at least one command line argument was given for the various input functions.
def get_first_argument():
	if len(sys.argv) < 2:
		print("An argument is required, but none was given.")
		print_usage
		exit()
	else:
		return sys.argv[1]

# Read a filename in from arguments and give the contents of the file as a list of lines
def get_input_file():
	filename = get_first_argument()
	try:
		file = open(filename, 'r')
		return file.readlines()
	except:
		print("There has been a file reading error with file " + filename + ":")
		exit()

def get_input_file_numbers():
	return map(int, get_input_file())

def get_input_string():
	return get_first_argument()

def get_input_int():
	return int(get_first_argument())



def print_usage():
	print("Usage: " + USAGE_MESSAGE)


if len(sys.argv) > 1 and sys.argv[1] == "-h":
	print_usage()
elif len(sys.argv) > 1 and sys.argv[1] == "-t":
	# Remove command line arguments for test run
	unittest.main(argv = [sys.argv[0]])
else:
	main()
