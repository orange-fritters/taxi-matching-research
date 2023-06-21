import numpy as np
import pandas as pd
import random
import argparse
from simulator import Simulator


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/output.csv')
    parser.add_argument('--total_time', type=int, default=180)
    parser.add_argument('--time_window', type=int, default=1)
    parser.add_argument('--tolerance', type=int, default=0)
    parser.add_argument('--a', type=float, default=0.9)
    parser.add_argument('--b', type=float, default=0.1)
    parser.add_argument('--exp_name', type=str, default='visual')
    parser.add_argument('--is_greedy', type=bool, default=True)
    args = parser.parse_args()
    return args


def main(args):
    random.seed(0)
    if args.is_greedy:
        args.a = 0
        args.tolerance = 0
    sim = Simulator(args.data_path,
                    args.exp_name,
                    args.total_time, 
                    args.time_window, 
                    args.tolerance,
                    args.a,
                    args.b,
                    args.is_greedy)
    total_time = sim.simulate()
    print(total_time / sim.matched_number)

if __name__ == '__main__':
    args = get_arguments()
    main(args)