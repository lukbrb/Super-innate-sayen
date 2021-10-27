""" Python file containing some utils functions that are called in several other main scripts."""
import os
import shutil
import numpy as np
from unidip import UniDip
import scipy.stats as stat
from file_params import INFO_PATH
import time
import sys
import re


def unimodal(dat):
    dat = list(dat)
    dat = np.msort(dat)
    intervals = UniDip(dat, alpha=0.05).run()
    return intervals


def spread(dat):
    return stat.iqr(dat)


def unimodal_bool(dat):
    dat = list(dat)  # TODO : Essaye np.asarray()
    dat = np.msort(dat)
    intervals = UniDip(dat, alpha=0.05).run()
    if len(intervals) != 1:
        return False
    else:
        return True


def spread_bool(dat):
    IQR = stat.iqr(dat)
    if IQR < 200:
        return True
    else:
        return False


def write_info(text, kind="[INFO]"):
    with open(INFO_PATH, "a") as f:
        f.write(f"{kind} - {text} - ({time.asctime()}\n)")


def create_files(metric):
    cwd = sys.path[0]
    os.chdir(cwd)

    paths = ['Results', 'Results/metrics', f"Results/metrics/{metric}",
             f'Results/metrics/{metric}/_1', f'Results/metrics/{metric}/_1/UMAP',
             f'Results/metrics/{metric}/_1/UMAP/other_markers',
             f'Results/metrics/{metric}/_1/Clusters',
             f'Results/metrics/{metric}/_01', f'Results/metrics/{metric}/_01/UMAP',
             f'Results/metrics/{metric}/_01/UMAP/other_markers',
             f'Results/metrics/{metric}/_01/Clusters']

    for path in paths:

        if os.path.exists(path):  # DELETES EXISTING DIRS AND RECREATE THEM
            shutil.rmtree(path)
        os.makedirs(path)

    # BASELINE
    files = os.listdir('files')

    # ALL BASELINE FILES

    baseline_files = list()
    for file in files:
        if re.match('BL', file):
            baseline_files.append(file)
    return baseline_files, files
