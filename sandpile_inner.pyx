import numpy as np
cimport numpy as np

ctypedef np.double_t DTYPE_t


cpdef unstable_locs(np.ndarray[DTYPE_t, ndim=2] grid):
    return np.argwhere(grid >= 4)


cpdef topple_loc(np.ndarray[DTYPE_t, ndim=2] grid,
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


cpdef topple_all_unstable(np.ndarray[DTYPE_t, ndim=2] grid):
    cdef int avalanche_size = 0

    cdef int grid_x_size = grid.shape[0]
    cdef int grid_y_size = grid.shape[1]

    while True:

        locs_to_topple = unstable_locs(grid)

        if not len(locs_to_topple):
            return avalanche_size

        for loc_x, loc_y in locs_to_topple:
            topple_loc(grid, loc_x, loc_y, grid_x_size, grid_y_size)
            avalanche_size += 1
