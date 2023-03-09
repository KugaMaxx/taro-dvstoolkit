import numpy as np
from abc import ABC, abstractmethod
from evtool.dtype import Event, Frame, Size


def _unravel_index(index, shape):
    row, col = np.unravel_index(index, shape)
    return row, col


def _ravel_multi_index(row, col, shape):
    ind = np.ravel_multi_index(np.array([row, col]), shape)
    return ind


def _reformat_layout(list_of_dict, mapping: dict):
    for _list in list_of_dict:
        for _dict in _list:
            _dict['type'] = mapping[_dict['type']]

    return list_of_dict
