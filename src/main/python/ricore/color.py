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

import re
import unittest
import numpy as np


class FakeColor(object):
    def __init__(self, rgb, hsv, hec):
        self.rgb = Color.fmt_rgb(rgb)
        self.hsv = Color.fmt_hsv(hsv)
        self.hec = Color.fmt_hec(hec)

    def export(self):
        return {"rgb": self.rgb.tolist(), "hsv": self.hsv.tolist(), "hex_code": self.hec}

class Color(object):
    def __init__(self, item, tp="color", overflow="cutoff"):
        self.set_overflow(overflow)
        if isinstance(tp, str) and tp in ("rgb", "hsv", "hec", "color"):
            self.setti(item, tp)
        else:
            raise ValueError("expect tp in str type and list 'rgb', 'hsv', 'hec' and 'color': {}.".format(tp))

    def setti(self, item, tp):
        if not isinstance(tp, str):
            raise ValueError("expect tp in str type: {}.".format(tp))
        if tp.lower() == "color":
            if isinstance(item, (Color, FakeColor)):
                self._rgb, self._hsv, self._hec = self.fmt_rgb(item.rgb), self.fmt_hsv(item.hsv), self.fmt_hec(item.hec)
            else:
                raise ValueError("expect item in Color type: {}.".format(item))
        elif tp.lower() == "rgb":
            self._rgb = self.fmt_rgb(item)
            self._hsv = self.rgb2hsv(self._rgb)
            self._hec = self.rgb2hec(self._rgb)
        elif tp.lower() == "hsv":
            self._hsv = self.fmt_hsv(item, overflow=self._overflow)
            self._rgb = self.hsv2rgb(self._hsv)
            self._hec = self.hsv2hec(self._hsv)
        elif tp.lower() == "hec":
            self._hec = self.fmt_hec(item)
            self._rgb = self.hec2rgb(self._hec)
            self._hsv = self.hec2hsv(self._hec)
        elif tp.lower() == "r":
            rgb = list(self._rgb)
            rgb[0] = item
            self.setti(rgb, "rgb")
        elif tp.lower() == "g":
            rgb = list(self._rgb)
            rgb[1] = item
            self.setti(rgb, "rgb")
        elif tp.lower() == "b":
            rgb = list(self._rgb)
            rgb[2] = item
            self.setti(rgb, "rgb")
        elif tp.lower() == "h":
            hsv = list(self._hsv)
            hsv[0] = item
            self.setti(hsv, "hsv")
        elif tp.lower() == "s":
            hsv = list(self._hsv)
            hsv[1] = item
            self.setti(hsv, "hsv")
        elif tp.lower() == "v":
            hsv = list(self._hsv)
            hsv[2] = item
            self.setti(hsv, "hsv")
        else:
            raise ValueError("expect tp in list 'rgb', 'hsv', 'hec', 'r', 'g', 'b', 'h', 's', 'v' and 'color'.")

    def getti(self, tp):
        if not isinstance(tp, str):
            raise ValueError("expect tp in str type: {}.".format(tp))
        if tp.lower() == "color":
            return Color(self)
        elif tp.lower() == "rgb":
            return tuple(self._rgb)
        elif tp.lower() == "hsv":
            return tuple(self._hsv)
        elif tp.lower() == "hec":
            return str(self._hec)
        elif tp.lower() == "r":
            return int(self._rgb[0])
        elif tp.lower() == "g":
            return int(self._rgb[1])
        elif tp.lower() == "b":
            return int(self._rgb[2])
        elif tp.lower() == "h":
            return float(self._hsv[0])
        elif tp.lower() == "s":
            return float(self._hsv[1])
        elif tp.lower() == "v":
            return float(self._hsv[2])
        else:
            raise ValueError("expect tp in list 'rgb', 'hsv', 'hec', 'r', 'g', 'b', 'h', 's', 'v' and 'color'.")

    def set_overflow(self, overflow):
        if isinstance(overflow, str) and overflow in ("cutoff", "return", "repeat"):
            self._overflow = str(overflow)
        else:
            raise ValueError("expect value in str type and list 'cutoff', 'return', 'repeat': {}.".format(overflow))

    def get_overflow(self):
        return str(self._overflow)

    def __str__(self):
        return "Color(hec {})".format(self.hec)

    def __repr__(self):
        return "Color(hec {})".format(self.hec)
    '''

    def __eq__(self, other):
        if isinstance(other, Color):
            return self._hec == other.hec
        else:
            raise ValueError("expect other in Color type: {}.".format(other))

    def __ne__(self, other):
        if isinstance(other, Color):
            return self._hec != other.hec
        else:
            raise ValueError("expect other in Color type: {}.".format(other))
    '''
    @property

    def rgb(self):
        return self.getti("rgb")
    @property

    def hsv(self):
        return self.getti("hsv")
    @property

    def hec(self):
        return self.getti("hec")
    @property

    def r(self):
        return self.getti("r")
    @property

    def g(self):
        return self.getti("g")
    @property

    def b(self):
        return self.getti("b")
    @property

    def h(self):
        return self.getti("h")
    @property

    def s(self):
        return self.getti("s")
    @property

    def v(self):
        return self.getti("v")
    @property

    def color(self):
        return self.getti("color")
    @rgb.setter

    def rgb(self, item):
        self.setti(item, "rgb")
    @hsv.setter

    def hsv(self, item):
        self.setti(item, "hsv")
    @hec.setter

    def hec(self, item):
        self.setti(item, "hec")
    @r.setter

    def r(self, item):
        self.setti(item, "r")
    @g.setter

    def g(self, item):
        self.setti(item, "g")
    @b.setter

    def b(self, item):
        self.setti(item, "b")
    @h.setter

    def h(self, item):
        self.setti(item, "h")
    @s.setter

    def s(self, item):
        self.setti(item, "s")
    @v.setter

    def v(self, item):
        self.setti(item, "v")
    @color.setter

    def color(self, item):
        self.setti(item, "color")

    def export(self):
        return {"rgb": self._rgb.tolist(), "hsv": self._hsv.tolist(), "hex_code": self._hec}

    def ref_h(self, hue):
        if self.h < 180.0:
            if hue < self.h + 180.0:
                return hue - self.h
            else:
                return hue - (self.h + 360.0)
        else:
            if hue < self.h - 180.0:
                return hue - (self.h - 360.0)
            else:
                return hue - self.h

    def ref_h_array(self, hue_array):
        data = np.array(hue_array, dtype=np.float64)
        if self.h < 180.0:
            p1 = np.where(data < self.h + 180.0)
            p2 = np.where(data >= self.h + 180.0)
            data[p1] = data[p1] - self.h
            data[p2] = data[p2] - (self.h + 360.0)
        else:
            p1 = np.where(data < self.h - 180.0)
            p2 = np.where(data >= self.h - 180.0)
            data[p1] = data[p1] - (self.h - 360.0)
            data[p2] = data[p2] - self.h
        return data
    @classmethod

    def fmt_rgb(cls, rgb):
        if len(rgb) == 3:
            _rgb = np.rint(rgb)
            _rgb[np.where(_rgb < 0)] = 0
            _rgb[np.where(_rgb > 255)] = 255
            return _rgb.astype(np.uint8)
        else:
            raise ValueError("expect rgb color in length 3 and int: {}.".format(rgb))
    @classmethod

    def fmt_rgb_array(cls, rgb_array):
        if isinstance(rgb_array, np.ndarray) and len(rgb_array.shape) == 3 and rgb_array.shape[2] == 3:
            _rgb = np.rint(rgb_array)
            _rgb[np.where(_rgb < 0)] = 0
            _rgb[np.where(_rgb > 255)] = 255
            return _rgb.astype(np.uint8)
        else:
            raise ValueError("expect rgb array in length 3: {}.".format(rgb_array))
    @classmethod

    def fmt_hsv(cls, hsv, overflow="cutoff"):
        if not isinstance(overflow, str):
            raise ValueError("expect overflow in str type: {}.".format(overflow))
        if len(hsv) == 3:
            _h, _s, _v = hsv
            if not (0.0 <= _s <= 1.0 and 0.0 <= _v <= 1.0):
                if overflow.lower() == "cutoff":
                    _s = 0.0 if _s < 0.0 else _s
                    _s = 1.0 if _s > 1.0 else _s
                    _v = 0.0 if _v < 0.0 else _v
                    _v = 1.0 if _v > 1.0 else _v
                elif overflow.lower() == "return":
                    _s = _s % 1.0 if _s // 1.0 % 2.0 == 0.0 else 1.0 - (_s % 1.0)
                    _v = _v % 1.0 if _v // 1.0 % 2.0 == 0.0 else 1.0 - (_v % 1.0)
                elif overflow.lower() == "repeat":
                    _s = _s % 1.0
                    _v = _v % 1.0
                else:
                    raise ValueError("expect overflow in list 'cutoff', 'return' and 'repeat'.")
            _h = round(_h % 360.0 * 1E5) / 1E5
            _s = round(_s * 1E5) / 1E5
            _v = round(_v * 1E5) / 1E5
            return np.array((_h, _s, _v), dtype=np.float32)
        else:
            raise ValueError("expect hsv color in length 3 and float: {}.".format(hsv))
    @classmethod

    def fmt_hsv_array(cls, hsv_array):
        if isinstance(hsv_array, np.ndarray) and len(hsv_array.shape) == 3 and hsv_array.shape[2] == 3:
            _h = hsv_array[:, :, 0]
            _s = hsv_array[:, :, 1]
            _v = hsv_array[:, :, 2]
            _s[np.where(_s < 0.0)] = 0.0
            _s[np.where(_s > 1.0)] = 1.0
            _v[np.where(_v < 0.0)] = 0.0
            _v[np.where(_v > 1.0)] = 1.0
            _h = np.round(_h % 360.0 * 1E5) / 1E5
            _s = np.round(_s * 1E5) / 1E5
            _v = np.round(_v * 1E5) / 1E5
            return np.stack((_h, _s, _v), axis=2).astype(np.float32)
        else:
            raise ValueError("expect hsv color in length 3: {}.".format(hsv_array))
    @classmethod

    def fmt_hec(cls, hec):
        _hec = re.match(r"[0-9A-F]+", str(hec).upper())
        if _hec and len(_hec[0]) == 6:
            return _hec[0]
        else:
            raise ValueError("expect hec color in hex type and length 6: {}.".format(hec))
    @classmethod

    def fmt_lab(cls, lab):
        if len(lab) == 3:
            _l, _a, _b = lab
            _l = 0.0 if _l < 0.0 else _l
            _l = 100.0 if _l > 100.0 else _l
            _a = -128.0 if _a < -128.0 else _a
            _a = 128.0 if _a > 128.0 else _a
            _b = -128.0 if _b < -128.0 else _b
            _b = 128.0 if _b > 128.0 else _b
            return np.array((_l, _a, _b), dtype=np.float32)
        else:
            raise ValueError("expect lab color in length 3 and float: {}.".format(lab))
    @classmethod

    def fmt_cmyk(cls, cmyk):
        if len(cmyk) == 4:
            _cmyk = np.array(cmyk)
            _cmyk[np.where(_cmyk < 0.0)] = 0.0
            _cmyk[np.where(_cmyk > 1.0)] = 1.0
            return _cmyk.astype(np.float32)
        else:
            raise ValueError("expect cmyk color in length 4 and float: {}.".format(cmyk))
    @classmethod

    def findall_hec_lst(cls, hec):
        _hec = re.findall(r"[0-9A-F]+", str(hec).upper())
        _hec = ["" if len(i) < 6 else i[:6] for i in _hec]
        while "" in _hec:
            _hec.remove("")
        return _hec
    @classmethod

    def sys_rgb2ryb(cls, h):
        _h = h % 360
        if 0 <= _h < 60:
            return _h / 60 * 120
        elif 60 <= _h < 240:
            return (_h - 60) / 180 * 120 + 120
        else:
            return _h
    @classmethod

    def sys_ryb2rgb(cls, h):
        _h = h % 360
        if 0 <= _h < 120:
            return _h / 120 * 60
        elif 120 <= _h < 240:
            return (_h - 120) / 120 * 180 + 60
        else:
            return _h
    @classmethod

    def stri2color(cls, stri):
        _stri = re.findall(r"[0-9A-F\.]+", str(stri).upper())
        if len(_stri) > 2:
            _num = re.findall(r"[0-9\.]+", str(stri))
            if len(_num) > 2:
                _a, _b, _c = _num[:3]
                _a = float(".".join(_a.split(".")[:2])) if "." in _a else int(_a)
                _b = float(".".join(_b.split(".")[:2])) if "." in _b else int(_b)
                _c = float(".".join(_c.split(".")[:2])) if "." in _c else int(_c)
                if _a > 255:
                    return Color((_a, _b, _c), tp="hsv")
                elif _b > 1.0 or _c > 1.0:
                    return Color((_a, _b, _c), tp="rgb")
                elif isinstance(_a, float) or isinstance(_b, float) or isinstance(_c, float):
                    return Color((_a, _b, _c), tp="hsv")
                else:
                    return Color((_a, _b, _c), tp="rgb")
            else:
                return None
        elif len(_stri) > 0:
            if len(_stri[0]) > 5:
                return Color(Color.fmt_hec(_stri[0]), tp="hec")
            return None
        else:
            return None
    @classmethod

    def rgb2hsv(cls, rgb):
        color = cls.fmt_rgb(rgb)
        v = max(color) / 255.0
        if abs(v - 0) < 1E-5:
            color = np.array((255, 0, 0))
        else:
            color = color / v
        s = 1 - min(color) / 255.0
        if abs(s - 0) < 1E-5:
            color = np.array((255, 0, 0))
        else:
            color = (color - 255 * (1 - s)) / s
            color = np.rint(color).astype(np.uint8)
        if color[0] == 255:
            if color[2] == 0:
                h = color[1] / 255 * 60
            elif color[1] == 0:
                h = 360 - color[2] / 255 * 60
            else:
                raise ValueError("value 0 is not found in red area: {}.".format(color))
        elif color[1] == 255:
            if color[0] == 0:
                h = 120 + color[2] / 255 * 60
            elif color[2] == 0:
                h = 120 - color[0] / 255 * 60
            else:
                raise ValueError("value 0 is not found in green area: {}.".format(color))
        elif color[2] == 255:
            if color[1] == 0:
                h = 240 + color[0] / 255 * 60
            elif color[0] == 0:
                h = 240 - color[1] / 255 * 60
            else:
                raise ValueError("value 0 is not found in blue area: {}.".format(color))
        else:
            raise ValueError("value 255 is not found in color: {}.".format(color))
        return cls.fmt_hsv((h, s, v))
    @classmethod

    def rgb2hsv_array(cls, rgb_array):
        colors = cls.fmt_rgb_array(rgb_array).astype(np.float64)
        v = np.max(colors, axis=2) / 255.0
        v[np.where(v < 1E-5)] = 1E-12
        colors[:, :, 0] = colors[:, :, 0] / v
        colors[:, :, 1] = colors[:, :, 1] / v
        colors[:, :, 2] = colors[:, :, 2] / v
        colors[np.where(v < 1E-5)] = np.array((255, 0, 0))
        v[np.where(v < 1E-5)] = 0
        s = 1 - np.min(colors, axis=2) / 255.0
        s[np.where(s < 1E-5)] = 1E-12
        colors[:, :, 0] = (colors[:, :, 0] - 255 * (1 - s)) / s
        colors[:, :, 1] = (colors[:, :, 1] - 255 * (1 - s)) / s
        colors[:, :, 2] = (colors[:, :, 2] - 255 * (1 - s)) / s
        colors[np.where(s < 1E-5)] = np.array((255, 0, 0))
        colors = np.rint(colors).astype(np.uint8)
        s[np.where(s < 1E-5)] = 0
        h = np.zeros(v.shape, dtype=np.float32)
        pos = np.where((colors[:, :, 2] == 255) & (colors[:, :, 0] == 0))
        h[pos] = 240 - colors[pos][:, 1] / 255 * 60
        pos = np.where((colors[:, :, 2] == 255) & (colors[:, :, 1] == 0))
        h[pos] = 240 + colors[pos][:, 0] / 255 * 60
        pos = np.where((colors[:, :, 1] == 255) & (colors[:, :, 2] == 0))
        h[pos] = 120 - colors[pos][:, 0] / 255 * 60
        pos = np.where((colors[:, :, 1] == 255) & (colors[:, :, 0] == 0))
        h[pos] = 120 + colors[pos][:, 2] / 255 * 60
        pos = np.where((colors[:, :, 0] == 255) & (colors[:, :, 1] == 0))
        h[pos] = 360 - colors[pos][:, 2] / 255 * 60
        pos = np.where((colors[:, :, 0] == 255) & (colors[:, :, 2] == 0))
        h[pos] = colors[pos][:, 1] / 255 * 60
        return cls.fmt_hsv_array(np.stack((h, s, v), axis=2))
    @classmethod

    def hsv2rgb(cls, hsv):
        h, s, v = cls.fmt_hsv(hsv)
        if 0 <= h < 60:
            g = round(h / 60 * 255)
            color = np.array((255, g, 0))
        elif 60 <= h < 120:
            r = round((1 - (h - 60) / 60) * 255)
            color = np.array((r, 255, 0))
        elif 120 <= h < 180:
            b = round((h - 120) / 60 * 255)
            color = np.array((0, 255, b))
        elif 180 <= h < 240:
            g = round((1 - (h - 180) / 60) * 255)
            color = np.array((0, g, 255))
        elif 240 <= h < 300:
            r = round((h - 240) / 60 * 255)
            color = np.array((r, 0, 255))
        elif 300 <= h < 360:
            b = round((1 - (h - 300) / 60) * 255)
            color = np.array((255, 0, b))
        else:
            raise ValueError("unexpect h: {}.".format(h))
        color = color + (color * -1 + 255) * (1 - s)
        color = color * v
        return cls.fmt_rgb(color)
    @classmethod

    def hsv2rgb_array(cls, hsv_array):
        colors = cls.fmt_hsv_array(hsv_array)
        r = np.zeros(colors.shape[:2], dtype=np.uint8)
        g = np.zeros(colors.shape[:2], dtype=np.uint8)
        b = np.zeros(colors.shape[:2], dtype=np.uint8)
        pos = np.where((colors[:, :, 0] >= 0) & (colors[:, :, 0] < 60))
        r[pos] = 255
        g[pos] = np.round(colors[pos][:, 0] / 60 * 255)
        pos = np.where((colors[:, :, 0] >= 60) & (colors[:, :, 0] < 120))
        r[pos] = np.round((1 - (colors[pos][:, 0] - 60) / 60) * 255)
        g[pos] = 255
        pos = np.where((colors[:, :, 0] >= 120) & (colors[:, :, 0] < 180))
        g[pos] = 255
        b[pos] = np.round((colors[pos][:, 0] - 120) / 60 * 255)
        pos = np.where((colors[:, :, 0] >= 180) & (colors[:, :, 0] < 240))
        g[pos] = np.round((1 - (colors[pos][:, 0] - 180) / 60) * 255)
        b[pos] = 255
        pos = np.where((colors[:, :, 0] >= 240) & (colors[:, :, 0] < 300))
        r[pos] = np.round((colors[pos][:, 0] - 240) / 60 * 255)
        b[pos] = 255
        pos = np.where((colors[:, :, 0] >= 300) & (colors[:, :, 0] < 360))
        r[pos] = 255
        b[pos] = np.round((1 - (colors[pos][:, 0] - 300) / 60) * 255)
        r = r + (r * -1 + 255) * (1 - colors[:, :, 1])
        g = g + (g * -1 + 255) * (1 - colors[:, :, 1])
        b = b + (b * -1 + 255) * (1 - colors[:, :, 1])
        r = r * colors[:, :, 2]
        g = g * colors[:, :, 2]
        b = b * colors[:, :, 2]
        return cls.fmt_rgb_array(np.stack((r, g, b), axis=2))
    @classmethod

    def rgb2hec(cls, rgb):
        r, g, b = cls.fmt_rgb(rgb)
        hec_r = hex(r)[2:].upper()
        hec_g = hex(g)[2:].upper()
        hec_b = hex(b)[2:].upper()
        hec_r = "0" + hec_r if len(hec_r) < 2 else hec_r
        hec_g = "0" + hec_g if len(hec_g) < 2 else hec_g
        hec_b = "0" + hec_b if len(hec_b) < 2 else hec_b
        return cls.fmt_hec(hec_r + hec_g + hec_b)
    @classmethod

    def hec2rgb(cls, hec):
        pr_hec_code = cls.fmt_hec(hec)
        hec_r = pr_hec_code[0:2]
        hec_g = pr_hec_code[2:4]
        hec_b = pr_hec_code[4:6]
        r = int("0x{}".format(hec_r), 16)
        g = int("0x{}".format(hec_g), 16)
        b = int("0x{}".format(hec_b), 16)
        return cls.fmt_rgb((r, g, b))
    @classmethod

    def hsv2hec(cls, hsv):
        rgb = cls.hsv2rgb(hsv)
        hec = cls.rgb2hec(rgb)
        return hec
    @classmethod

    def hec2hsv(cls, hec):
        rgb = cls.hec2rgb(hec)
        hsv = cls.rgb2hsv(rgb)
        return hsv
    @classmethod

    def rgb2lab(cls, rgb, white_ref=(95.047, 100.0, 108.883)):
        normed_rgb = [((i + 0.055) / 1.055) ** 2.4 if i > 0.04045 else i / 12.92 for i in cls.fmt_rgb(rgb) / 255.0]
        normed_rgb = np.array(normed_rgb) * 100.0
        xyz = np.array([
            [0.412453, 0.357580, 0.180423],
            [0.212671, 0.715160, 0.072169],
            [0.019334, 0.119193, 0.950227],
        ]).dot(normed_rgb) / white_ref
        normed_xyz = [i ** (1 / 3) if i > 0.008856 else (7.787 * i) + (16 / 116) for i in xyz]
        l = 116 * normed_xyz[1] - 16
        a = 500 * (normed_xyz[0] - normed_xyz[1])
        b = 200 * (normed_xyz[1] - normed_xyz[2])
        return cls.fmt_lab((l, a, b))
    @classmethod

    def lab2rgb(cls, lab, white_ref=(95.047, 100.0, 108.883)):
        l, a, b = cls.fmt_lab(lab)
        y = (l + 16) / 116
        x = a / 500 + y
        z = y - b / 200
        normed_xyz = [i ** 3 if i > 0.008856 else (i - 16 / 116) / 7.787 for i in (x, y, z)]
        xyz = np.array(normed_xyz) * white_ref / 100.0
        normed_rgb = np.array([
            [ 3.24048134, -1.53715152, -0.49853633],
            [-0.96925495,  1.87599   ,  0.04155593],
            [ 0.05564664, -0.20404134,  1.05731107],
        ]).dot(xyz)
        rgb = [1.055 * (i ** (1 / 2.4)) - 0.055 if i > 0.0031308 else 12.92 * i for i in normed_rgb]
        rgb = np.array(rgb) * 255
        return cls.fmt_rgb(rgb)
    @classmethod

    def rgb2cmyk(cls, rgb):
        r, g, b = cls.fmt_rgb(rgb)
        c = 1.0 - (r / 255.0)
        m = 1.0 - (g / 255.0)
        y = 1.0 - (b / 255.0)
        k = min((c, m, y))
        if k == 1.0:
            c = m = y = 0.0
        else:
            c = (c - k) / (1 - k)
            m = (m - k) / (1 - k)
            y = (y - k) / (1 - k)
        return cls.fmt_cmyk((c, m, y, k))
    @classmethod

    def cmyk2rgb(cls, cmyk):
        c, m, y, k = cls.fmt_cmyk(cmyk)
        c = (c * (1.0 - k) + k)
        m = (m * (1.0 - k) + k)
        y = (y * (1.0 - k) + k)
        r = (1.0 - c) * 255.0
        g = (1.0 - m) * 255.0
        b = (1.0 - y) * 255.0
        return cls.fmt_rgb((r, g, b))
    @classmethod

    def sign(cls, hsv):
        h, s, v = cls.fmt_hsv(hsv)
        if v < 0.08:
            return (0, 0)
        if v > 0.95 and s < 0.05:
            return (1, 1)
        prefix = 2
        for start, end, idx in ((0, 20, 0), (20, 40, 6), (40, 70, 1), (70, 160, 2), (160, 190, 3), (190, 250, 4), (250, 310, 5), (310, 340, 7), (340, 360, 0)):
            if start <= h % 360 < end:
                prefix = idx + 2
                break
        if 0.0 <= v < 0.25:
            return (2, prefix)
        elif 0.25 <= v < 0.5:
            if 0 <= s < 0.25:
                return (4, prefix)
            elif 0.25 <= s < 0.75:
                return (3, prefix)
            else:
                return (8, prefix)
        elif 0.5 <= v < 0.75:
            if 0 <= s < 0.5:
                return (4, prefix)
            else:
                return (8, prefix)
        else:
            if 0 <= s < 0.25:
                return (5, prefix)
            if 0.25 <= s < 0.5:
                return (6, prefix)
            if 0.5 <= s < 0.75:
                return (7, prefix)
            else:
                return (9, prefix)

class TestColor(unittest.TestCase):
    def test_translate(self):
        pr_color = Color((0, 0, 0), tp="rgb")
        for r in range(256):
            for g in range(256):
                print("testing rgb2hsv with r, g = {}, {}.".format(r, g))
                for b in range(256):
                    color = Color((r, g, b), tp="rgb")
                    self.assertEqual(color.rgb, (r, g, b))
                    self.assertEqual(color.r, r)
                    self.assertEqual(color.g, g)
                    self.assertEqual(color.b, b)
                    hsv = Color.rgb2hsv(color.rgb)
                    self.assertEqual(color.hsv, tuple(hsv))
                    self.assertEqual(color.h, hsv[0])
                    self.assertEqual(color.s, hsv[1])
                    self.assertEqual(color.v, hsv[2])
                    hsv_array = Color.rgb2hsv_array(np.array([[color.rgb]]))
                    self.assertTrue(abs(hsv[0] - hsv_array[0, 0][0]) < 1E-4)
                    self.assertTrue(abs(hsv[1] - hsv_array[0, 0][1]) < 1E-4)
                    self.assertTrue(abs(hsv[2] - hsv_array[0, 0][2]) < 1E-4)
                    rgb = Color.hsv2rgb(hsv)
                    self.assertTrue(color.rgb == tuple(rgb))
                    rgb_array = Color.hsv2rgb_array(hsv_array)
                    self.assertEqual(tuple(rgb), tuple(rgb_array[0, 0]))
                    pr_color.r = r
                    pr_color.g = g
                    pr_color.b = b
                    self.assertEqual(pr_color, color)
                    pr_color.h = hsv[0]
                    pr_color.s = hsv[1]
                    pr_color.v = hsv[2]
                    self.assertEqual(pr_color, color)
        for h in range(361):
            for s in range(101):
                print("testing hsv2rgb with h, s = {}, {}.".format(h, s))
                for v in range(101):
                    hsv = np.array([h, s / 100, v / 100])
                    color = Color(hsv, tp="hsv")
                    rgb = Color.hsv2rgb(hsv)
                    ar_hsv = Color.rgb2hsv(rgb)
                    ar_rgb = Color.hsv2rgb(ar_hsv)
                    self.assertTrue((rgb == ar_rgb).all())
                    ar_color = Color(ar_rgb, tp="rgb")
                    self.assertEqual(color, ar_color)
if __name__ == "__main__":
    unittest.main()
