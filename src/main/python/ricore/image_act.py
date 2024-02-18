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

import random
import numpy as np
from ricore.color import Color, CTP


def get_centers(data, k, max_iters=100):
    """
    One dimensional kmeans for searching color centers.
    """

    sep = len(data) // k
    centers = data[int(sep / 2)::sep][:k]

    for _ in range(max_iters):
        labels = np.argmin(np.abs(data[:, None] - centers), axis=1)
        new_centers = np.array([np.mean(data[labels == i]) if len(data[labels == i]) else 0 for i in range(k)])

        if np.all(centers == new_centers):
            break

        centers = new_centers
    return centers

def get_h_ref(h_array):
    """
    Get ref h of data.
    """

    sel_pro = [1.0 / (len(np.where((h_array >= 345) | (h_array < 15))[0]) + 1E-2)] + \
              [1.0 / (len(np.where((h_array >= i * 30 + 15) & (h_array < i * 30 + 45.0))[0]) + 1E-2) for i in range(11)]

    sel_pro_sum = sum(sel_pro)
    sel_pro = [i / sel_pro_sum for i in sel_pro]
    sel_idx = random.choices(range(len(sel_pro)), sel_pro)[0]
    return [30 * i for i in range(12)][sel_idx]

def get_color_type(h_array):
    """
    Determine whether the image has richer hue or brightness.
    """

    sel_pro = [len(np.where((h_array >= 345) | (h_array < 15))[0])] + \
              [len(np.where((h_array >= i * 30 + 15) & (h_array < i * 30 + 45.0))[0]) for i in range(11)]

    sel_max = max(sel_pro)
    sel_pro = [int(i > sel_max * 0.05) for i in sel_pro]
    sel_pro = 0 if sum(sel_pro) < 2 else random.choice(sel_pro)
    return sel_pro * 3

def extract_image(display_data, rand_num, color_type, useryb=False):
    """
    Extract a set of colors in different extract types.

    Args:
        process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        values (tuple or list): (random number, color type).
    """

    color_tp = 0 if color_type < 0 else color_type
    image_size = display_data.shape[0] * display_data.shape[1]

    if image_size < 9:
        return [
            (np.random.random(), np.random.random()),
            (np.random.random(), np.random.random()),
            (np.random.random(), np.random.random()),
            (np.random.random(), np.random.random()),
            (np.random.random(), np.random.random()),
        ]

    if rand_num > 0 and image_size > rand_num * 1.5:
        ratio = np.sqrt(rand_num / image_size)
        rand_num_0 = int(ratio * display_data.shape[0])
        rand_num_1 = int(ratio * display_data.shape[1])
        mesh = np.meshgrid(
            ((np.linspace(0.0, 1.0, rand_num_0, endpoint=False) + 1.0 / (rand_num_0 * 2)) * display_data.shape[0]).astype(int),
            ((np.linspace(0.0, 1.0, rand_num_1, endpoint=False) + 1.0 / (rand_num_1 * 2)) * display_data.shape[1]).astype(int),
        )

        data = display_data[(mesh[0].reshape(-1), mesh[1].reshape(-1))]
    else:
        data = np.vstack(display_data)

    if len(data) < 9:
        data = np.vstack([data,] * (9 // len(data) + 1))

    hsv_data = Color.rgb2hsv_array(np.array([data,]))[0]

    if len(hsv_data) > 12:
        s_data = hsv_data[:, 1]

        for ext in (0.1, 0.05, 0.01):
            data_pos = np.where(s_data >= ext)

            if len(data_pos[0]) > max(9, len(hsv_data) * 5 * ext):
                hsv_data = hsv_data[data_pos]
                break

        v_data = hsv_data[:, 2]

        for ext in (0.1, 0.05, 0.01):
            data_pos = np.where(v_data >= ext)

            if len(data_pos[0]) > max(9, len(hsv_data) * 5 * ext):
                hsv_data = hsv_data[data_pos]
                break

    if len(hsv_data) > 12:
        s_data = hsv_data[:, 1]
        v_data = hsv_data[:, 2]
        s_range = (s_data.min(), s_data.max(), s_data.max() - s_data.min())
        v_range = (v_data.min(), v_data.max(), v_data.max() - v_data.min())

        for ext in (1.0, 0.8, 0.6, 0.3):
            if color_tp in (0, 3):
                data_pos = np.where((s_data >= s_range[0] + s_range[2] * 0.3 * ext) & (v_data >= v_range[0] + v_range[2] * 0.3 * ext))

            elif color_tp in (1, 4):
                data_pos = np.where((s_data <= s_range[1] - s_range[2] * 0.3 * ext) & (v_data >= v_range[0] + v_range[2] * 0.5 * ext))

            else:
                data_pos = np.where(v_data <= v_range[1] - v_range[2] * 0.4 * ext)

            if len(data_pos[0]) > max(9, len(hsv_data) * 0.3 * ext):
                hsv_data = hsv_data[data_pos]
                break

    if useryb:
        hsv_data = Color.spc_rgb2ryb_array(np.array([hsv_data,]))[0]

    if len(hsv_data) < 9:
        hsv_data = np.vstack([hsv_data,] * (9 // len(hsv_data) + 1))

    h_data = hsv_data[:, 0]
    h_ref = get_h_ref(h_data)

    if color_type < 0:
        color_tp = get_color_type(h_data)

    h_data = Color((h_ref, 1, 1), tp=CTP.hsv).ref_h_array(h_data)
    hsv_data[:, 0] = h_data
    h_centers = get_centers(h_data, 5)
    hsv_data = np.unique(hsv_data, axis=0)
    h_data = hsv_data[:, 0]
    h_labels = np.argmin(np.abs(h_data[:, None] - h_centers), axis=1)

    if color_tp < 3:
        data_comb = []

        for label_idx in range(5):
            if label_idx in h_labels:
                hsv_sel = hsv_data[np.where(h_labels == label_idx)]

                if len(hsv_sel) > 12:
                    s_sel = hsv_sel[:, 1]
                    v_sel = hsv_sel[:, 2]
                    s_range = (s_sel.min(), s_sel.max(), s_sel.max() - s_sel.min())
                    v_range = (v_sel.min(), v_sel.max(), v_sel.max() - v_sel.min())

                    for ext in (1.0, 0.8, 0.6, 0.3):
                        if color_tp == 0:
                            data_pos = np.where((s_sel >= s_range[0] + s_range[2] * 0.6 * ext) & (v_sel >= v_range[0] + v_range[2] * 0.6 * ext))

                        elif color_tp == 1:
                            data_pos = np.where((s_sel <= s_range[1] - s_range[2] * 0.3 * ext) & (v_sel >= v_range[0] + v_range[2] * 0.6 * ext))

                        else:
                            data_pos = np.where(v_sel <= v_range[1] - v_range[2] * 0.1 * ext)

                        if len(data_pos[0]) > max(9, len(hsv_sel) * 0.3 * ext):
                            hsv_sel = hsv_sel[data_pos]
                            break

                data_comb.append(hsv_sel)

        if data_comb:
            h_sel = np.vstack(data_comb)

        else:
            h_sel = hsv_data

        hsv_ans = [h_sel[np.argmin(np.abs(h_sel[:, 0] - h_centers[i]))] for i in range(5)]
    else:
        hsv_sel = hsv_data[np.where(h_labels == np.random.randint(0, 5))]

        if len(hsv_sel) < 9:
            if len(hsv_data) > 9:
                hsv_sel = hsv_data

            else:
                hsv_sel = np.vstack([hsv_data,] * (9 // len(hsv_data) + 1))

        if color_tp == 3:
            sv_sel = hsv_sel[:, 1] * 2 + hsv_sel[:, 2]

        elif color_tp == 4:
            sv_sel = hsv_sel[:, 1]

        else:
            sv_sel = hsv_sel[:, 2]

        sv_centers = get_centers(sv_sel, 5)
        hsv_ans = [hsv_sel[np.argmin(np.abs(sv_sel - sv_centers[i]))] for i in range(5)]

    hsv_ans = np.array(hsv_ans)
    hsv_ans[:, 0] = hsv_ans[:, 0] + h_ref

    if useryb:
        hsv_ans = Color.spc_ryb2rgb_array(np.array([hsv_ans,]))[0]

    rgb_ans = Color.hsv2rgb_array(np.array([hsv_ans,]))[0]
    extracts = []

    for idx in range(5):
        sample = rgb_ans[idx]
        sample_pos = np.where(
            (display_data[:, :, 0] == sample[0]) & \
            (display_data[:, :, 1] == sample[1]) & \
            (display_data[:, :, 2] == sample[2])
        )

        if len(sample_pos) < 1:
            sample_pos = np.where(
                (display_data[:, :, 0] > sample[0] - 3) & (display_data[:, :, 0] < sample[0] + 3) & \
                (display_data[:, :, 1] > sample[1] - 3) & (display_data[:, :, 1] < sample[1] + 3) & \
                (display_data[:, :, 2] > sample[2] - 3) & (display_data[:, :, 2] < sample[2] + 3)
            )

        if len(sample_pos) > 0:
            pos = int(np.random.random() * len(sample_pos[0]))
            extracts.append((sample_pos[1][pos] / (display_data.shape[1] - 1), sample_pos[0][pos] / (display_data.shape[0] - 1)))

        else:
            extracts.append((np.random.random(), np.random.random()))

    return extracts
