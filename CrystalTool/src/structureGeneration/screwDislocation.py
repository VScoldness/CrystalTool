import os
import math
import pandas as pd
import random
import re
import shutil
import numpy as np


class screwDis:
    def __init__(self, comp: list[int], lattice_constant, size = [50, 30, 65]) -> None:
        self.num_comp = comp.copy()
        self.comp               = "_".join([str(i) for i in comp])
        self.lc                 = lattice_constant
        self.burger             = self.lc*(math.sqrt(3)/2)
        self.output_path        = f"{self.comp}_screw.lmp"
        self.size               = size
    
    def toRandom(self):
        self.toPerfectBCC()
        self.insertScrew()
        self.tiltBox()
        self.toLammps()
        self.changeComp()
    
    def toPerfectBCC(self) -> None:
        powerShell_Input = "atomsk --create bcc {} Mo orient [121] [-101] [1-11] -duplicate {} {} {} single.lmp".format(self.lc, self.size[0], self.size[1], self.size[2])
        os.system("powershell.exe {}".format(powerShell_Input))

    def insertScrew(self) -> None:
        toScrew = f"atomsk single.lmp -disloc 0.501*box 0.501*box screw z y {self.burger} screwMo.xsf"
        os.system(f"powershell.exe {toScrew}")
        os.remove("single.lmp")
    
    def tiltBox(self, input_file="screwMo.xsf", output_file="titledScrewMo.xsf"):
        f = open(input_file, 'r')
        output = open(output_file, 'w')
        for _ in range(3):
            line = f.readline()
            output.write(line)
        line = f.readline()
        coordinates = re.findall(r'[\d\.\d]+', line)
        new_line = f"{coordinates[0]}     {coordinates[1]}       {str(self.burger/2)}\n"
        output.write(new_line)
        for _ in range(3):
            line = f.readline()
            output.write(line)
        line = f.readline()
        coordinates = re.findall(r'[\d\.\d]+', line)
        new_line = f"{coordinates[0]}     {coordinates[1]}       {str(self.burger/2)}\n"
        output.write(new_line)
        output.write(f.read())
        f.close()
        output.close()
        os.remove(input_file)
    
    def toLammps(self) -> None:
        powerShell_Input = f"atomsk titledScrewMo.xsf titledScrewMo.lmp"
        os.system(f"powershell.exe {powerShell_Input}")
        os.remove("titledScrewMo.xsf")


    def changeComp(self) -> None:
        s = open("titledScrewMo.lmp", 'r')
        First_Part = ""
        while True:
            line = s.readline()
            if ("atom types" in line):
                First_Part = First_Part + line.replace('1', '4')
            elif ("Masses" in line) or ("1   95.96000000             # Mo" in line):
                continue
            else:
                First_Part = First_Part + line
            if ('atoms' in line):
                totalNum = int(re.findall("[0-9]+", line)[0])
            if ("Atoms # atomic" in line):
                First_Part = First_Part + '\n'
                break
        [Mo, Nb, Ta, _] = self.num_comp
        Mo, Nb, Ta = round(Mo*totalNum/100), round(Nb*totalNum/100), round(Ta*totalNum/100)
        df = pd.read_csv(s, header=None, delimiter=' +', engine='python')
        s.close()
        L_elements = df.index.tolist()
        random.shuffle(L_elements)
        L_Mo, L_Ta, L_Nb, L_W = L_elements[0:Mo], L_elements[Mo:(Mo+Ta)], L_elements[(Mo+Ta):(Mo+Ta+Nb)], L_elements[(Mo+Ta+Nb):]
        df.iloc[L_Mo, 1] = 1
        df.iloc[L_Nb, 1] = 2
        df.iloc[L_Ta, 1] = 3
        df.iloc[L_W,  1] = 4
        df.to_csv("tmp.lmp", header=None, index=None, sep=' ', mode='a')
        f_tmp = open("tmp.lmp", 'r')
        text_Second_part = f_tmp.read()
        f_tmp.close()
        f_write = open(self.output_path, 'w')
        text = First_Part + text_Second_part
        f_write.write(text)
        f_write.close()
        os.remove("tmp.lmp")
        os.remove("titledScrewMo.lmp")


# alloys = [[25, 10, 25, 40], [25, 25, 25, 25], [25, 40, 25, 10]]
# alloys = [[25, 25, 25, 25]]
# for alloy in alloys:
#     sd = screwDis(alloy)
#     sd.toRandom()