import cv2
import numpy as np
import pandas as pd
from pint import UnitRegistry


def to_timestamp(timestamp: str, to_unit='us'):
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    if "inf" in timestamp: timestamp = "inf s"
    return Q_(timestamp).to('us').magnitude


def to_unit_frame(image):
    if image.shape[2] == 1:
        image = np.dstack((image,)*3)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def to_datetime(timestamp, to_format="%S.%f"):
    return pd.to_datetime(timestamp, unit='us').strftime(to_format)
