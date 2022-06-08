#===========================================variable declaration===============================================================
pc_address = 0          # Address of the Program Counter
arthm_cnt = 0           # Count of number of Arithmetic instructions
logic_ins_cnt = 0       # Count of number of logical instructions
memory_ins_cnt = 0      # Count of number of memory instructions
contr_count = 0         # Count of number of branch instructions
immediate = 0           # immediate value from the instruction memory
flag = 0                # initial Flag
stalls = 0              # number of stalls
forward_stalls = 0      # number of stalls after forwarding
branch_penality = 0     # number of instructions having branch penality
rs = 0                  # address of register rs
rt = 0                  # address of register rt
rd = 0                  # address of register rd
dregister = []          # track of contents of register
instruction_memory_instructions = [] 
dynamic_instruction_memory = []  
branch_flg_cnt = {}
raw_hazards = {}  
branch_flg2 = {}  
memory= {}              # storing the memory contents
register = {}           # storing the register contents
current_instruction = '' 
for x in range(32):
    dregister.append(0)
    register[x] = 0

#=====================================initialisations=====================================================================================
Add = '000000'
AddI = '000001'
Sub = '000010'
SubI = '000011'
Mul = '000100'
MulI = '000101'
Or = '000110'
OrI = '000111'
And = '001000'
AndI = '001001'
Xor = '001010'
XorI = '001011'
LDW = '001100'
STW = '001101'
BZ = '001110'
BEQ = '001111'
JR = '010000'
Halt = '010001'


rtype = [Add, Sub, Mul, Or, And, Xor] 
itype = [AddI, SubI, MulI, OrI, AndI, XorI]
arithemetic_instructions = [Add, AddI, Sub, SubI, Mul, MulI] 
logical_instructions = [Or, OrI, And, AndI, Xor, XorI]  
mem = [LDW, STW]  
cont = [BZ, BEQ, JR] 
#==================================reading the image file =====================================================================================

file_op = [l.rstrip('\n') for l in open(r'C:\Users\19713\Desktop\final_proj_trace.txt')]


for i in file_op:
    instruction_memory_instructions.append(str(bin(int(i, 16)))[2:].zfill(32))


#============================display the results of the timing simulator with forwarding ====================================================

def print_results():
    global register, arthm_cnt, logic_ins_cnt, memory_ins_cnt, contr_count, dynamic_instruction_memory, forward_stalls, flag, dregister
    print('Instruction counts---------------------->')
    print('Total instructions: ', arthm_cnt + logic_ins_cnt + memory_ins_cnt + contr_count)
    print('arithemetic_instructions: ', arthm_cnt)
    print("logical_ instructions: ", logic_ins_cnt)
    print('memory_instructions : ', memory_ins_cnt)
    print('branch_ instructions: ', contr_count)
    print('_' * 100)
    print('_' * 100)
    print('Program counter: ', pc_address)
    print('Final registerister states---------------------->')
    for loop in range(32):
        if dregister[loop] == 1:
            print('R', loop, ':', 'changed')

    print('_' * 100)
    for ite, val in register.items():
        if dregister[ite] == 1:
            print('R', ite, ':', val)
    print('_' * 100)
    print('Final memory_instructions state---------------------->')
    for ite, val in memory.items():
        print('Address: ', ite, ', Contents: ', val)
    print('_' * 100)
    print('_' * 100)
    print('Stalls without forwarding: ', stalls)
    print("average cycle stall for hazards:", stalls / len(raw_hazards))
    print('Single stalls: ', list(raw_hazards.values()).count(-2))
    print('Double stalls: ', list(raw_hazards.values()).count(-1))
    print('No. of raw_hazards hazards: ', len(raw_hazards))
    print('_' * 100)
    print('branch_penalities because of branch_instructions: ', branch_penality)
    print('Number of branches leading to branch_penalities: ', len(branch_flg2))
    print('Average Branch penality: ', branch_penality / len(branch_flg2), 'cycles')
    print('_' * 100)
    print('_' * 100)
    print('Stalls with forwarding: ', forward_stalls)
    print('_' * 100)
    print('_' * 100)
    print('Total number of clock cycles (without forwarding): ', flag + 5 + stalls + branch_penality)
    print("Total number of clock cycles (with forwarding): ", flag + 5 + forward_stalls + branch_penality)
    print('_' * 100)
    print('_' * 100)
    print("Speedup acheive by forwarding: ", ((flag + 5 + stalls + branch_penality) / (flag + 5 + forward_stalls + branch_penality)))




def twos_comp(val, bits):
    '''

    :param val: input signed value in binary form
    :param bits: number of signed bits
    :return: twos complement of the binary number
    '''
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val



def immediate_twos_comp():
    '''

    :return: twos complement exclusively for immediate operand
    '''
    global current_instruction, immediate
    immediate = twos_comp(int(current_instruction[16:], 2), len(current_instruction[16:]))



def arithemetic_instruction():
    '''
    update the count of the arthemetic instruction and update the program counter value and destination registers
    :return:
    '''
    global register, immediate, current_instruction
    if current_instruction[0:6] == Add:  # ADD
        register[rd] = register[rs] + register[rt]
        dregister[rd]= 1 # turning tracking bit of the destination registerister high

        return
    elif current_instruction[0:6] == Sub:  # SUB
        register[rd] = register[rs] - register[rt]
        dregister[rd]= 1

        return
    elif current_instruction[0:6] == Mul:  # MUL
        register[rd] = register[rs] * register[rt]
        dregister[rd]=1

        return
    else:
        immediate_twos_comp()
        if current_instruction[0:6] == AddI:  # ADDI
            register[rt] = register[rs] + immediate
            dregister[rt]=1 # turning tracking bit of the destination registerister high

            return
        elif current_instruction[0:6] == SubI:  # SUBI
            register[rt] = register[rs] - immediate
            dregister[rt]= 1

            return
        elif current_instruction[0:6] == MulI:  # MULI
            register[rt] = register[rs] * immediate
            dregister[rt]=1

            return



def logical_instruction():
    '''
    update the count of the logical instruction and update the program counter value and destination registers
    :return: :
    '''
    global register, immediate, current_instruction
    if current_instruction[0:6] == Or:  # OR
        register[rd] = register[rs] | register[rt]
        dregister[rd]=1

        return
    elif current_instruction[0:6] == And:  # AND
        register[rd] = register[rs] & register[rt]
        dregister[rd]= 1

        return
    elif current_instruction[0:6] == Xor:  # XOR
        register[rd] = register[rs] ^ register[rt]
        dregister[rd] =1

        return
    else:
        immediate_twos_comp()
        if current_instruction[0:6] == OrI:  # ORI
            register[rt] = register[rs] | immediate
            dregister[rt]=1

            return
        elif current_instruction[0:6] == AndI:  # ANDI
            register[rt] = register[rs] & immediate
            dregister[rt]= 1

            return
        elif current_instruction[0:6] == XorI:  # XORI
            register[rt] = register[rs] ^ immediate
            dregister[rt]=1

            return



def memory_instruction():
    '''
    update the count of the memory instruction and update the program counter value and memory , destination registers
    :return:
    '''
    global register, immediate, current_instruction
    immediate_twos_comp()
    if current_instruction[0:6] == LDW:  # LDW
        register[rt] = twos_comp(int(instruction_memory_instructions[int((register[rs] + immediate) / 4)], 2), 32)
        dregister.insert[rt]= 1

        return
    elif current_instruction[0:6] == STW:  # STW
        instruction_memory_instructions[int((register[rs] + immediate) / 4)] = str(bin(register[rt]))[2:].zfill(32)
        memory[(register[rs] + immediate)] = register[rt]
        return


def branch_instruction():
    '''
    update the count of the branch instruction and update the program counter value and destination registers
    :return:
    '''
    global register, pc_address, current_instruction, branch_flg_cnt, flag
    immediate_twos_comp()
    branch_flg_cnt[flag] = 0
    if current_instruction[0:6] == BZ:  # BZ
        if register[rs] == 0:
            pc_address += (immediate * 4)
            branch_flg_cnt[flag] = 1
        else:
            pc_address =pc_address +4
            return
    elif current_instruction[0:6] == BEQ:  # BEQ
        if register[rs] == register[rt]:
            pc_address += (immediate * 4)
            branch_flg_cnt[flag] = 1
        else:
            pc_address =pc_address +4
            return
    elif current_instruction[0:6] == JR:  # JR
        pc_address = register[rs]
        branch_flg_cnt[flag] = 1


def dependencies():
    '''
    this function tracks all the dependency cases and updates the number of stalls and penalities
    :return:
    '''
    global flag, dynamic_instruction_memory, stalls, branch_penality, raw_hazards, forward_stalls
    if (dynamic_instruction_memory[flag][0:6] in rtype) or (dynamic_instruction_memory[flag][0:6] == STW) or (dynamic_instruction_memory[flag][0:6] == BEQ):
        if dynamic_instruction_memory[flag - 1][0:6] in rtype:
            if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][16:21]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 1][16:21]):
                if dynamic_instruction_memory[flag - 1][0:6] in mem:
                    forward_stalls += 1
                stalls += 2
                raw_hazards[flag] = -1
                return
        elif (dynamic_instruction_memory[flag - 1][0:6] in itype) or (dynamic_instruction_memory[flag - 1][0:6] == LDW):
            if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][11:16]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 1][11:16]):
                if dynamic_instruction_memory[flag - 1][0:6] in mem:
                    forward_stalls += 1
                stalls += 2
                raw_hazards[flag] = -1
                return
        if flag - 1 in raw_hazards.values():
            return
        elif dynamic_instruction_memory[flag - 2][0:6] in rtype:
            if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 2][16:21]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 2][16:21]):
                stalls += 1
                raw_hazards[flag] = -2
                return
        elif (dynamic_instruction_memory[flag - 2][0:6] in itype) or (dynamic_instruction_memory[flag - 2][0:6] == LDW):
            if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 2][11:16]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 2][11:16]):
                stalls += 1
                raw_hazards[flag] = -2
                return
    elif (dynamic_instruction_memory[flag][0:6] in itype) or (dynamic_instruction_memory[flag][0:6] == LDW) or (dynamic_instruction_memory[flag][0:6] == BZ) or (dynamic_instruction_memory[flag][0:6] == JR):
        if dynamic_instruction_memory[flag - 1][0:6] in rtype:
            if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][16:21]:
                if dynamic_instruction_memory[flag - 1][0:6] in mem:
                    forward_stalls += 1
                stalls += 2
                raw_hazards[flag] = -1
                return
        elif (dynamic_instruction_memory[flag - 1][0:6] in itype) or (dynamic_instruction_memory[flag - 1][0:6] == LDW):
            if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][11:16]:
                if dynamic_instruction_memory[flag - 1][0:6] in mem:
                    forward_stalls += 1
                stalls += 2
                raw_hazards[flag] = -1
                return
        if flag - 1 in raw_hazards.keys():
            return
        elif dynamic_instruction_memory[flag - 2][0:6] in rtype:
            if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 2][16:21]:
                stalls += 1
                raw_hazards[flag] = -2
                return
        elif (dynamic_instruction_memory[flag - 2][0:6] in itype) or (dynamic_instruction_memory[flag - 2][0:6] == LDW):
            if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 2][11:16]:
                stalls += 1
                raw_hazards[flag] = -2
                return

def hazard_cnt():
    '''
    this function tracks all the hazard cases and updates the number of stalls and penalities

    :return:
    '''
    global flag, dynamic_instruction_memory, stalls, branch_penality, raw_hazards, branch_flg2, branch_flg_cnt, forward_stalls
    if flag == 0:
        return
    elif flag == 1:
        if (dynamic_instruction_memory[flag][0:6] in rtype) or (dynamic_instruction_memory[flag][0:6] == STW) or (dynamic_instruction_memory[flag][0:6] == BEQ):
            if dynamic_instruction_memory[flag - 1][0:6] in rtype:
                if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][16:21]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 1][16:21]):
                    if dynamic_instruction_memory[flag - 1][0:6] in mem:
                        forward_stalls += 1
                    stalls += 2
                    raw_hazards[flag] = -1
                    return
                else:
                    return
            elif (dynamic_instruction_memory[flag - 1][0:6] in itype) or (dynamic_instruction_memory[flag - 1][0:6] == LDW):
                if (dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][11:16]) or (dynamic_instruction_memory[flag][11:16] == dynamic_instruction_memory[flag - 1][11:16]):
                    if dynamic_instruction_memory[flag - 1][0:6] in mem:
                        forward_stalls += 1
                    stalls += 2
                    raw_hazards[flag] = -1
                    return
                else:
                    return
        elif (dynamic_instruction_memory[flag][0:6] in itype) or (dynamic_instruction_memory[flag][0:6] == LDW) or (dynamic_instruction_memory[flag][0:6] == BZ) or (
                dynamic_instruction_memory[flag][0:6] == JR):
            if dynamic_instruction_memory[flag - 1][0:6] in rtype:
                if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][16:21]:
                    if dynamic_instruction_memory[flag - 1][0:6] in mem:
                        forward_stalls += 1
                    stalls += 2
                    raw_hazards[flag] = -1
                    return
                else:
                    return
            elif (dynamic_instruction_memory[flag - 1][0:6] in itype) or (dynamic_instruction_memory[flag - 1][0:6] == LDW):
                if dynamic_instruction_memory[flag][6:11] == dynamic_instruction_memory[flag - 1][11:16]:
                    if dynamic_instruction_memory[flag - 1][0:6] in mem:
                        forward_stalls += 1
                    stalls += 2
                    raw_hazards[flag] = -1
                    return
                else:
                    return
        else:
            return
    else:
        if (dynamic_instruction_memory[flag - 1][0:6] not in cont) and (dynamic_instruction_memory[flag - 2][0:6] not in cont):
            dependencies()
        elif (branch_flg_cnt[flag - 1] != 1) and (branch_flg_cnt[flag - 2] != 1):
            dependencies()
        elif branch_flg_cnt[flag - 1] == 1:
            branch_penality += 2
            branch_flg2[flag] = -1
        elif branch_flg_cnt[flag - 2] == 1:
            dependencies()
        else:
            return



while (1):

    current_instruction = instruction_memory_instructions[int(pc_address / 4)]
    # print(current_instruction)
    dynamic_instruction_memory.append(current_instruction)
    branch_flg_cnt[flag] = 0
    rs = int(current_instruction[6:11], 2)
    rt = int(current_instruction[11:16], 2)
    rd = int(current_instruction[16:21], 2)
    if current_instruction[0:6] == Halt:  # HALT
        contr_count =contr_count+1
        pc_address = pc_address+4
        break
    elif current_instruction[0:6] in arithemetic_instructions: 
        hazard_cnt()
        arthm_cnt =arthm_cnt +1 
        arithemetic_instruction()
        pc_address =pc_address +4

    elif current_instruction[0:6] in logical_instructions:  
        hazard_cnt()
        logic_ins_cnt =logic_ins_cnt +1  
        logical_instruction()
        pc_address =pc_address +4
    elif current_instruction[0:6] in mem:  
        hazard_cnt()
        memory_ins_cnt =memory_ins_cnt +1  
        memory_instruction()
        pc_address =pc_address +4
    elif current_instruction[0:6] in cont: 
        hazard_cnt()
        contr_count =contr_count +1 
        branch_instruction()
    flag += 1
print_results()
