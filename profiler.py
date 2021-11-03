""" Module containing methods to profile the code.
Ex : Keep track of memory or the time execution.
"""

import logging
import time
from functools import wraps
import tracemalloc
from inspect import getframeinfo, stack
import os
# sys.getsizeof(variable)  # to get the size in bytes of a variable


def memory_tracer():
    """ Function returning the total amount of memory (in bytes) used by the programm """
    tracemalloc.start()
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("filename")  # autres options : "lineno" (gives filename and line number) and traceback
    return stats[0].size


# Examples adapted from Corey Schafer's tutorial on decorators
def sayen_logger(func):
    """ Function writing information on :
        - how a function has been called
        - the time it took to run
        - the total amount of memory used by the programm when the function has been called (in kB)
    """
    logging.basicConfig(filename=f"run_info.log", level=logging.INFO,
                        format="%(levelname)s: %(message)s : %(asctime)s")

    @wraps(func)  # If we want to chain decorators
    def wrapper(*args, **kwargs):
        resultat = func(*args, **kwargs)
        caller = getframeinfo(stack()[1][0])  # from StackOverflow ...
        filename = os.path.basename(caller.filename)
        logging.info(f"File {filename} line {caller.lineno}, Function: {func.__name__}, "
                     f"Memory: {memory_tracer()/1024: .2f} kB, Run time")
        return resultat

    return wrapper


# ==================================================================================================================
#                                                   USELESS
# ==================================================================================================================
def sayen_timer(func):
    logging.basicConfig(filename=f"{func.__name__}_time", level=logging.INFO)

    @wraps(func)  # If we want to chain decorators
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        res = func(*args, **kwargs)
        t2 = time.perf_counter() - t1
        logging.info(f"Ran in {t2} seconds")
        return res

    return wrapper

