#! /usr/bin/python3

from contexttimer import Timer
import time
import pickle
from tqdm import tqdm
from multiprocessing import Pool

from time_cell import TimeCell, Config


def run_set(cfg):
    """run a number of sets for a particular config.
    cfg: Config object represetting settings."""
    ca = TimeCell(config=cfg, quick_compute=True)
    res = ca.run_until_time_loop()
    return cfg, res

if __name__ == '__main__':

    rules = list(range(20))
    ratios = [.1, .5, .9]
    widths = [36, 37, 38]
    reps = 5

    # generate all the experiments to run with a cartesian product generator
    # for very large lists, generators are way faster
    experiments_gen = (Config(rule=rule, ratio=ratio, t_enter=80, t_exit=40, portal_w=width)
                for rule in rules
                for ratio in ratios
                for width in widths
                for _ in range(reps))
    num_experiments = len(rules) * len(ratios) * len(widths) * reps


    with Timer() as t:
        with Pool(8) as p:
            results = []
            for result in tqdm(
                               p.imap(run_set, experiments_gen),
                               total=num_experiments):
                results.append(result)




    # print("Total time: {}".format(t.elapsed))

    # print(results)
    # f_name = "results_{}.p".format(time.time())
    # with open(f_name, "ab") as f:
    #     pickle.dump(results, f)
