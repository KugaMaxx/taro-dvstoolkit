import numpy as np
import numpy.lib.recfunctions as rfn

from typing import Any, Union, Iterator, Iterable, List, Tuple, TypeVar

from evtool.utils.func import to_timestamp

KT = TypeVar("KT")
VT = TypeVar("VT")
Self = TypeVar('Self')
