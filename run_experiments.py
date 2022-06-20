#! /usr/bin/python3

import pickle
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

from time_cell import TimeCell, Config


def single_run(cfg):
    """run a set for a particular config.
    cfg: Config object represetting settings."""
    ca = TimeCell(config=cfg, quick_compute=True)
    res = ca.run_until_time_loop()
    return cfg, res

def count_pickles(f_name):
    """Count the number of objects that has been stored in a pickle file"""
    count = 0
    try:
        with open(f_name, "rb") as f:
            while True:
                try:
                    pickle.load(f)
                    count += 1
                except EOFError:
                    return count
    except IOError:  # handle case of no file there yet
        return 0

def run_job_server(func, experiments, save_file, resume=True, num_experiments=None, n_cores=None):
    """Runs a job server to run the given func over a list of many input args (experiments).
    Runs with a multiprocess pool, saves all results to a picke file, can resume if cancelled,
    and displays a progress bar.
    func: the function the job server will be calling.
    experiments: list or generator of args to pass to func. If a generator, also pass in num_experiments.
    save_file: str file name of where to save our picked results.
    resume: whether to resume a cancelled run.
    num_experiments: None or int. required if experiments is a generator expression.
    n_cores: None or int. overrides using all they systems cores.
    """

    if n_cores is None:
        n_cores = cpu_count()

    if hasattr(experiments, "__len__"):
        num_experiments = len(experiments)

    # resume a previous run?
    start_index = 0
    if resume:
        start_index = count_pickles(save_file)
        if start_index != 0:
            print("Resuming from index: {}".format(start_index))
        # burn off that many experiments
        for _ in range(start_index):
            next(experiments)

    with Pool(n_cores) as p:
        for result in tqdm(
                            p.imap(single_run, experiments),
                            total=num_experiments,
                            initial=start_index):
            # write results one at a time to a pickle object, so we never need to store them in mem
            with open(save_file, "ab") as f:
                pickle.dump(result, f)


if __name__ == '__main__':
    # build experiments
    rules = [30, 45, 73, 97, 110, 137, 161, 165, 169]
    ratios = [.1, .5, .9]
    widths = [32, 33, 34, 35, 36, 37]
    reps = 1500*12

    # generate all the experiments to run with a cartesian product generator
    # for very large lists, generators are way faster
    experiments_gen = (Config(rule=rule, ratio=ratio, t_enter=80, t_exit=40, portal_w=width)
                for _ in range(reps)  # reps as outermost loop to spread out everything
                for rule in rules
                for ratio in ratios
                for width in widths)

    num_experiments = len(rules) * len(ratios) * len(widths) * reps

    # run!
    run_job_server(
        single_run,
        experiments_gen,
        "main_rules.p",
        num_experiments=num_experiments,
        resume=True)
