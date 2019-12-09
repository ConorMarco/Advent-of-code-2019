#!/usr/bin/python
import operator

class IntcodeComputer:
	def __init__(self, code, io_handler):
		self.code = code
		self.io_handler = io_handler

	# Other functions can be defined here.
	def run_intcode(self):
		pointer = 0
		while pointer < len(self.code):
			instruction = self.code[pointer]
			op = instruction % 100
			num_parameters,func = self.dispatch_table[op]

			if pointer + num_parameters >= len(self.code):
				intcode_error("Not enough parameters for instruction at memory value " + str(pointer))

			# Get parameters with modes
			parameters = []
			instruction //= 100
			for i in range(1, num_parameters+1):
				mode = instruction % 10
				instruction //= 10

				val = self.code[pointer + i]
				parameters.append((val, mode))

			result = func(self, *parameters)
			if result == -1:
				# Halt program
				return self.code
			elif result != None:
				pointer = result
			else:
				pointer += 1 + num_parameters

		intcode_error("Ran out of instructions before halting")


	def memory_get(self, addr):
		val, mode = addr
		if mode == 0:
			return self.code[val]
		elif mode == 1:
			return val
		else:
			intcode_error("Invalid read parameter mode")

	def memory_set(self, addr, new_val):
		val, mode = addr
		if mode == 0:
			self.code[val] = new_val
		else:
			intcode_error("Invalid write parameter mode")

	# If a function takes two inouts and has an otput, write it more easily with this
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
			return self.memory_get(next_instr)

	def intcode_jump_false(self, zero, next_instr):
		if self.memory_get(self, zero) == 0:
			return self.memory_get(next_instr)

	def intcode_less_than(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.lt)

	def intcode_equals(self, a, b, out):
		self.intcode_standard_instr(a, b, out, operator.eq)

	def intcode_halt(self):
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

	def intcode_error(self):
		self.io_handler.error(error)





class TerminalIoHandler:
	def get_input(self):
		while True:
			try:
				x = int(input("Intcode input: "))
				return x
			except ValueError:
				print("A non-integer was input")

	def send_ouput(self, m):
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
