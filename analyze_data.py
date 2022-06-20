#! /usr/bin/python3

import time
import pickle
from collections import defaultdict

from time_cell import TimeCell, Result, Config

f_name = "rule_sweep.p"
data = []
with open(f_name, "rb") as f:
    while True:
        try:
            data.append(pickle.load(f))
        except EOFError:
            break

print(len(data))

stats = defaultdict(lambda: defaultdict(int))
for config, result in data:
    stats[config.rule]["count"] += 1
    if result is None:
        stats[config.rule]["nones"] += 1
    else:
        stats[config.rule]["total_cycle"] += result.cycle_length

for r, v in stats.items():
    print("Rule: {:3d} Count: {:3d} Nones: {:3d} Total: {:5d}".format(r, v["count"], v["nones"], v["total_cycle"]))

##### keepers for good diversity: [30, 45, 73, 97, 110, 137, 161, 165, 169]

# no time travel: 161, 126, 165,    135,    73,    109,    18,   149,   86,    22, 151, 183, 90, 30
#                tri, tri, weird, weird, square, square, weird, werid, weird, tri, tri, tri, cool, cool,

# medium time travel: 129, 135, 137, 18, 146, 147, 149, 22, 150, 151, 153, 30, 161,
#  37, 165, 41, 169, 45, 54, 182, 183, 60, 193, 195, 73, 75, 86, 89, 90, 91, 97, 101, 102, 105, 107, 109, 110, 120, 121, 122, 124, 126

# long time travel: 161, 135, 73, 109, 18, 149, 86, 22, 151, 183, 30
