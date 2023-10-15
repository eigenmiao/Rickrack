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


def rotate_point(point, theta):
    """
    Rotate point in anti-clockwise direction. Rotating center is (0, 0), theta is in angle type and r_theta is in radian type.

    Args:
        point (tuple or list): point for rotating.
        theta (int or float): rotating angle (in angle type).

    Returns:
        rotated point.
    """

    r_theta = theta * np.pi / 180
    Rz = np.array([
        [np.cos(r_theta), np.sin(r_theta) * -1],
        [np.sin(r_theta), np.cos(r_theta)     ],

    ])
    pt = Rz.dot(np.array(point))
    return pt

def rotate_point_center(center, point, theta):
    """
    Rotate point in anti-clockwise direction around given center.

    Args:
        center (tuple or list): rotating center.
        point (tuple or list): point for rotating.
        theta (int or float): rotating angle (in angle type).

    Returns:
        rotated point.
    """

    delta_point = np.array(point) - np.array(center)
    rotated_point = rotate_point(delta_point, theta)
    pt = rotated_point + np.array(center)
    return pt

def get_theta(point):
    """
    Get angle between point and x axis in anti-clockwise direction. Center is (0, 0).

    Args:
        point (tuple or list): rotated point.

    Returns:
        rotated theta.
    """

    delta_x = point[0]
    delta_y = point[1]

    if delta_x == 0:
        if delta_y > 0:
            hue = 90

        else:
            hue = 270

    else:
        _hue = np.arctan(delta_y / delta_x) * 180 / np.pi

        if delta_x > 0:
            hue = _hue if _hue > 0 else 360 + _hue

        else:
            hue = _hue + 180

    return hue

def get_theta_center(center, point):
    """
    Get angle between point and x axis in anti-clockwise direction around given center.

    Args:
        center (tuple or list): rotating center.
        point (tuple or list): rotated point.

    Returns:
        rotated theta.
    """

    delta_point = np.array(point) - np.array(center)
    hue = get_theta(delta_point)
    return hue

def get_outer_box(center, radius):
    """
    Get outer box of circle with raduis.

    Args:
        center (tuple or list): circle center.
        radius (int or float): circle radius.

    Returns:
        outer box.
    """

    box = np.array((center[0] - radius, center[1] - radius, 2 * radius, 2 * radius))
    return box

def get_box_center(box):
    """
    Get the center of a circle box.

    Args:
        box (tuple or list): circle box.

    Returns:
        center.
    """

    return np.array((box[0] + box[2] / 2, box[1] + box[3] / 2))

def get_link_tag(box):
    """
    Get link tag shape with two square and one line.

    Args:
        box (tuple or list): outer box.
    """

    shift = box[2] / 8
    shift_box = (box[0] + shift, box[1] + shift, box[2] - shift * 2, box[3] - shift * 2)
    square_left = np.array((shift_box[0], shift_box[1] + (shift_box[3] - shift_box[2] / 2) / 2, shift_box[2] / 2, shift_box[2] / 2))
    square_right = np.array((shift_box[0] + shift_box[2] / 2, shift_box[1] + (shift_box[3] - shift_box[2] / 2) / 2, shift_box[2] / 2, shift_box[2] / 2))
    line_start = np.array((shift_box[0] + shift_box[2] / 4, shift_box[1] + shift_box[3] / 2))
    line_end = np.array((shift_box[0] + shift_box[2] * 3 / 4, shift_box[1] + shift_box[3] / 2))
    return square_left, square_right, shift, line_start, line_end

def snap_point(pt, wid):
    """
    Snap point on special locations, such as (1, 1) or (0.5, 0.5).

    Args:
        pt (tuple or list): point before snap.
        wid (float): box width (or half widh if snap (0.5, 0.5)).

    Returns:
        point after snap.
    """

    x, y = pt

    if (x % wid) < wid * 0.15:
        x = (x // wid) * wid

    elif (x % wid) > wid * 0.85:
        x = (x // wid + 1) * wid

    if (y % wid) < wid * 0.15:
        y = (y // wid) * wid

    elif (y % wid) > wid * 0.85:
        y = (y // wid + 1) * wid

    return [x, y]

def get_outer_circles(pt_array, activated_idx, pts_array, assit_pts_array, pt_radius, assit_pt_radius, info_pt_radius, last_result, major=True, minor=True):
    """
    Add info circles around pts and ref pts.

    Args:
        pt (tuple or list): current point.
        activated_idx (int): current activated index of main points.
        pts (tuple or list): main point locations.
        assit_pts (tuple or list): ref point locations.
        pt_radius (int or float): radius of a main point.
        assit_pt_radius (int or float): radius of a ref point.
        info_pt_radius (int or float): radius of a info point around a main point.
        major (bool): consider major points.
        minor (bool): consider minor points.

    Return:
        (sel_idx, sel_assit_idx, is_in_pt, is_in_assit_pt, ((circle_0, pattern_0), (circle_1, pattern_1), ...), sel_info_idx)
    """

    info_pt_radius_int = int(info_pt_radius)
    sel_idx = -1
    sel_assit_idx = -1
    all_pt_dist = []
    idx_seq = list(range(5))
    idx_seq = idx_seq[activated_idx + 1: ] + idx_seq[: activated_idx + 1]
    pt_info_pt_radius_2 = (pt_radius + info_pt_radius_int * 2) ** 2
    pt_radius_2 = pt_radius ** 2
    assit_pt_info_pt_radius_2 = (assit_pt_radius + info_pt_radius_int * 2) ** 2
    assit_pt_radius_2 = assit_pt_radius ** 2
    info_pt_radius_int_2 = info_pt_radius_int ** 2

    for idx in idx_seq:
        pt_dist_2 = np.sum((pt_array - pts_array[idx]) ** 2)

        if major:
            all_pt_dist.append((pt_dist_2, (idx,)))

            if pt_dist_2 < pt_info_pt_radius_2:
                sel_idx = idx

        if pt_dist_2 < pt_radius_2:
            return None

        assit_len = len(assit_pts_array[idx])

        if assit_len > 25:
            return None

        for assit_idx in range(assit_len):
            assit_pt_dist_2 = np.sum((pt_array - assit_pts_array[idx][assit_idx]) ** 2)

            if minor:
                all_pt_dist.append((assit_pt_dist_2, (idx, assit_idx)))

                if assit_pt_dist_2 < assit_pt_info_pt_radius_2:
                    sel_idx = idx
                    sel_assit_idx = assit_idx

            if not (minor and last_result) and assit_pt_dist_2 < assit_pt_radius_2:
                return None

    is_in_pt = False
    is_in_assit_pt = False

    if sel_assit_idx > -1:
        is_in_assit_pt = True

    elif sel_idx > -1:
        is_in_pt = True

    else:
        all_pt_dist.sort(key=lambda x: x[0])
        sel_pt = all_pt_dist[0]

        if sel_pt[0] > pt_radius_2 * 4:
            return None

        if len(sel_pt[1]) == 1:
            sel_idx = sel_pt[1][0]
            sel_assit_idx = -1

        else:
            sel_idx, sel_assit_idx = sel_pt[1]

    if is_in_assit_pt and last_result and sel_idx == last_result[0] and sel_assit_idx == last_result[1] and is_in_pt == last_result[2] and is_in_assit_pt == last_result[3]:
        circle_locations = last_result[4]
        sel_info_idx = -1

        for loc_idx in range(len(circle_locations)):
            o_center = get_box_center(circle_locations[loc_idx][0])

            if np.sum((pt_array - o_center) ** 2) < info_pt_radius_int_2:
                sel_info_idx = loc_idx

    else:
        circle_locations = []

        if sel_assit_idx == len(assit_pts_array[sel_idx]):
            sel_assit_idx = -1

        if sel_assit_idx > -1:
            info_around_center = assit_pts_array[sel_idx][sel_assit_idx]
            info_around_radius = assit_pt_radius + info_pt_radius_int

        else:
            info_around_center = pts_array[sel_idx]
            info_around_radius = pt_radius + info_pt_radius_int

        theta = get_theta_center(info_around_center, pt_array)
        info_pt_center = rotate_point_center(info_around_center, (info_around_center[0] + info_around_radius, info_around_center[1]), theta).astype(int)
        sel_info_idx = -1

        if np.sum((pt_array - info_pt_center) ** 2) < info_pt_radius_int_2:
            sel_info_idx = 0

        circle_locations.append((
            get_outer_box(info_pt_center, info_pt_radius_int),
            info_pt_center + np.array((
                (-0.5, 0),
                ( 0.5, 0),

            )) * info_pt_radius_int, info_pt_center + np.array((
                (0, -0.5),
                (0,  0.5),

            )) * info_pt_radius_int,
        ))

        if sel_assit_idx > -1:
            theta = theta + 120
            info_pt_center = rotate_point_center(info_around_center, (info_around_center[0] + info_around_radius, info_around_center[1]), theta).astype(int)
            circle_locations.append((
                get_outer_box(info_pt_center, info_pt_radius_int),
                info_pt_center + np.array((
                    (-0.5, 0),
                    ( 0.5, 0),

                )) * info_pt_radius_int,
            ))
            theta = theta + 120
            info_pt_center = rotate_point_center(info_around_center, (info_around_center[0] + info_around_radius, info_around_center[1]), theta).astype(int)
            circle_locations.append((
                get_outer_box(info_pt_center, info_pt_radius_int),
                info_pt_center + np.array((
                    (-0.708, -0.708),
                    ( 0.708,  0.708),

                )) * info_pt_radius_int, info_pt_center + np.array((
                    ( 0.0834386, -0.6349818),
                    ( 0.6349818, -0.0834386),
                    ( 0.2404163,  0.1216223),
                    ( 0.2262741,  0.4440630),
                    (-0.0975807,  0.0975807),
                    (-0.5275016,  0.5275016),
                    (-0.0975807,  0.0975807),
                    (-0.4440630, -0.2262741),
                    (-0.1216223, -0.2404163),

                )) * info_pt_radius_int,
            ))

    return (sel_idx, sel_assit_idx, is_in_pt, is_in_assit_pt, circle_locations, sel_info_idx)
