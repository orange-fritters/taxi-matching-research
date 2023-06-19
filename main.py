import numpy as np
import pandas as pd
import argparse
from simulator import Simulator


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/output.csv')
    parser.add_argument('--total_time', type=int, default=1440)
    parser.add_argument('--time_window', type=int, default=5)
    parser.add_argument('--tolerance', type=int, default=0)
    parser.add_argument('--a', type=float, default=0.1)
    parser.add_argument('--b', type=float, default=0.1)
    args = parser.parse_args()
    return args

def main(args):
    sim = Simulator(args.data_path,
                    args.total_time, 
                    args.time_window, 
                    args.tolerance,
                    args.a,
                    args.b)
    sim.simulate()
    print(sim.matched_number)

if __name__ == '__main__':
    args = get_arguments()
    main(args)