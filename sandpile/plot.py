#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def plot_grid(grid, path):
    """Plot a sandpile grid."""
    fig = plt.figure(figsize=(20, 20), dpi=200.0, frameon=False)

    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()

    fig.add_axes(ax)

    if grid.sum() == 0:
        ax.imshow(grid)
    else:
        ax.imshow(grid/np.max(grid))

    plt.savefig(path)
    plt.close('all')
