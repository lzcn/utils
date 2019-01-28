"""Transfer utils."""
from collections import deque

import numpy as np


def smooth(xs, win_size=10):
    """Average smooth for 1d signal."""
    if len(xs) < win_size:
        return _smooth(xs, win_size)
    weights = np.ones(win_size) / win_size
    data = np.convolve(xs, weights, mode='valid')
    pre = _smooth(xs[:win_size - 1], win_size)
    return np.hstack((pre, data))


def _smooth(xs, win_size=10):
    """Slow verison."""
    x_buffer = []
    s_xs = 0
    xs = np.array(xs) * 1.0
    smoothed_xs = np.zeros_like(xs)
    num = xs.size
    for i in range(num):
        x = xs[i]
        if len(x_buffer) < win_size:
            x_buffer.append(x)
            size = len(x_buffer)
            s_xs = (s_xs * (size - 1) + x) / size
            smoothed_xs[i] = s_xs
        else:
            idx = i % win_size
            s_xs += (x - x_buffer[idx]) / win_size
            x_buffer[idx] = x
            smoothed_xs[i] = s_xs
    return smoothed_xs


class MovingAverage(object):
    """History recorder with moving average."""

    def __init__(self, win_size=50):
        """Average meter for criterions."""
        self.x = []
        self.y = []
        self.val = np.nan
        self._queue = deque(maxlen=win_size)
        self._smooth = False if win_size == 1 else True
        self.win_size = win_size

    def reset(self,):
        """Reset all attribute."""
        self.val = np.nan
        self.x = []
        self.y = []
        self._queue.clear()

    @property
    def avg(self):
        """Return moving average."""
        try:
            return sum(self._queue) / len(self._queue)
        except ZeroDivisionError:
            return np.nan

    def update(self, x, y):
        """Update attributes."""
        self.x.append(x)
        self.y.append(y)
        self._queue.append(y)
        self.val = y

    def numpy(self):
        """Retrun smoothed numpy history until now."""
        x = np.array(self.x)
        if self._smooth:
            y = smooth(self.y, self.win_size)
        else:
            y = np.array(self.y)
        return x, y

    def __repr__(self):
        """Return val and avg."""
        if self._smooth:
            msg = '{:.4f} ({:.4f})'.format(self.val, self.avg)
        else:
            msg = '{:.4f}'.format(self.val)
        return msg


class TrainMeter(object):
    """Compute moving average."""

    def __init__(self, win_size=50):
        """Average meter for criterions."""
        self.x, self.y = [], []
        self.pre = np.NaN
        self.win_size = win_size
        self.data = deque(maxlen=win_size)

    def numpy(self):
        """Retrun smoothed numpy history until now."""
        x = np.array(self.x)
        y = smooth(self.y, self.win_size)
        return x, y

    def reset(self):
        """Reset all attribute."""
        self.pre = np.NaN
        self.x, self.y = [], []
        self.data.clear()

    @property
    def val(self):
        """Return moving average value."""
        try:
            return sum(self.data) / len(self.data)
        except ZeroDivisionError:
            return np.NaN

    def update(self, x, val):
        """Update attributes."""
        self.x.append(x)
        self.y.append(val)
        self.data.append(val)
        self.pre = val

    def __repr__(self):
        """Return val and avg."""
        return '{:.4f} ({:.4f})'.format(self.pre, self.val)


class TestMeter(object):
    """Compute moving average."""

    def __init__(self):
        """History without moving average."""
        self.weights = []
        self.val = np.NaN
        self.x, self.y = [], []

    def numpy(self):
        """Retrun history until now as numpy array."""
        x = np.array(self.x)
        y = np.array(self.y)
        return x, y

    @property
    def avg(self):
        """Return fake average."""
        v, w = np.array(self.y), np.array(self.weights)
        return np.sum(v * w) / np.sum(w)

    def sum(self):
        return np.sum(self.y)

    def update(self, x, val, weight=1):
        """Update attributes."""
        self.x.append(x)
        self.y.append(val)
        self.weights.append(weight)
        self.val = val

    def __repr__(self):
        """Return val and avg."""
        return '{:.4f}'.format(self.val)
