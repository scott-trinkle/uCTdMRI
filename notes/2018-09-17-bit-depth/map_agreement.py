import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tifffile as tf
from skimage import color, img_as_float, io

df = pd.read_pickle('./df_raw.pkl')
im = tf.imread('./slice_samples/recon_10250.tiff')

# Values from ImageJ selectio box
width = 5496
height = 3378
x0 = 1890
y0 = 1488

# Setting ROI corners
nrows = 15
xs = np.linspace(x0, x0 + width, nrows, dtype=np.int)
ys = np.linspace(y0, y0 + height, nrows, dtype=np.int)
d = 125


def make_metric_RGB(im, metric='ACC', df=df, xs=xs, ys=ys, d=d, saturation=0.75):
    print('Calculating map')
    metric_map = np.zeros(im.shape)
    count = 0
    for x in xs:
        for y in ys:
            val = df.iloc[count][metric]
            metric_map[y:y+d, x:x+d] = val
            count += 1

    mask = metric_map != 0
    saturation = np.zeros_like(metric_map)
    saturation[mask] = 0.75

    hsv = np.zeros(im.shape + (3,))
    hsv[..., 0] = metric_map  # hue
    hsv[..., 1] = saturation  # saturation
    hsv[..., 2] = img_as_float(im)  # value

    print('Converting to rgb')
    rgb = color.hsv2rgb(hsv)

    return rgb


# for col in df.columns:
#     print(col)
#     metric_map = make_metric_RGB(im, metric=col)
#     io.imsave('metric_maps/{}.png'.format(col), metric_map)


jsd = df.JSD
jsd -= jsd.min()
jsd /= jsd.max()
jsd = pd.DataFrame(jsd)
jsd_map = make_metric_RGB(im, metric='JSD', df=jsd)
io.imsave('metric_maps/JSD.png', jsd_map)

rmse = df.RMSE
rmse -= rmse.min()
rmse /= rmse.max()
rmse = pd.DataFrame(rmse)
rmse_map = make_metric_RGB(im, metric='RMSE', df=rmse)
io.imsave('metric_maps/RMSE.png', rmse_map)

n = 200
hue_gradient = np.flip(np.linspace(0, 1, n), 0)
hsv = np.ones(shape=(len(hue_gradient), 1, 3), dtype=float)
hsv[:, :, 0] = hue_gradient[:, None]
hsv[:, :, 1] = 0.75

all_hues = color.hsv2rgb(hsv)

fig, ax = plt.subplots(figsize=(2, 5))
ax.imshow(all_hues, extent=(0, 0.2, 0.1, 1))
ax.xaxis.set_ticks([])

plt.tight_layout()
plt.savefig('metric_maps/cmap.pdf')
