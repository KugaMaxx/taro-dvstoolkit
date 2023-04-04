import os
import sys
import time
import os.path as osp
from evtool.dvs import DvsFile
from evtool.utils import Player


root = osp.dirname(__file__)

st = time.time()
data = DvsFile.load(osp.join(root, '../data/test-01.aedat4'))

st = time.time()
data['events'] = data['events'].shot_noise(data['size'], rate=5, down_sample=0.9) # TODO add_leak_noise()
print('time to generate shot noise: %.5f' % (time.time() - st))

p = Player(data, core='matplotlib')
p.view("25ms", use_aps=True)
