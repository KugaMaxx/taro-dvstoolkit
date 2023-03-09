import numpy as np
import pandas as pd
import os.path as osp

from dv import AedatFile
import numpy.lib.recfunctions as rfn

from evtool.utils.func import to_unit_frame
from evtool.dtype import Event, Frame, Size, Data


def _split_file(path):
    root, file = osp.split(path)
    name, ext = osp.splitext(file)
    return root, name, ext


class Load:
    @staticmethod
    def from_file(path: str):
        *_, extention = _split_file(path)

        if extention == '.aedat4':
            return Load.from_aedat4(path)
        if extention == '.txt':
            return Load.from_txt(path)

        raise ValueError(f"not support typy of {extention}")

    @staticmethod
    def from_aedat4(path: str) -> Data:
        data = Data()
        with AedatFile(path) as f:
            data['size'] = Size(f['events'].size)

            # events
            if 'events' in f.names:
                array_ev = np.hstack([packet for packet in f['events'].numpy()])
                array_ev = rfn.structured_to_unstructured(array_ev)[..., :4]
                data['events'] = Event(array_ev)

            # frames
            if 'frames' in f.names:
                array_fr = [(frame.timestamp, to_unit_frame(frame.image)) for frame in f['frames']]
                data['frames'] = Frame(array_fr)

        return data

    @staticmethod
    def from_txt(path: str) -> Data:
        data = Data()
        with open(path, "r+") as f:
            data['size'] = Size(np.loadtxt(f, max_rows=1))

            # events
            array_ev = pd.read_csv(f, sep='\s+', header=None).values
            data['events'] = Event(array_ev)

            # frames
            data["frames"] = Frame()

        return data


class Save:
    @staticmethod
    def to_file(data: Data, path):
        *_, extention = _split_file(path)

        if extention == '.aedat4':
            pass
        elif extention == '.txt':
            return Save.to_txt(data, path)

    @staticmethod
    def to_txt(data: Data, path):
        with open(path, 'wt') as f:
            f.write('%3d %3d\n' % data['size'])
        with open(path, 'at') as f:
            np.savetxt(f, rfn.structured_to_unstructured(data['events']),
                       fmt='%16d %3d %3d %1d', delimiter=' ', newline='\n')


class DvsFile:
    @staticmethod
    def load(path) -> Data:
        return Load.from_file(path)

    def save(self) -> Data:
        pass
