import numpy as np
import pickle
import pandas as pd
import os.path as osp

from dv import AedatFile
import numpy.lib.recfunctions as rfn
from scipy.io import savemat

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
        elif extention == '.txt':
            return Load.from_txt(path)
        elif extention == '.pkl':
            return Load.from_pkl(path)

        raise ValueError(f"not support typy of {extention}")

    @staticmethod
    def from_aedat4(path: str) -> Data:
        data = Data()
        with AedatFile(path) as f:
            # events
            if 'events' in f.names:
                array_ev = np.hstack([packet for packet in f['events'].numpy()])
                array_ev = rfn.structured_to_unstructured(array_ev)[..., :4]
                data['events'] = Event(array_ev)

            # frames
            if 'frames' in f.names:
                array_fr = [(frame.timestamp, to_unit_frame(frame.image))
                            for frame in f['frames']]
                data['frames'] = Frame(array_fr)

            # size
            data['size'] = f['events'].size

        return data

    @staticmethod
    def from_txt(path: str) -> Data:
        data = Data()
        with open(path, "r+") as f:
            data['size'] = Size(np.loadtxt(f, max_rows=1))

            # events
            array_ev = pd.read_csv(f, sep='\s+', header=None).values
            data['events'] = Event(array_ev)

        return data
    
    
    @staticmethod
    def from_pkl(path: str) -> Data:
        data = Data()
        with open(path, "rb+") as f:
            pkl_dict = pd.read_pickle(f)

        # events
        if 'events' in pkl_dict.keys():
            data['events'] = Event(pkl_dict['events'])

        # frames
        if 'frames' in pkl_dict.keys():
            data['frames'] = Frame(pkl_dict['frames'])

        # size
        if 'size' in pkl_dict.keys():
            data['size'] = Size(pkl_dict['size'])

        return data


class Save:
    @staticmethod
    def to_file(data: Data, path):
        *_, extention = _split_file(path)

        if extention == '.aedat4':
            pass
        elif extention == '.txt':
            return Save.to_txt(data, path)
        elif extention == '.mat':
            return Save.to_mat(data, path)
        elif extention == '.pkl':
            return Save.to_pkl(data, path)

    @staticmethod
    def to_txt(data: Data, path):
        with open(path, 'wt') as f:
            f.write('%3d %3d\n' % data['size'])
        with open(path, 'at') as f:
            np.savetxt(f, rfn.structured_to_unstructured(data['events']),
                       fmt='%16d %3d %3d %1d', delimiter=' ', newline='\n')    

    @staticmethod
    def to_mat(data: Data, path):
        class Struct:
            pass

        # events
        events = Struct()
        if 'events' in data.keys():
            events.timestamp = data['events'].timestamp
            events.x = data['events'].x
            events.y = data['events'].y
            events.polarity = data['events'].polarity

        # frames
        frames = Struct()
        if 'frames' in data.keys():
            frames.timestamp = data['frames'].timestamp
            frames.image = data['frames'].image

        savemat(path, {'events': events, 'frames': frames,
                        'sizeX': data['size'][0], 'sizeY': data['size'][1]})
        
    @staticmethod
    def to_pkl(data: Data, path):
        with open(path, 'wb+') as f:
            pickle_dict = dict(size=data['size'])

            # events
            if 'events' in data.keys():
                pickle_dict['events'] = data['events']

            # frames
            if 'frames' in data.keys():
                pickle_dict['frames'] = data['frames']

            # size
            if 'size' in data.keys():
                pickle_dict['size'] = data['size']

            pickle.dump(pickle_dict, f)


class DvsFile:
    @staticmethod
    def load(path) -> Data:
        return Load.from_file(path)

    @staticmethod
    def save(data: Data, path) -> Data:
        Save.to_file(data, path)
