from .func import to_timestamp, to_datetime
from evtool.dtype import Event, Frame, Size

from ._player import go_player as gop
from ._player import mpl_player as mlp


class Player(object):
    def __init__(self, data=None, core='matplotlib', max_sample=300000):
        self.data = data
        self.core = core
        self.max_sample = max_sample

    def _init_package(self, duration):
        figure, preset = None, None
        if self.core == 'plotly':
            figure, preset = gop.Figure(), gop.Preset(self.data, duration, self.max_sample)
        elif self.core == 'matplotlib':
            figure, preset = mlp.Figure(), mlp.Preset(self.data, duration, self.max_sample)
        figure.set_ticks(preset.get_ticks())
        return figure, preset

    def view(self, duration='inf', use_aps=True):
        fig, pre = self._init_package(duration)
        fig.set_subplot(rows=1, cols=2, specs=[[{"type": "2d"}, {"type": "3d"}]])
        fig.append_trace(row=1, col=1, func=pre.plot_2d_frame, kwargs=pre.set_2d_plot) if use_aps else None
        fig.append_trace(row=1, col=1, func=pre.plot_2d_event, kwargs=pre.set_2d_plot)
        fig.append_trace(row=1, col=2, func=pre.plot_3d_frame, kwargs=pre.set_3d_plot) if use_aps else None
        fig.append_trace(row=1, col=2, func=pre.plot_3d_event, kwargs=pre.set_3d_plot)
        fig.show()

    def view_2d(self, duration="inf", use_aps=True):
        fig, pre = self._init_package(duration)
        fig.set_subplot(rows=1, cols=1, specs=[[{"type": "2d"}]])
        fig.append_trace(row=1, col=1, func=pre.plot_2d_frame, kwargs=pre.set_2d_plot) if use_aps else None
        fig.append_trace(row=1, col=1, func=pre.plot_2d_event, kwargs=pre.set_2d_plot)
        fig.show()

    def view_3d(self, duration='inf', use_aps=True):
        fig, pre = self._init_package(duration)
        fig.set_subplot(rows=1, cols=1, specs=[[{"type": "3d"}]])
        fig.append_trace(row=1, col=1, func=pre.plot_3d_frame, kwargs=pre.set_3d_plot) if use_aps else None
        fig.append_trace(row=1, col=1, func=pre.plot_3d_event, kwargs=pre.set_3d_plot)
        fig.show()
