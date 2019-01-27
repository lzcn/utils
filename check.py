"""Check utils mod."""
import os

import logging
LOGGER = logging.getLogger(__name__)


def check_dirs(folders, action='check', mode='all', verbose=False):
    """Check whether all folders exist."""
    falgs = []
    if action.lower() not in ['check', 'mkdir']:
        raise ValueError("{} not in ['check', 'mkdir']".format(action.lower()))
    if mode.lower() not in ['all', 'any']:
        raise ValueError("{} not in ['all', 'any']".format(mode.lower()))
    ops = {'any': any, 'all': all}
    if verbose:
        LOGGER.info('Checked folder(s):')
    if isinstance(folders, list):
        for folder in folders:
            falgs.append(_check_dir(folder, action, verbose))
    else:
        falgs.append(_check_dir(folders, action, verbose))
    return ops[mode](falgs)


def _check_dir(folder, action='check', verbose=False):
    """Check if directory exists and make it when necessary.

    Parameters
    ----------
    folder: folder to be checked
    action: what should be do if the folder does not exists, if action is
            'mkdir', than the Return will also be True
    verbose: For rich info
    Return
    ------
    exists: whether the folder exists

    """
    exists = os.path.isdir(folder)
    if not exists:
        if action == 'mkdir':
            # make dirs recursively
            os.makedirs(folder)
            exists = True
            LOGGER.info("folder '%s' has been created.", folder)
        if action == 'check' and verbose:
            LOGGER.info("folder '%s' does not exiets.", folder)
    else:
        if verbose:
            LOGGER.info("folder '%s' exiets.", folder)
    return exists


def check_files(file_list, mode='any', verbose=False):
    """Check whether files exist, optiaonl modes are ['all','any']."""
    n_file = len(file_list)
    opt_modes = ['all', 'any']
    ops = {'any': any, 'all': all}
    if mode not in opt_modes:
        LOGGER.info('Wrong choice of mode, optiaonl modes %s', opt_modes)
        return False
    exists = [os.path.isfile(fn) for fn in file_list]
    if verbose:
        LOGGER.info('names\t status')
        info = [file_list[i] + '\t' + str(exists[i]) for i in range(n_file)]
        LOGGER.info('\n'.join(info))
    return ops[mode](exists)


def check_exists(lists, mode='any', verbose=False):
    """Check whether file(s)/folder(s) exist(s)."""
    n_file = len(lists)
    opt_modes = ['all', 'any']
    ops = {'any': any, 'all': all}
    if mode not in opt_modes:
        LOGGER.info("Wrong choice of mode, optiaonl modes {}".format(opt_modes))
        return False
    exists = [os.path.exists(fn) for fn in lists]
    if verbose:
        LOGGER.info('filename\t status')
        info = [lists[i] + '\t' + str(exists[i]) for i in range(n_file)]
        LOGGER.info('\n'.join(info))
    return ops[mode](exists)


def list_files(folder, suffix='', recursive=False):
    """List all files.

    Parameters
    ----------
    suffix: filename must end with suffix if given, it can also be a tuple
    recursive: if recursive, return sub-pathes
    """
    files = []
    if recursive:
        for path, _, fls in os.walk(folder):
            files += [os.path.join(path, f)
                      for f in fls if f.endswith(suffix)]
    else:
        files = [f for f in os.listdir(folder) if f.endswith(suffix)]
    return files
