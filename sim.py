from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys

# Registers

# General Purpose

reg = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'H':0, 'L':0, 'PC':0, 'SP':0}

PC = 0
stack = []
flags = [0, 0, 0, 0, 0, 0, 0, 0]
oplen = {}
dbloc = []

def calculatelen():
	inputFile = open('lenopcodes.cf',"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		line = line.lstrip().rstrip()
		if line != '' :
			oplen[line.split(' ')[0]] = int(line.split(' ')[1])

calculatelen()
memory = {}

def load(filename):
	inputFile = open(filename,"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		mem = line.split('   ')[0]
		cinstr = line.split('   ')[1]
		op = cinstr.split(' ')[0].lstrip().rstrip()
		if (op != 'DB' and op != 'DA'):
			memory[mem] = cinstr
			# mem += oplen[op]
		elif op == 'DB':
			memory[mem] = int(cinstr.split(' ')[1].lstrip().rstrip())
			dbloc.append(mem)
			# mem += 1
		elif op == 'DA':
			pass

def simulator(pc = 0):

	# read next instruction from memory, get the opcode
	inst = memory[pc]
	opcode = inst.split(' ')[0]


	print ('Current Instruction : ' + str(memory[pc]))
	curinst.set(str(memory[pc]))
	print ('Register Values' )
	print ('A : ' + str(reg['A']))
	rega.set(str(reg['A']))
	print ('B : ' + str(reg['B']))
	regb.set(str(reg['B']))
	print ('C : ' + str(reg['C']))
	regc.set(str(reg['C']))
	print ('D : ' + str(reg['D']))
	regd.set(str(reg['D']))
	print ('E : ' + str(reg['E']))
	rege.set(str(reg['E']))
	print ('F : ' + str(reg['F']))
	regf.set(str(reg['F']))
	print ('G : ' + str(reg['G']))
	regg.set(str(reg['G']))
	print ('H : ' + str(reg['H']))
	regh.set(str(reg['H']))
	print ('Variable Memory Locations')
	memlocs = ''
	for db in dbloc:
		memlocs += (str(db) + ' : ' + str(memory[db]) + '\n')
	memstr.set(memlocs)
	print (memlocs)
	# raw_input("Press Enter to continue...")
	if opcode == 'HLT':
		progcompleted.set('DONE')
		return


	elif opcode == 'MVI':
		regvar = inst.split(' ')[1].lstrip().rstrip()
		reg[regvar] = int(inst.split(' ')[2].lstrip().rstrip())
		PC = pc + int(oplen[opcode])

	elif opcode == 'ADI':
		reg['A'] = int(reg['A']) + int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])

	elif opcode == 'STA':
		memloc = int(inst.split(' ')[1])
		memory[memloc] = int(reg['A'])
		PC = pc + int(oplen[opcode])
	elif opcode == 'LDA':
		memloc = int(inst.split(' ')[1])
		reg['A'] = int(memory[memloc])
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
		PC = pc + int(oplen[opcode])

	# subtract immediate
	elif opcode == 'SUI':
		reg['A'] = int(reg['A']) - int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])
	elif opcode == 'SUB':
		memaddr = (reg['H'] << 8) + reg['L']
		reg['A'] = int(reg['A']) - int(mem[memaddr])
		PC = pc + int(oplen[opcode])
	elif opcode == 'DCR':
		dcrreg = inst.split(' ')[1]
		reg[dcrreg] -= 1
		PC = pc + int(oplen[opcode])

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
		if int(reg['A']) != 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JZ':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) == 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JP':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) > 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JM':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) < 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])


	reg['PC'] = PC

def callbackf():
	simulator(int(reg['PC']))

#######
# Gui #
#######
def askopenfilename(*args):
	# get filename
	filename = filedialog.askopenfilename()
	load(filename)

def openexist(*args):
	# get filename
	filename = sys.argv[1]
	load(filename)
	
root = Tk()
root.title("Simulator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

curinst = StringVar()
rega = StringVar()
regb = StringVar()
regc = StringVar()
regd = StringVar()
rege = StringVar()
regf = StringVar()
regg = StringVar()
regh = StringVar()
memstr = StringVar()
meters = StringVar()
progcompleted = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
ttk.Button(mainframe, text="Open Passed File", command=openexist).grid(column=1, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Open Another File", command=askopenfilename).grid(column=2, row=1, sticky=(W, E))



ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Run", command=callbackf).grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Current Instruction").grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=curinst).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Register Values").grid(column=1, row=4, sticky=(W, E))
ttk.Label(mainframe, text="A").grid(column=1, row=5, sticky=(W, E))
ttk.Label(mainframe, textvariable=rega).grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, text="B").grid(column=1, row=6, sticky=(W, E))
ttk.Label(mainframe, textvariable=regb).grid(column=2, row=6, sticky=(W, E))
ttk.Label(mainframe, text="C").grid(column=1, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=regc).grid(column=2, row=7, sticky=(W, E))
ttk.Label(mainframe, text="D").grid(column=1, row=8, sticky=(W, E))
ttk.Label(mainframe, textvariable=regd).grid(column=2, row=8, sticky=(W, E))
ttk.Label(mainframe, text="E").grid(column=1, row=9, sticky=(W, E))
ttk.Label(mainframe, textvariable=rege).grid(column=2, row=9, sticky=(W, E))
ttk.Label(mainframe, text="F").grid(column=1, row=10, sticky=(W, E))
ttk.Label(mainframe, textvariable=regf).grid(column=2, row=10, sticky=(W, E))
ttk.Label(mainframe, text="G").grid(column=1, row=11, sticky=(W, E))
ttk.Label(mainframe, textvariable=regg).grid(column=2, row=11, sticky=(W, E))
ttk.Label(mainframe, text="H").grid(column=1, row=12, sticky=(W, E))
ttk.Label(mainframe, textvariable=regh).grid(column=2, row=12, sticky=(W, E))
ttk.Label(mainframe, text="Memory Locations").grid(column=1, row=13, sticky=(W, E))
ttk.Label(mainframe, textvariable=memstr).grid(column=2, row=13, sticky=(W, E))
ttk.Label(mainframe, textvariable=progcompleted).grid(column=2, row=14, sticky=(W, E))

# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
root.bind('<Return>', simulator)

root.mainloop()