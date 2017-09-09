#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import gzip
import cPickle as pickle

import numpy as np

try:
    from sandpile_inner import topple_all_unstable
except ImportError:
    # Importing cython failed: fall back to python

    print('Falling back to slow code...')

    def unstable_locs(grid):
        """Return the coordinates of all unstable spots on the grid."""
        return np.argwhere(grid >= 4)

    def topple_loc(grid, x, y, grid_x_size, grid_y_size):
        """
        Topple elements in x, y on the grid by moving them to the neighboring
        spots. If x, y is on the boundary of the grid, some of the chips fall
        off the grid and disapear.
        """
        grid[x, y] -= 4

        if x - 1 >= 0:
            grid[x - 1, y] += 1
        if x + 1 < grid_x_size:
            grid[x + 1, y] += 1
        if y - 1 >= 0:
            grid[x, y - 1] += 1
        if y + 1 < grid_y_size:
            grid[x, y + 1] += 1

    def topple_all_unstable(grid):
        """
        Topple all unstable spots on the grid.

        If any other site becomes unstable after toppling repeat until the
        whole grid becomes stable.
        """
        avalanche_size = 0

        grid_x_size, grid_y_size = grid.shape

        while True:

            locs_to_topple = unstable_locs(grid)

            if not len(locs_to_topple):
                return avalanche_size

            for loc_x, loc_y in locs_to_topple:
                topple_loc(grid, loc_x, loc_y, grid_x_size, grid_y_size)
                avalanche_size += 1


def progress(step, n, n_dropped, avalanche_size):
    print('{}/{}, n dropped: {}, avalanche size: {}'.format(
          step, n, n_dropped, avalanche_size))


class Sandpile(object):
    """
    Class for creating sandpiles.

    On a grid, each site with more than 3 chips topples and sends one of its
    chips to each of its 4 neighbours.

    For more information see:
        https://en.wikipedia.org/wiki/Abelian_sandpile_model
    """

    def __init__(self, x_size, y_size, store_avalanche_sizes=False):

        self.x_size = x_size
        self.y_size = y_size
        self.store_avalanche_sizes = store_avalanche_sizes

        if self.store_avalanche_sizes:
            self.avalanche_sizes = []

        self.n_dropped = 0
        self.grid = np.zeros((x_size, y_size))

    def pour_sand(self, loc=(None, None), n=1, verbose=False,
                  checkpoint_every=None, checkpoint_dir=None):
        """
        Drop n grains of sand on loc.

        The grains are dropped one by one and unstable locations are toppled
        after dropping each grain.
        """

        x_loc, y_loc = loc

        for step in range(n):

            if checkpoint_every is not None and step % checkpoint_every == 0:
                path = os.path.join(
                    checkpoint_dir,
                    'sandpile-{:012d}.pckl.gz'.format(self.n_dropped))
                self.save(path)

            self.grid[x_loc, y_loc] += 1
            self.n_dropped += 1

            avalanche_size = self.topple_all_unstable()

            if self.store_avalanche_sizes:
                self.avalanche_sizes.append(avalanche_size)

            if verbose:
                progress(step, n, self.n_dropped, avalanche_size)

    def topple_all_unstable(self):
        """Topple all unstable locations on the grid."""
        return topple_all_unstable(self.grid)

    def grid_size(self):
        """Size of the grid."""
        return self.x_size * self.y_size

    def grains_per_dot(self):
        """Calculate an average number of grains per grid field."""
        return self.grid.sum()/self.grid_size()

    def save(self, fname):
        """Pickle the sandpile."""
        with gzip.open(fname, 'w') as fout:
            pickle.dump(self, fout)

    @staticmethod
    def load(fname):
        """Load the sandpile from a pickle."""
        with gzip.open(fname, 'rb') as fout:
            return pickle.load(fout)
