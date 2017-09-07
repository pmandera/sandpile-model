#!python
#cython: boundscheck=False, wraparound=False

import numpy as np
cimport numpy as np

ctypedef np.double_t DTYPE_t


cdef topple_loc(np.ndarray[DTYPE_t, ndim=2] grid,
                int x, int y, int grid_x_size, int grid_y_size):
        grid[x, y] -= 4

        if x - 1 >= 0:
            grid[x - 1, y] += 1

        if x + 1 < grid_x_size:
            grid[x + 1, y] += 1

        if y - 1 >= 0:
            grid[x, y - 1] += 1

        if y + 1 < grid_y_size:
            grid[x, y + 1] += 1


cdef int topple_loop(np.ndarray[DTYPE_t, ndim=2] grid,
                     int grid_x_size, int grid_y_size):

    cdef int avalanche_size = 0

    while True:

        locs_to_topple = np.argwhere(grid >= 4)

        if not len(locs_to_topple):
            return avalanche_size

        for x, y in locs_to_topple:
            avalanche_size += 1
            topple_loc(grid, x, y, grid_x_size, grid_y_size)



cpdef topple_all_unstable(np.ndarray[DTYPE_t, ndim=2] grid):

    cdef int grid_x_size = grid.shape[0]
    cdef int grid_y_size = grid.shape[1]

    return topple_loop(grid, grid_x_size, grid_y_size)
