""" Python file containing some utils functions that are called in several other main scripts."""
# third part dependencies
import numpy as np
import scipy.stats as stat
from unidip import UniDip
# Custom modules
import profiler


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
def unimodal_vectorised(array):
    """ Prend un tableau numpy en argument.
        Renvoie un tableau numpy de booléen.
    """
    array = np.msort(array)
    intervals = [UniDip(array[:, i], alpha=0.05).run() for i in array.shape[1]]
    return np.array([False if len(interval) != 1 else True for interval in intervals])


@profiler.sayen_logger
def spread_vectorised(array):
    """ Description: scipy.stats.iqr(x, axis=None, rng=(25, 75), scale=1.0, nan_policy='propagate',
    interpolation='linear', keepdims=False)

    axis: int or sequence of int, optional

        Axis along which the range is computed. The default is to compute the IQR for the entire array.
"""
    # On peut essayer :
    IQR = stat.iqr(array, axis=0)  # voir de quelle manière il prend l'axe en compte

    return IQR < 200  # devrait renvoyer un tableau de booléen


@profiler.sayen_logger
def quality_control(array, colonnes):
    is_unimodal = unimodal_vectorised(array)
    not_spread = spread_vectorised(array)
    is_good_marker = is_unimodal & not_spread

    good_marker = colonnes[is_good_marker]
    bad_marker = [marker for marker in colonnes if marker not in good_marker]

    return good_marker, bad_marker
