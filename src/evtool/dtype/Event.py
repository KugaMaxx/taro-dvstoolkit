from ._package import *
from scipy.ndimage import median_filter
import cv2


def histogram(x, y, weight, size):
    _bins  = [size[0], size[1]]
    _range = [[0, size[0]], [0, size[1]]]
    return np.histogram2d(x, y, weights=weight, bins=_bins, range=_range)[0]


class Event(np.recarray):
    """
    Generate events

    Receives
    --------
    A list of tuples,
        refer to https://numpy.org/doc/stable/user/basics.rec.html

    Returns
    -------
    A numpy.recarray of events
    """

    def __new__(cls, array=None):
        dtype = np.dtype({'names':   ['timestamp', 'y', 'x', 'polarity'], 
                          'formats': ['<i8', '<i2', '<i2', 'i1'], 
                          'offsets': [0, 8, 10, 12], 'itemsize': 16})
        # dtype = np.dtype([('ts', '<M8[us]'), ('y', '<i2'), ('x', '<i2'), ('p', 'i1')])
        if array is None:
            structured_array = np.array([], dtype)
        elif array.dtype.names is None:
            structured_array = rfn.unstructured_to_structured(array, dtype).view(Event)
        elif array.dtype.names is not None:
            structured_array = array.astype(dtype).view(Event)
        return structured_array

    def to_array(self):
        return rfn.structured_to_unstructured(self)

    def slice(self, t) -> Iterator[Tuple[Any, Self]]:
        delta_t = to_timestamp(t)
        ts_bin = np.arange(self.timestamp[0], self.timestamp[-1], delta_t).astype(np.int64)
        index = np.searchsorted(self.timestamp, ts_bin[1:])
        return zip(ts_bin, [ev for ev in np.split(self, index)])

    def project(self, size, mode='accumulate'):
        if mode == 'accumulate':
            counts = histogram(self.x, self.y, (-1) ** (1 + self.polarity), size)
            return counts

        elif mode == 'monopolar':
            counts = histogram(self.x, self.y, (+1) ** (1 + self.polarity), size)
            return counts

        elif mode == 'bipolar':
            pos_index = self.polarity == 1
            neg_index = self.polarity == 0
            pos_counts = histogram(self.x[pos_index], self.y[pos_index], (+1) ** (1 + self.polarity[pos_index]), size)
            neg_counts = histogram(self.x[neg_index], self.y[neg_index], (-1) ** (1 + self.polarity[neg_index]), size)
            return pos_counts, neg_counts

        return None
    
    def hotpixel(self, size, thres=300):
        counts = histogram(self.x, self.y, np.ones(self.polarity.shape), size)
        seeker = np.where((counts - median_filter(counts, 3)).flatten() >= thres)
        idx = ~np.in1d(np.ravel_multi_index((self.x, self.y), size), seeker)
        return idx
        

    def __repr__(self):
        return str(self.dtype)
