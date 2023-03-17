# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details.

Please visit https://github.com/eigenmiao/DigitalPalette for more 
infomation about DigitalPalette.

Copyright (c) 2019-2021 by Eigenmiao. All Rights Reserved.
"""

import numpy as np
from ricore.color import Color


def extract_image(display_data, rand_num, color_type):
    """
    Extract a set of colors in different extract types.

    Args:
        process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        values (tuple or list): (random number, color type).
    """

    if rand_num > 0 and (display_data.shape[0] * display_data.shape[1]) > rand_num:
        data_pos = ((np.random.rand(rand_num) * display_data.shape[0]).astype(int), (np.random.rand(rand_num) * display_data.shape[1]).astype(int))
        data = display_data[data_pos]

    else:
        data = np.vstack(display_data)

    data = data // 2 * 2
    data = np.unique(data, axis=0)

    if len(data) > 240:
        data_pos = np.where(np.logical_not(((data[:, 0] < 25) & (data[:, 1] < 25) & (data[:, 2] < 25)) | ((data[:, 0] > 225) & (data[:, 1] > 225) & (data[:, 2] > 225))))

        if len(data_pos[0]) > 240:
            data = data[data_pos]

    data = Color.rgb2hsv_array(np.array([data,]))[0]

    s_range = (data[:, 1].min(), data[:, 1].max())
    v_range = (data[:, 2].min(), data[:, 2].max())

    for ext in (0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.0):
        if color_type == 0:
            data_pos = np.where((data[:, 1] > s_range[0] + (s_range[1] - s_range[0]) * ext * 0.5) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * (ext + 0.1) * 0.5))

        elif color_type == 1:
            data_pos = np.where((data[:, 1] < s_range[1] - (s_range[1] - s_range[0]) * ext * 0.5) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * (ext + 0.1) * 0.5))

        elif color_type == 2:
            data_pos = np.where(data[:, 2] < v_range[1] - (v_range[1] - v_range[0]) * (ext + 0.1) * 0.5)

        elif color_type == 3:
            data_pos = np.where((data[:, 1] > s_range[0] + (s_range[1] - s_range[0]) * ext) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * (ext + 0.1)))

        elif color_type == 4:
            data_pos = np.where((data[:, 1] < s_range[1] - (s_range[1] - s_range[0]) * ext) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * (ext + 0.1)))

        else:
            data_pos = np.where(data[:, 2] < v_range[1] - (v_range[1] - v_range[0]) * (ext + 0.1))

        if len(data_pos[0]) > 120:
            data = data[data_pos]

            break

    extracts = []

    h_range = (data[:, 0].min(), data[:, 0].max())
    h_range = (h_range[0], h_range[1] - 1 / 12 * (h_range[1] - h_range[0]))

    for idx in range(5):
        mu = h_range[0] + (h_range[1] - h_range[0]) / 4 * idx
        sigma = (h_range[1] - h_range[0]) / 5

        for ext in (-0.5, -0.4, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 2.0):
            data_pos = np.where((data[:, 0] > (mu - sigma - ext * sigma - 1E-3)) & (data[:, 0] < (mu + sigma + ext * sigma + 1E-3)))

            if len(data_pos[0]) > 1:
                break

        sample = data[data_pos]
        sample = sample[int(sample.shape[0] * 0.5)]
        sample = Color.hsv2rgb(sample)

        sample_pos = np.where((display_data[:, :, 0] > sample[0] - 3) & (display_data[:, :, 0] < sample[0] + 3) & (display_data[:, :, 1] > sample[1] - 3) & (display_data[:, :, 1] < sample[1] + 3) & (display_data[:, :, 2] > sample[2] - 3) & (display_data[:, :, 2] < sample[2] + 3))

        pos = int(np.random.random() * len(sample_pos[0]))
        extracts.append((sample_pos[1][pos] / (display_data.shape[1] - 1), sample_pos[0][pos] / (display_data.shape[0] - 1)))

    return extracts
