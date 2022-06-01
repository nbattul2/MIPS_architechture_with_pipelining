import Functional_simulator
import MIPS_instruction_set1 as ms
import threading
instr_set=ms.instruction_set()
fs=Functional_simulator.values_set()
clock =0
f = open(r"C:\Users\19713\Documents\comparc_project\sample_memory_image_1.txt")
instruction_memory=[]
a=f.readlines()
for i in range(len(a)):
    instruction_memory.append(a[i][0:8])
debug = 0
pipelining_array=['0',[],[],[],[],[]]
my_clock=4
rd=0
rt=0
rs=0
stall=0
dreg=[]

# ==============================instruction types declaration====================================================================
rtype = {"ADD": "000000", "SUB": "000010", "MUL": "000100", "OR": "000100", "AND": "001000", "XOR": "001010"}
itype = {"ADDI": "000001", "SUBI": "000011", "MULI": "000101", "ORI": "000111", "ANDI": "001001",
              "XORI": "001011","BZ": "001110", "BEQ": "001111", "JR": "010000"}
itype_mem = {"LDW": "001100", "STW": "001101", "HALT": "010001"}

modified_registers=[]
modified_memory=[]
pc_address=0
# ==============================Register and memory declaration ===================================================================
register = {0: 0 , 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                         9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                         14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0,
                         22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0,
                         29: 0, 30: 0, 31: 0}
memory = {}

for x in range(32):
    dreg.append(0)
#======================================================================================================================


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def fetch():
    global pipelining_array
    while(1):
        if pipelining_array[0] == '0':
            global pc_address
            pc_address = fs.get_pc()
            print(pc_address)
            hex_instruction=0
            bin_instruction=0
            try:
                hex_instruction = instruction_memory[int(pc_address/4)]
                bin_instruction =bin(int(hex_instruction, 16))[2:].zfill(32)  # bad way of coding change
                pipelining_array[0]=str(bin_instruction)
            except Exception as e :
                print("fetch completed ")
                print(e)
                exit()
            if debug:
                print("PC Address :{}".format(pc_address))
                #print("Hex instruction{}".format(hex_instruction))
                #print("Bin instruction{}".format(bin_instruction))
                print("Fetch ",pipelining_array)

def decode():
    global pipelining_array,rd,rs,rt
    while(1):
        if pipelining_array[0]!='0' and len(pipelining_array[1])==0:
            global rd,rt,rs,immediate
            opcode = pipelining_array[0]
            opcode_1 = opcode[0:6]
            execute_var=[]
            if opcode_1 in [j for j in rtype.values()]:
                rd = opcode[16:21]
                rt = opcode[11:16]
                rs = opcode[6:11]
                for key, value in rtype.items():
                    if opcode_1 == value:
                        execute_var = ["rtype", key, rd, rs, rt]
                if debug:
                    print("The instruction is Rtype")


            elif opcode_1 in [j for j in itype.values()]:
                immediate = opcode[16:32]
                rt = opcode[11:16]
                rs = opcode[6:11]
                for key, value in itype.items():
                    if opcode_1 == value:
                        execute_var = ["itype", key, rt, rs, immediate]

                if debug:
                    print("The instruction is Itype")


            elif opcode_1 in [j for j in itype_mem.values()]:
                immediate = opcode[16:32]
                rt = opcode[11:16]
                rs = opcode[6:11]
                for key, value in itype_mem.items():
                    if opcode_1 == value:
                        execute_var = ["itype_mem",key]

                if debug:
                    print("The instruction is Itype_mem")

            pipelining_array[1] = execute_var
            pipelining_array[0] = '0'

            if debug:
                #print("execute_var", execute_var)
                print("Decode ",pipelining_array)


def execute():

    global pipelining_array
    while(1):
        if len(pipelining_array[1])!=0 and len(pipelining_array[2])==0:
            alu_result=[]
            execute_var=pipelining_array[1]
            if execute_var[1] == "ADD" :
                alu_result = instr_set.ADD(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "SUB" :
                alu_result = instr_set.SUB(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "MUL" :
                alu_result = instr_set.MUL(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "AND" :
                alu_result = instr_set.AND(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "OR" :
                alu_result = instr_set.OR(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "XOR" :
                alu_result = instr_set.XOR(register[int(execute_var[3],2)],register[int(execute_var[4],2)])
            elif execute_var[1] == "ADDI":
                alu_result=instr_set.ADDI(register[int(execute_var[3],2)],register[int(execute_var[2],2)],int('0b'+str(execute_var[4]),2))
                print(alu_result)
            elif execute_var[1] == "SUBI":
                alu_result=instr_set.SUBI(register[int(execute_var[3],2)],register[int(execute_var[2],2)],int('0b'+str(execute_var[4]),2))
            elif execute_var[1] == "MULI":
                alu_result=instr_set.MULI(register[int(execute_var[3],2)],register[int(execute_var[2],2)],int('0b'+str(execute_var[4]),2))
            elif execute_var[1] == "ANDI":
                alu_result=instr_set.ANDI(register[int(execute_var[3],2)],register[int(execute_var[2],2)],int('0b'+str(execute_var[4]),2))
            elif execute_var[1] == "ORI":
                alu_result = instr_set.ORI(register[int(execute_var[3], 2)], register[int(execute_var[2], 2)],int('0b' + str(execute_var[4]), 2))
            elif execute_var[1] == "XORI":
                alu_result = instr_set.XORI(register[int(execute_var[3], 2)], register[int(execute_var[2], 2)],int('0b' + str(execute_var[4]), 2))

            elif execute_var[1] == "BEQ":
                alu_result = instr_set.BEQ(register[int(execute_var[3], 2)], register[int(execute_var[2], 2)],int('0b' + str(execute_var[4]), 2),fs.get_pc_only())

            elif execute_var[1] == "BZ":
                alu_result = instr_set.BZ(register[int(execute_var[3], 2)], register[int(execute_var[2], 2)],int('0b' + str(execute_var[4]), 2),fs.get_pc_only())

            elif execute_var[1] == "JR":
                alu_result = instr_set.JR(register[int(execute_var[3], 2)], register[int(execute_var[2], 2)],int('0b' + str(execute_var[4]), 2),fs.get_pc_only())

            elif execute_var[1]=="LDW":
                alu_result = instr_set.LDW()
            elif execute_var[1]=="STW":
                alu_result = instr_set.STW()

            elif execute_var[1]=="HALT":
                print_results()
                exit()

            pipelining_array[2]=alu_result
            pipelining_array[1]=[]
            if debug:
                #print(alu_result)
                print("Execute ",pipelining_array)

def memory_phase():

    global pipelining_array
    while(1):
        if len(pipelining_array[3])==0 and len(pipelining_array[2])!=0:
            global rt,rd,rs,immediate
            alu_result=pipelining_array[2]
            if alu_result[0] == "mem":
                if alu_result[1] == "ldw":
                    #print(twos_comp(memory[int((register[int('0b'+str(rs),2)]+ int('0b'+immediate,2)) / 4)], 32))
                    if int((register[int('0b'+str(rs),2)]+ int('0b'+immediate,2)) / 4) in memory.keys():
                        register[int('0b'+str(rt),2)] = twos_comp(int(memory[int((register[int('0b'+str(rs),2)]+ int('0b'+immediate,2)) / 4)],2), 32)
                        dreg[int('0b'+str(rt),2)]=1

                else:
                    #memory[register[int('0b'+str(rs),2)] + int('0b'+immediate,2)] = register[int('0b'+str(rt),2)]
                    memory[int((register[int('0b'+str(rs),2)] + int('0b'+immediate,2))/ 4)] = str(bin(register[int('0b'+str(rt),2)]))[2:].zfill(32)
                    modified_memory.append(int((register[int('0b'+str(rs),2)] + int('0b'+immediate,2))/ 4))

            pipelining_array[3] = alu_result
            pipelining_array[2] = []

            if debug:
                #print(alu_result)
                print("Memory",pipelining_array)

def write_back():

    global pipelining_array,rd,rs,rt
    while(1):
        if len(pipelining_array[4])==0 and len(pipelining_array[3])!=0:
            alu_result=pipelining_array[3]
            if alu_result[1] == "rtype":
                register[int('0b'+str(rd),2)] = alu_result[2]
                dreg[int('0b'+str(rd),2)]=1
                modified_registers.append(int('0b'+str(rd),2))


            elif alu_result[1] == "itype":
                register[int('0b'+str(rt),2)] = alu_result[2]
                dreg[int('0b' + str(rt), 2)] = 1
                modified_registers.append(int('0b'+str(rt),2))

            pipelining_array[4] = alu_result
            pipelining_array[3] = []

            if debug:
                print("write_back",pipelining_array)
                #print(alu_result)
def count_clock():

    global pipelining_array
    while(1):
        global my_clock
        if len(pipelining_array[4])!=0 :
            pipelining_array[5]= pipelining_array[4]
            my_clock = my_clock +1
            pipelining_array[4] = []
            print(my_clock)
            #if (pipelining_array[0]=='0' and pipelining_array[1]==[] and pipelining_array[2]==[] and pipelining_array[3]==[] and pipelining_array[4]==[]):
            #    print_results()


def print_results():
    global my_clock,pc_address
    print("Instruction counts:\n")
    print("-----------------------------\n")
    my_ins_count=instr_set.ins_count()

    print("Total number of instructions:{}".format(my_ins_count["total_ins"]))
    print("Arithmetic instructions:{}".format(my_ins_count["arth_ins"]))
    print("Logical instructions: {}".format(my_ins_count["log_ins"]))
    print("Memory access instructions: {}".format(my_ins_count["mem_ins"]))
    print("Control transfer:{}".format(my_ins_count["bnch_ins"]))
    print('_' * 100)
    print('_' * 100)
    print('Program counter: ', pc_address)
    print('Final register states->')
    for loop in range(32):
        if dreg[loop] ==1:
            print('R',loop,':','changed')
    print('_' * 100)
    for ite, val in register.items():
        if dreg[ite] == 1:
            print('R',ite, ':',val)
    print('_' * 100)
    print('Final memory state->')
    for ite, val in memory.items():
        print('Address: ', ite, ', Contents: ', val)
    print('_' * 100)
    print('_' * 100)
    #-----------------------------------------------------------------------------------------
    '''
    print('Stalls without forwarding: ', stalls)
    print("average cycle stall for hazards:", stalls / len(raw))
    print('Single stalls: ', list(raw.values()).count(-2))
    print('Double stalls: ', list(raw.values()).count(-1))
    print('No. of RAW hazards: ', len(raw))
    print('_' * 50)
    print('Penalties because of branches: ', penal)
    print('No. of branches leading to penalties: ', len(bran))
    print('Average Branch Penality: ', penal / len(bran), 'cycles')
    print('_' * 50)
    print('_' * 50)
    print('Stalls with forwarding: ', fstalls)
    print('_' * 50)
    print('_' * 50)
    print('Total no. of cycles(without forwarding): ', f + 5 + stalls + penal)
    print("Total no. of cycles(with forwarding): ", f + 5 + fstalls + penal)
    print('_' * 50)
    print('_' * 50)
    print("Speedup acheive by forwarding: ", ((f + 5 + stalls + penal) / (f + 5 + fstalls + penal)))
    #------------------------------------------------------------------------------------------------------
    
    print("Total clock:{}".format(my_clock+stall))
    for i in range(len(modified_registers)):
        print("Modified register R{}:{}".format(int(modified_registers[i]),
                                                register[int(modified_registers[i])]))

    for i in range(len(modified_memory)):
        print("Modified Memory M{}:{}".format(modified_memory[i], memory[int(modified_memory[i])]))
    '''
def check_hazard():
    global pc_address,my_clock,stall
    instruction_one = bin(int(instruction_memory[pc_address], 16))[2:].zfill(32)
    instruction_two = bin(int(instruction_memory[pc_address+4], 16))[2:].zfill(32)
    instruction_three = bin(int(instruction_memory[pc_address+8], 16))[2:].zfill(32)
    if instruction_one[0:6] in [j for j in rtype.values()]:
        if instruction_one[16:21]==instruction_two[6:11] or instruction_one[16:21]==instruction_two[11:16]:
            stall=stall+2
        elif instruction_one[16:21]==instruction_three[6:11] or instruction_one[16:21]==instruction_three[11:16]:
            stall = stall + 1
    elif instruction_one[0:6] in [j for j in itype.values()]:
        if instruction_one[11:16] == instruction_two[6:11]:
            stall = stall + 2
        elif instruction_one[11:16] == instruction_three[6:11]:
            stall=stall + 1


t1 = threading.Thread(target=fetch)# Thread(target=fetch, args=(10,))
t2 = threading.Thread(target=decode)
t3 = threading.Thread(target=execute)
t4 = threading.Thread(target=memory_phase)
t5 = threading.Thread(target=write_back)
t6 = threading.Thread(target=count_clock)

# starting all threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
