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

import unittest
import numpy as np


class FakeColor(object):
    """
    FakeColor object. Storing rgb, hsv and hex code (hec) color without functional methods.
    """

    def __init__(self, rgb, hsv, hec):
        """
        Init FakeColor ojbect.

        Args:
            rgb (tuple or list): rgb color.
            rgb (tuple or list): hsv color.
            hec (str): hex code (hec).
        """

        self.rgb = Color.fmt_rgb(rgb)
        self.hsv = Color.fmt_hsv(hsv)
        self.hec = Color.fmt_hec(hec)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def export(self):
        """
        Export color in dict type (for json file).

        Returns:
          color dict {"rgb": rgb_color_list, "hsv": hsv_color_list, "hex_code": hex code (hec)}.
        """

        return {"rgb": self.rgb.tolist(), "hsv": self.hsv.tolist(), "hex_code": self.hec}


class Color(object):
    """
    Color object. Storing rgb, hsv and hex code (hec) color.
    """

    def __init__(self, item, tp="color", overflow="cutoff"):
        """
        Init Color ojbect.

        Args:
            item (tuple, list, str or Color): rgb, hsv, hex code (hec) or another Color object.
            tp (str): type of color, in "rgb", "hsv", "hec" and "color".
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        self.set_overflow(overflow)

        if isinstance(tp, str) and tp in ("rgb", "hsv", "hec", "color"):
            self.setti(item, tp)

        else:
            raise ValueError("expect tp in str type and list 'rgb', 'hsv', 'hec' and 'color': {}.".format(tp))

    # ---------- ---------- ---------- Setting and Getting Funcs ---------- ---------- ---------- #

    def setti(self, item, tp):
        """
        Set color item.

        Args:
            item (tuple, list, str, int, float or Color): rgb, hsv, hex code (hec), r, g, b, h, s, v or another Color object.
            tp (str): type of color, in  "rgb", "hsv", "hec", "r", "g", "b", "h", "s", "v" and "color".
        """

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
        """
        Get color item.

        Args:
            tp (str): type of color, in  "rgb", "hsv", "hec", "r", "g", "b", "h", "s", "v" and "color".

        Returns:
            rgb, hsv, hex code (hec), r, g, b, h, s, v or another Color object.
        """

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
        """
        Set the overflow method.

        Args:
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        if isinstance(overflow, str) and overflow in ("cutoff", "return", "repeat"):
            self._overflow = str(overflow)

        else:
            raise ValueError("expect value in str type and list 'cutoff', 'return', 'repeat': {}.".format(overflow))

    def get_overflow(self):
        """
        Get the overflow method.
        """

        return str(self._overflow)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __str__(self):
        """
        Str format.
        """

        return "Color(hec {})".format(self.hec)

    def __repr__(self):
        """
        Repr format.
        """

        return "Color(hec {})".format(self.hec)

    '''
    def __eq__(self, other):
        """
        Compare two colors by equal.

        Args:
            other (Color): another Color object for compare.

        Returns:
            True or False.
        """

        if isinstance(other, Color):
            return self._hec == other.hec

        else:
            raise ValueError("expect other in Color type: {}.".format(other))

    def __ne__(self, other):
        """
        Compare two colors by not equal.

        Args:
            other (Color): another Color object for compare.

        Returns:
            True or False.
        """

        if isinstance(other, Color):
            return self._hec != other.hec

        else:
            raise ValueError("expect other in Color type: {}.".format(other))
    '''

    # ---------- ---------- ---------- Properties and Setters ---------- ---------- ---------- #

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

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def export(self):
        """
        Export color in dict type (for json file).

        Returns:
          color dict {"rgb": rgb_color_list, "hsv": hsv_color_list, "hex_code": hex code (hec)}.
        """

        return {"rgb": self._rgb.tolist(), "hsv": self._hsv.tolist(), "hex_code": self._hec}

    def ref_h(self, hue):
        """
        Get reference hue angle by hue.

        Args:
            hue (int or float): hue value.

        Returns:
            relative hue angle.
        """

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
        """
        Get reference hue angle array by hue.

        Args:
            hue (int or float): hue array value.

        Returns:
            relative hue angle array.
        """

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

    # ---------- ---------- ---------- Classmethods ---------- ---------- ---------- #

    @classmethod
    def fmt_rgb(cls, rgb):
        """
        Class method. Format item to standard rgb color.

        Args:
            rgb (tuple or list): color item to be formated.

        Returns:
            standard rgb color.
        """

        if len(rgb) == 3:
            _rgb = np.rint(rgb)
            _rgb[np.where(_rgb < 0)] = 0
            _rgb[np.where(_rgb > 255)] = 255

            return _rgb.astype(np.uint8)

        else:
            raise ValueError("expect rgb color in length 3 and int: {}.".format(rgb))

    @classmethod
    def fmt_rgb_array(cls, rgb_array):
        """
        Class method. Format item to standard rgb array.

        Args:
            rgb_array (3D array): array item to be formated.

        Returns:
            standard rgb array.
        """

        if isinstance(rgb_array, np.ndarray) and len(rgb_array.shape) == 3 and rgb_array.shape[2] == 3:
            _rgb = np.rint(rgb_array)
            _rgb[np.where(_rgb < 0)] = 0
            _rgb[np.where(_rgb > 255)] = 255

            return _rgb.astype(np.uint8)

        else:
            raise ValueError("expect rgb array in length 3: {}.".format(rgb_array))

    @classmethod
    def fmt_hsv(cls, hsv, overflow="cutoff"):
        """
        Class method. Format item to standard hsv color.

        Args:
            hsv (tuple or list): color item to be formated.
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".

        Returns:
            standard hsv color.
        """

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
        """
        Class method. Format item to standard hsv array.

        Args:
            hsv_array (3D array): array item to be formated.

        Returns:
            standard hsv array.
        """

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
        """
        Class method. Format item to standard hex code (hec) color.

        Args:
            hec (str): color item to be formated.

        Returns:
            standard hex code (hec) color.
        """

        if not isinstance(hec, str):
            raise ValueError("expect hex code (hec) in str type: {}.".format(hec))

        if len(hec) == 6:
            for stri in hec.upper():
                if stri not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"):
                    raise ValueError("expect code in hex type: {}.".format(hec))

        else:
            raise ValueError("expect hex code (hec) in length 6: {}.".format(hec))

        return hec.upper()

    @classmethod
    def fmt_lab(cls, lab):
        """
        Class method. Format item to standard lab color.

        Args:
            lab (tuple or list): color item to be formated.

        Returns:
            standard lab color.
        """

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
        """
        Class method. Format item to standard cmyk color.

        Args:
            cmyk (tuple or list): color item to be formated.

        Returns:
            standard cmyk color.
        """

        if len(cmyk) == 4:
            _cmyk = np.array(cmyk)
            _cmyk[np.where(_cmyk < 0.0)] = 0.0
            _cmyk[np.where(_cmyk > 1.0)] = 1.0

            return _cmyk.astype(np.float32)

        else:
            raise ValueError("expect cmyk color in length 4 and float: {}.".format(cmyk))

    @classmethod
    def rgb2hsv(cls, rgb):
        """
        Translate rgb color into hsv color.

        Args:
            rgb (tuple or list): rgb color.

        Returns:
            hsv color.
        """

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
                # red to yellow, 0 to 60.
                h = color[1] / 255 * 60

            elif color[1] == 0:
                # magenta to red, 300 to 360.
                h = 360 - color[2] / 255 * 60

            else:
                raise ValueError("value 0 is not found in red area: {}.".format(color))

        elif color[1] == 255:
            if color[0] == 0:
                # green to cyan, 120 to 180.
                h = 120 + color[2] / 255 * 60

            elif color[2] == 0:
                # yellow to green, 60 to 120.
                h = 120 - color[0] / 255 * 60

            else:
                raise ValueError("value 0 is not found in green area: {}.".format(color))

        elif color[2] == 255:
            if color[1] == 0:
                # blue to magenta, 240 to 300.
                h = 240 + color[0] / 255 * 60

            elif color[0] == 0:
                # cyan to blue, 180 to 240.
                h = 240 - color[1] / 255 * 60

            else:
                raise ValueError("value 0 is not found in blue area: {}.".format(color))

        else:
            raise ValueError("value 255 is not found in color: {}.".format(color))

        return cls.fmt_hsv((h, s, v))

    @classmethod
    def rgb2hsv_array(cls, rgb_array):
        """
        Translate rgb array into hsv array.

        Args:
            rgb (3D array): rgb array.

        Returns:
            hsv array.
        """

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

        # cyan to blue, 180 to 240.
        pos = np.where((colors[:, :, 2] == 255) & (colors[:, :, 0] == 0))
        h[pos] = 240 - colors[pos][:, 1] / 255 * 60

        # blue to magenta, 240 to 300.
        pos = np.where((colors[:, :, 2] == 255) & (colors[:, :, 1] == 0))
        h[pos] = 240 + colors[pos][:, 0] / 255 * 60

        # yellow to green, 60 to 120.
        pos = np.where((colors[:, :, 1] == 255) & (colors[:, :, 2] == 0))
        h[pos] = 120 - colors[pos][:, 0] / 255 * 60

        # green to cyan, 120 to 180.
        pos = np.where((colors[:, :, 1] == 255) & (colors[:, :, 0] == 0))
        h[pos] = 120 + colors[pos][:, 2] / 255 * 60

        # magenta to red, 300 to 360.
        pos = np.where((colors[:, :, 0] == 255) & (colors[:, :, 1] == 0))
        h[pos] = 360 - colors[pos][:, 2] / 255 * 60

        # red to yellow, 0 to 60.
        pos = np.where((colors[:, :, 0] == 255) & (colors[:, :, 2] == 0))
        h[pos] = colors[pos][:, 1] / 255 * 60

        return cls.fmt_hsv_array(np.stack((h, s, v), axis=2))

    @classmethod
    def hsv2rgb(cls, hsv):
        """
        Translate hsv color into rgb color.

        Args:
            hsv (tuple or list): hsv color.

        Returns:
            rgb color.
        """

        h, s, v = cls.fmt_hsv(hsv)

        # red to yellow.
        if 0 <= h < 60:
            g = round(h / 60 * 255)
            color = np.array((255, g, 0))

        # yellow to green.
        elif 60 <= h < 120:
            r = round((1 - (h - 60) / 60) * 255)
            color = np.array((r, 255, 0))

        # green to cyan.
        elif 120 <= h < 180:
            b = round((h - 120) / 60 * 255)
            color = np.array((0, 255, b))

        # cyan to blue.
        elif 180 <= h < 240:
            g = round((1 - (h - 180) / 60) * 255)
            color = np.array((0, g, 255))

        # blue to magenta.
        elif 240 <= h < 300:
            r = round((h - 240) / 60 * 255)
            color = np.array((r, 0, 255))

        # magenta to red.
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
        """
        Translate hsv array into rgb array.

        Args:
            hsv (3D array): hsv array.

        Returns:
            rgb array.
        """

        colors = cls.fmt_hsv_array(hsv_array)

        r = np.zeros(colors.shape[:2], dtype=np.uint8)
        g = np.zeros(colors.shape[:2], dtype=np.uint8)
        b = np.zeros(colors.shape[:2], dtype=np.uint8)

        # red to yellow.
        pos = np.where((colors[:, :, 0] >= 0) & (colors[:, :, 0] < 60))
        r[pos] = 255
        g[pos] = np.round(colors[pos][:, 0] / 60 * 255)

        # yellow to green.
        pos = np.where((colors[:, :, 0] >= 60) & (colors[:, :, 0] < 120))
        r[pos] = np.round((1 - (colors[pos][:, 0] - 60) / 60) * 255)
        g[pos] = 255

        # green to cyan.
        pos = np.where((colors[:, :, 0] >= 120) & (colors[:, :, 0] < 180))
        g[pos] = 255
        b[pos] = np.round((colors[pos][:, 0] - 120) / 60 * 255)

        # cyan to blue.
        pos = np.where((colors[:, :, 0] >= 180) & (colors[:, :, 0] < 240))
        g[pos] = np.round((1 - (colors[pos][:, 0] - 180) / 60) * 255)
        b[pos] = 255

        # blue to magenta.
        pos = np.where((colors[:, :, 0] >= 240) & (colors[:, :, 0] < 300))
        r[pos] = np.round((colors[pos][:, 0] - 240) / 60 * 255)
        b[pos] = 255

        # magenta to red.
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
        """
        Translate rgb color into hex code (hec) color.

        Args:
            rgb (tuple or list): rgb color.

        Returns:
            hex code (hec) color.
        """

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
        """
        Translate hex code (hec) color into rgb color.

        Args:
            hec (str): hex code (hec) color.

        Returns:
            rgb color.
        """

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
        """
        Translate hsv color into hex code (hec) color.

        Args:
            hsv (tuple or list): hsv color.

        Returns:
            hex code (hec) color.
        """

        rgb = cls.hsv2rgb(hsv)
        hec = cls.rgb2hec(rgb)

        return hec

    @classmethod
    def hec2hsv(cls, hec):
        """
        Translate hex code (hec) color into rgb color.

        Args:
            hec (str): hex code (hec) color.

        Returns:
            rgb color.
        """

        rgb = cls.hec2rgb(hec)
        hsv = cls.rgb2hsv(rgb)

        return hsv

    @classmethod
    def rgb2lab(cls, rgb, white_ref=(95.047, 100.0, 108.883)):
        """
        Translate rgb color into lab color (ref: http://www.easyrgb.com/en/math.php).

        Args:
            rgb (tuple or list): rgb color.
            white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".

        Returns:
            lab color.
        """

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
        """
        Translate lab color into rgb color (ref: http://www.easyrgb.com/en/math.php).

        Args:
            lab (tuple or list): lab color.
            white_ref (tuple or list): xyz (Tristimulus) Reference values of a perfect reflecting diffuser. default: value of standard "D65, 2Ang".

        Returns:
            rgb color.
        """

        lab = cls.fmt_lab(lab)

        y = (lab[0] + 16) / 116
        x = lab[1] / 500 + y
        z = y - lab[2] / 200

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
        """
        Translate rgb color into cmyk color (ref: http://www.easyrgb.com/en/math.php).

        Args:
            rgb (tuple or list): rgb color.

        Returns:
            cmyk color.
        """

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
        """
        Translate cmyk color into rgb color (ref: http://www.easyrgb.com/en/math.php).

        Args:
            cmyk (tuple or list): cmyk color.

        Returns:
            rgb color.
        """

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
        """
        Sign the name of color by dividing colors into different blocks by h, s and v values.

        Diagram:
            s
            +---+---+---+---+
            | 5 | 6 | 7 | 9 |
            +---+---+---+---+
            | 4 | 4 | 8 | 8 |
            +---+---+---+---+
            | 4 | 3 | 3 | 8 |
            +---+---+---+---+
            | 2 | 2 | 2 | 2 |
            +---+---+---+---+ v

            0 - deep black; 1 - snow white; 2 - heavy; 3 - dull; 4 - grey; 5 - pale, 6 - light; 7 - bright; 8 - dark; 9 - vivid.

        Args:
            hsv (tuple or list): hsv color.

        Returns:
            serial number of color name.
        """

        h, s, v = cls.fmt_hsv(hsv)

        if v < 0.08:
            return (0, 0)

        if v > 0.95 and s < 0.05:
            return (1, 1)

        prefix = int((h + 30) // 60 % 6) + 2

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
    """
    Test Color object.
    """

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
