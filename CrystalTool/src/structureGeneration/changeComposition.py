import re, random, os
import pandas as pd

def changeComp(input_path: str, output_path: str, num_comp: list[int]) -> None:
    s = open(input_path, 'r')
    First_Part = ""
    while True:
        line = s.readline()
        if ("Masses" in line) or ("1   95.96000000             # Mo" in line):
            continue
        else:
            First_Part = First_Part + line
        if ('atoms' in line):
            totalNum = int(re.findall("[0-9]+", line)[0])
        if ("Atoms # atomic" in line):
            First_Part = First_Part + '\n'
            break
    [Mo, Nb, Ta, _] = num_comp
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
    f_write = open(output_path, 'w')
    text = First_Part + text_Second_part
    f_write.write(text)
    f_write.close()
    os.remove("tmp.lmp")
    # os.remove("titledScrewMo.lmp")