import numpy as np
import pandas as pd
from pint import UnitRegistry


def to_timestamp(timestamp: str, to_unit='us'):
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    if "inf" in timestamp: timestamp = "inf s"
    return Q_(timestamp).to('us').magnitude


def to_unit_frame(image):
    return np.dstack((image,)*3)


def to_datetime(timestamp, to_format="%S.%f"):
    return pd.to_datetime(timestamp, unit='us').strftime(to_format)
