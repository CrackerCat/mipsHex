# mips_asm_arithmetic.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from mips_asm import *

# instruction(arthmetic operation)
class MIPS_Asm_Arithmetic(MIPS_Asm):
	def __init__(self, addr):
		super(MIPS_Asm_Arithmetic, self).__init__(addr)

	# addiu instruction
	def do_addiu(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != addiu".format(hex(self.addr), self.ins), self.ins == 'addiu')

		if self.get_operand_count() == 3:
			if self.opr2.type == ASM_TYPE['Gen_Reg']:
				if o_reg.get_register(self.opr2.value) == '$sp' and self.opr3.feature == OPND_FEATURE['Imm_Imm']:
					# addiu opr1, sp, 0x50_var
					new_opr = Operand(ASM_TYPE['Base_Idx_Disp'], self.opr3.value + '(' + o_reg.get_register(self.opr2.value) + ')')
					o_reg.set_register(self.opr1.value, new_opr.convert(o_reg))
				else:
					# addit opr1, v0, opr3
					reg_val = o_reg.get_register(self.opr2.value)
					cvt_opr3 = self.opr3.convert(o_reg)
					if idc.LocByName(reg_val) != 0xffffffff:
						o_reg.set_register(self.opr1.value, hex(idc.LocByName(reg_val) + int(cvt_opr3, 16)))
					else:
						o_reg.set_register(self.opr1.value, '(' + reg_val + ' + ' + cvt_opr3 + ')')

				comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr2.value, opr3=self.opr3.value, operation='+')
			else:
				error("[-] current({0}), Not defined addiu operand2 type".format(hex(self.addr)))

		elif self.get_operand_count() == 2:
			if self.opr2.type == ASM_TYPE['Gen_Reg']:
				# addiu opr1, v0
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' + ' + o_reg.get_register(self.opr2.value) + ')')

			elif self.opr2.type == ASM_TYPE['Imm']:
				if self.opr2.feature == OPND_FEATURE['Addr_Imm']:
					new_opr = Operand(ASM_TYPE['Base_Idx_Disp'], self.opr2.value + '(' + self.opr1.value + ')')
					cvt_opr = new_opr.convert(o_reg)
					if asmutils.have_string(cvt_opr):
						c_string = asmutils.get_string(cvt_opr)
						o_reg.set_register(self.opr1.value, c_string)
					else:
						o_reg.set_register(self.opr1.value, cvt_opr)
				elif o_reg.get_register(self.opr1.value) == '$sp':
					# for skip prologue
					# need to parse a opnd_feature's reg for line 20
					pass
				else:
					# addiu v0, 1
					o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' + ' + self.opr2.value + ')')

			else:
				error("[-] current({0}), Not defined addiu operand type".format(hex(self.addr)))

			comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr1.value, opr3=self.opr2.value, operation='+')
		else:
			error("[-] current({0}), Not defined addiu".format(hex(self.addr)))			

		return comment, None

	# addu instruction
	def do_addu(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != addu".format(hex(self.addr), self.ins), self.ins == 'addu')

		if self.get_operand_count() == 3:
			if self.opr3.type == ASM_TYPE['Gen_Reg']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr2.value) + ' + ' + o_reg.get_register(self.opr3.value) + ')')

			elif self.opr3.type == ASM_TYPE['Imm']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr2.value) + ' + ' + self.opr3.value + ')')

			else:
				error("[-] address({0}), Not defined addu opr3 type({1})".format(hex(self.addr), self.opr3.type))

			comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr2.value, opr3=self.opr3.value, operation='+')

		elif self.get_operand_count() == 2:
			if self.opr2.type == ASM_TYPE['Gen_Reg']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' + ' + o_reg.get_register(self.opr2.value) + ')')

			elif self.opr2.type == ASM_TYPE['Imm']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' + ' + self.opr2.value + ')')

			else:
				error("[-] address({0}), Not defined addu opr2 type({1})".format(hex(self.addr), self.opr2.type))

			comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr1.value, opr3=self.opr2.value, operation='+')

		else:
			error("[-] current({0}), Not defined addu".format(hex(self.addr)))

		return comment, None

	# subu instruction
	def do_subu(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != subu".format(hex(self.addr), self.ins), self.ins == 'subu')

		if self.get_operand_count() == 3:
			if self.opr3.type == ASM_TYPE['Gen_Reg']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr2.value) + ' - ' + o_reg.get_register(self.opr3.value) + ')')

			elif self.opr3.type == ASM_TYPE['Imm']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr2.value) + ' - ' + self.opr3.value + ')')

			else:
				error("[-] address({0}), Not defined subu opr3 type({1})".format(hex(self.addr), self.opr3.type))

			comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr2.value, opr3=self.opr3.value, operation='-')

		elif self.get_operand_count() == 2:
			if self.opr2.type == ASM_TYPE['Gen_Reg']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' - ' + o_reg.get_register(self.opr2.value) + ')')

			elif self.opr2.type == ASM_TYPE['Imm']:
				o_reg.set_register(self.opr1.value, '(' + o_reg.get_register(self.opr1.value) + ' - ' + self.opr2.value + ')')

			else:
				error("[-] address({0}), Not defined subu opr2 type({1})".format(hex(self.addr), self.opr2.type))

			comment = o_func.get_comment(opr1=self.opr1.value, opr2=self.opr1.value, opr3=self.opr2.value, operation='-')

		else:
			error("[-] current({0}), Not defined subu".format(hex(self.addr)))

		return comment, None

	# multiply instruction
	def do_mult(self, o_reg, o_func):
		check_assert("[-] Check ins, current({0}) : {1} != mult".format(hex(self.addr), self.ins), self.ins == 'mult')
		check_assert("[-] Check operand count, current({0}) : {1}".format(hex(self.addr), self.get_operand_count()), self.get_operand_count() == 2)

		o_reg.set_register('$hi', '(' + self.opr1.value + ' * ' + self.opr2.value + ')' + ' / 0xFFFFFFFF')
		o_reg.set_register('$lo', '(' + self.opr1.value + ' * ' + self.opr2.value + ')' + ' %% 0xFFFFFFFF')

		comment = o_func.get_comment(opr1='$hi, $lo', opr2=self.opr1.value, opr3=self.opr2.value, operation='*')

		return comment, None
