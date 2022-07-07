import os
from _main import *
from LogSystem import *

cwd = os.getcwd()
filename = cwd.split('\\')[-1]
OutputDataX = []
defaultList(OutputDataX, 0)
OutputDataY = []
defaultList(OutputDataY, 0)
##
# load CNK1
CNK1 = ReadFile('CNK1.INP', os.path.basename(__file__))
# get Fnum and construct FList
FNum = int(CNK1.readline().split()[0])
FList = []
for i in range(FNum) :
    tmp = CNK1.readline().split()[0]
    if tmp[-1] == 'L' :
        tmp = tmp[:-2]
    else :
        tmp = tmp[:-1]
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
    Fc = float(item.split('M')[0])
    Fn = int(item.split('M')[1])
    for i in range(Fn) :
        FCdic[FList[count]] = Fc
        count = count + 1
#
Fsydic = {}
Fsydata = CNK1.readline().split(',')
count = 0
for item in Fsydata :
    Fsy = float(item.split('M')[0])
    Fn = int(item.split('M')[1])
    for i in range(Fn) :
        Fsydic[FList[count]] = Fsy
        count = count + 1

# load CXX
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
    ALLCOLUMN.append(COLUMN(name, BC, HC, No1, No, Numx, Numy, FCdic[whichFloor], Fsydic[whichFloor], whichFloor))
    CaseCXX = CaseCXX + 6
    ## progress bar
    # if float(CaseCXX / LineLen) * 10.0 > Progress:
    #     Progress = Progress + 1
    #     print("\r", end = '')
    #     print('[', end = '')
    #     for i in range(Progress):
    #         print('|', end = '')
    #     for i in range(10 - Progress):
    #         print(' ', end = '')
    #     print(']', end = '')
    #     time.sleep(0.05)
    ## progress bar
ALLCOLUMN.sort(key=compare)
for column in ALLCOLUMN :
    OutputDataX.append(f'\t{column.name}\t{column.Fc}\t{column.Fsy}\t{column.AVx}\t{column.Numx}\t{column.Numy}\n')
    OutputDataY.append(f'\t{column.name}\t{column.Fc}\t{column.Fsy}\t{column.AVy}\t{column.Numy}\t{column.Numx}\n')

outputX = open(filename + '+X.MET', mode = 'w')
for line in OutputDataX :
    outputX.write(line)
outputY = open(filename + '+Y.MET', mode = 'w')
for line in OutputDataY :
    outputY.write(line)