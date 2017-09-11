#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import argparse

from sandpile.sandpile import Sandpile
from sandpile.plot import plot_grid


def plot_main(args):
    """Plot checkpoints."""
    for checkpoint in args.checkpoints:
        sandpile = Sandpile.load(checkpoint)
        path = os.path.join(
            args.plot_dir, 'sandpile-{:012d}.png'.format(sandpile.n_dropped))

        print('Plotting: {} ==> {}'.format(checkpoint, path))

        plot_grid(sandpile.grid, path)


def pour_main(args):
    """Pour sand on the sandpile."""
    n_steps = int(args.n_steps)

    if args.checkpoint is None:
        grid_size = int(args.grid_size)
        sandpile = Sandpile(grid_size, grid_size,
                            store_avalanche_sizes=args.store_avalanche_sizes)
    else:
        sandpile = Sandpile.load(args.checkpoint)

    if args.checkpoint_every is not None:
        checkpoint_every = int(args.checkpoint_every)
    else:
        checkpoint_every = None

    x_grid_center = sandpile.x_size/2
    y_grid_center = sandpile.y_size/2

    sandpile.pour_sand((x_grid_center, y_grid_center), n_steps,
                       verbose=args.verbose,
                       checkpoint_every=checkpoint_every,
                       checkpoint_dir=args.checkpoint_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Abelian sandpile')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    pour_parser = subparsers.add_parser('pour', help='Pour sand.')
    pour_parser.add_argument('--grid_size', default=200, type=int,
                             help='Size of the grid.')
    pour_parser.add_argument('--n_steps', default=3e5, type=float,
                             help='Number of steps to compute.')
    pour_parser.add_argument('--checkpoint',
                             help='Start from checkpoint, not from empty grid.')
    pour_parser.add_argument('--checkpoint_every', default=1e4, type=float,
                             help='Directory to save checkpoints.')
    pour_parser.add_argument('--checkpoint_dir', default='./checkpoints/',
                             help='Directory to save checkpoint.')
    pour_parser.add_argument('--store_avalanche_sizes', action='store_true',
                             help='Remember avalanche sizes.')
    pour_parser.add_argument('--verbose', action='store_true',
                             help='Inform about progress.')

    plot_parser = subparsers.add_parser('plot', help='Plot checkpoints.')
    plot_parser.add_argument('checkpoints', nargs='+',
                             help='Directory to read checkpoints from.')
    plot_parser.add_argument('plot_dir',
                             help='Directory to save plots.')

    args = parser.parse_args()

    if args.command == 'pour':
        pour_main(args)
    elif args.command == 'plot':
        plot_main(args)
