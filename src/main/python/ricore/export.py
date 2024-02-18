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

import time
import struct
import swatch
from lxml import etree
from ricore.color import Color, CTP
from ricore.grid import gen_color_grid, gen_assit_color
from ricore.check import fmt_name


def get_export_color_list(color_list, export_grid=False, max_len=65535, useryb=False):
    """
    Get the export_color_list and export_cname_list for formatting aco, gpl, xml, txt or others.

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        export_grid (bool): True for exporting colors in grid list and False for exporting color set.
        max_len (int): max length of color list.
        useryb (bool): if use ryb color space.

    Returns:
        export_color_list and export_cname_list.
    """

    export_color_list = []
    export_cname_list = []

    if export_grid:
        for idx in range(len(color_list)):
            if color_list[idx][7][0]:
                for i in range(len(color_list[idx][7][0])):
                    export_color_list.append(Color(color_list[idx][7][0][i], tp=CTP.hec))

                    if len(color_list) == 1:
                        name = "{} {}: {}".format(fmt_name(color_list[idx][2]), i + 1, fmt_name(color_list[idx][7][1][i]))

                    else:
                        name = "{} {}-{}: {}".format(fmt_name(color_list[idx][2]), idx + 1, i + 1, fmt_name(color_list[idx][7][1][i]))

                    export_cname_list.append(name.replace("\"", "'"))

                    if len(export_color_list) >= max_len:
                        break

            else:
                color_grid = gen_color_grid(color_list[idx][0], color_list[idx][5], color_list[idx][6], grid_list=None, **color_list[idx][8], useryb=useryb).tolist()

                for i in range(len(color_grid)):
                    for j in range(len(color_grid[i])):
                        export_color_list.append(Color(color_grid[i][j], tp=CTP.rgb))

                        if len(color_list) == 1:
                            name = "{} {}-{}".format(fmt_name(color_list[idx][2]), i + 1, j + 1)

                        else:
                            name = "{} {}-{}-{}".format(fmt_name(color_list[idx][2]), idx + 1, i + 1, j + 1)

                        export_cname_list.append(name.replace("\"", "'"))

                        if len(export_color_list) >= max_len:
                            break

                    if len(export_color_list) >= max_len:
                        break

            if len(export_color_list) >= max_len:
                break

    else:
        for idx in range(len(color_list)):
            for i in (2, 1, 0, 3, 4):
                export_color_list.append(Color(color_list[idx][0][i]))
                name = "{} {}-{}".format(fmt_name(color_list[idx][2]), idx + 1, i + 1)
                export_cname_list.append(name)

            export_color_list.append(Color("FFFFFF", tp=CTP.hec))
            name = fmt_name(color_list[idx][2])
            export_cname_list.append(name)

            for i in (2, 1, 0, 3, 4):
                export_color_list.append(Color(color_list[idx][0][i]))
                name = "{} {}-{}".format(fmt_name(color_list[idx][2]), idx + 1, i + 1)
                export_cname_list.append(name)

                for assit_idx in range(len(color_list[idx][6][i])):
                    assit_color = gen_assit_color(color_list[idx][0][i], *color_list[idx][6][i][assit_idx][2:6])
                    export_color_list.append(assit_color)
                    name = "{} {}-{}-{}".format(fmt_name(color_list[idx][2]), idx + 1, i + 1, assit_idx + 1)
                    export_cname_list.append(name)

    export_color_list = export_color_list[:max_len]
    export_cname_list = export_cname_list[:max_len]
    return export_color_list, export_cname_list

def export_ase(color_list, ctp="rgb", asetp="process", export_grid=False, white_ref=(95.047, 100.0, 108.883), useryb=False):
    """
    Export color set list in ase type (for Adobe exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        ctp (str): 'rgb', 'hsv', 'cmyk', 'lab' or 'grey'.
        asetp (str): 'spot', 'global' or 'process'. ref: see https://github.com/nsfmc/swatch.
        export_grid (bool): True for exporting colors in grid list and False for exporting color set.
        white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".
        useryb (bool): if use ryb color space.

    Returns:
        Binary strings.
    """

    export_color_list, export_cname_list = get_export_color_list(color_list, export_grid=export_grid, useryb=useryb)
    data = []

    for idx in range(len(export_color_list)):
        if ctp == "cmyk":
            c, m, y, k = Color.rgb2cmyk(export_color_list[idx].rgb)
            data_values = (c, m, y, k)
            data_mode = "CMYK"

        elif ctp == "lab":
            l, a, b = Color.rgb2lab(export_color_list[idx].rgb, white_ref=white_ref)
            data_values = (l / 100.0, a, b)
            data_mode = "LAB"

        elif ctp == "gray":
            r, g, b = export_color_list[idx].rgb
            g = 0.2125 * r + 0.7154 * g + 0.0721 * b
            data_values = (g / 255.0,)
            data_mode = "Gray"

        else:
            r, g, b = export_color_list[idx].rgb
            data_values = (r / 255.0, g / 255.0, b / 255.0)
            data_mode = "RGB"

        data.append({
            "name": export_cname_list[idx],
            "type": asetp[0].upper() + asetp[1:],
            "data": {
                "mode": data_mode,
                "values": data_values,
            },

        })
    return swatch.dumps(data)

def import_ase(file_path, white_ref=(95.047, 100.0, 108.883)):
    """
    Import color list from ase file (for Adobe exchange).

    Args:
        file_path (str): swatch file.
        white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".

    Returns:
        grid list (contains colors, names).
    """

    data = swatch.parse(file_path)
    grid_list = []
    name_list = []

    for line in data:
        name_list.append(line["name"])

        if line["data"]["mode"].lower() == "rgb":
            color = Color.rgb2hec((line["data"]["values"][0] * 255, line["data"]["values"][1] * 255, line["data"]["values"][2] * 255))

        elif line["data"]["mode"].lower() == "cmyk":
            color = Color.rgb2hec(Color.cmyk2rgb((line["data"]["values"][0], line["data"]["values"][1], line["data"]["values"][2], line["data"]["values"][3])))

        elif line["data"]["mode"].lower() == "lab":
            color = Color.rgb2hec(Color.lab2rgb((line["data"]["values"][0] * 100.0, line["data"]["values"][1], line["data"]["values"][2]), white_ref=white_ref))

        elif line["data"]["mode"].lower() == "gray":
            color = Color.rgb2hec((255 * line["data"]["values"][0], 255 * line["data"]["values"][0], 255 * line["data"]["values"][0]))

        else:
            color = "FFFFFF"

        grid_list.append(color)
    return grid_list, name_list

def export_swatch(color_list, ctp="rgb", export_grid=False, white_ref=(95.047, 100.0, 108.883), useryb=False):
    """
    Export color set list in swatch type (for Adobe exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        ctp (str): 'rgb', 'hsv', 'cmyk', 'lab' or 'grey'.
        export_grid (bool): True for exporting colors in grid list and False for exporting color set.
        white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".
        useryb (bool): if use ryb color space.

    Returns:
        Binary strings.
    """

    export_color_list, export_cname_list = get_export_color_list(color_list, export_grid=export_grid, useryb=useryb)
    swatch_chars_v1 = struct.pack("!H", 1) + struct.pack("!H", len(export_color_list))
    swatch_chars_v2 = struct.pack("!H", 2) + struct.pack("!H", len(export_color_list))

    for idx in range(len(export_color_list)):
        if ctp == "hsv":
            h, s, v = export_color_list[idx].hsv
            pr_chars = struct.pack("!H", 1) + struct.pack("!H", int(h * 182.04167)) + struct.pack("!H", int(s * 65535)) + struct.pack("!H", int(v * 65535)) + struct.pack("!H", 0)

        elif ctp == "cmyk":
            c, m, y, k = Color.rgb2cmyk(export_color_list[idx].rgb)
            pr_chars = struct.pack("!H", 2) + struct.pack("!H", int((1.0 - c) * 65535)) + struct.pack("!H", int((1.0 - m) * 65535)) + struct.pack("!H", int((1.0 - y) * 65535)) + struct.pack("!H", int((1.0 - k) * 65535))

        elif ctp == "lab":
            l, a, b = Color.rgb2lab(export_color_list[idx].rgb, white_ref=white_ref)
            pr_chars = struct.pack("!H", 7) + struct.pack("!H", int(l * 100)) + struct.pack("!h", int(a * 100)) + struct.pack("!h", int(b * 100)) + struct.pack("!H", 0)

        elif ctp == "gray":
            r, g, b = export_color_list[idx].rgb
            g = 0.2125 * r + 0.7154 * g + 0.0721 * b
            pr_chars = struct.pack("!H", 8) + struct.pack("!H", int((255 - g) * 39.2156862745098)) + struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 0)

        else:
            r, g, b = export_color_list[idx].rgb
            pr_chars = struct.pack("!H", 0) + struct.pack("!H", int(r * 257)) + struct.pack("!H", int(g * 257)) + struct.pack("!H", int(b * 257)) + struct.pack("!H", 0)

        swatch_chars_v1 = swatch_chars_v1 + pr_chars
        swatch_chars_v2 = swatch_chars_v2 + pr_chars
        name = export_cname_list[idx]
        swatch_chars_v2 = swatch_chars_v2 + struct.pack("!H", 0) + struct.pack("!H", len(name) + 1)

        for n in name:
            swatch_chars_v2 = swatch_chars_v2 + struct.pack("!H", ord(n))

        swatch_chars_v2 = swatch_chars_v2 + struct.pack("!H", 0)
    swatch_chars = swatch_chars_v1 + swatch_chars_v2
    return swatch_chars

def import_swatch(file_path, white_ref=(95.047, 100.0, 108.883)):
    """
    Import color list from swatch file (for Adobe exchange).

    Args:
        file_path (str): swatch file.
        white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".

    Returns:
        grid list (contains colors, names).
    """

    with open(file_path, "rb") as df:
        data = df.read()

    if len(data) % 2 != 0 and len(data) < 4:
        return None

    init_ver = 1
    init_pos = 4
    init_len = struct.unpack('!H', data[2:4])[0]

    if struct.unpack('!H', data[0:2])[0] == 2:
        init_ver = 2

    elif struct.unpack('!H', data[0:2])[0] == 1 and len(data) > init_len * 10 + 6 and struct.unpack('!H', data[init_len * 10 + 4: init_len * 10 + 6])[0] == 2:
        init_ver = 2
        init_pos = init_len * 10 + 8
        init_len = struct.unpack("!H", data[init_len * 10 + 6: init_len * 10 + 8])[0]

    last_pos = init_pos
    grid_list = []
    name_list = []

    for idx in range(init_len):
        color_type = struct.unpack('!H', data[last_pos: last_pos + 2])[0]
        color_a = struct.unpack('!H', data[last_pos + 2: last_pos + 4 ])[0]
        color_b = struct.unpack('!H', data[last_pos + 4: last_pos + 6 ])[0]
        color_c = struct.unpack('!H', data[last_pos + 6: last_pos + 8 ])[0]
        color_d = struct.unpack('!H', data[last_pos + 8: last_pos + 10])[0]

        if color_type == 0:
            color = Color.rgb2hec((color_a / 257, color_b / 257, color_c / 257))

        elif color_type == 1:
            color = Color.hsv2hec((color_a / 182.04167, color_b / 65535, color_c / 65535))

        elif color_type == 2:
            color = Color.rgb2hec(Color.cmyk2rgb((1.0 - color_a / 65535, 1.0 - color_b / 65535, 1.0 - color_c / 65535, 1.0 - color_d / 65535)))

        elif color_type == 7:
            color_b = struct.unpack('!h', data[last_pos + 4: last_pos + 6 ])[0]
            color_c = struct.unpack('!h', data[last_pos + 6: last_pos + 8 ])[0]
            color = Color.rgb2hec(Color.lab2rgb((color_a / 100, color_b / 100, color_c / 100), white_ref=white_ref))

        elif color_type == 8:
            color = Color.rgb2hec((255 - color_a / 39.2156862745098, 255 - color_a / 39.2156862745098, 255 - color_a / 39.2156862745098))

        else:
            color = "FFFFFF"

        last_pos = last_pos + 10

        if init_ver == 2:
            if struct.unpack('!H', data[last_pos: last_pos + 2])[0] == 0:
                char_len = struct.unpack('!H', data[last_pos + 2: last_pos + 4])[0] - 1

                if struct.unpack('!H', data[last_pos + char_len * 2 + 4: last_pos + char_len * 2 + 6])[0] == 0:
                    name = ""

                    for name_idx in range(char_len):
                        name = name + chr(struct.unpack('!H', data[last_pos + name_idx * 2 + 4: last_pos + name_idx * 2 + 6])[0])

                else:
                    name = ""

                last_pos = last_pos + char_len * 2 + 6
            else:
                name = ""

        else:
            name = ""

        grid_list.append(color)
        name_list.append(name)

    return grid_list, name_list

def export_gpl(color_list, export_grid=False, useryb=False):
    """
    Export color set list in gpl type (for GIMP exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        export_grid (bool): True for exporting colors in grid list and False for exporting color set.
        useryb (bool): if use ryb color space.

    Returns:
        Plain text strings.
    """

    export_color_list, export_cname_list = get_export_color_list(color_list, export_grid=export_grid, useryb=useryb)
    gpl_chars = "GIMP Palette\n"

    for idx in range(len(export_color_list)):
        r, g, b = export_color_list[idx].rgb
        name = export_cname_list[idx]
        gpl_chars += "{:<5}{:<5}{:<5}{}\n".format(r, g, b, name)

    return gpl_chars

def import_gpl(file_path):
    """
    Import color list from gpl file (for GIMP exchange).

    Args:
        file_path (str): gpl file.

    Returns:
        grid list (contains colors, names).
    """

    grid_list = []
    name_list = []
    with open(file_path, "r", encoding="utf-8") as df:
        data = df.read()

    for line in data.split("\n"):
        items = line.split()

        if len(items) >= 3:
            color_text = ", ".join(items[:3])
            color = Color.stri2color(color_text)
            color = color.hec if color else "#FFFFFF"

            if len(items) > 3:
                name = " ".join(items[3:])

            else:
                name = ""

            grid_list.append(color)
            name_list.append(name)

    return grid_list, name_list

def export_xml(color_list, export_grid=False, useryb=False):
    """
    Export color set list in xml type (for Pencil exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        export_grid (bool): True for exporting colors in grid list and False for exporting color set.
        useryb (bool): if use ryb color space.

    Returns:
        Plain text strings.
    """

    export_color_list, export_cname_list = get_export_color_list(color_list, export_grid=export_grid, useryb=useryb)
    xml_chars = "<!DOCTYPE PencilPalette>\n<palette>\n"

    for idx in range(len(export_color_list)):
        r, g, b = export_color_list[idx].rgb
        name = export_cname_list[idx]
        xml_chars += "    <colour red='{}'{} green='{}'{} blue='{}'{} alpha='255' name='{}'/>\n".format(r, " " * (3 - len(str(r))), g, " " * (3 - len(str(g))), b, " " * (3 - len(str(b))), name)

    xml_chars += "</palette>\n"
    return xml_chars

def import_xml(file_path):
    """
    Import color list from xml flie (for Pencil exchange).

    Args:
        file_path (str): xml file.

    Returns:
        grid list (contains colors, names).
    """

    grid_list = []
    name_list = []
    with open(file_path, "r", encoding="utf-8") as df:
        data = df.read()

    html = etree.HTML(data)
    colour_xmls = html.xpath("//colour")
    color_xmls = html.xpath("//color")

    for color_xml in colour_xmls + color_xmls:
        color_text = ""
        color = None
        r = color_xml.xpath("@red")
        r = r if r else color_xml.xpath("@r")
        g = color_xml.xpath("@green")
        g = g if g else color_xml.xpath("@g")
        b = color_xml.xpath("@blue")
        b = b if b else color_xml.xpath("@b")
        h = color_xml.xpath("@hue")
        h = h if h else color_xml.xpath("@h")
        s = color_xml.xpath("@saturation")
        s = s if s else color_xml.xpath("@s")
        v = color_xml.xpath("@value")
        v = v if v else color_xml.xpath("@v")
        rgb = color_xml.xpath("@rgb")

        if r and g and b:
            color_text = "{}, {}, {}".format(r[0], g[0], b[0])

        elif h and s and v:
            color_text = "{}, {}, {}".format(h[0], s[0], v[0])

        elif rgb:
            color_text = rgb[0]

        if color_text:
            color = Color.stri2color(color_text)
            color = color.hec if color else "#FFFFFF"

        if color:
            name = color_xml.xpath("@name")
            name = name[0] if name else ""
            grid_list.append(color)
            name_list.append(name)

    return grid_list, name_list

def export_text(color_list, useryb=False):
    """
    Export color set list in plain text (for directly reading).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]
        useryb (bool): if use ryb color space.

    Returns:
        Plain text strings.
    """

    plain_text = ""

    for idx in range(len(color_list)):
        rule_str = color_list[idx][1]
        rule_str = rule_str[0].upper() + rule_str[1:].lower()

        if color_list[idx][4][0] < 0:
            time_str = "Unknown"

        else:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(color_list[idx][4][0]))

        if color_list[idx][4][1] < 0:
            time_str += "; Unknown"

        else:
            time_str += "; {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(color_list[idx][4][1])))

        name = "{} {}".format(fmt_name(color_list[idx][2]), idx + 1)
        plain_text += "# Name: {}\n".format(name)
        plain_text += "# Rule: {}\n".format(rule_str)
        plain_text += "# Time: {}\n".format(time_str)
        plain_text += "{:<8}{:<8}{:<8}{:<8}{:<10}{:<10}{:<10}{:<8}\n".format("# Index", "R", "G", "B", "H", "S", "V", "Hex Code")

        for i in (2, 1, 0, 3, 4):
            r, g, b = color_list[idx][0][i].rgb
            h, s, v = color_list[idx][0][i].hsv
            hex_code = "{}".format(color_list[idx][0][i].hec)
            plain_text += "  {:<6}{:<8}{:<8}{:<8}{:<10.3f}{:<10.3f}{:<10.3f}{:<8}\n".format(i, r, g, b, h, s, v, hex_code)

        plain_text += "\n# Full Colors\n"
        grid_list = []

        for i in (2, 1, 0, 3, 4):
            grid_list.append(color_list[idx][0][i].hec)

            for assit_idx in range(len(color_list[idx][6][i])):
                assit_color = gen_assit_color(color_list[idx][0][i], *color_list[idx][6][i][assit_idx][2:6])
                grid_list.append(assit_color.hec)

        plain_text += "  " + " ".join(grid_list)
        plain_text += "\n\n# Color Grid ...\n"
        color_grid = gen_color_grid(color_list[idx][0], color_list[idx][5], color_list[idx][6], grid_list=None, **color_list[idx][8], useryb=useryb).tolist()

        for i in range(len(color_grid)):
            grid_list = []

            for j in range(len(color_grid[i])):
                grid_list.append(Color(color_grid[i][j], tp=CTP.rgb).hec)

            plain_text += "  " + " ".join(grid_list) + "\n"
        plain_text += "\n"

    plain_text += "\n"
    return plain_text

def import_text(file_path):
    """
    Import color list from plain text (for directly reading).

    Args:
        file_path (str): plain text.

    Returns:
        grid list (contains colors, names).
    """

    grid_list = []
    name_list = []
    with open(file_path, "r", encoding="utf-8") as df:
        data = df.read()

    grid_list = Color.findall_hec_lst(data)
    name_list = ["",] * len(grid_list)
    return grid_list, name_list

def export_list(color_list):
    """
    Export color set list in list type (for Rickrack output).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values), ...]

    Returns:
        Json List.
    """

    expt_list = []

    for color in color_list:
        color_dict = {"rule": color[1], "name": color[2], "desc": color[3], "time": list(color[4])}

        for i in (2, 1, 0, 3, 4):
            color_dict["color_{}".format(i)] = color[0][i].export()

        color_dict["grid_locations"] = color[5]
        color_dict["grid_assitlocs"] = color[6]
        color_dict["grid_list"] = color[7]
        color_dict["grid_values"] = color[8]
        expt_list.append(color_dict)

    return expt_list
