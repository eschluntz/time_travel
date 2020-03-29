#! /usr/bin/python3

import time
# import pickle
from multiprocessing import Pool

from time_cell import TimeCell, Result, Config


def run_set(cfg):
    n_runs = 20
    results = []
    print("Starting run for {}".format(cfg))
    for _ in range(n_runs):
        ca = TimeCell(config=cfg, quick_compute=True)
        res = ca.gen_until_time_loop()
        results.append((cfg,res))

    return results

if __name__ == '__main__':
    experiments = []

    # rules = list(range(256))
    rules = [110, 110, 72]
    ratios = [.1, .5, .9]
    for rule in rules:
        for ratio in ratios:
            cfg = Config(rule=rule, ratio=ratio, t_enter=80, t_exit=40, portal_w=32)
            experiments.append(cfg)

    # with Pool(8) as p:
    #     results = p.map(run_set, experiments)

    t0 = time.time()
    results = []
    for cfg in experiments:
        results.append(run_set(cfg))
    t1 = time.time()
    print(t1 - t0)
    # print(results)
    # f_name = "results_{}.p".format(time.time())
    # with open(f_name, "ab") as f:
    #     pickle.dump(results, f)
