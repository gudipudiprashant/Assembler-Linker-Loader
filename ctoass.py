import re

def trans(filename):
    #Opens the input File and extracts the lines of C code
    inputFile = open(filename,'r')
    cCode = inputFile.read().split('\n')
    print(cCode)
    cLines = []
    for line in cCode:
        if line !='':
            line = line.lstrip().rstrip()
            cLines.append(line)
    print(cLines)

    # Output File
    assemblyFile = open(filename+'_tr','w')

    #Defining all the lists and counters
    symbolList = []
    globalList = []
    arrayList = []
    extList = []
    loopCounter = 0
    ifCounter = 0
    varCounter = 0

    #RegEx
    add = re.compile(r'(.+)=(.+)\+(.+)')
    var = re.compile(r'var (.*)=(.*)')
    sub = re.compile(r'(.+)=(.+)\-(.+)')
    glo = re.compile(r'glob var (.+)=(.+)')
    arr = re.compile(r'var (.+)\[(.+)\]')       #seems to be working
    ext = re.compile(r'extern (.*)')
    slop = re.compile(r'loop(.+)')
    elop = re.compile(r'endloop(.*)')
    ifgt = re.compile(r'if (.*) > (.*)')
    eif = re.compile(r'endif(.*)')
    ifgte = re.compile(r'if (.*) >= (.*)')
    ifeq = re.compile(r'if (.*) == (.*)')
    assign = re.compile(r'(.+) = (.+)')
    arrAssign = re.compile(r'(.+)\[(.+)\] := (.+)')
    #Boolean for Integer Checking
    def tryInt(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    #Shit starts
    for line in cLines:
        code = ''
        # add = re.compile(r'(.+)=(.+)\+(.+)')
        if add.match(line):
            c = add.match(line).group(1).lstrip().rstrip()
            a = add.match(line).group(2).lstrip().rstrip()
            b = add.match(line).group(3).lstrip().rstrip()
            if c in extList:
                c = c + '_g'
            else:
                c = c + '_'

            if not tryInt(a):
                if a in extList:
                    a = a + '_g'
                else:
                    a = a + '_'
            if not tryInt(b):
                if b in extList:
                    b = b + '_g'
                else:
                    b = b + '_'
            #Both integers so do direct addition
            if tryInt(b) and tryInt(a):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'ADI ' + str(b) + '\n'
                code = code + 'STA ' + c + '\n'
            #Single part is integer

            elif tryInt(a):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'ADD M'+ '\n'
                code = code + 'STA ' + c + '\n'
            elif tryInt(b):
                code = code + 'LDA ' + a + '\n'
                code = code + 'ADI ' + str(b) + '\n'
                code = code + 'STA ' + c + '\n'
            #None integers
            else:
                code = code + 'LDA ' + a + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'ADD M' + '\n'
                code = code + 'STA ' + c + '\n'
        #Similar to addition
        elif sub.match(line):
            c = sub.match(line).group(1).lstrip().rstrip()
            a = sub.match(line).group(2).lstrip().rstrip()
            b = sub.match(line).group(3).lstrip().rstrip()
            if c in extList:
                c = c + '_g'
            else:
                c = c + '_'

            if not tryInt(a):
                if a in extList:
                    a = a + '_g'
                    print('AAAAAAAAAA' + ' ' + a)
                else:
                    a = a + '_'
                    print('BBBBBBBBB' + ' ' + a)
                    print(extList)
            if not tryInt(b):
                if b in extList:
                    b = b + '_g'
                else:
                    b = b + '_'
            if tryInt(b) and tryInt(a):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'SUI ' + str(b) + '\n'
                code = code + 'STA ' + c + '\n'
            elif tryInt(a):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'SUB M'+ '\n'
                code = code + 'STA ' + c + '\n'
            elif tryInt(b):
                code = code + 'LDA ' + a + '\n'
                code = code + 'SUI ' + str(b) + '\n'
                code = code + 'STA ' + c + '\n'
            else:
                code = code + 'LDA ' + a + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'SUB M' + '\n'
                code = code + 'STA ' + c + '\n'

        # Various variables definitions
        elif ext.match(line):
            variable = ext.match(line).group(1).lstrip().rstrip()
            extList.append(variable)
            print('extern added')
        elif glo.match(line):
            variable = glo.match(line).group(1).lstrip().rstrip()
            content = glo.match(line).group(2).lstrip().rstrip()
            varCounter +=1
            code = code + 'JMP DEF' + str(varCounter) + '\n'
            code = code + variable + '_g:' + ' DB ' + str(content) + '\n'
            code = code + 'DEF' + str(varCounter) + ': '
        elif var.match(line):
            variable = var.match(line).group(1).lstrip().rstrip()
            content = var.match(line).group(2).lstrip().rstrip()
            symbolList.append(variable)
            varCounter +=1
            code = code + 'JMP DEF' + str(varCounter) + '\n'
            code = code + variable + '_:' + ' DB ' + str(content) + '\n'
            code = code + 'DEF' + str(varCounter) + ': '

        elif arr.match(line):
            arrName = arr.match(line).group(1).lstrip().rstrip()
            arrSize = arr.match(line).group(2).lstrip().rstrip()
            arrayList.append(arrName)
            varCounter += 1
            code = code + 'JMP DEF' + str(varCounter) + '\n'
            code = code + arrName + '_:' + ' DA ' + str(arrSize) + '\n'
            code = code + 'DEF' + str(varCounter) + ': '


        ### Variable Assignment
        elif assign.match(line):
            variable = assign.match(line).group(1).lstrip().rstrip()
            number = assign.match(line).group(2).lstrip().rstrip()
            if variable in extList:
                variable = variable + '_g'
            else:
                variable = variable + '_'
            code = code + 'MVI A,' + str(number) + '\n'
            code = code + 'STA ' + variable + '\n'
        elif arrAssign.match(line):
            arrVar = arrAssign.match(line).group(1).lstrip().rstrip()
            arrIndex = arrAssign.match(line).group(2).lstrip().rstrip()
            arrValue = arrAssign.match(line).group(3).lstrip().rstrip()
            arrVar = arrVar + '_'
            print(arrVar)
            code = code + 'MVI A,' + str(arrValue) + '\n'
            code = code + 'STA ' + arrVar + '+' + str(arrIndex) + '\n'
        #What if we kept the burden of putting proper loops and endloops indexes to
        #the user itself? We extract the counter presented by the user and
        #use it to set the labels accordingly. Would be a little easier, but not much.
        elif slop.match(line):
            num = slop.match(line).group(1).lstrip().rstrip()
            if not tryInt(num):
                if num in extList:
                    num = num + '_g'
                else:
                    num = num + '_'
            loopCounter += 1
            code = code + 'PUSH E' + '\n'
            if tryInt(num):
                code = code + 'MVI E,' + str(num) + '\n'
            else:
                code = code + 'LXI H,' + num + '\n'
                code = code + 'MOV E,M' + '\n'
            code = code + 'LOOP' + str(loopCounter) + ': '
        elif elop.match(line):
            code = code + 'DCR E' + '\n'
            code = code + 'JNZ LOOP' + str(loopCounter) + '\n'
            code = code + 'POP E' + '\n'
            loopCounter -=1

        ##Conditionals start from here
        ##
        elif ifgte.match(line):
            a = ifgte.match(line).group(1).lstrip().rstrip()
            b = ifgte.match(line).group(2).lstrip().rstrip()
            if not tryInt(a):
                if a in extList:
                    a = a + '_g'
                else:
                    a = a + '_'
            if not tryInt(b):
                if b in extList:
                    b = b + '_g'
                else:
                    b = b + '_'
            ifCounter += 1
            if tryInt(a) and tryInt(b):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'SUI ' + str(b) + '\n'
            elif tryInt(a):
                code = code + 'MVI A,' + str(a) + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'SUB M' + '\n'
            elif tryInt(b):
                code = code + 'LDA ' + a + '\n'
                code = code + 'SUI ' + str(b) + '\n'
            else:
                code = code + 'LDA ' + a + '\n'
                code = code + 'LXI H,' + b + '\n'
                code = code + 'SUB M' + '\n'
            code = code + 'JM ' + 'ENDIF' + str(ifCounter) + '\n'
        elif ifgt.match(line):
            a = ifgt.match(line).group(1).lstrip().rstrip()
            b = ifgt.match(line).group(2).lstrip().rstrip()
            if not tryInt(a):
                if a in extList:
                    a = a + '_g'
                else:
                    a = a + '_'
            if not tryInt(b):
                if b in extList:
                    b = b + '_g'
                else:
                    b = b + '_'
            ifCounter += 1
            if tryInt(a) and tryInt(b):
                code = code + 'MVI A,' + str(b) + '\n'
                code = code + 'SUI ' + str(a) + '\n'
            elif tryInt(b):
                code = code + 'MVI A,' + str(b) + '\n'
                code = code + 'LXI H,' + a + '\n'
                code = code + 'SUB M' + '\n'
            elif tryInt(b):
                code = code + 'LDA ' + b + '\n'
                code = code + 'SUI ' + str(a) + '\n'
            else:
                code = code + 'LDA ' + b + '\n'
                code = code + 'LXI H,' + a + '\n'
                code = code + 'SUB M' + '\n'
            code = code + 'JP ' + 'ENDIF' + str(ifCounter) + '\n'
        elif ifeq.match(line):
            a = ifeq.match(line).group(1).lstrip().rstrip()
            b = ifeq.match(line).group(2).lstrip().rstrip()
            if not tryInt(a):
                if a in extList:
                    a = a + '_g'
                else:
                    a = a + '_'
            if not tryInt(b):
                if b in extList:
                    b = b + '_g'
                else:
                    b = b + '_'
            ifCounter += 1
            if tryInt(a) and tryInt(b):
                code = code + 'MVI A,' + str(b) + '\n'
                code = code + 'SUI ' + str(a) + '\n'
            elif tryInt(b):
                code = code + 'MVI A,' + str(b) + '\n'
                code = code + 'LXI H,' + a + '\n'
                code = code + 'SUB M' + '\n'
            elif tryInt(b):
                code = code + 'LDA ' + b + '\n'
                code = code + 'SUI ' + str(a) + '\n'
            else:
                code = code + 'LDA ' + b + '\n'
                code = code + 'LXI H,' + a + '\n'
                code = code + 'SUB M' + '\n'
            code = code + 'JNZ ' + 'ENDIF' + ifCounter + '\n'
        elif eif.match(line):
            code = code + 'ENDIF' + str(ifCounter) + ': '
            ifCounter -=1


        assemblyFile.write(code)

    code = 'HLT\n'
    assemblyFile.write(code)
