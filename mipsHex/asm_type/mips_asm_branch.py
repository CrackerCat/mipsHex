# mips_asm_branch.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from mips_asm import *

import idc

# instruction(conditional branch)
class MIPS_Asm_Branch(MIPS_Asm):
	def __init__(self, addr, dispatch, o_reg, o_func):
		super(MIPS_Asm_Branch, self).__init__(addr)

		self.next_addr = idc.NextHead(addr)
		self.next_result, n_addr = dispatch(self.next_addr, o_reg, o_func)
		# check_assert("[-] address({0}), dispatch error in branch".format(hex(self.next_addr)), result is None)
		check_assert("[-] address({0}), dispatch error in branch".format(hex(self.next_addr)), n_addr is None)

	# branch instruction
	def do_b(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != b".format(hex(self.addr), self.ins), self.ins == 'b')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'goto ' + self.opr1.value + ';'

		return line, self.next_addr

	# branch equal zero instruction
	def do_beqz(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != beqz".format(hex(self.addr), self.ins), self.ins == 'beqz')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += '!' + o_reg.get_register(self.opr1.value)
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr

	# branch not equal zero instruction
	def do_bnez(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != bnez".format(hex(self.addr), self.ins), self.ins == 'bnez')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value)
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr
	
	# branch equal instruction
	def do_beq(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != beq".format(hex(self.addr), self.ins), self.ins == 'beq')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' == ' + o_reg.get_register(self.opr2.value)
		line += ') ' + self.opr3.value + ';'

		return line, self.next_addr

	# branch not equal instruction
	def do_bne(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != bne".format(hex(self.addr), self.ins), self.ins == 'bne')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' != ' + o_reg.get_register(self.opr2.value)
		line += ') ' + self.opr3.value + ';'

		return line, self.next_addr

	# branch less than zero instruction
	def do_bltz(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != bltz".format(hex(self.addr), self.ins), self.ins == 'bltz')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' < 0'
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr

	# branch on greater than zero instruction
	def do_bgtz(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != bgtz".format(hex(self.addr), self.ins), self.ins == 'bgtz')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' > 0'
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr

	# branch on greater than or equal to zero instruction
	def do_bgez(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != bgez".format(hex(self.addr), self.ins), self.ins == 'bgez')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' >= 0'
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr

	# branch on less than or equal to zero instruction
	def do_blez(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != blez".format(hex(self.addr), self.ins), self.ins == 'blez')

		line = ''
		if self.next_result is not None:
			line = self.next_result
			line += '\n    '
		line += 'if('
		line += o_reg.get_register(self.opr1.value) + ' <= 0'
		line += ') ' + self.opr2.value + ';'

		return line, self.next_addr
