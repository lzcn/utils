"""
The :mod:`utils.progress` module.

Module includes utils for progress like ProgressBar.
"""
import sys
from time import time
from collections import deque


class ProgressBar(object):
    """Class for progress bar."""

    # configuration of ProgressBar
    info = '%(now)d/%(max)d'
    # the width of progress bar
    width = 28
    # the full mark in progress bar
    full = '#'
    # the empty mark in progress bar
    empty = ' '
    # prefix and suffix to define marks
    prefix = ' |'
    suffix = '| '
    # windos size of moving average for computing the speed
    smooth_window = 100

    def __init__(self, size=1, message="Progress bar", **kwargs):
        """Customize a progress bar.

        Parameters
        ----------
        size: total size of progress.
        message: Customized message before progress bar.
        width: the length of progress bar.
        full, empty: marker types

        """
        assert (size > 0), 'None-negative size'
        # the message before the progress bar
        self._mesg = '\r' + message
        # current step
        self._current_iter = 0
        # max iterations
        self._max_iter = size
        # time queue for moving average
        self._time_queue = deque(maxlen=self.smooth_window + 1)
        self._time_queue.append(time())
        # update configurations or ser other attributes for progress bar
        for key, value in kwargs.items():
            self[key] = value

    @property
    def max(self):
        """Maximun iterations, i.e. the size of progress."""
        # read only for max iteration
        return self._max_iter

    @property
    def now(self):
        """Return current iteration."""
        return self._current_iter

    def __getitem__(self, key):
        """Get attribute by self[key]."""
        if key.startswith('_'):
            return None
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        """Set attribute."""
        if not key.startswith('_'):
            setattr(self, key, value)

    def line(self):
        """Get current line.

        Format: e.g message |#####     | 0/1(1.0e+00s/iter).
        """
        full_size = int(1. * self.width * self.now / self.max)
        empty_size = self.width - full_size
        full = self.full * full_size
        empty = self.empty * empty_size
        # customized message
        mesg = self._mesg % self
        info = self.info % self
        now = time()
        self._time_queue.append(now)
        elapsed_time = self._time_queue[-1] - self._time_queue[0]
        second_per_iter = 1. * elapsed_time / (len(self._time_queue) - 1)
        speed = '({:.2e}s/iter)'.format(second_per_iter)
        line = ''.join(
            [mesg, self.prefix, full, empty, self.suffix, info, speed])
        # drop the very first time
        if self._current_iter == 1:
            self._time_queue.popleft()
        return line

    def reset(self, size=None, message=None, **kwargs):
        """Reset the state of progress bar."""
        if size is not None:
            self._max_iter = size
        if message is not None:
            self._mesg = '\r' + message
        # set other customized attributes
        for key, value in kwargs.items():
            self[key] = value
        self._current_iter = 0
        self._time_queue.clear()
        self._time_queue.append(time())

    def __iter__(self):
        """Get iterator.

        Example:
            >> progress = ProgressBar(size)
            >> for i in progress:
                   run()
               progress.end()
        """
        return self

    def next(self):
        """Next state for iterator."""
        if self.now < self.max:
            self._current_iter += 1
            sys.stdout.write(self.line())
            sys.stdout.flush()
            return self.now - 1
        else:
            raise StopIteration()

    def end(self):
        """End a progress bar.

        After finish, call ProgressBar.end().
        """
        sys.stdout.write('\n')

    def forward(self):
        """Move forward."""
        self.next()
