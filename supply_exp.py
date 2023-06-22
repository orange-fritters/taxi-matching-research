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
    parser.add_argument('--c', type=float, default=0.3)
    parser.add_argument('--exp_name', type=str, default='visual')
    args = parser.parse_args()
    return args


def main(args):
    # csv writer.
    with open('data/plus.csv', 'w') as f:
        f.write('additional_supply,total_time,equity_measure\n')
        for i in range(5, 101, 5):
            random.seed(0)
            data_path = 'data/supply/plus_' + str(i) + '.csv'
            sim = Simulator(data_path,
                            args.exp_name,
                            args.total_time, 
                            args.time_window, 
                            args.tolerance,
                            args.a,
                            args.b,
                            args.c)
            result = sim.simulate()
            f.write(str(i) + ',' + str(result) + '\n')
            print(i, " ", result)

if __name__ == '__main__':
    args = get_arguments()
    main(args)