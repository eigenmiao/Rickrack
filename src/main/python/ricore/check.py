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

import os
import time


def check_key(name):
    """
    Check the name of keymap.
    """

    if isinstance(name, str):
        if name == "+":
            return name

        else:
            nsplit = name.split("+")

            if len(nsplit) == 1:
                if nsplit[0] and nsplit[0] in [i.upper() for i in [chr(32 + i) for i in range(95)]] + ["Space", "Tab", "Esc", "Up", "Down", "Left", "Right", "PgUp", "PgDown", "Home", "End", "Insert", "Del"] + ["F{}".format(i + 1) for i in range(12)]:
                    return name

            elif len(nsplit) == 2:
                if nsplit[0] and nsplit[1] and nsplit[0] in ("Shift", "Alt", "Ctrl") and nsplit[1] in [i.upper() for i in [chr(32 + i) for i in range(95)]] + ["Space", "Tab", "Del", "Insert"]:
                    return name

    return None

def check_file_name(name):
    """
    Parse string without special chars for file name.
    """

    name_stri = ""
    allow_chars = [chr(48 + i) for i in range(10)] + [chr(65 + i) for i in range(26)] + [chr(97 + i) for i in range(26)] + ["(", ")", "[", "]", "_", "-", "+", "=", ".", ",", " "]

    for stri in str(name):
        if stri in allow_chars:
            name_stri = name_stri + stri

    return name_stri.lstrip().rstrip()

def check_is_num(num_str, length=0, scope=[str(i) for i in range(10)]):
    """
    Parse if is a number string.
    """

    stri = str(num_str)
    is_num = True

    if isinstance(length, int) and length > 0 and len(stri) > length:
        is_num = False

    if is_num:
        for num in stri:
            if num not in scope:
                is_num = False
                break

    return is_num

def check_nonempt_str_lst(str_lst):
    """
    Parse not empty string list.
    """

    fmt_lst = []

    if isinstance(str_lst, (tuple, list)):
        for vl in str_lst:
            str_vl = check_file_name(vl)

            if str_vl:
                fmt_lst.append(str_vl)

    return tuple(fmt_lst)

def check_image_desc(desc, parse_full_locs=True):
    """
    Parse image url and full loc from desc.
    """

    if "::" not in desc:
        return "", []

    image_url = ""
    full_locs = [[], [], [], [], []]

    items = str(desc).split("::")

    for pre_item in items:
        item = ""

        if pre_item[:3] == "img" and "=" in pre_item:
            item = pre_item.split("=")[1].lstrip().rstrip()

        else:
            continue

        if os.path.isfile(item) and item.split(".")[-1] in ("png", "bmp", "jpg", "jpeg", "tif", "tiff", "webp"):
            image_url = str(item)

            break

    if image_url and parse_full_locs:
        for pre_item in items:
            item = ""

            if pre_item[:3] == "loc" and "=" in pre_item:
                item = pre_item.split("=")[1].lstrip().rstrip()

            else:
                continue

            if check_is_num(item, scope=[str(i) for i in range(10)] + [".", ",", ";", "N"]):
                item_str_lst = item.split(";;")

                if len(item_str_lst) == 5:
                    for idx in range(5):
                        loc_str_lst = item_str_lst[idx].split(";")

                        for loc_str in loc_str_lst:
                            if loc_str == "N":
                                full_locs[idx].append(None)

                            else:
                                loc = loc_str.split(",")

                                if len(loc) == 2 and check_is_num(loc[0], scope=[str(i) for i in range(10)] + [".",]) and check_is_num(loc[1], scope=[str(i) for i in range(10)] + [".",]) and loc[0].count(".") < 2 and loc[1].count(".") < 2:
                                    loc = (float(loc[0]), float(loc[1]))

                                    if 0.0 <= loc[0] <= 1.0 and 0.0 <= loc[1] <= 1.0:
                                        full_locs[idx].append(loc)

                                else:
                                    return image_url, []

                else:
                    full_locs = [[], [], [], [], []]

            if full_locs[0] or full_locs[1] or full_locs[2] or full_locs[3] or full_locs[4]:
                break

    else:
        return image_url, []

    return image_url, full_locs

def fmt_name(name):
    """
    Delete prefix and endfix of name.
    """

    stri = str(name).lstrip().rstrip()
    stri_prefix = ("Rickrack ", "Rickrack-", "Rickrack:")
    stri_endfix = tuple([str(i) for i in range(10)] + ["-", ":", " "])

    while len(stri) >= 9 and stri[:9] in stri_prefix:
        stri = stri[9:].lstrip()

    while len(stri) >= 1 and stri[-1] in stri_endfix:
        stri = stri[:-1]

    if stri:
        return stri

    else:
        return "Rickrack"

def fmt_im_time(im_time):
    """
    Verify and normalize value im_time.

    Args:
        im_time (tuple or list): default value.

    Returns:
        corrected time.
    """

    current_time = time.time()

    init_time = 0
    modify_time = 0

    if isinstance(im_time, (tuple, list)):
        if len(im_time) > 1:
            init_time, modify_time = im_time[:2]

        else:
            init_time = im_time[0]
            modify_time = 0

    elif isinstance(im_time, (float, int)):
        init_time = im_time
        modify_time = 0

    else:
        init_time = 0
        modify_time = 0

    if isinstance(init_time, (int, float)):
        init_time = float(init_time)
    else:
        init_time = 0

    if isinstance(modify_time, (int, float)):
        modify_time = float(modify_time)
    else:
        modify_time = 0

    init_time = 0 if init_time < 0 else init_time
    init_time = current_time if init_time > current_time else init_time

    modify_time = 0 if modify_time < 0 else modify_time
    modify_time = current_time if modify_time > current_time else modify_time

    modify_time = init_time if modify_time < init_time else modify_time

    cr_time = (init_time, modify_time)

    return cr_time
