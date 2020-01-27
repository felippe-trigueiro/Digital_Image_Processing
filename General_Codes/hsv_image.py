import numpy as np
from skimage import color
from matplotlib import pyplot as plt

hue_gradient = np.linspace(0, 1)
hsv = np.ones(shape=(1, len(hue_gradient), 3), dtype=float)
hsv[:, :, 0] = hue_gradient

print(hsv.shape)

all_hues = color.hsv2rgb(hsv)

fig, ax = plt.subplots(figsize=(5, 2))

# Set image extent so hues go from 0 to 1 and the image is a nice aspect ratio.
ax.imshow(all_hues, extent=(0, 1, 0, 0.2))
ax.set_axis_off()

plt.show()
