import logging
from collections import defaultdict

import numpy as np
from visdom import Visdom

from .meter import MovingAverage

LOGGER = logging.getLogger(__name__)


class Tracer(object):
    """Class for tracing traning history."""

    def __init__(self, env='main'):
        self.vis = Visdom(env=env)
        self._figure_ops = dict()
        self._registered_figures = dict()
        self._registered_lines = dict()
        self._history = dict(
            train=defaultdict(lambda: MovingAverage(win_size=50)),
            test=defaultdict(lambda: MovingAverage(win_size=1)),
        )

    def register_figure(self, title, xlabel, ylabel, trace_dict):
        """Register a new figure for visdom.

        keys in trace_dict must be unique acorss all figures.
        Parameters
        ----------
        title: figure titile
        xlabel, ylabe: name for x-axis and y-axis
        trace_dict: key-value pairs for traces/lines in figure
            trace_dict.values() are legends for the traces
            trace_dict.keys() are names for the traces
        the name has format 'phase.key'
        Return
        ------
        win: window id in current visdom environment

        """
        num_trace = len(trace_dict)
        legend = list(trace_dict.values())
        x = np.zeros(1)
        y = np.ones((1, num_trace)) * np.nan
        opts = dict(title=title, xlabel=xlabel, ylabel=ylabel, legend=legend)
        win = self.vis.line(X=x, Y=y, opts=opts)
        self._figure_ops[win] = opts
        self._registered_figures[win] = trace_dict
        for line_name in trace_dict:
            self._registered_lines[line_name] = win
        return win

    def resume(self, tracer):
        """Resume from another tracer."""
        self.__dict__.update(tracer.__dict__)
        old_win_ids = list(self._figure_ops.keys())
        for old_win in old_win_ids:
            opts = self._figure_ops[old_win]
            trace_dict = self._registered_figures[old_win]
            num_trace = len(trace_dict)
            new_win = self.vis.line(
                X=np.zeros(1),
                Y=np.ones((1, num_trace)) * np.nan,
                opts=opts,
            )
            self._figure_ops.pop(old_win)
            self._registered_figures.pop(old_win)
            self._figure_ops[new_win] = opts
            self._registered_figures[new_win] = trace_dict
            for line_name in trace_dict.keys():
                self._registered_lines[line_name] = new_win
        for line_name, win in self._registered_lines.items():
            phase, key = line_name.split('.')
            x, y = self._history[phase][key].numpy()
            legend = self._registered_figures[win][line_name]
            self.vis.line(X=x, Y=y, update='append', name=legend, win=win,
                          opts={'showlegend': True})

    def update(self, phase, x, **data):
        # update history
        history = self._history[phase]
        for key, value in data.items():
            # update history
            history[key].update(x, value)
            line_name = '{}.{}'.format(phase, key)
            # get figure id
            win = self._registered_lines.get(line_name, None)
            if win:
                legend = self._registered_figures[win][line_name]
                self.vis.line(
                    X=np.array([x]),
                    Y=np.array([history[key].avg]),
                    name=legend, win=win,
                    update='append',
                    opts={'showlegend': True}
                )

    def update_history(self, phase, x, **data):
        """Update the history only."""
        # update history
        history = self._history[phase]
        for key, value in data.items():
            # update history
            history[key].update(x, value)

    def update_trace(self, x, y, phase, key):
        """Update single trace only."""
        line_name = '{}.{}'.format(phase, key)
        win = self._registered_lines.get(line_name, None)
        if win:
            legend = self._registered_figures[win][line_name]
            self.vis.line(X=x, Y=y, update='append', name=legend, win=win,
                          opts={'showlegend': True})
