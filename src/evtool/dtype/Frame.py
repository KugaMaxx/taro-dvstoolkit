from ._package import *


class Frame(np.recarray):
    def __new__(cls, array=None):
        image_shape = array[0][1].shape if array is not None else (1, 1, 1)
        dtype = np.dtype([('timestamp', '<i8'), ('image', 'i2', image_shape)])
        # dtype = np.dtype([('ts', '<M8[us]'), ('image','i2', list_of_tuple[0][1].shape)])
        if array is None:
            structured_array = np.array([], dtype)
        elif type(array) is list:
            structured_array = np.asarray(array, dtype).view(Frame)
        elif array.dtype.names is not None:
            structured_array = array.astype(dtype).view(Frame)
        structured_array = np.sort(structured_array, order='timestamp')
        return structured_array

    def find_closest(self, t):
        # idx = np.argmin(np.abs(self['ts'] - t)).astype(int)
        idx = np.searchsorted(self.timestamp, t)
        if idx >= len(self):
            idx = len(self) - 1
        return idx

    def __repr__(self) -> str:
        return str(self.dtype)
