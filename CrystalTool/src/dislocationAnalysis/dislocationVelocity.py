import numpy as np
import os
from tqdm import tqdm
from ovito.io import import_file
from ovito.modifiers import DislocationAnalysisModifier
import pandas as pd


def getPosition_OneCase(file_list: list[str]) -> tuple[list[float], float]:
    res = []
    for tmp in tqdm(file_list):
        time, curPos, lenX = getPosition_OneFrame(tmp)
        pos = list(np.mean(curPos, axis=0))
        res.append([time] + pos)
    return res, lenX


# get the position of dislocation at different timesteps and the length in x direction
def getPosition_OneFrame(filename: str):
    pipeline = import_file(filename, multiple_frames=True)
    modifier = DislocationAnalysisModifier()
    modifier.input_crystal_structure = DislocationAnalysisModifier.Lattice.BCC
    pipeline.modifiers.append(modifier)
    timestep = pipeline.compute().attributes['Timestep']
    data = pipeline.compute()
    len_x = pipeline.source.data.cell[:][0, 0]
    segment = findLongestDis(data.dislocations.segments)
    pos = segment.points
    return timestep, pos, len_x


def findLongestDis(segments):
    if len(segments) == 1:
        return segments[0]
    res = segments[0]
    for seg in segments:
        if (seg.length >= res.length):
            res = seg
    return res
    

def getDisVel(Pos: list[list[int, float, float, float]]) -> list[list[int, float, float, float, float]]:
    origin = Pos[0][1:]
    for i in Pos:
        curPos = i[1:]
        curDis = ((curPos[0] - origin[0]) ** 2 + (curPos[1] - origin[1]) ** 2) ** 0.5
        if (i[0] == 0):
            curVel = 0
        else:
            curVel = curDis / i[0] * 1000
        i.append(curDis)
        i.append(curVel)
    return Pos


def updatePos(Pos: list[int, float, float, float], lenX: float) -> list[int, float, float, float]:
    count = 0
    prev = None
    for i in Pos:
        cur = i[1]
        prev, cur, count = solveBoundary(prev, cur, lenX, count)
        i[1] = cur
    return Pos


def solveBoundary(prev: float, cur: float, lenX: float, count: int) -> float:
    if (count != 0) and (cur > prev - lenX * 0.2):
        return cur, cur, count
    cur += count * lenX
    if (not prev):
        return cur, cur, count
    if (cur + lenX / 2 < prev):
        cur += lenX
        count += 1
    return cur, cur, count


def disVel(file_list: list[str]) -> list[list[int, float, float, float, float]]:
    res, lenX = getPosition_OneCase(file_list)
    res = updatePos(res, lenX)
    res = getDisVel(res)
    return res


