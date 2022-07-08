import os
from _main import *
from LogSystem import *
import time
##
def myexcepthook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press RETURN. ")
sys.excepthook = myexcepthook
##
cwd = os.getcwd()
filename = cwd.split('\\')[-1]
OutputDataX = []
defaultList(OutputDataX, 0)
OutputDataY = []
defaultList(OutputDataY, 0)
##
# load CNK1
print('reading data from CNK1...')
CNK1 = ReadFile('CNK1.INP', os.path.basename(__file__))
# get Fnum and construct FList
FNum = int(CNK1.readline().split()[0])
FList = []
FOname = []
for i in range(FNum) :
    tmp = CNK1.readline().split()[0]
    FOname.append(tmp)
    try :
        if tmp[-1] == 'L' :
            tmp = tmp[:-2]
        else :
            tmp = tmp[:-1]
    except Exception as e:
        WriteEx()
        ExceptionExit('FloorName Out of range in CNK1')
    FList.append(tmp)
# load useless data
KeepRead  = True
while KeepRead :
    line = CNK1.readline()
    if line.find('col.data') != -1:
        KeepRead = False
    if line == '' :
        WriteError('CNK1 Read File Error. No col.data.', os.path.basename(__file__))
        ExceptionExit('CNK1 Read File Error. No col.data.')
for i in range(int(CNK1.readline().split()[0]) + 7) :
    CNK1.readline()
FCdic = {}
Fcdata = CNK1.readline().split(',')
count = 0
for item in Fcdata :
    try:
        Fc = float(item.split('M')[0])
        Fn = int(item.split('M')[1])
    except Exception as e:
        WriteEx()
        ExceptionExit('Fc read error in CNK1')
    for i in range(Fn) :
        FCdic[FList[count]] = Fc
        count = count + 1
#
Fsydic = {}
Fsydata = CNK1.readline().split(',')
count = 0
for item in Fsydata :
    try :
        Fsy = float(item.split('M')[0])
        Fn = int(item.split('M')[1])
    except Exception as e:
        WriteEx()
        ExceptionExit('Fsy read error in CNK1')
    for i in range(Fn) :
        Fsydic[FList[count]] = Fsy
        count = count + 1

# load CXX
print('reading data from CXX...')
CXX = ReadFile('CXX.DAT', os.path.basename(__file__))
## get Floor and Cross section
CandF = CXX.readline().split()
try :
    C = int(CandF[0])
    F = int(CandF[1])
except Exception as e:
    WriteEx()
    ExceptionExit('CXX Read File Error.')
for i in range(C):
    CXX.readline()
for i in range(F):
    CXX.readline()
for i in range(F):
    CXX.readline()
ALLCOLUMN = []
CXX_Data = CXX.readlines()
LineLen = len(CXX_Data)
Progress = 0
CaseCXX = 0
##
while CaseCXX < LineLen:
    ## set lines
    lines = []
    try :
        lines.append(CXX_Data[CaseCXX].split())
        lines.append(CXX_Data[CaseCXX + 1].split())
        lines.append(CXX_Data[CaseCXX + 2].split())
        lines.append(CXX_Data[CaseCXX + 3].split())
        lines.append(CXX_Data[CaseCXX + 4].split())
        lines.append(CXX_Data[CaseCXX + 5].split())
    except Exception as e:
        WriteEx()
        ExceptionExit('CXXData Out of range.')
    #floor and name
    try :
        if lines[0][0][-1] >= '0' and lines[0][0][-1] <= '9' or lines[0][0][-1] == 'F':
            floor = lines[0][0]
        else :
            floor = lines[0][0][:-1]
        name = floor + lines[0][2]
    except Exception as e:
        WriteEx()
        ExceptionExit('CXX: line 0 Out of range. Doing floor name.')
    ## BC HC type
    try :
        BC = float(lines[1][0])
        HC = float(lines[1][1])
    except Exception as e:
        WriteEx()
        ExceptionExit('CXX: line 1 Out of range. Doing BC HC.')
    if BC == 0 and HC == 0:
        CaseCXX = CaseCXX + 6
        continue
    ## No1
    try :
        No1 = lines[2][0]
    except Exception as e:
        WriteEx()
        ExceptionExit('CXX: line 2 Out of range. Doing No1 No2.')
    No1 = '#' + No1
    # No Numx Numy
    try :
        if lines[5][0] != lines[5][3]:
            ExceptionExit('Error in No. First Element diff with last Element in line 5.')
        No = '#' + lines[5][0]
        Numx = int(lines[4][3]) + 2
        Numy = int(lines[3][3]) + 2
        S = int(lines[5][1])
        SM = int(lines[5][2])
    except Exception as e:
        WriteEx()
        ExceptionExit('CXX: line 4 or 5 Out of range. Doing No Numxy S.')
    whichFloor = floor
    if whichFloor[0] >= '0' and whichFloor[0] <= '9' or whichFloor == 'R1':
        ALLCOLUMN.append(COLUMN(name, BC, HC, No1, No, Numx, Numy, FCdic[whichFloor], Fsydic[whichFloor], whichFloor))
    CaseCXX = CaseCXX + 6
    # progress bar
    if float(CaseCXX / LineLen) * 10.0 > Progress:
        Progress = Progress + 1
        print("\r", end = '')
        print('[', end = '')
        for i in range(Progress):
            print('|', end = '')
        for i in range(10 - Progress):
            print(' ', end = '')
        print(']', end = '')
        time.sleep(0.02)
    # progress bar

#load beam data
print('\nreading data from A6B103C...')
Beam = ReadFile('A6B103C.dat', os.path.basename(__file__))
#load useless data
KeepRead  = True
while KeepRead:
    line = Beam.readline()
    if line.find('BEAM') != -1:
        KeepRead = False
KeepRead  = True
while KeepRead:
    line = Beam.readline()
    if line != '\n':
        KeepRead = False
ALLBEAM = []
BEAM_Data = [line]
for line in Beam.readlines():
    if line != '\n' and line.find('BEAM') == -1:
        BEAM_Data.append(line)
LineLen = len(BEAM_Data)
Progress = 0
CaseBeam = 0
while CaseBeam < LineLen:
    ## set lines
    lines = []
    try :
        lines.append(BEAM_Data[CaseBeam])
        lines.append(BEAM_Data[CaseBeam + 1])
        lines.append(BEAM_Data[CaseBeam + 2])
        lines.append(BEAM_Data[CaseBeam + 3])
        lines.append(BEAM_Data[CaseBeam + 4])
        lines.append(BEAM_Data[CaseBeam + 5])
        lines.append(BEAM_Data[CaseBeam + 6])
        lines.append(BEAM_Data[CaseBeam + 7])
    except Exception as e:
        WriteEx()
        ExceptionExit('BEAMData Out of range.')
    ## get case num of these line
    Casenum = lines[0].count('*') - 1
    ## get name and BC, HC
    nameList = []
    BCList = []
    HCList = []
    SNoList = []
    SNumList = []
    WFList = []
    #
    tmp = lines[0].split('*')
    tmp2 = lines[2].replace('*', ' ').split()
    tmp3 = lines[3].replace('#', ' ').split()
    tmp4 = lines[4].replace('#', ' ').split()
    tmp5 = lines[5].replace('*', ' ').split()
    tmp6 = lines[6].split()
    STIRcount = 2
    for i in range(1, 1 + Casenum) :
        tmp[i] = tmp[i].replace('(', ' ')
        tmp[i] = tmp[i].replace(')', ' ')
        tmp[i] = tmp[i].replace('x', ' ')
        tmp[i] = tmp[i].replace('/', ' ')
        data = tmp[i].split()
        try :
            nameList.append(data[0] + data[1])
            if data[0][-1] >= '0' and data[0][-1] <= '9' or data[0][-1] == 'F' or data[0][-1] == 'R':
                floor = data[0]
            else :
                floor = data[0][:-1]
            WFList.append(floor)
            BCList.append(data[2])
            HCList.append(data[3])
            if tmp6[STIRcount].split('#')[0] == '' :
                SNumList.append(1)
            else :
                SNumList.append(int(tmp6[STIRcount].split('#')[0]))
            SNoList.append('#' + tmp6[STIRcount].split('#')[-1])
        except Exception as e:
            WriteEx()
            ExceptionExit('BEAMData Out of range.')
        STIRcount = STIRcount + 4
    for i in range(Casenum) :
        if nameList[i].find('P') == -1 and (BCList[i] != '0' or HCList[i] != '0'):
            if WFList[i][0] >= '0' and WFList[i][0] <= '9' or WFList[i] == 'R1':
                ALLBEAM.append(BEAM(nameList[i], float(BCList[i]), float(HCList[i]), SNoList[i], SNumList[i], FCdic[WFList[i]], Fsydic[WFList[i]], WFList[i]))
    CaseBeam = CaseBeam + 8
    # progress bar
    if float(CaseBeam / LineLen) * 10.0 > Progress:
        Progress = Progress + 1
        print("\r", end = '')
        print('[', end = '')
        for i in range(Progress):
            print('|', end = '')
        for i in range(10 - Progress):
            print(' ', end = '')
        print(']', end = '')
        time.sleep(0.02)
    # progress bar
##
ALLCOLUMN.sort(key=compare)
ALLBEAM.sort(key=compare)
print('\ngenerating column data...')
LineLen = len(ALLCOLUMN)
Progress = 0
CaseC = 0
for column in ALLCOLUMN :
    OutputDataX.append(f'\t{column.name}\t{column.Fc}\t{column.Fsy}\t{column.AVx}\t{column.Numx}\t{column.Numy}\n')
    OutputDataY.append(f'\t{column.name}\t{column.Fc}\t{column.Fsy}\t{column.AVy}\t{column.Numy}\t{column.Numx}\n')
    CaseC = CaseC + 1
    # progress bar
    if float(CaseC / LineLen) * 10.0 > Progress:
        Progress = Progress + 1
        print("\r", end = '')
        print('[', end = '')
        for i in range(Progress):
            print('|', end = '')
        for i in range(10 - Progress):
            print(' ', end = '')
        print(']', end = '')
        time.sleep(0.02)
    # progress bar
print('\ngenerating beam data...')
LineLen = len(ALLBEAM)
Progress = 0
CaseC = 0
for beam in ALLBEAM :  
    OutputDataX.append(f'\t{beam.name}\t{beam.Fc}\t{beam.Fsy}\t{beam.Av}\t{beam.N}\t{beam.N}\n')
    OutputDataY.append(f'\t{beam.name}\t{beam.Fc}\t{beam.Fsy}\t{beam.Av}\t{beam.N}\t{beam.N}\n')
    CaseC = CaseC + 1
    # progress bar
    if float(CaseC / LineLen) * 10.0 > Progress:
        Progress = Progress + 1
        print("\r", end = '')
        print('[', end = '')
        for i in range(Progress):
            print('|', end = '')
        for i in range(10 - Progress):
            print(' ', end = '')
        print(']', end = '')
        time.sleep(0.02)
    # progress bar
##
defaultList(OutputDataX, 1)
defaultList(OutputDataY, 1)
##
print('\ngenerating data in second part...')
LineLen = len(FList)
Progress = 0
count = 0
for item in FList :
    if FOname[count][0] >= '0' and FOname[count][0] <= '9' or FOname[count] == 'R1F':
        OutputDataX.append(f'\t{FOname[count]}_CONC_fy\t\t{str(Fsydic[item])}\t\t2040000.00\n')
        OutputDataY.append(f'\t{FOname[count]}_CONC_fy\t\t{str(Fsydic[item])}\t\t2040000.00\n')
    count = count + 1
    # progress bar
    if float(count / LineLen) * 10.0 > Progress:
        Progress = Progress + 1
        print("\r", end = '')
        print('[', end = '')
        for i in range(Progress):
            print('|', end = '')
        for i in range(10 - Progress):
            print(' ', end = '')
        print(']', end = '')
        time.sleep(0.02)
    # progress bar
defaultList(OutputDataX, 2)
defaultList(OutputDataY, 2)
##
print('\noutput data...')
with open(filename + '+X.MET', 'w') as outputX:
    for line in OutputDataX :
        outputX.write(line)
with open(filename + '+Y.MET', 'w') as outputY:
    for line in OutputDataY :
        outputY.write(line)
print('\nComplete!!')
os.system('pause')