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
from ricore.color import Color


class ColorSet(object):
    def __init__(self, h_range, s_range, v_range, overflow="cutoff", dep_wtp=1):
        self.synchronization = 0
        self.dep_wtp = dep_wtp
        self.set_hsv_ranges(h_range, s_range, v_range)
        assert 0.0 <= self._h_range[0] <= 360.0
        assert 0.0 <= self._h_range[1] <= 360.0
        assert self._h_range[0] <= self._h_range[1]
        assert 0.0 <= self._s_range[0] <= 1.0
        assert 0.0 <= self._s_range[1] <= 1.0
        assert self._s_range[0] <= self._s_range[1]
        assert 0.0 <= self._v_range[0] <= 1.0
        assert 0.0 <= self._v_range[1] <= 1.0
        assert self._v_range[0] <= self._v_range[1]
        self._color_set = [
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            ]
        self.initialize()

    def set_hsv_ranges(self, h_range, s_range, v_range):
        if isinstance(h_range, (tuple, list)) and isinstance(s_range, (tuple, list)) and isinstance(v_range, (tuple, list)):
            self._h_range = tuple([float(i) for i in h_range[:2]])
            self._s_range = tuple([float(i) for i in s_range[:2]])
            self._v_range = tuple([float(i) for i in v_range[:2]])
        else:
            raise ValueError("expect h, s, v ranges in tuple or list type: {}, {}, {}.".format(h_range, s_range, v_range))

    def set_color_system(self, dep_wtp):
        self.dep_wtp = dep_wtp

    def set_overflow(self, overflow):
        for color in self._color_set:
            color.set_overflow(overflow)

    def get_overflow(self):
        assert self._color_set[1].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[2].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[3].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[4].get_overflow() == self._color_set[0].get_overflow()
        return self._color_set[0].get_overflow()

    def __str__(self):
        return "ColorSet({}, {}, {}, {}, {})".format(*self._color_set)

    def __repr__(self):
        return "ColorSet({}, {}, {}, {}, {})".format(*self._color_set)

    def __getitem__(self, idx):
        return self._color_set[idx]

    def __len__(self):
        return 5

    def backup(self):
        color_set = (
            Color(self._color_set[0], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[1], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[2], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[3], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[4], tp="color", overflow=self.get_overflow()),
        )
        return color_set

    def recover(self, color_set):
        self._color_set = [
            Color(color_set[0], tp="color", overflow=self.get_overflow()),
            Color(color_set[1], tp="color", overflow=self.get_overflow()),
            Color(color_set[2], tp="color", overflow=self.get_overflow()),
            Color(color_set[3], tp="color", overflow=self.get_overflow()),
            Color(color_set[4], tp="color", overflow=self.get_overflow()),
        ]

    def initialize(self):
        for i in range(5):
            h = self._h_range[0] + (self._h_range[1] - self._h_range[0]) * random.random()
            s = self._s_range[0] + (self._s_range[1] - self._s_range[0]) * random.random()
            v = self._v_range[0] + (self._v_range[1] - self._v_range[0]) * random.random()
            if self.dep_wtp:
                h = Color.sys_ryb2rgb(h)
            self._color_set[i].hsv = (h, s, v)

    def create(self, harmony_rule):
        if harmony_rule == "custom":
            return
        methods = {
            "analogous": self._analogous_create,
            "monochromatic": self._monochromatic_create,
            "triad": self._triad_create,
            "tetrad": self._tetrad_create,
            "pentad": self._pentad_create,
            "complementary": self._complementary_create,
            "shades": self._shades_create,
        }
        if harmony_rule in methods:
            methods[harmony_rule]()
        else:
            raise ValueError("expect harmony rule in list 'analogous', 'monochromatic', etc.: {}.".format(harmony_rule))

    def modify(self, harmony_rule, idx, color, do_sync=True):
        if do_sync and self.synchronization:
            self._sync_modify(idx, color)
        else:
            methods = {
                "analogous": self._analogous_modify,
                "monochromatic": self._monochromatic_modify,
                "triad": self._multiple_modify,
                "tetrad": self._tetrad_modify,
                "pentad": self._multiple_modify,
                "complementary": self._multiple_modify,
                "shades": self._shades_modify,
                "custom": self._custom_modify,
            }
            if harmony_rule in methods:
                methods[harmony_rule](idx, color)
            else:
                raise ValueError("unexpect harmony rule name for modify: {}.".format(harmony_rule))

    def _rotate(self, delta_h, delta_s, delta_v):
        for idx in range(5):
            if self.dep_wtp:
                self._color_set[idx].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[idx].h) + delta_h)
            else:
                self._color_set[idx].h = self._color_set[idx].h + delta_h
            self._color_set[idx].s = self._color_set[idx].s + delta_s
            self._color_set[idx].v = self._color_set[idx].v + delta_v

    def _analogous_create(self):
        if self.dep_wtp:
            angle = (Color.sys_rgb2ryb(self._color_set[3].h) - Color.sys_rgb2ryb(self._color_set[1].h)) / 2
        else:
            angle = (self._color_set[3].h - self._color_set[1].h) / 2
        while angle > 30.0 or angle < -30.0:
            angle = angle / 1.5
        if self.dep_wtp:
            self._color_set[1].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - angle)
            self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - angle * 2)
            self._color_set[3].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + angle)
            self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + angle * 2)
        else:
            self._color_set[1].h = self._color_set[0].h - angle
            self._color_set[2].h = self._color_set[0].h - angle * 2
            self._color_set[3].h = self._color_set[0].h + angle
            self._color_set[4].h = self._color_set[0].h + angle * 2

    def _analogous_modify(self, idx, pr_color):
        if idx == 0:
            if self.dep_wtp:
                delta_h = Color.sys_rgb2ryb(pr_color.h) - Color.sys_rgb2ryb(self._color_set[0].h)
            else:
                delta_h = pr_color.h - self._color_set[0].h
            delta_s = pr_color.s - self._color_set[0].s
            delta_v = pr_color.v - self._color_set[0].v
            self._rotate(delta_h, delta_s, delta_v)
        else:
            if idx in (1, 2):
                if self.dep_wtp:
                    angle = Color.sys_rgb2ryb(self._color_set[0].h) - Color.sys_rgb2ryb(pr_color.h)
                else:
                    angle = self._color_set[0].h - pr_color.h
            else:
                if self.dep_wtp:
                    angle = Color.sys_rgb2ryb(pr_color.h) - Color.sys_rgb2ryb(self._color_set[0].h)
                else:
                    angle = pr_color.h - self._color_set[0].h
            if idx in (2, 4):
                angle = angle - 360 if angle > 180 else angle
                angle = angle + 360 if angle < -180 else angle
                angle /= 2
            if self.dep_wtp:
                self._color_set[1].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - angle)
                self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - angle * 2)
                self._color_set[3].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + angle)
                self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + angle * 2)
            else:
                self._color_set[1].h = self._color_set[0].h - angle
                self._color_set[2].h = self._color_set[0].h - angle * 2
                self._color_set[3].h = self._color_set[0].h + angle
                self._color_set[4].h = self._color_set[0].h + angle * 2
        self._color_set[idx] = pr_color

    def _monochromatic_create(self):
        self._color_set[1].h = self._color_set[0].h
        self._color_set[2].h = self._color_set[0].h
        self._color_set[3].h = self._color_set[0].h
        self._color_set[4].h = self._color_set[0].h
        us_random = self._color_set[0].s
        ls_random = self._color_set[0].s
        if us_random < 0.5:
            us_random = us_random + 0.2 + 0.25 * random.random()
            ls_random = ls_random + 0.15 * random.random()
        else:
            us_random = us_random - 0.2 - 0.25 * random.random()
            ls_random = ls_random - 0.15 * random.random()
        uv_random = self._color_set[0].v
        lv_random = self._color_set[0].v
        if uv_random < 0.5:
            uv_random = uv_random + 0.2 + 0.25 * random.random()
            lv_random = lv_random + 0.15 * random.random()
        else:
            uv_random = uv_random - 0.2 - 0.25 * random.random()
            lv_random = lv_random - 0.15 * random.random()
        self._color_set[1].s = us_random
        self._color_set[2].s = us_random
        self._color_set[3].s = ls_random
        self._color_set[4].s = ls_random
        self._color_set[1].v = uv_random
        self._color_set[2].v = lv_random
        self._color_set[3].v = uv_random
        self._color_set[4].v = lv_random

    def _monochromatic_modify(self, idx, pr_color):
        for i in range(5):
            self._color_set[i].h = pr_color.h
        self._color_set[idx] = pr_color

    def _triad_create(self):
        if self.dep_wtp:
            self._color_set[1].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 120.0)
            self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 120.0)
            self._color_set[3].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 120.0)
            self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 120.0)
        else:
            self._color_set[1].h = self._color_set[0].h - 120.0
            self._color_set[2].h = self._color_set[0].h - 120.0
            self._color_set[3].h = self._color_set[0].h + 120.0
            self._color_set[4].h = self._color_set[0].h + 120.0

    def _multiple_modify(self, idx, pr_color):
        if self.dep_wtp:
            delta_h = Color.sys_rgb2ryb(pr_color.h) - Color.sys_rgb2ryb(self._color_set[idx].h)
        else:
            delta_h = pr_color.h - self._color_set[idx].h
        if idx == 0:
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
            self._rotate(delta_h, delta_s, delta_v)
        else:
            if self.dep_wtp:
                for i in range(5):
                    self._color_set[i].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[i].h) + delta_h)
            else:
                for i in range(5):
                    self._color_set[i].h = self._color_set[i].h + delta_h
        self._color_set[idx] = pr_color

    def _tetrad_create(self):
        if self.dep_wtp:
            self._color_set[1].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 90)
            self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 180)
            self._color_set[3].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 90)
            self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 180)
        else:
            self._color_set[1].h = self._color_set[0].h - 90
            self._color_set[2].h = self._color_set[0].h - 180
            self._color_set[3].h = self._color_set[0].h + 90
            self._color_set[4].h = self._color_set[0].h + 180

    def _tetrad_modify(self, idx, pr_color):
        if self.dep_wtp:
            delta_h = Color.sys_rgb2ryb(pr_color.h) - Color.sys_rgb2ryb(self._color_set[idx].h)
        else:
            delta_h = pr_color.h - self._color_set[idx].h
        if idx == 0:
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
            self._rotate(delta_h, delta_s, delta_v)
        else:
            if idx in (2, 4):
                self._color_set[0].h += delta_h
                self._color_set[2].h += delta_h
                self._color_set[4].h += delta_h
            else:
                self._color_set[1].h += delta_h
                self._color_set[3].h += delta_h
        self._color_set[idx] = pr_color

    def _pentad_create(self):
        if self.dep_wtp:
            self._color_set[1].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 72)
            self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) - 144)
            self._color_set[3].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 72)
            self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 144)
        else:
            self._color_set[1].h = self._color_set[0].h - 72
            self._color_set[2].h = self._color_set[0].h - 144
            self._color_set[3].h = self._color_set[0].h + 72
            self._color_set[4].h = self._color_set[0].h + 144

    def _complementary_create(self):
        self._color_set[1].h = self._color_set[0].h
        self._color_set[3].h = self._color_set[0].h
        if self.dep_wtp:
            self._color_set[2].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 180.0)
            self._color_set[4].h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._color_set[0].h) + 180.0)
        else:
            self._color_set[2].h = self._color_set[0].h + 180.0
            self._color_set[4].h = self._color_set[0].h + 180.0
        us_random = self._color_set[0].s
        ls_random = self._color_set[0].s
        if us_random < 0.5:
            us_random = us_random + 0.2 + 0.25 * random.random()
            ls_random = ls_random + 0.15 * random.random()
        else:
            us_random = us_random - 0.2 - 0.25 * random.random()
            ls_random = ls_random - 0.15 * random.random()
        uv_random = self._color_set[0].v
        lv_random = self._color_set[0].v
        if uv_random < 0.5:
            uv_random = uv_random + 0.2 + 0.25 * random.random()
            lv_random = lv_random + 0.15 * random.random()
        else:
            uv_random = uv_random - 0.2 - 0.25 * random.random()
            lv_random = lv_random - 0.15 * random.random()
        self._color_set[1].s = us_random
        self._color_set[2].s = us_random
        self._color_set[3].s = ls_random
        self._color_set[4].s = ls_random
        self._color_set[1].v = uv_random
        self._color_set[2].v = lv_random
        self._color_set[3].v = uv_random
        self._color_set[4].v = lv_random

    def _shades_create(self):
        self._color_set[1].hsv = self._color_set[0].hsv
        self._color_set[2].hsv = self._color_set[0].hsv
        self._color_set[3].hsv = self._color_set[0].hsv
        self._color_set[4].hsv = self._color_set[0].hsv
        self._color_set[1].v = 0.15
        self._color_set[2].v = 0.40
        self._color_set[3].v = 0.65
        self._color_set[4].v = 0.90

    def _shades_modify(self, idx, pr_color):
        for i in range(5):
            self._color_set[i].h = pr_color.h
            self._color_set[i].s = pr_color.s
        self._color_set[idx] = pr_color

    def _custom_modify(self, idx, pr_color):
        if idx in range(5):
            self._color_set[idx].hsv = pr_color.hsv
        else:
            raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))

    def _sync_modify(self, idx, pr_color):
        if self.dep_wtp:
            delta_h = Color.sys_rgb2ryb(pr_color.h) - Color.sys_rgb2ryb(self._color_set[idx].h)
        else:
            delta_h = pr_color.h - self._color_set[idx].h
        if self.synchronization == 1:
            delta_h = 0
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
        elif self.synchronization == 2:
            delta_s = delta_v = 0
        elif self.synchronization == 3:
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
        elif self.synchronization == 4:
            for i in range(5):
                self._color_set[i].s = pr_color.s
                self._color_set[i].v = pr_color.v
            delta_s = 0
            delta_v = 0
        elif self.synchronization == 5:
            if idx == 1:
                self._color_set[1].s = pr_color.s
                self._color_set[2].s = self._color_set[1].s * 2 - self._color_set[0].s
                self._color_set[4].s = self._color_set[3].s * 2 - self._color_set[0].s
                self._color_set[1].v = pr_color.v
                self._color_set[2].v = self._color_set[1].v * 2 - self._color_set[0].v
                self._color_set[4].v = self._color_set[3].v * 2 - self._color_set[0].v
            elif idx == 3:
                self._color_set[3].s = pr_color.s
                self._color_set[2].s = self._color_set[1].s * 2 - self._color_set[0].s
                self._color_set[4].s = self._color_set[3].s * 2 - self._color_set[0].s
                self._color_set[3].v = pr_color.v
                self._color_set[2].v = self._color_set[1].v * 2 - self._color_set[0].v
                self._color_set[4].v = self._color_set[3].v * 2 - self._color_set[0].v
            elif idx == 2:
                self._color_set[2].s = pr_color.s
                self._color_set[1].s = (self._color_set[2].s + self._color_set[0].s) / 2
                self._color_set[3].s = (self._color_set[4].s + self._color_set[0].s) / 2
                self._color_set[2].v = pr_color.v
                self._color_set[1].v = (self._color_set[2].v + self._color_set[0].v) / 2
                self._color_set[3].v = (self._color_set[4].v + self._color_set[0].v) / 2
            elif idx == 4:
                self._color_set[4].s = pr_color.s
                self._color_set[1].s = (self._color_set[2].s + self._color_set[0].s) / 2
                self._color_set[3].s = (self._color_set[4].s + self._color_set[0].s) / 2
                self._color_set[4].v = pr_color.v
                self._color_set[1].v = (self._color_set[2].v + self._color_set[0].v) / 2
                self._color_set[3].v = (self._color_set[4].v + self._color_set[0].v) / 2
            else:
                self._color_set[0].s = pr_color.s
                self._color_set[1].s = (self._color_set[2].s + self._color_set[0].s) / 2
                self._color_set[3].s = (self._color_set[4].s + self._color_set[0].s) / 2
                self._color_set[0].v = pr_color.v
                self._color_set[1].v = (self._color_set[2].v + self._color_set[0].v) / 2
                self._color_set[3].v = (self._color_set[4].v + self._color_set[0].v) / 2
            delta_s = 0
            delta_v = 0
        elif self.synchronization == 6:
            self._color_set[idx].s = pr_color.s
            self._color_set[idx].v = pr_color.v
            if idx in (1, 2):
                self._color_set[3].s = self._color_set[1].s
                self._color_set[4].s = self._color_set[2].s
                self._color_set[3].v = self._color_set[1].v
                self._color_set[4].v = self._color_set[2].v
            elif idx in (3, 4):
                self._color_set[1].s = self._color_set[3].s
                self._color_set[2].s = self._color_set[4].s
                self._color_set[1].v = self._color_set[3].v
                self._color_set[2].v = self._color_set[4].v
            else:
                self._color_set[1].s = (self._color_set[1].s + self._color_set[3].s) / 2
                self._color_set[2].s = (self._color_set[2].s + self._color_set[4].s) / 2
                self._color_set[3].s = self._color_set[1].s
                self._color_set[4].s = self._color_set[2].s
                self._color_set[1].v = (self._color_set[1].v + self._color_set[3].v) / 2
                self._color_set[2].v = (self._color_set[2].v + self._color_set[4].v) / 2
                self._color_set[3].v = self._color_set[1].v
                self._color_set[4].v = self._color_set[2].v
            delta_s = 0
            delta_v = 0
        else:
            raise ValueError("unexpect synchronization code for special rule: {}.".format(self.synchronization))
        self._rotate(delta_h, delta_s, delta_v)
