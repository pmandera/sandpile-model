#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import numpy as np
import matplotlib.pyplot as plt

from sandpile import Sandpile


def plot_grid(grid, fout):
    fig = plt.figure(figsize=(20, 20), dpi=200.0, frameon=False)

    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()

    fig.add_axes(ax)

    ax.imshow(sandpile.grid/np.max(sandpile.grid))
    plt.savefig(fout)
    plt.close('all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Abelian sandpile')
    parser.add_argument('--grid_size', default=200, type=int,
                        help='Size of the grid.')
    parser.add_argument('--n_steps', default=3e5, type=float,
                        help='Number of steps to compute.')

    parser.add_argument('--plot_every', default=1e3, type=float,
                        help='Directory to save plots.')
    parser.add_argument('--plot_dir', default='./plots/',
                        help='Directory to save plots.')
    parser.add_argument('--verbose', action='store_true',
                        help='Inform about progress.')

    args = parser.parse_args()

    n_steps = int(args.n_steps)
    grid_size = int(args.grid_size)

    if args.plot_every is not None:
        plot_every = int(args.plot_every)
    else:
        plot_every = None

    grid_center = grid_size/2

    sandpile = Sandpile(grid_size, grid_size)

    def plot_sandpile(sandpile):
        plot_grid(sandpile.grid,
                  args.plot_dir + '/sandpile-{:012d}.png'.format(
                      sandpile.n_dropped))

    sandpile.drop_sand(grid_center, grid_center, n_steps, verbose=args.verbose,
                       report_every=plot_every, report_func=plot_sandpile)
