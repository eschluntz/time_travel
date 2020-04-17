#! /usr/bin/python3

import time
import pickle
from multiprocessing import Pool

from time_cell import TimeCell, Result, Config


def run_set(cfg):
    n_runs = 5000
    results = []
    print("Starting run for {}".format(cfg))
    for _ in range(n_runs):
        ca = TimeCell(config=cfg, quick_compute=True)
        res = ca.gen_until_time_loop()
        results.append((cfg,res))

    return results

if __name__ == '__main__':
    experiments = []

    rules = list(range(256))
    ratios = [.1, .5, .9]
    widths = [35, 36, 37, 38]
    for rule in rules:
        for ratio in ratios:
            for width in widths:
                cfg = Config(rule=rule, ratio=ratio, t_enter=80, t_exit=40, portal_w=width)
                experiments.append(cfg)

    with Pool(8) as p:
        results = p.map(run_set, experiments)

    # print(results)
    f_name = "results_{}.p".format(time.time())
    with open(f_name, "ab") as f:
        pickle.dump(results, f)
