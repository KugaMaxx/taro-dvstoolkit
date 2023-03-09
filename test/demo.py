import os, sys, time
import os.path as osp
from evtool.dvs import DvsFile


root = osp.dirname(__file__)

st = time.time()
data = DvsFile.load(osp.join(root, '../data/test-01.aedat4'))
print(f"load aedat4 file ==> {time.time() - st:.5f} s")

st = time.time()
data = DvsFile.load(osp.join(root, '../data/test-02.txt'))
print(f"load txt file    ==> {time.time() - st:.5f} s")
