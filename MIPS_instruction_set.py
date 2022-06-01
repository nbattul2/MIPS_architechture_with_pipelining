import functional_simulator
fs=functional_simulator.values_set()

# return positive value as is


class instruction_set:
    def __init__(self):
        self.arithematic_instruction=0
        self.logical_instruction=0
        self.memory_var=0
        self.branch = 0
        self.rs_len= 5
        self.rt_len= 5
        self.rd_len= 5
        self.immediate_len=16
    def twos_comp(self,val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)  # compute negative value
        return val

    def ADD(self,rs,rt):

        self.arithematic_instruction = self.arithematic_instruction+1

        result = rs + rt
        return result

    def SUB(self,rs,rt):

        self.arithematic_instruction = self.arithematic_instruction + 1

        result = rs - rt
        return result

    def MUL(self,rs,rt):

        self.arithematic_instruction = self.arithematic_instruction + 1

        result = rs* rt
        return result

    def OR(self,rs,rt):

        self.logical_instruction = self.logical_instruction+1

        result = rs | rt
        return result

    def AND(self,rs,rt):

        self.logical_instruction = self.logical_instruction + 1

        result = rs & rt
        return result

    def XOR(self,rs,rt):

        self.logical_instruction = self.logical_instruction + 1

        result = rs ^ rt

        return result


    def ADDI(self,rs,immediate):

        self.arithematic_instruction = self.arithematic_instruction + 1

        result = rs + immediate

        return result

    def SUBI(self,rs,immediate):

        self.arithematic_instruction = self.arithematic_instruction + 1

        result = rs - immediate

        return result


    def MULI(self,rs,immediate):

        self.arithematic_instruction = self.arithematic_instruction + 1

        result = rs* immediate

        return result

    def ORI(self,rs,immediate):

        self.logical_instruction = self.logical_instruction + 1

        result = rs | immediate

        return result

    def ANDI(self,rs,immediate):

        self.logical_instruction = self.logical_instruction + 1

        result = rs & immediate

        return result

    def XORI(self,rs,immediate):

        self.logical_instruction = self.logical_instruction + 1

        result = rs ^ immediate

        return result

    def LDW(self):

        self.memory_var = self.memory_var +1





    def STW(self):

        self.memory_var = self.memory_var + 1


    def BEQ(self,rs,rt,immediate,curr_pc):
        self.branch = self.branch + 1

        if rs == rt:
            fs.update_pc(curr_pc+(immediate*4))  # need to update pc value


    def BZ(self,rs,immediate,curr_pc):

        self.branch = self.branch + 1
        imm = self.twos_comp(immediate, self.immediate_len)
        if rs == 0:
            fs.update_pc(curr_pc+(imm*4))


    def JR(self,rs):
        self.branch = self.branch + 1

        #result = (rs /0b100) +1
        fs.update_pc(rs)  # jump to new pc  # branching should happen in execute stage itself.


    def ins_count(self):
        total_ins= self.arithematic_instruction+self.logical_instruction+self.branch+self.memory_var
        arth_ins=self.arithematic_instruction
        log_ins =self.logical_instruction
        mem_ins = self.memory_var
        bnch_ins = self.branch

        result = {"total_ins":total_ins,"arth_ins":arth_ins,"log_ins":log_ins,
                  "mem_ins":mem_ins,"bnch_ins":bnch_ins}
        return result

