from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from simulate import simulate

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

from main import *

class baseWindow():
    def __init__(self,parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.fileName = ''
        self.frame.grid(row = 0, column = 0)
        self.populateFrame()

    def populateFrame(self):
        openButton = Button(self.frame, text = 'Open File', command = self.openFile)
        openButton.grid(row = 0, column = 0)
        self.statusText = StringVar()
        self.statusText.set('No file selected')
        statusLabel = Label(self.frame, textvariable = self.statusText)
        statusLabel.grid(row = 1, column = 0)
        runButton = Button(self.frame, text = 'Run File', command = self.runFile)
        runButton.grid(row = 2, column = 0)

    def openFile(self):
        self.fileName = filedialog.askopenfilename()
        self.fileName = self.fileName.split('/')[-1]
        if self.fileName != '':
            self.statusText.set('Selected File: ' + self.fileName)
             #Open C to Assembly code here


    def runFile(self):
        if self.fileName!='':
            self.frame.grid_forget()
            newWindow = runALL(self.parent,self.fileName)
        else:
            messagebox.showerror(title="Error",message='Choose a file',parent=self.frame)

class runALL():
    def __init__(self,parent,file):
        self.parent = parent
        self.file = file
        self.frame = Frame(self.parent)
        self.frame.grid(row = 0, column = 0)
        self.populateFrame()

    def populateFrame(self):
        Label(self.frame, text = self.file + '\nCurrent Status:').grid(row = 0, column = 0)
        self.currentStatus = StringVar()
        self.content = 'Nothing done yet.'
        self.currentStatus.set(self.content)
        statusLabel = Label(self.frame, textvariable = self.currentStatus)
        statusLabel.grid(row = 1, column = 0)

        workPane = PanedWindow(self.frame)
        workPane.grid(row = 2, column = 0)
        offsetLabel = Label(workPane,text = 'Set offset:')
        workPane.add(offsetLabel)
        self.offsetAddress = Entry(workPane)
        workPane.add(self.offsetAddress)
        assembleButton = Button(workPane, text = 'Run Assembler', command = self.runAssembler)
        workPane.add(assembleButton)
        #linkButton = Button(workPane, text = 'Run Linker', command = self.runLinker)
        #workPane.add(linkButton)
        #loadButton = Button(workPane, text = 'Run Loader', command = self.runLoader)
        #workPane.add(loadButton)

        self.simulateButton = Button(self.frame, text = 'Simulate Code!',state = DISABLED, command = self.simulate)
        self.simulateButton.grid(row = 3, column = 0)

    def runAssembler(self):
        self.content = 'Assembly Done\nLinking Done\nLoading Done'
        offset = self.offsetAddress.get()
        self.var_tab=ugly_func(self.file,offset)
        self.simulateButton.config(state = NORMAL)

        self.currentStatus.set(self.content)
        #Assembler Code here

    def runLinker(self):
        self.content += '\nLinker Run'
        self.currentStatus.set(self.content)

    def runLoader(self):
        self.content +='\nLoader Run'
        self.currentStatus.set(self.content)
        self.simulateButton.config(state = NORMAL)

    def simulate(self):
        simulate(self.offsetAddress.get())
        pass




root = Tk()
#root.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))
base = baseWindow(root)
root.mainloop()
