""" Python file containing some utils functions that are called in several other main scripts."""
# Built-in library
import time
# third part dependencies
import numpy as np
import scipy.stats as stat
from unidip import UniDip
# Custom modules
import profiler
from file_params import LOG_PATH


@profiler.sayen_logger
def unimodal(dat):
    dat = list(dat)
    dat = np.msort(dat)
    intervals = UniDip(dat, alpha=0.05).run()
    return intervals


@profiler.sayen_logger
def spread(dat):
    return stat.iqr(dat)


@profiler.sayen_logger
def unimodal_bool(dat):
    dat = list(dat)  # TODO : Essaye np.asarray()
    dat = np.msort(dat)
    intervals = UniDip(dat, alpha=0.05).run()
    if len(intervals) != 1:
        return False
    else:
        return True


@profiler.sayen_logger
def spread_bool(dat):
    IQR = stat.iqr(dat)
    if IQR < 200:
        return True
    else:
        return False


@profiler.sayen_logger
def write_info(text, kind="[INFO]"):
    with open(f"{LOG_PATH}/info.txt", "a") as f:
        f.write(f"{kind} - {text} - ({time.asctime()}\n)")
