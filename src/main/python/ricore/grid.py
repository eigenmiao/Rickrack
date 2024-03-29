# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

Copyright (c) 2019-2022 by Eigenmiao. All Rights Reserved.
"""

import re
import numpy as np
from ricore.color import Color, CTP


def gen_color_grid(color_set, grid_locations, grid_assitlocs, grid_list=None, col=9, ctp=("r", "g", "b"), sum_factor=1.0, dim_factor=1.0, assist_factor=0.4, rev_grid=False, useryb=False):
    """
    Generate color grid (board) from peroid colors and points (or fixed point list).

    Args:
        color_set (tuple or list): colors in color set.
        grid_locations (tuple or list): main of colors in color set.
        grid_assitlocs (tuple or list): assistant colors around color set.
        grid_list (tuple or list): fix the grid instead generate grid from color points, contains color list and name list.
        col (int): grid coulmn. suggest 0~50.
        ctp (str): color type, "r", "g", "b" or "h", "s", "v".
        sum_factor (int or float): sum factor, suggest 0~5. The larger the sum_factor is, the larger the circile is.
        dim_factor (int or float): dim factor, suggest 0~1. The larger the dim_factor is, the lighter the circile is.
        assist_factor (int or float): weight for assistant points, suggest 0~1. The larger the assist_factor is, the heavier the weight is.
        rev_grid (bool): if rgb grid generation reversed.
        useryb (bool): if use ryb color space.

    Returns:
        color grid in rgb type.
    """

    if grid_list and grid_list[0]:
        color_grid_a = np.ones((col, col)) * 255
        color_grid_b = np.ones((col, col)) * 255
        color_grid_c = np.ones((col, col)) * 255

        for fixed_idx in range(len(grid_list[0])):
            if fixed_idx < col * col:
                r, g, b = Color.hec2rgb(grid_list[0][fixed_idx])
                color_grid_a[fixed_idx // col, fixed_idx % col] = r
                color_grid_b[fixed_idx // col, fixed_idx % col] = g
                color_grid_c[fixed_idx // col, fixed_idx % col] = b

        final_grid = np.stack((color_grid_a, color_grid_b, color_grid_c), axis=2)
        final_grid = Color.fmt_rgb_array(final_grid)
        return final_grid

    else:
        if useryb and "h" in ctp:
            fmt_color_set = [Color.spc_rgb2ryb(c) for c in color_set]

        else:
            fmt_color_set = color_set

        assi_colors = [[], [], [], [], []]
        assi_points = [[], [], [], [], []]
        colors = []
        points = []

        for idx in range(5):
            pt_rxy = np.array(grid_locations[idx])

            for assit_idx in range(len(grid_assitlocs[idx])):
                assit_rpt = pt_rxy + np.array(grid_assitlocs[idx][assit_idx][0:2])
                assi_points[idx].append(assit_rpt)
                assit_color = gen_assit_color(color_set[idx], *grid_assitlocs[idx][assit_idx][2:6])

                if useryb and "h" in ctp:
                    assi_colors[idx].append(Color.spc_rgb2ryb(assit_color))

                else:
                    assi_colors[idx].append(assit_color)

            for shift_i in (-1, 0, 1):
                for shift_j in (-1, 0, 1):
                    if "r" in ctp or "g" in ctp or "b" in ctp:
                        pt_color = fmt_color_set[idx].rgb

                    else:
                        pt_color = list(fmt_color_set[idx].hsv)
                        pt_color[0] = fmt_color_set[0].ref_h(pt_color[0])

                    colors.append(pt_color)
                    points.append(np.array(grid_locations[idx]) + np.array((shift_i, shift_j)))

        for idx in range(5):
            for assidx in range(len(assi_colors[idx])):
                if "r" in ctp or "g" in ctp or "b" in ctp:
                    pt_color = assi_colors[idx][assidx].rgb

                else:
                    pt_color = list(assi_colors[idx][assidx].hsv)
                    pt_color[0] = fmt_color_set[0].ref_h(pt_color[0])

                colors.append(pt_color)
                points.append(np.array(assi_points[idx][assidx]))

        colors = np.array(colors)
        points = np.array(points)
        distance_grid = []

        for p in range(len(points)):
            grid_x = (np.arange(col, dtype=float) + 0.5) / col
            grid_y = (np.arange(col, dtype=float) + 0.5) / col
            grid_x = (grid_x - points[p][0]) ** 2
            grid_y = (grid_y - points[p][1]) ** 2
            grid = np.array([grid_x,] * col, dtype=float).T + np.array([grid_y,] * col, dtype=float)
            distance_grid.append(grid)

        distance_grid = np.array(distance_grid, dtype=float)
        distance_grid = distance_grid ** sum_factor
        distance_grid[np.where(distance_grid < 0.001)] = 0.001
        distance_grid = 1.0 / distance_grid
        distance_grid[45:] = distance_grid[45:] * assist_factor
        distance_grid = distance_grid / distance_grid.sum(axis=0)
        distance_grid = distance_grid * dim_factor
        distance_grid = distance_grid.swapaxes(0, 2)

        if rev_grid:
            if "r" in ctp or "g" in ctp or "b" in ctp:
                color_grid_a = distance_grid.dot(255.0 - colors[:, 0]) if "r" in ctp else np.ones((col, col)) * (255.0 - fmt_color_set[0].r)
                color_grid_b = distance_grid.dot(255.0 - colors[:, 1]) if "g" in ctp else np.ones((col, col)) * (255.0 - fmt_color_set[0].g)
                color_grid_c = distance_grid.dot(255.0 - colors[:, 2]) if "b" in ctp else np.ones((col, col)) * (255.0 - fmt_color_set[0].b)
                color_grid_a = 255.0 - color_grid_a
                color_grid_b = 255.0 - color_grid_b
                color_grid_c = 255.0 - color_grid_c

            else:
                color_grid_a = distance_grid.dot(      colors[:, 0]) + fmt_color_set[0].h if "h" in ctp else np.ones((col, col)) * (      fmt_color_set[0].h)
                color_grid_b = distance_grid.dot(      colors[:, 1])                      if "s" in ctp else np.ones((col, col)) * (      fmt_color_set[0].s)
                color_grid_c = distance_grid.dot(1.0 - colors[:, 2])                      if "v" in ctp else np.ones((col, col)) * (1.0 - fmt_color_set[0].v)
                color_grid_c = 1.0 - color_grid_c

        else:
            if "r" in ctp or "g" in ctp or "b" in ctp:
                color_grid_a = distance_grid.dot(colors[:, 0]) if "r" in ctp else np.ones((col, col)) * fmt_color_set[0].r
                color_grid_b = distance_grid.dot(colors[:, 1]) if "g" in ctp else np.ones((col, col)) * fmt_color_set[0].g
                color_grid_c = distance_grid.dot(colors[:, 2]) if "b" in ctp else np.ones((col, col)) * fmt_color_set[0].b

            else:
                color_grid_a = distance_grid.dot(colors[:, 0]) + fmt_color_set[0].h if "h" in ctp else np.ones((col, col)) * fmt_color_set[0].h
                color_grid_b = distance_grid.dot(colors[:, 1])                      if "s" in ctp else np.ones((col, col)) * fmt_color_set[0].s
                color_grid_c = distance_grid.dot(colors[:, 2])                      if "v" in ctp else np.ones((col, col)) * fmt_color_set[0].v

        final_grid = np.stack((color_grid_a, color_grid_b, color_grid_c), axis=2)

        if "r" in ctp or "g" in ctp or "b" in ctp:
            final_grid = Color.fmt_rgb_array(final_grid)

        else:
            if useryb:
                final_grid = Color.spc_ryb2rgb_array(final_grid)

            final_grid = Color.hsv2rgb_array(final_grid)
        return final_grid

def norm_grid_locations(grid_locations, grid_assitlocs):
    """
    Verify and normalize value grid_locations and grid_assitlocs in args.

    Args:
        grid_locations (tuple or list): ref to self._args.sys_grid_locations. default value.
        grid_assitlocs (tuple or list): ref to self._args.sys_grid_assitlocs. default value.

    Returns:
        corrected grid_locations and grid_assitlocs.
    """

    cr_grid_locations = []
    cr_grid_assitlocs = [[], [], [], [], []]
    clear_grid_loc = False
    clear_assi_loc = False

    if len(grid_locations) == 5:
        for grid_i in range(5):
            if len(grid_locations[grid_i]) == 2:
                loc_x = grid_locations[grid_i][0]
                loc_y = grid_locations[grid_i][1]

                if isinstance(loc_x, (int, float)) and isinstance(loc_y, (int, float)):
                    loc_x = 0.0 if loc_x < 0.0 else loc_x
                    loc_y = 0.0 if loc_y < 0.0 else loc_y
                    loc_x = 1.0 if loc_x > 1.0 else loc_x
                    loc_y = 1.0 if loc_y > 1.0 else loc_y
                    cr_grid_locations.append((float(loc_x), float(loc_y)))

                else:
                    clear_grid_loc = True

            else:
                clear_grid_loc = True

            if clear_grid_loc:
                break

    else:
        clear_grid_loc = True

    if not clear_grid_loc and len(grid_assitlocs) == 5:
        for grid_i in range(5):
            for grid_j in range(len(grid_assitlocs[grid_i])):
                if len(grid_assitlocs[grid_i][grid_j]) == 4:
                    loc_a, loc_b, loc_c, loc_d = grid_assitlocs[grid_i][grid_j]

                    if isinstance(loc_a, (int, float)) and isinstance(loc_b, (int, float)) and isinstance(loc_c, str) and loc_c in ("h", "s", "v") and isinstance(loc_d, (int, float)):
                        loc_a = -1.0 if loc_a < -1.0 else loc_a
                        loc_b = -1.0 if loc_b < -1.0 else loc_b
                        loc_a = 1.0 if loc_a > 1.0 else loc_a
                        loc_b = 1.0 if loc_b > 1.0 else loc_b

                        if loc_c == "h":
                            h, s, v = loc_d, 0, 0

                        elif loc_c == "s":
                            h, s, v = 0, loc_d, 0

                        else:
                            h, s, v = 0, 0, loc_d

                        loc_a, loc_b, loc_c, loc_d, loc_e, loc_f = float(loc_a), float(loc_b), float(h), float(s), float(v), True
                    else:
                        loc_a, loc_b, loc_c, loc_d, loc_e, loc_f = None, None, None, None, None, None

                elif len(grid_assitlocs[grid_i][grid_j]) == 6:
                    loc_a, loc_b, loc_c, loc_d, loc_e, loc_f = grid_assitlocs[grid_i][grid_j]

                else:
                    loc_a, loc_b, loc_c, loc_d, loc_e, loc_f = None, None, None, None, None, None

                if isinstance(loc_a, (int, float)) and isinstance(loc_b, (int, float)) and isinstance(loc_c, (int, float)) and isinstance(loc_d, (int, float)) and isinstance(loc_e, (int, float)):
                    loc_a = -1.0 if loc_a < -1.0 else loc_a
                    loc_b = -1.0 if loc_b < -1.0 else loc_b
                    loc_a = 1.0 if loc_a > 1.0 else loc_a
                    loc_b = 1.0 if loc_b > 1.0 else loc_b
                    cr_grid_assitlocs[grid_i].append([float(loc_a), float(loc_b), float(loc_c), float(loc_d), float(loc_e), bool(loc_f)])

                else:
                    clear_assi_loc = True

                if clear_assi_loc:
                    break

    else:
        clear_assi_loc = True

    if clear_grid_loc:
        cr_grid_locations = [(0.5, 0.5), (0.85, 0.85), (0.15, 0.85), (0.85, 0.15), (0.15, 0.15)]

    if clear_assi_loc:
        cr_grid_assitlocs = [[], [], [], [], []]

    return cr_grid_locations, cr_grid_assitlocs

def norm_grid_list(grid_list):
    """
    Verify and normalize value grid_list in args.

    Args:
        grid_list (tuple or list): ref to self._args.sys_grid_list. default value. contains color list and name list.

    Returns:
        corrected grid_list.
    """

    cr_colr_list = []
    cr_name_list = []

    if isinstance(grid_list, (tuple, list)) and grid_list:
        grid_tran = grid_list
        name_tran = []

        if isinstance(grid_list[0], (tuple, list)):
            grid_tran = grid_list[0]

        if isinstance(grid_list[1], (tuple, list)):
            name_tran = grid_list[1]

        for grid_item_idx in range(len(grid_tran)):
            color = Color.stri2color(grid_tran[grid_item_idx])

            if color:
                cr_colr_list.append(color.hec)

                if len(name_tran) > grid_item_idx:
                    name_stri = re.split(r"[\v\a\f\n\r\t]", str(name_tran[grid_item_idx]))

                    while "" in name_stri:
                        name_stri.remove("")

                    if name_stri:
                        name_stri = name_stri[0].lstrip().rstrip()

                    else:
                        name_stri = ""

                    cr_name_list.append(name_stri)
                else:
                    cr_name_list.append("")

            else:
                cr_colr_list.append("FFFFFF")
                cr_name_list.append("")

    cr_grid_list = [cr_colr_list, cr_name_list]
    return cr_grid_list

def norm_grid_values(grid_values):
    """
    Verify and normalize value grid_values in args.

    Args:
        grid_values (dict): ref to self._args.sys_grid_values. default value.

    Returns:
        corrected grid_values.
    """

    cr_grid_values = {"col": 9, "ctp": ("r", "g", "b"), "sum_factor": 1.0, "dim_factor": 1.0, "assist_factor": 0.4, "rev_grid": False}

    if isinstance(grid_values, dict):
        if "col" in grid_values:
            value = grid_values["col"]

            if isinstance(value, (int, float)):
                value = 1 if value < 1 else value
                value = 51 if value > 51 else value
                cr_grid_values["col"] = int(value)

        if "ctp" in grid_values:
            value = grid_values["ctp"]

            if isinstance(value, (tuple, list)):
                ctp_lst = []

                if "r" in value or "g" in value or "b" in value:
                    for ctp in ("r", "g", "b"):
                        if ctp in value:
                            ctp_lst.append(ctp)

                else:
                    for ctp in ("h", "s", "v"):
                        if ctp in value:
                            ctp_lst.append(ctp)

                if not ctp_lst:
                    ctp_lst = ("r", "g", "b")

                cr_grid_values["ctp"] = tuple(ctp_lst)

        if "sum_factor" in grid_values:
            value = grid_values["sum_factor"]

            if isinstance(value, (int, float)):
                value = 0.0 if value < 0.0 else value
                value = 5.0 if value > 5.0 else value
                cr_grid_values["sum_factor"] = float(value)

        if "dim_factor" in grid_values:
            value = grid_values["dim_factor"]

            if isinstance(value, (int, float)):
                value = 0.0 if value < 0.0 else value
                value = 1.0 if value > 1.0 else value
                cr_grid_values["dim_factor"] = float(value)

        if "assist_factor" in grid_values:
            value = grid_values["assist_factor"]

            if isinstance(value, (int, float)):
                value = 0.0 if value < 0.0 else value
                value = 1.0 if value > 1.0 else value
                cr_grid_values["assist_factor"] = float(value)

        if "rev_grid" in grid_values:
            value = grid_values["rev_grid"]

            if isinstance(value, (int, float, bool)):
                cr_grid_values["rev_grid"] = bool(value)

    return cr_grid_values

def gen_assit_color(curr_color, assit_h, assit_s, assit_v, relativity):
    """
    Generate assit color relative to current color.

    Args:
        assit_h: delta h or absoluate h value.
        assit_s: delta s or absoluate s value.
        assit_v: delta v or absoluate v value.
        relativity: is relative or absoluate.

    Returns:
        assit color.
    """

    if relativity:
        assit_color = Color((
            curr_color.h + assit_h,
            curr_color.s + assit_s,
            curr_color.v + assit_v,

        ), tp=CTP.hsv, overflow=curr_color.get_overflow())
    else:
        assit_color = Color((
            assit_h,
            assit_s,
            assit_v,

        ), tp=CTP.hsv, overflow=curr_color.get_overflow())
    return assit_color

def gen_assit_args(curr_color, assit_color, relativity):
    """
    Generate assit arguments relative to current color.
    """

    if relativity:
        assit_h = assit_color.h - curr_color.h
        assit_s = assit_color.s - curr_color.s
        assit_v = assit_color.v - curr_color.v

    else:
        assit_h = assit_color.h
        assit_s = assit_color.s
        assit_v = assit_color.v

    return assit_h, assit_s, assit_v
