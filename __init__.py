"""Mode utility."""
import torch

# mode metrics
from . import math, meter, metrics, tracer, check
# mode datafile
from .datafile import resize_image

_COLORS = dict(
    Red='\033[91m',
    Green='\033[92m',
    Blue='\033[94m',
    Cyan='\033[96m',
    White='\033[97m',
    Yellow='\033[93m',
    Magenta='\033[95m',
    Grey='\033[90m',
    Black='\033[90m',
    Default='\033[0m',
)


def colour(string, color='Green'):
    """Add color for string."""
    color = _COLORS.get(color.capitalize(), 'Default')
    result = '{}{}{}'.format(color, string, _COLORS['Default'])
    return result


def get_named_class(module):
    """Get the class member in module."""
    from inspect import isclass
    return {k: v for k, v in module.__dict__.items() if isclass(v)}


def one_hot(uidx, num):
    """Convert the index to one-hot encoding."""
    uidx = uidx.view(-1, 1)
    return torch.zeros(uidx.numel(), num).scatter_(1, uidx, 1.0)


def get_device(gpus):
    """Get device from gpus information.

    Returns
    -------
    parallel: True if len(gpus) > 1
    device: if parallel then device is cpu.
    """
    if len(gpus) > 1:
        parallel = True
        device = torch.device('cpu')
    else:
        parallel = False
        device = torch.device(gpus[0])
    return parallel, device


def to_device(data, device):
    """Move data to device."""
    from collections import Sequence
    error_msg = "data must contain tensors or lists; found {}"
    if isinstance(data, Sequence):
        return tuple(to_device(v, device) for v in data)
    elif isinstance(data, torch.Tensor):
        return data.to(device)
    raise TypeError((error_msg.format(type(data))))


def config_log(stream_level='DEBUG', file_level='INFO', log_file=None):
    """Config logging with dictConfig.
    Parameters
    ----------
    log_file: log file
    stream_level: logging level for STDOUT
    file_level: logging level for log file
    """
    import tempfile
    from logging.config import dictConfig
    if log_file is None:
        _, log_file = tempfile.mkstemp()
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '[%(levelname)s] - %(asctime)s - '
                          '[%(name)s.%(funcName)s:%(lineno)d]: %(message)s',
                'datefmt': '%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'stream': {  # config stream handler
                'class': 'logging.StreamHandler',
                'level': stream_level,
                'formatter': 'simple',
            },
            'file': {  # config file handler
                'class': 'logging.FileHandler',
                'level': file_level,
                'formatter': 'simple',
                'filename': log_file,
            }
        },
        'loggers': {
            'main': {  # main logger
                'handlers': ['stream', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
        'root': {  # root logger
            'level': 'DEBUG',
            'handlers': ['stream', 'file']
        },
    })
    return log_file


__all__ = [
    'math',
    'check',
    'tracer',
    'meter',
    'metrics',
]
