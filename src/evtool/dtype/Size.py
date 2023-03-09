from ._package import *


class Size(tuple):
    def __new__(cls, array):
        if array is None:
            return tuple(260, 346)
        elif type(array) is tuple:
            return array
        elif type(array) is np.ndarray:
            return tuple(array.astype(np.int_).tolist())

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
