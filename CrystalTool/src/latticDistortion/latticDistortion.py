from ovito.io import import_file
from ovito.data import NearestNeighborFinder
import numpy as np
from tqdm import tqdm


class LatticDistortion:
    def __init__(self, file: str) -> None:
        pipeline = import_file(file)
        self.data = pipeline.compute()
        self.finder = NearestNeighborFinder(8, self.data)


class LD_Local(LatticDistortion):        
    def getLD(self) -> list[float]:
        local_LD = []
        for idx in tqdm(range(self.data.particles.count)):
            tmp = self.getLocalLD(idx)
            local_LD.append(tmp)
        return local_LD

    def getLocalLD(self, idx: int) -> float:
        raise NotImplementedError


class LD_Local_std(LD_Local):    
    def getLocalLD(self, idx: int) -> float:
        local_ld = []
        for neigb in self.finder.find(idx):
            local_ld.append(neigb.distance)
        return np.std(local_ld)