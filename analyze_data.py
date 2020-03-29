#! /usr/bin/python3

import time
import pickle
from multiprocessing import Pool

from time_cell import TimeCell, Result, Config

f_name = "results_1585454175.033965.p"
with open(f_name, "rb") as f:
    data = pickle.load(f)

print(data)
