class values_set():
    def __init__(self):
        self.pc = 0b000


    def update_pc(self,addr):
        self.pc = addr

    def get_pc(self):
        pc_1=self.pc
        self.update_pc(self.pc+0b100)
        return pc_1

    def get_pc_only(self):
        pc_1 = self.pc
        return pc_1

