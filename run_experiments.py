#! /usr/bin/python3

import time
from multiprocessing import Pool

from time_cell import TimeCell, Result


def run_set(width):
    n_runs = 100
    starts = []
    cycle_lengths = []
    for i in range(n_runs):
        ca = TimeCell(ratio=.2)
        ca.w = width
        res = ca.gen_until_time_loop()

        starts.append(res.cycle_start)
        cycle_lengths.append(res.cycle_length)

    avg_starts = 1.0 * sum(starts) / n_runs
    avg_cycles = 1.0 * sum(cycle_lengths) / n_runs
    return (width, avg_starts, avg_cycles)

if __name__ == '__main__':
    widths = range(15, 36, 5)
    t0 = time.time()
    with Pool(8) as p:
        ress = p.map(run_set, widths)
    t1 = time.time()

    for res in ress:
        width, avg_starts, avg_cycles = res
        print("width: {:.2f}\tAve start: {:.1f}\tAve cycle: {:.1f}".format(width, avg_starts, avg_cycles))

    print("total time: {}".format(t1 - t0))
