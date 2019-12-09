#!/usr/bin/python
import operator
import sys
import functools


# ----------------- IO Handlers -----------------------------------------------------------------

class TerminalIoHandler:
	def get_input(self):
		while True:
			try:
				x = int(input("Intcode input: "))
				return x
			except ValueError:
				print("A non-integer was input")

	def send_output(self, m):
		print("Intcode output: " + str(m))

	def error(self, e):
		print("Error running intcode: " + e)


class QueueIoHandler:
	def __init__(self, in_queue, out_queue):
		self.in_queue = in_queue
		self.out_queue = out_queue	

	def get_input(self):
		return self.in_queue.get()

	def send_output(self, m):
		self.out_queue.put(m)

	def error(self, e):
		print("Error running intcode: " + e)






# ---------------- Intcode Computer --------------------------------------------------------

class IntcodeComputer:
	def __init__(self, code, io_handler=TerminalIoHandler()):
		self.code = code
		self.io_handler = io_handler

	relative_base = 0
	pointer = 0

	# Other functions can be defined here.
	def run_intcode(self):
		self.pointer = 0
		while self.pointer < len(self.code):
			instruction = self.retrieve_at_pointer()
			op = instruction % 100
			num_parameters,func = self.dispatch_table[op]

			# Get parameters with modes
			parameters = []
			instruction //= 100
			for i in range(1, num_parameters+1):
				mode = instruction % 10
				instruction //= 10

				parameters.append((self.retrieve_at_pointer(), mode))

			if func(self, *parameters):
				# Halt program
				return self.code

		self.io_handler.error("Ran out of instructions before halting")

#----Memory-------------------------------------------------------------------------

	def retrieve_at_pointer(self):
		value = self.raw_memory_access(self.pointer)
		self.pointer += 1
		return value

	def raw_memory_access(self, addr, write=None):
		if addr >= len(self.code):
			self.code += [0] * (addr - len(self.code) + 1)

		if write:
			self.code[addr] = write
		else:
			return self.code[addr]


	def memory_get(self, addr):
		val, mode = addr
		if mode == 0:
			return self.raw_memory_access(val)
		elif mode == 1:
			return val
		elif mode == 2:
			return self.raw_memory_access(val + self.relative_base)
		else:
			self.io_handler.error("Invalid read parameter mode")

	def memory_set(self, addr, new_val):
		val, mode = addr
		if mode == 0:
			mem_location = val
		elif mode == 2:
			mem_location = val + self.relative_base
		else:
			self.io_handler.error("Invalid write parameter mode")
			return None
		return self.raw_memory_access(mem_location, new_val)

#----Operations-------------------------------------------------------------------------

	# If a function takes two inouts and one output, write it more easily with this
	def intcode_standard_instr(self, a, b, out, f):
		result = f(self.memory_get(a), self.memory_get(b))
		self.memory_set(out, result)

	def intcode_add(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.add)

	def intcode_mult(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.mul)

	def intcode_input(self, out):
		x = self.io_handler.get_input()
		self.memory_set(out, x)

	def intcode_ouput(self, x):
		self.io_handler.send_output(self.memory_get(x))

	def intcode_jump_true(self, nonzero, next_instr):
		if self.memory_get(nonzero) != 0:
			self.pointer = self.memory_get(next_instr)

	def intcode_jump_false(self, zero, next_instr):
		if self.memory_get(zero) == 0:
			self.pointer = self.memory_get(next_instr)

	def intcode_less_than(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.lt)

	def intcode_equals(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.eq)

	def intcode_increment_relative_base(self, a):
		self.relative_base += self.memory_get(a)

	def intcode_halt(self):
		return True

	# Dispatch table contains the opcode, the number of parameters to the operation, and the function to perform.
	# Functions should return True if the program should halt after their completion.
	dispatch_table = {
		1: (3, intcode_add),
		2: (3, intcode_mult),
		3: (1, intcode_input),
		4: (1, intcode_ouput),
		5: (2, intcode_jump_true),
		6: (2, intcode_jump_false),
		7: (3, intcode_less_than),
		8: (3, intcode_equals),
		9: (1, intcode_increment_relative_base),
		99: (0, intcode_halt),
	}



# Directly run an intcode program from the command line -------------------------------------------------------
def get_file_tokens(filename):
	file = open(filename, 'r')
	nested_tokens = list(map(lambda x: x.split(','),file.readlines()))
	return functools.reduce(operator.iconcat, nested_tokens, [])

if __name__ == "__main__":
	code = list(map(int, get_file_tokens(sys.argv[1])))
	comp = IntcodeComputer(code)
	comp.run_intcode()