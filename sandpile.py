#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse

import numpy as np
import matplotlib.pyplot as plt


def progress(step, n, n_dropped, avalanche_size):
    print('{}/{}, n dropped: {}, avalanche size: {}'.format(
          step, n, n_dropped, avalanche_size))


def plot_grid(grid, fout):
    fig = plt.figure(figsize=(20, 20), dpi=200.0, frameon=False)

    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()

    fig.add_axes(ax)

    ax.imshow(sandpile.grid/np.max(sandpile.grid))
    plt.savefig(fout)
    plt.close('all')


class Sandpile(object):
    def __init__(self, x_size, y_size, unstable_h=4,
                 store_avalanche_sizes=False):

        self.x_size = x_size
        self.y_size = y_size
        self.unstable_h = unstable_h
        self.store_avalanche_sizes = store_avalanche_sizes

        if self.store_avalanche_sizes:
            self.avalanche_sizes = []

        self.n_dropped = 0
        self.grid = np.zeros((x_size, y_size))

    def drop_sand(self, x_loc=None, y_loc=None, n=1, verbose=False,
                  report_every=None, report_func=None):
        for step in range(n):

            self.grid[x_loc, y_loc] += 1
            self.n_dropped += 1

            avalanche_size = self.topple_all_unstable()

            if self.store_avalanche_sizes:
                self.avalanche_sizes.append(avalanche_size)

            if report_every is not None and step % report_every == 0:
                report_func(self)

            if verbose:
                progress(step, n, self.n_dropped, avalanche_size)


    def unstable_locs(self):
        return np.argwhere(self.grid >= self.unstable_h)

    def topple_loc(self, x, y):
        self.grid[x, y] -= self.unstable_h

        if x - 1 >= 0:
            self.grid[x - 1, y] += 1

        if x + 1 < self.x_size:
            self.grid[x + 1, y] += 1

        if y - 1 >= 0:
            self.grid[x, y - 1] += 1

        if y + 1 < self.y_size:
            self.grid[x, y + 1] += 1

    def topple_all_unstable(self):
        avalanche_size = 0

        while True:

            locs_to_topple = self.unstable_locs()

            if not len(locs_to_topple):
                return avalanche_size

            for loc_x, loc_y in locs_to_topple:
                self.topple_loc(loc_x, loc_y)
                avalanche_size += 1

    def grid_size(self):
        return self.x_size * self.y_size

    def grains_per_dot(self):
        return self.grid.sum()/self.grid_size()


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
        plot_grid(sandpile.grid, args.plot_dir + '/sandpile-{}.png'.format(
            sandpile.n_dropped))

    sandpile.drop_sand(grid_center, grid_center, n_steps, verbose=True,
                       report_every=plot_every, report_func=plot_sandpile)
