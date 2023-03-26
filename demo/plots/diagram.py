# -*- coding: utf-8 -*-

"""
This is a demo script for using the Rickrack module. It plots curves, 
bars, maps and polar bars with colors from the Rickrack. The colors can be 
modified by the Rickrack module in real-time.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

Copyright (c) 2019-2023 by Eigenmiao. All Rights Reserved.
"""

import os
import time
import numpy as np
from rickrack import Rickrack, Color
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap


# setup rickrack.
# 
rr = Rickrack()
rr.timeout = 9
rr.port = 23333

current_dir = os.path.dirname(os.path.abspath(__file__))

dp_argv = {}
dp_proj = r"C:\Program Files\Rickrack"
rr.run(dp_argv=dp_argv, dp_proj=dp_proj)

colors = [
    lambda r: "#" + r.colors_in_order[0].color.hec,
    lambda r: "#" + r.colors_in_order[1].color.hec,
    lambda r: "#" + r.colors_in_order[2].color.hec,
    lambda r: "#" + r.colors_in_order[3].color.hec,
    lambda r: "#" + r.colors_in_order[4].color.hec,
]

# setup matplotlib.
# 
fig = plt.figure(figsize=(10, 8))
fig.subplots_adjust(left=0.1, bottom=0.04, right=0.96, top=0.94, wspace=0.16, hspace=0.16)
plt.ion()

# setup numpy.
# 
np.random.seed(0)

# sample 1.
# ref: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html
# 
ax1 = plt.subplot(221)

for i in range(5):
    x = np.arange(0, 360, 1)
    y = np.sin(2 * x * np.pi / 180 + i * 36)

    line = ax1.plot(x, y, color="white", linewidth=1, zorder=2)
    rr.add_items_for_render(line, "set_color", colors[i])

ax1.set_xlabel("Angle (degrees)")
ax1.set_ylabel("Signal")

ax1.set_xlim(0, 360)
ax1.set_ylim(-1.1, 1.1)

def deg2rad(x):
    return x * np.pi / 180

def rad2deg(x):
    return x * 180 / np.pi

secax = ax1.secondary_xaxis("top", functions=(deg2rad, rad2deg))
secax.set_xlabel("Angle (rad)")

# sample 2.
# ref: https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
# 
ax2 = plt.subplot(222)

category_names = ["A", "B", "C", "D", "E"]
results = {
    "G1": [10, 15, 17, 32, 26],
    "G2": [26, 22, 29, 10, 13],
    "G3": [35, 37,  7,  2, 19],
    "G4": [32, 11,  9, 15, 33],
    "G5": [21, 29,  5,  5, 40],
    "G6": [8,  19,  5, 30, 38],
}

labels = list(results.keys())
data = np.array(list(results.values()))
data_cum = data.cumsum(axis=1)
category_colors = ("white", "white", "white", "white", "white")

ax2.invert_yaxis()
ax2.xaxis.set_visible(False)
ax2.set_xlim(0, np.sum(data, axis=1).max())

for i, (colname, color) in enumerate(zip(category_names, category_colors)):
    widths = data[:, i]
    starts = data_cum[:, i] - widths
    rects = ax2.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
    rr.add_items_for_render(rects, "set_color", colors[i])

# sample 3.
# ref: http://datav.aliyun.com/portal/school/atlas/area_selector
# 
ax3 = plt.subplot(223)
ax3_sub = fig.add_axes([0.45, 0.05, 0.1, 0.15])

map = Basemap(llcrnrlon=80, llcrnrlat=0, urcrnrlon=160, urcrnrlat=46, projection="lcc", lat_1=33, lat_2=45, lon_0=100)
map.readshapefile(os.sep.join([current_dir, "map", "PRC"]), "states", color="white", zorder=0)

area_idx = [("北京市", 0), ("天津市", 1), ("河北省", 2), ("山西省", 1), ("内蒙古自治区", 0), ("辽宁省", 4), ("吉林省", 3), ("黑龙江省", 2), ("上海市", 3), ("江苏省", 2), ("浙江省", 4), ("安徽省", 1), ("福建省", 1), ("江西省", 2), ("山东省", 0), ("河南省", 4), ("湖北省", 0), ("湖南省", 4), ("广东省", 0), ("广西壮族自治区", 2), ("海南省", 1), ("重庆市", 3), ("四川省", 4), ("贵州省", 1), ("云南省", 3), ("西藏自治区", 0), ("陕西省", 2), ("甘肃省", 1), ("青海省", 3), ("宁夏回族自治区", 4), ("新疆维吾尔自治区", 2), ("台湾省", 3), ("香港特别行政区", 3), ("澳门特别行政区", 3)]
area_idx = dict(area_idx)

for i, shapedict in enumerate(map.states_info):
    s = shapedict["name"].split("\x00")[0]

    if s:
        idx = area_idx[s]

    else:
        idx = 2

    poly = Polygon(map.states[i], alpha=0.8, linewidth=0, color="white", zorder=1)
    ax3.add_patch(poly)
    rr.add_items_for_render(poly, "set_color", colors[idx])

    poly = Polygon(map.states[i], alpha=1.0, linewidth=1, fill=None, joinstyle="round", color="black", zorder=2)
    ax3.add_patch(poly)
    rr.add_items_for_render(poly, "set_color", colors[2])

    poly = Polygon(map.states[i], alpha=0.8, linewidth=0, color="white", zorder=1)
    ax3_sub.add_patch(poly)
    rr.add_items_for_render(poly, "set_color", colors[idx])

    poly = Polygon(map.states[i], alpha=1.0, linewidth=1, fill=None, joinstyle="round", color="black", zorder=2)
    ax3_sub.add_patch(poly)
    rr.add_items_for_render(poly, "set_color", colors[2])

ax3.axis("off")
ax3.set_xlim(400000, 6000000)
ax3.set_ylim(1900000, 6400000)
ax3.set_aspect("equal", adjustable="box")

ax3_sub.axis("on")
ax3_sub.get_xaxis().set_visible(False)
ax3_sub.get_yaxis().set_visible(False)
ax3_sub.set_xlim(3600000, 5500000)
ax3_sub.set_ylim(200000, 3200000)
ax3_sub.set_aspect("equal", adjustable="box")

# sample 4.
# ref: https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html
# 
ax4 = plt.subplot(224, projection="polar")

radii = 10 * np.random.rand(10)
width = np.pi / 5 * np.random.rand(10)
theta = np.linspace(0.0, 2 * np.pi, 10, endpoint=False) + np.pi / 5 * np.random.rand(10)

for i in range(10):
    bar = ax4.bar(theta[i], radii[i], width=width[i], bottom=0.0, color="white", linewidth=1, alpha=0.5, zorder=1)
    rr.add_items_for_render(bar, "set_color", colors[i % 5])

    bar = ax4.bar(theta[i], radii[i], width=width[i], bottom=0.0, color="white", fill=None, linewidth=1, alpha=1.0, zorder=2)
    rr.add_items_for_render(bar, "set_color", colors[i % 5])

ax4.set_ylim(0, 10)

# render.
# 
def head_func():
    ax2.legend(ncol=len(category_names), bbox_to_anchor=(-0.01, 1), loc="lower left", framealpha=0)
    plt.pause(1)

rr.render(head=head_func)

# display.
# 
plt.savefig(os.sep.join([current_dir, "diagram.png"]), dpi=300, transparent=False)
plt.close()

# please don't close Rickrack abnormally.
# 
rr.close()
