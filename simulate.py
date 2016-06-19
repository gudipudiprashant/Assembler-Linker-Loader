from tkinter import *
def simulate(offset):
    #print(var_table)
    CONST_minColumnSize = 50
    CONST_minRowSize = 20

    reg = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'H':0, 'L':0, 'PC':int(offset), 'SP':0}

    PC = 0
    stack = []
    flags = [0, 0, 0, 0, 0, 0, 0, 0]
    zeroFlag = 0
    oplen = {}
    varMemory = {}
    varAdd = []
    memory = {}
    memAdd = []



    def calculatelen():
        inputFile = open('lenopcodes.cf',"r")
        code = inputFile.read()
        lines = code.split('\n')
        for line in lines :
            line = line.lstrip().rstrip()
            if line != '' :
                oplen[line.split(' ')[0]] = int(line.split(' ')[1])

    calculatelen()

    def load(filename):
        inputFile = open(filename,"r")
        code = inputFile.read()
        lines = code.split('\n')
        for line in lines :
            if(line != ''):
                mem = int(line.split('   ')[0].lstrip().rstrip())
                cinstr = line.split('   ')[1]
                op = cinstr.split(' ')[0].lstrip().rstrip()
                if (op != 'DB' and op != 'DA'):
                    memory[mem] = cinstr.lstrip().rstrip()
                    memAdd.append(mem)
                    #mem += oplen[op]
                elif op == 'DB':
                    varMemory[mem] = int(cinstr.split(' ')[1].lstrip().rstrip())
                    varAdd.append(mem)
                    memory[mem] = varMemory[mem]
                    # mem += 1
                elif op == 'DA':
                    sizeOfArray = int(cinstr.split()[1].lstrip().rstrip())
                    for i in range(sizeOfArray):
                        varMemory[mem] = 0
                        varAdd.append(mem)
                        mem +=1


    load('sim.txt')
    #print(memory)

    def simulator(pc,window):
        #print(pc)
        #print(memory)
        global zeroFlag
        #zeroFlag = IntVar()
        # read next instruction from memory, get the opcode
        inst = memory[pc]

        opcode = inst.split(' ')[0]
        PC = pc
        # raw_input("Press Enter to continue...")
        if opcode == 'HLT':
            return 1
        elif opcode == 'MVI':
            regvar = inst.split(' ')[1].lstrip().rstrip()
            reg[regvar] = int(inst.split(' ')[2].lstrip().rstrip())
            PC = pc + int(oplen[opcode])
        elif opcode == 'ADI':
            reg['A'] = int(reg['A']) + int(inst.split(' ')[1])
            PC = pc + int(oplen[opcode])
            if reg['A']> 0:
                zeroFlag = 1
            elif reg['A'] == 0:
                zeroFlag = 0
            elif reg['A'] < 0:
                zeroFlag = -1
        elif opcode == 'STA':
            memloc = int(inst.split(' ')[1])
            memory[memloc] = int(reg['A'])
            varMemory[memloc] = int(reg['A'])
            PC = pc + int(oplen[opcode])
        elif opcode == 'LDA':
            memloc = int(inst.split(' ')[1])
            reg['A'] = int(memory[memloc])
            print(reg['A'])
            PC = pc + int(oplen[opcode])
        elif opcode == 'LXI':
            destreg = inst.split(' ')[1].lstrip().rstrip()
            val = int(inst.split(' ')[2].lstrip().rstrip())
            valh = (val >> 8)
            vall = val ^ (valh << 8)
            reg[destreg] = int(valh)
            if destreg == 'H':
                reg['L'] = int(vall)
            PC = pc + int(oplen[opcode])
        elif opcode == 'MOV':
            destreg = inst.split(' ')[1].lstrip().rstrip()
            srcreg = inst.split(' ')[2].lstrip().rstrip()
            reg[destreg] = reg[srcreg]
            PC = pc + int(oplen[opcode])
        elif opcode == 'ADD':
            # ADD is ADD M , hex code 86
            memaddr = (reg['H'] << 8) + reg['L']
            reg['A'] = int(reg['A']) + int(memory[memaddr])
            # reg['A'] = res & (~ (1 << 8) )
            # flags['C'] = ( res >> 8 ) & 1
            if reg['A']> 0:
                zeroFlag = 1
            elif reg['A'] == 0:
                zeroFlag = 0
            elif reg['A'] < 0:
                zeroFlag = -1
            PC = pc + int(oplen[opcode])
        # subtract immediate
        elif opcode == 'SUI':
            reg['A'] = int(reg['A']) - int(inst.split(' ')[1])
            PC = pc + int(oplen[opcode])
            if reg['A']> 0:
                zeroFlag = 1
            elif reg['A'] == 0:
                zeroFlag = 0
            elif reg['A'] < 0:
                zeroFlag = -1
        elif opcode == 'SUB':
            memaddr = (reg['H'] << 8) + reg['L']
            reg['A'] = int(reg['A']) - int(memory[memaddr])
            PC = pc + int(oplen[opcode])
            if reg['A']> 0:
                zeroFlag = 1
            elif reg['A'] == 0:
                zeroFlag = 0
            elif reg['A'] < 0:
                zeroFlag = -1
        elif opcode == 'DCR':
            dcrreg = inst.split(' ')[1]
            reg[dcrreg] -= 1
            PC = pc + int(oplen[opcode])
            if reg[dcrreg]> 0:
                zeroFlag = 1
            elif reg[dcrreg] == 0:
                zeroFlag = 0
            elif reg[dcrreg] < 0:
                zeroFlag = -1
        elif opcode == 'ANI':
            reg['A'] = int(reg['A']) & int(inst.split(' ')[1])
            PC = pc + int(oplen[opcode])
        elif opcode == 'ANA':
            srcreg = inst.split(' ')[1]
            reg['A'] = int(reg['A']) & int(reg[srcreg])
            PC = pc + int(oplen[opcode])
        elif opcode == 'ORI':
            reg['A'] = int(reg['A']) | int(inst.split(' ')[1])
            PC = pc + int(oplen[opcode])
        elif opcode == 'ORA':
            srcreg = inst.split(' ')[1]
            reg['A'] = int(reg['A']) | int(reg[srcreg])
            PC = pc + int(oplen[opcode])
        elif opcode == 'PUSH':
            srcreg = inst.split(' ')[1]
            stack.append(int(reg[srcreg]))
            if srcreg == 'D':
                stack.append(int(reg['E']))
            PC = pc + int(oplen[opcode])
        elif opcode == 'POP':
            srcreg = inst.split(' ')[1]
            reg[srcreg] = stack.pop()
            if srcreg == 'D':
                reg['E'] = stack.pop()
            PC = pc + int(oplen[opcode])
        elif opcode == 'JMP':
            nextinst = int(inst.split(' ')[1])
            PC = nextinst
            print(nextinst)
            print(PC)
        elif opcode == 'JNZ':
            nextinst = int(inst.split(' ')[1])
            if zeroFlag != 0:
                PC = nextinst
            else:
                PC = pc + int(oplen[opcode])
        elif opcode == 'JZ':
            nextinst = int(inst.split(' ')[1])
            if zeroFlag == 0:
                PC = nextinst
            else:
                PC = pc + int(oplen[opcode])
        elif opcode == 'JP':
            nextinst = int(inst.split(' ')[1])
            if zeroFlag > 0:
                PC = nextinst
            else:
                PC = pc + int(oplen[opcode])
        elif opcode == 'JM':
            nextinst = int(inst.split(' ')[1])
            if zeroFlag < 0:
                PC = nextinst
            else:
                PC = pc + int(oplen[opcode])

        reg['PC'] = PC
        return 0

    def performInstruction(pc,window):
        flag = simulator(pc,window)

        if(flag == 1):
            window.nextButton.config(state = DISABLED)
        else:
            window.frame.grid_forget()
            window.createFrame()




    class simulateWindow():
        def __init__(self, parent):

            self.parent = parent
            self.codeSize = len(memAdd)
            self.createFrame()
            #self.noVariables = 4
        def createFrame(self):
            self.frame = Frame(self.parent)
            self.frame.grid(row = 0, column = 0)
            self.bigPane = PanedWindow(self.frame)
            self.bigPane.grid(row = 0, column = 0)
            self.littlePane = PanedWindow(self.bigPane, orient = VERTICAL)
            self.instructionList()
            self.bigPane.add(self.littlePane)
            self.registerList()
            self.variableList()
            self.footerPane = PanedWindow(self.frame)
            self.footerPane.grid(row = 1, column = 0)
            self.nextButton = Button(self.footerPane, text = 'Next instruction',
                                     command =lambda: performInstruction(reg['PC'],self))
            self.footerPane.add(self.nextButton)

        def instructionList(self):
            self.instructionFrame = Frame(self.bigPane)
            self.bigPane.add(self.instructionFrame)

            for i in range(3):
                self.instructionFrame.grid_columnconfigure(i,minsize= CONST_minColumnSize)
            for i in range(self.codeSize):
                self.instructionFrame.grid_rowconfigure(i,minsize = CONST_minRowSize)

            self.instructionTable = [[Label(self.instructionFrame,relief= RAISED) \
                                      for i in range(3)] for j in range(self.codeSize)]
            i=0
            for mem in sorted(memAdd):
                self.instructionTable[i][1].config(text = str(mem))
                self.instructionTable[i][2].config(text = str(memory[mem]))
                self.instructionTable[i][1].grid(row = i, column = 1, sticky = (E,W))
                self.instructionTable[i][2].grid(row = i, column = 2,sticky = (E,W))
                i +=1

            for i in range(self.codeSize):
                #self.instructionTable[i][0].config(image = 'icon.jpg')
                self.instructionTable[i][0].grid(row = i, column = 0,sticky = (E,W))



        def registerList(self):
            self.registerFrame = Frame(self.littlePane)
            self.littlePane.add(Label(self.littlePane,text = 'List of Registers'))
            self.littlePane.add(self.registerFrame)

            for i in range(2):
                self.registerFrame.grid_columnconfigure(i,minsize= CONST_minColumnSize)
            for i in range(len(reg)):
                self.registerFrame.grid_rowconfigure(i,minsize = CONST_minRowSize)

            self.registerTable = [[Label(self.registerFrame,relief = RAISED) \
                                   for i in range(2)] for j in range(len(reg))]
            i=0
            for register in sorted(reg):
                self.registerTable[i][0].config(text = register)
                self.registerTable[i][1].config(text = reg[register])
                self.registerTable[i][0].grid(row = i, column = 0,sticky = (E,W))
                self.registerTable[i][1].grid(row = i, column = 1, sticky = (E,W))
                i+=1

        def variableList(self):
            self.variableFrame = Frame(self.littlePane)
            self.littlePane.add(Label(self.littlePane, text = 'List of variables'))
            self.littlePane.add(self.variableFrame)

            for i in range(3):
                self.variableFrame.grid_columnconfigure(i,minsize= CONST_minColumnSize)
            for i in range(len(varAdd)):
                self.variableFrame.grid_rowconfigure(i,minsize = CONST_minRowSize)

            self.variableTable = [[Label(self.variableFrame, relief = RAISED) for i in range(2)] \
                                  for j in range(len(varAdd))]
            i=0
            for mem in sorted(varAdd):
                #print(mem)
                #print(varMemory)
                #self.variableTable[i][0].config(text = var_table[int(mem)])
                self.variableTable[i][0].config(text = mem)
                self.variableTable[i][1].config(text = varMemory[mem])
                #self.variableTable[i][0].grid(row = 1, column = 0, sticky = (W,E))
                self.variableTable[i][0].grid(row = i, column = 1,sticky = (W,E))
                self.variableTable[i][1].grid(row = i, column = 2, sticky = (W,E))
                i +=1


    root = Tk()
    win = simulateWindow(root)
    root.mainloop()
