class COLUMN :
    def __init__(self, name, BC, HC, No1, No, Numx, Numy, Fc, Fsy, whichFloor):
        self.name = name
        self.RCMaterial = name + '_CONC'
        if whichFloor[0] == 'R':
            self.FloorPtr = int(whichFloor[1:]) + 1000
        elif whichFloor[0] == 'B':
            self.FloorPtr = int(whichFloor[1:]) * -1
        elif IsInt(whichFloor) :
            self.FloorPtr = int(whichFloor)
        else :
            self.FloorPtr = -1000
        self.BC = BC  
        self.HC = HC  
        self.No1 = No1  
        self.No = No  
        self.Numx = Numx
        self.Numy = Numy
        self.Fc = Fc
        self.Fsy = Fsy
        self.AVx = "{:.2f}".format(float(Numx * NosDic[int(No[1:])]))
        self.AVy = "{:.2f}".format(float(Numy * NosDic[int(No[1:])]))
class BEAM :
    def __init__(self, name, BC, HC, No, Nonum, Fc, Fsy, whichFloor):
        self.name = name
        self.RCMaterial = name + '_CONC'
        if whichFloor[0] == 'R':
            if len(whichFloor) == 1:
                self.FloorPtr = 1000
            elif whichFloor[-1] >= '0' and whichFloor[-1] <= '9' :
                self.FloorPtr = int(whichFloor[1:]) + 1000
            else :
                self.FloorPtr = int(whichFloor[1:-1]) + 1000
        elif whichFloor[0] == 'B':
            self.FloorPtr = int(whichFloor[1:]) * -1
        elif IsInt(whichFloor) :
            self.FloorPtr = int(whichFloor)
        else :
            self.FloorPtr = -1000
        self.type = type  
        self.BC = BC  
        self.HC = HC  
        self.No = No
        self.N = "{:.2f}".format(Nonum * 2.0)
        self.Fc = Fc
        self.Fsy = Fsy
        self.Av = "{:.2f}".format(float(NosDic[int(No[1:])] * Nonum * 2.0))
        self.whichFloor = whichFloor
def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def compare(case):
    return -case.FloorPtr
NosDic = {3 : 0.713, 
          4 : 1.267, 
          5 : 1.986, 
          6 : 2.865, 
          7 : 3.871, 
          8 : 5.067, 
          9 : 6.469, 
          10 : 8.143, 
          11 : 10.07,
          12 : 12.19,
          14 : 14.52,
          16 : 19.79,
          18 : 25.79}
def defaultList(InList, phase) :
    if phase == 0 :
        InList.append('$Unit\n')
        InList.append('KGF-CM\n\n')
        InList.append('$ Kawashima constitutive law\n')
        InList.append('$ Name	Fc		Fsy	Av	EL(2)	EL(3)\n')
        InList.append('$ 	(kgf/cm^2)	(kgf/cm^2)		(cm^2)		(cm)	(cm)\n\n')
        InList.append('$ End Kawashima constitutive law\n\n')
        InList.append('$ Mander constitutive law\n')
        InList.append('$ Mander constitutive law\n')
        InList.append('$\tName\tFc\tFsy\tAv\tN2\tN3\n')
        InList.append('$\t\t(kgf/cm^2)\t(kgf/cm^2)\t(cm^2)\n')
    if phase ==  1 :
        InList.append('\n$ End Mander constitutive law\n\n')
        InList.append('$ Steel stress strain\n')
        InList.append('$\tName\t\tYieldingStress\t\tEs\n')
        InList.append('$\t\t\t(kgf/cm^2)\t\t(kgf/cm^2)\n')
