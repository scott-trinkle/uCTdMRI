import numpy as np
from strtens import StructureTensor
from strtens.util import read_tif_stack, imsave, imread


def get_inds(imshape, k=4, g_buf=25):
    slices, rows, cols = imshape
    d_row = rows // k
    d_col = cols // k

    row_grid = [[i * d_row - g_buf, (i + 1) * d_row + g_buf] for i in range(k)]
    col_grid = [[i * d_col - g_buf, (i + 1) * d_col + g_buf] for i in range(k)]
    row_grid[0][0] = 0
    col_grid[0][0] = 0
    row_grid[k-1][1] = -1
    col_grid[k-1][1] = -1

    final_rows = [[i * d_row, (i + 1)*d_row] for i in range(k)]
    final_cols = [[i * d_col, (i + 1)*d_col] for i in range(k)]
    final_rows[k-1][1] = -1
    final_cols[k-1][1] = -1
    return row_grid, col_grid, final_rows, final_cols


i = 1
start = 0
stop = 100

print("Reading image")
# im = read_tif_stack("../../data/xray/recon_2x/recon_2x_",
#                     start=start, stop=stop)

rows, cols, frows, fcols = get_inds(im.shape)

test = []

for i, (row, frow) in enumerate(zip(rows, frows)):
    for j, (col, fcol) in enumerate(zip(cols, fcols)):
        print(i+1, j+1)
        im_temp = im[:, row[0]:row[1], col[0]:col[1]]
        print(im_temp.shape)
        print((101, frow[1]-frow[0], fcol[1]-fcol[0]))
        # test[:, frow[0]:frow[1], fcol[0]:fcol[1]] =
        break


# print("Calculating Structure Tensor")
# FA, orientations = StructureTensor(im).results()

# print("Saving")
# np.save("../FA/FA_batch_{:0>2d}_sl_{}-{}".format(i, start, stop), FA)
# np.save("../orientations/orientations_batch_{:0>2d}_sl_{}-{}".format(i, start, stop), orientations)
