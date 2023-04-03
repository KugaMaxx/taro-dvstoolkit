import numpy as np
import plotly.graph_objects as go

from evtool.utils.func import to_datetime, to_timestamp
from evtool.dtype import Event, Frame, Size
from ._func import _reformat_layout


class Animator(object):
    def __init__(self, canvas, update, ticks, fps=25):
        self._canvas = canvas
        self._frames = [update(i) for i in range(len(ticks))]
        self._ticks = ticks
        self._interval = int(1E3 / fps)
        self._init_widgets()

    def _init_widgets(self):
        self._buttons = [{
            "type": "buttons",
            "buttons": [
                {
                    "method": "animate", "label": "&#9654;",
                    "args": [None, {"frame": {"duration": self._interval},
                                    "mode": "immediate", "fromcurrent": True}]
                },
                {
                    "method": "animate", "label": "&#9724;",
                    "args": [[None], {"frame": {"duration": self._interval},
                                      "mode": "immediate", "fromcurrent": True}]
                }
            ],
            "x": 0.1, "y": 0.0, "direction": "left", "pad": {"r": 10, "t": 70},
        }]

        self._sliders = [{
            "steps": [
                {
                    "method": "animate", "label": self._ticks[i],
                    "args": [[self._ticks[i]], {"frame": {"duration": self._interval},
                                          "mode": "immediate", "fromcurrent": True}]
                } for i, val in enumerate(self._frames)
            ],
            "x": 0.1, "y": 0.0, "len": 0.9, "pad": {"b": 10, "t": 50},
        }]
        self._canvas.layout.update(
            sliders=self._sliders,
            updatemenus=self._buttons,
            template="plotly_white",
        )

    def run(self):
        self._canvas.update(frames=self._frames)
        self._canvas.show()


class Figure(object):
    def __init__(self):
        self._figure = go.Figure()
        self._traces = {
            "inds": list(),
            "rows": list(),
            "cols": list(),
            "func": list(),
            "kwargs": list(),
        }

        self._index = 0
        self._nrows = 0
        self._ncols = 0
        self._shape = (0, 0)
        self._layouts = None
        self._ticks = range(1)

    def set_ticks(self, ticks):
        self._ticks = ticks

    def set_subplot(self, rows, cols, specs):
        self._nrows = rows
        self._ncols = cols
        self._shape = (rows, cols)
        self._layouts = _reformat_layout(specs, {'2d': 'xy', '3d': 'scene'})

    def append_trace(self, row, col, func, kwargs):
        self._index = self._index + 1
        self._traces["rows"].append(row)
        self._traces["cols"].append(col)
        self._traces["func"].append(func)
        self._traces["kwargs"].append(kwargs)
        self._traces["inds"].append(self._index - 1)

    def show(self):
        self._figure.set_subplots(rows=self._nrows, cols=self._ncols, specs=self._layouts)
        self._figure.add_traces(data=[func() for func in self._traces["func"]],
                                rows=self._traces["rows"], cols=self._traces["cols"])
        for kwargs in self._traces["kwargs"]:
            self._figure.layout.update(**kwargs())

        Animator(canvas=self._figure, update=self._update, ticks=self._ticks).run()

    def _update(self, k):
        return go.Frame(data=[func(k) for func in self._traces["func"]],
                        traces=self._traces["inds"], name=self._ticks[k])


class Preset(object):
    def __init__(self, data, duration, max_sample=300000):
        """
        Create a Figure() class with default settings

        Receives
        --------
        data
            The 'data' property is defined in evtool.dtype
        duration
            The 'duration' property helps divide the events into
            non-overlapping consecutive groups according to a certain time
        max_sample
            The 'max_sample' determines the max number of events can
            be displayed in 3d visualization. Otherwise, it may fail to
            correctly draw.
        """
        self._events: Event = data['events'] if 'events' in data.keys() else None
        self._frames: Frame = data['frames'] if 'frames' in data.keys() else None
        self._size:   Size  = data['size']   if 'size'   in data.keys() else (260, 346)
        self._packet: list  = [(ts, ev) for ts, ev in self._events.slice(duration)]
        self._delta_t = to_timestamp(duration) if 'inf' not in duration else self._events.timestamp[-1] - self._events.timestamp[0]
        self._ticks = [f'{to_datetime(ts)[:-4]}s' for ts, _ in self._packet]
        
        self._events.x = self._size[0] - self._events.x - 1
        self._frames.image = np.flip(self._frames.image, axis=1)

        self._max_sampler = lambda x: x[::np.ceil(len(x)/max_sample).astype(int)]
        self._fr_colormap = 'gray'
        self._ev_colormap = [[0.0, "rgba(223,73,63,1)"],
                             [0.5, "rgba(0,0,0,0)"],
                             [1.0, "rgba(46,102,153,1)"]]

    # ---------------- 2d settings ----------------
    def set_2d_plot(self):
        return {
            "xaxis": dict(range=[0, self._size[1]]),
            "yaxis": dict(range=[0, self._size[0]],
                          scaleanchor="x",
                          scaleratio=1.),
        }

    def plot_2d_event(self, i=None):
        if i is None:
            obj = go.Heatmap(
                z=[], zmin=-1, zmax=1,
                colorscale=self._ev_colormap,
                showscale=False,
                showlegend=False,
            )
        else:
            ts, data = self._packet[i]
            obj = go.Heatmap(
                z=data.project(self._size),
            )
        return obj

    def plot_2d_frame(self, i=None):
        if i is None:
            obj = go.Image(
                z=[],
            )
        else:
            ts, _ = self._packet[i]
            closest_id = self._frames.find_closest(ts)
            data = self._frames.image[closest_id]
            obj = go.Image(
                z=data,
            )
        return obj

    # ---------------- 3d settings ----------------
    def set_3d_plot(self):
        return {
            "scene": dict(xaxis=dict(range=[0, self._size[0]]),
                          yaxis=dict(range=[0, self._size[1]]),
                          aspectratio=dict(x=self._size[0]/500, y=self._size[1]/500, z=1.),
                          camera=dict(up=dict(x=1.0, y=0.0, z=0.0))),
        }

    def plot_3d_event(self, i=None):
        if i is None:
            obj = go.Scatter3d(
                x=[], y=[], z=[],
                mode='markers',
                marker=dict(
                    size=2,
                    cmin=0,
                    cmax=1,
                    colorscale=self._ev_colormap,
                ),
                showlegend=False,
            )
        else:
            ts, data = self._packet[i]
            data = self._max_sampler(data)
            obj = go.Scatter3d(
                x=data.x, y=self._size[1]-data.y-1, z=to_datetime(data.timestamp),
                marker=dict(color=data.polarity),
            )
        return obj

    def plot_3d_frame(self, i=None):
        if i is None:
            obj = go.Surface(
                x=[], y=[], z=[],
                surfacecolor=np.ones((1000, 1000)),
                colorscale=self._fr_colormap,
                cmin=0,
                cmax=255,
                showscale=False,
                showlegend=False,
            )
        else:
            ts, _ = self._packet[i]
            closest_id = self._frames.find_closest(ts)
            data = self._frames.image[closest_id]
            xx, yy = np.mgrid[0:self._size[0], 0:self._size[1]]
            obj = go.Surface(
                x=xx,
                y=yy,
                z=np.full(self._size, to_datetime(ts)),
                surfacecolor=np.flip(data[..., 0], axis=1)
            )
        return obj

    def get_ticks(self):
        return self._ticks
