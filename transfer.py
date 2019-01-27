"""Transfer utils."""
from collections import deque

import numpy as np


def smooth(xs, average=10):
    """Average smooth for 1d signal."""
    weights = np.ones(average) / average
    data = np.convolve(xs, weights, mode='valid')
    pre = _smooth(xs[:average - 1], average)
    return np.hstack((pre, data))


def _smooth(xs, average=10):
    x_buffer = []
    s_xs = 0
    xs = np.array(xs) * 1.0
    smoothed_xs = np.zeros_like(xs)
    num = xs.size
    for i in range(num):
        x = xs[i]
        if len(x_buffer) < average:
            x_buffer.append(x)
            size = len(x_buffer)
            s_xs = (s_xs * (size - 1) + x) / size
            smoothed_xs[i] = s_xs
        else:
            idx = i % average
            s_xs += (x - x_buffer[idx]) / average
            x_buffer[idx] = x
            smoothed_xs[i] = s_xs
    return smoothed_xs


class MovingAverage(object):
    """Compute moving average."""

    def __init__(self, win_size=50):
        """Average meter for criterions."""
        self.val = 0
        self.smooth = deque(maxlen=win_size)

    def reset(self, history=None):
        """Reset all attribute."""
        self.val = 0
        self.smooth.clear()
        if history:
            for val in history:
                self.update(val)

    @property
    def avg(self):
        """Return moving average."""
        try:
            return sum(self.smooth) / len(self.smooth)
        except ZeroDivisionError:
            return np.NaN

    def update(self, val):
        """Update attributes."""
        self.smooth.append(val)
        self.val = val

    def __repr__(self):
        """Return val and avg."""
        return '{:.4f} ({:.4f})'.format(self.val, self.avg)


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
