import os, sys, time
import os.path as osp
from evtool.dvs import DvsFile
from evtool.utils import Player

root = osp.dirname(__file__)
print('--------------------------------')

st = time.time()
file = '../data/test-01.aedat4'
data = DvsFile.load(osp.join(root, file))
print('loading: %s' % file)
print('time of load file: %f \n' % (time.time() - st))

st = time.time()
p = Player(data, core='matplotlib')
print('waiting for creating visualization, core: %s' % p.core)
p.view("25ms", use_aps=True)
print('time of creating visualization window: %f' % (time.time() - st))
