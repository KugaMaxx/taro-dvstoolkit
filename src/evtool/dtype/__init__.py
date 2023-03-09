from .Event import Event
from .Frame import Frame
from .Size import Size

from typing import TypedDict

__all__ = ['Data', 'Event', 'Frame', 'Size']


class Data(TypedDict):
    events: Event
    frames: Frame
    size:   Size
