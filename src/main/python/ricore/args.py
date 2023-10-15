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
import json
import re
import time
import locale
import shutil
import unittest
from ricore.color_set import ColorSet
from ricore.check import check_key, check_file_name, check_nonempt_str_lst


class Args(object):
    """
    Args object. Manage setting args.
    """

    def __init__(self, resources, resetall=False, uselang=""):
        """
        Init Args object.
        """

        self.info_version_zh = "v2.8.41-x3d3s3-稳定版"
        self.info_version_en = "v2.8.41-x3d3s3-stable"
        self.info_date_zh = "2023年10月15日"
        self.info_date_en = "October 15, 2023"
        self.global_temp_dir = None
        self.global_hm_rules = (
            "analogous",
            "monochromatic",
            "triad",
            "tetrad",
            "pentad",
            "complementary",
            "shades",
            "custom",
        )

        self.global_overflows = (
            "cutoff",
            "return",
            "repeat",
        )

        self.global_white_ref = (
            ((109.850, 100.000, 35.585), (111.144, 100.000, 35.200)),
            ((99.0927, 100.000, 85.313), (99.178, 100.000, 84.3493)),
            ((98.074, 100.000, 118.232), (97.285, 100.000, 116.145)),
            ((96.422, 100.000, 82.521), (96.720, 100.000, 81.427)),
            ((95.682, 100.000, 92.149), (95.799, 100.000, 90.926)),
            ((95.047, 100.000, 108.883), (94.811, 100.000, 107.304)),
            ((94.972, 100.000, 122.638), (94.416, 100.000, 120.641)),
            ((100.000, 100.000, 100.000), (100.000, 100.000, 100.000)),
            ((92.834, 100.000, 103.665), (94.791, 100.000, 103.191)),
            ((99.187, 100.000, 67.395), (103.280, 100.000, 69.026)),
            ((103.754, 100.000, 49.861), (108.968, 100.000, 51.965)),
            ((109.147, 100.000, 38.813), (114.961, 100.000, 40.963)),
            ((90.872, 100.000, 98.723), (93.369, 100.000, 98.636)),
            ((97.309, 100.000, 60.191), (102.148, 100.000, 62.074)),
            ((95.044, 100.000, 108.755), (95.792, 100.000, 107.687)),
            ((96.413, 100.000, 82.333), (97.115, 100.000, 81.135)),
            ((100.365, 100.000, 67.868), (102.116, 100.000, 67.826)),
            ((96.174, 100.000, 81.712), (99.001, 100.000, 83.134)),
            ((100.966, 100.000, 64.370), (103.866, 100.000, 65.627)),
            ((108.046, 100.000, 39.228), (111.428, 100.000, 40.353)),
        )

        self.global_log = False
        all_langs = (
            "en", "ar", "be", "bg", "ca", "cs", "da", "de", "el", "eo",
            "es", "et", "fi", "fr", "hr", "hu", "is", "it", "iw", "ja",
            "ko", "lt", "lv", "mk", "nl", "no", "pl", "pt", "ro", "ru",
            "sh", "sk", "sl", "sq", "sr", "sv", "th", "tr", "uk", "vn",
            "zh",
        )

        lang_paths = [(41, "default"),]
        langs_dir = os.sep.join((resources, "langs"))

        if not os.path.isdir(langs_dir):
            os.makedirs(langs_dir)

        for lang in os.listdir(langs_dir):
            if os.path.isfile(os.sep.join((langs_dir, lang))) and lang.split(".")[-1] == "qm":
                glang = re.split("\.|_|-", lang)

                while "" in glang:
                    glang.remove("")

                if glang:
                    glang = glang[0].lstrip().rstrip()

                else:
                    glang = ""

                if glang in all_langs:
                    lang_paths.append((all_langs.index(glang), lang[:-3]))

        self.usr_langs = tuple(lang_paths)
        self.info_main_site = "https://eigenmiao.com/rickrack"
        self.info_update_site = "https://github.com/eigenmiao/Rickrack/releases"
        self.info_dissc_site = "https://github.com/eigenmiao/Rickrack/discussions?discussions_q="
        self.info_font_site = "https://fonts.google.com/noto/fonts"
        self.info_author_zh = "本征喵函数"
        self.info_author_en = "Eigenmiao"
        self.home_dir = os.path.expanduser('~')
        self.doc_name = "Documents"
        self.pic_name = "Pictures"

        if os.path.isfile(os.sep.join([self.home_dir, ".config", "user-dirs.dirs"])):
            try:
                with open(os.sep.join([self.home_dir, ".config", "user-dirs.dirs"]), "r", encoding="utf-8") as f:
                    data = f.read().split()

            except Exception as err:
                data = []

            for line in data:
                if "DOCUMENTS" in line.upper():
                    if line.count('"') == 2:
                        doc_name = line.split('"')[-2].split("/")[-1]

                        if os.path.isdir(os.sep.join((self.home_dir, doc_name))):
                            self.doc_name = doc_name

                    elif line.count("'") == 2:
                        doc_name = line.split("'")[-2].split("/")[-1]

                        if os.path.isdir(os.sep.join((self.home_dir, doc_name))):
                            self.doc_name = doc_name

                elif "PICTURES" in line.upper():
                    if line.count('"') == 2:
                        pic_name = line.split('"')[-2].split("/")[-1]

                        if os.path.isdir(os.sep.join((self.home_dir, pic_name))):
                            self.pic_name = pic_name

                    elif line.count("'") == 2:
                        pic_name = line.split("'")[-2].split("/")[-1]

                        if os.path.isdir(os.sep.join((self.home_dir, pic_name))):
                            self.pic_name = pic_name

        self.usr_store = os.sep.join((self.home_dir, self.doc_name, "Rickrack"))
        self.resources = resources
        self.load_settings_failed = 0
        self.init_settings()
        self.stab_ucells = tuple()
        self.stab_column = 3
        self.sys_activated_idx = 0
        self.sys_activated_assit_idx = -1
        self.sys_color_set = ColorSet(self.h_range, self.s_range, self.v_range, overflow=self.overflow, dep_wtp=self.dep_wtp)
        self.sys_color_set.create(self.hm_rule)
        self.geometry_args = ""

        if os.path.isfile(os.sep.join((self.resources, "layouts.ini"))):
            with open(os.sep.join((self.resources, "layouts.ini")), "r", encoding="utf-8") as f:
                self.default_layout, self.layouts = json.load(f)

        else:
            self.default_layout = ""
            self.layouts = ("", "", "", "", "", "",)

        if not resetall:
            if self.store_loc:
                self.load_settings(os.sep.join((self.resources, "settings.json")))
                self.geometry_args = os.sep.join((self.resources, "geometry.ini"))

            else:
                self.load_settings(os.sep.join((self.usr_store, "settings.json")))
                self.geometry_args = os.sep.join((self.usr_store, "geometry.ini"))

        if uselang:
            self.modify_settings("lang", uselang)

        self.sys_category = 0
        self.sys_channel = 0
        self.sys_grid_locations = [(0.5, 0.5), (0.85, 0.85), (0.15, 0.85), (0.85, 0.15), (0.15, 0.15)]
        self.sys_grid_assitlocs = [[], [], [], [], []]
        self.sys_grid_list = [[], []]
        self.sys_grid_values = {"col": 9, "ctp": ("r", "g", "b"), "sum_factor": 1.0, "dim_factor": 1.0, "assist_factor": 0.4, "rev_grid": False}
        self.sys_choice_stat = []
        self.sys_link_colors = [False, False]
        self.sys_color_locs = [None, None, None, None, None]
        self.sys_assit_color_locs = [[], [], [], [], []]
        self.sys_image_url = ""

    def init_settings(self):
        """
        Init default settings.
        """

        default_locale = locale.getdefaultlocale()[0]
        default_locale = str(default_locale).lower() if default_locale else ""
        user_prefer_locale = "en"

        if len(default_locale) > 1:
            self.lang = default_locale[:2]

        else:
            self.lang = user_prefer_locale

        if self.lang not in [x[1] for x in self.usr_langs]:
            if user_prefer_locale in [x[1] for x in self.usr_langs]:
                self.lang = user_prefer_locale

            else:
                self.lang = "default"

        if self.lang == "zh":
            self.info_main_site = "https://eigenmiao.com/yanhuo"

        elif self.lang in ("eo", "ru", "ja", "fr", "de", "es"):
            self.info_main_site = "https://eigenmiao.com/yanhuo/{}.html".format(self.lang)

        else:
            self.info_main_site = "https://eigenmiao.com/rickrack"

        self.store_loc = True

        if os.path.isfile(os.sep.join((self.resources, "settings.json"))):
            try:
                with open(os.sep.join((self.resources, "settings.json")), "r", encoding="utf-8") as sf:
                    uss = json.load(sf)

            except Exception as err:
                uss = None

            if isinstance(uss, dict) and "store_loc" in uss:
                self.store_loc = bool(uss["store_loc"])

        if self.store_loc:
            self.usr_color = os.sep.join((self.resources, "MyColors"))
            self.usr_image = os.sep.join((self.resources, "samples"))

        else:
            self.usr_color = os.sep.join((self.home_dir, self.doc_name, "Rickrack", "MyColors"))
            self.usr_image = os.sep.join((self.home_dir, self.pic_name))

        if not os.path.isdir(self.usr_color):
            os.makedirs(self.usr_color)

        if not os.path.isdir(self.usr_image):
            os.makedirs(self.usr_image)

        self.hm_rule = "analogous"
        self.overflow = "return"
        self.press_move = True
        self.color_sys = 0
        self.show_rgb = False
        self.show_hsv = False
        self.show_info_pts = [3, 3, 3]
        self.h_range = (0.0, 360.0)
        self.s_range = (0.2, 0.5)
        self.v_range = (0.8, 1.0)
        self.wheel_ratio = 0.8
        self.volum_ratio = 0.8
        self.cubic_ratio = 0.9
        self.coset_ratio = 0.8
        self.board_ratio = 0.9
        self.s_tag_radius = 0.09
        self.v_tag_radius = 0.09
        self.rev_direct = True
        self.zoom_step = 1.1
        self.move_step = 5
        self.rand_num = 10000
        self.circle_dist = 12
        self.positive_wid = 1
        self.negative_wid = 1
        self.wheel_ed_wid = 1
        self.positive_color = (255, 255, 255)
        self.negative_color = ( 0,  0,  0)
        self.wheel_ed_color = ( 0,  0,  0)
        self.max_history_files = 10
        self.max_history_steps = 20
        self.export_grid_extns = "_Grid"
        self.export_swatch_ctp = "rgb"
        self.r_prefix = ("", "")
        self.rgb_prefix = ("(", ", ", ")")
        self.hec_prefix = ("'#", "'")
        self.lst_prefix = ("[", ", ", "]")
        self.win_on_top = False
        self.font_size = 12
        self.font_weight = 4
        self.font_family = ("Noto Sans",)
        self.bakgd_id = 0
        self.style_id = 0
        self.white_illuminant = 5
        self.white_observer = 0
        self.export_ase_type = "process"
        self.shortcut_keymaps = (
            ("F1", "Alt+H",          ), # 00 "Homepage".
            ("F2", "Alt+U",          ), # 01 "Update".
            ("F3", "Alt+B",          ), # 02 "About".
            ("`",  "Alt+T",          ), # 03 "Settings".
            ("Esc",                  ), # 04 "Close".
            ("Alt+Q",                ), # 05 "No_Save_Close".
            ("Ctrl+O", "Alt+O",      ), # 06 "Open".
            ("Ctrl+S", "Alt+S",      ), # 07 "Save".
            ("Ctrl+I", "Alt+I",      ), # 08 "Import".
            ("Ctrl+E", "Alt+E",      ), # 09 "Export".
            ("Ctrl+W", "Alt+C",      ), # 10 "Create".
            ("Ctrl+G", "Alt+L",      ), # 11 "Locate".
            ("Ctrl+B", "Alt+D",      ), # 12 "Derive".
            ("Ctrl+D", "Alt+A",      ), # 13 "Attach".
            ("R",                    ), # 14 "Clipboard_Cur_RGB".
            ("H",                    ), # 15 "Clipboard_Cur_HSV".
            ("X",                    ), # 16 "Clipboard_Cur_Hec".
            ("Shift+R",              ), # 17 "Clipboard_All_RGB".
            ("Shift+H",              ), # 18 "Clipboard_All_HSV".
            ("Shift+X",              ), # 19 "Clipboard_All_Hec".
            ("Ctrl+R",               ), # 20 "Clipboard_Set_RGB".
            ("Ctrl+H",               ), # 21 "Clipboard_Set_HSV".
            ("Ctrl+X",               ), # 22 "Clipboard_Set_Hec".
            ("1",     "6",           ), # 23 "Activate_Color_2".
            ("2",     "7",           ), # 24 "Activate_Color_1".
            ("3",     "8",           ), # 25 "Activate_Color_0".
            ("4",     "9",           ), # 26 "Activate_Color_3".
            ("5",     "0",           ), # 27 "Activate_Color_4".
            ("Up",                   ), # 28 "Move_Up".
            ("Down",                 ), # 29 "Move_Down".
            ("Left",                 ), # 30 "Move_Left".
            ("Right",                ), # 31 "Move_Right".
            ("=",     "+",     "*",  ), # 32 "Zoom_In".
            ("-",     "_",     "/",  ), # 33 "Zoom_Out".
            ("Home",                 ), # 34 "Reset_Home".
            ("End",                  ), # 35 "End".
            ("PgUp",                 ), # 36 "PageUp".
            ("PgDown",               ), # 37 "PageDown".
            ("Insert", "I",          ), # 38 "Insert".
            ("Del",                  ), # 39 "Delete".
            ("D",                    ), # 40 "Delete_Ver".
            ("F",                    ), # 41 "Show_Info".
            ("Tab", "S",             ), # 42 "Switch".
            ("Space", "Ctrl+Space",  ), # 43 "Show_Hide".
            ("Shift+Tab",            ), # 44 "Gen_Clear".
            ("Ctrl+C",               ), # 45 "Copy".
            ("Ctrl+V",               ), # 46 "Paste".
            ("Ctrl+Z", "U",          ), # 47 "Withdraw".
            ("Ctrl+T",               ), # 48 "On_Top".
            ("Ctrl+A",               ), # 49 "Show_Hide_All".
            ("F4", "Alt+Z",          ), # 50 "Support".
            ("Ctrl+Tab",             ), # 51 "Gen_Assit".
            ("F5",                   ), # 52 "Wheel_View".
            ("F6",                   ), # 53 "Image_View".
            ("F7",                   ), # 54 "Board_View".
            ("F8",                   ), # 55 "Depot_View".
            ("Shift+Z", "Z",         ), # 56 "Redo".
        )

        self.info_aucc_site = "https://eigenmiao.com/yanhuo/support.html"
        self.dep_circle_dist_2 = self.circle_dist ** 2
        self.dep_circle_dist_wid = self.circle_dist + (self.positive_wid + self.negative_wid) * 2
        self.dep_circle_dist_wid_2 = self.dep_circle_dist_wid ** 2
        self.dep_rtp = self.color_sys % 2
        self.dep_wtp = self.color_sys // 2
        self.dep_wtp_s, self.dep_wtp_n = (("s", 1), ("v", 2))[self.dep_rtp]
        self.dep_wtp_rev_s, self.dep_wtp_rev_n = (("v", 2), ("s", 1))[self.dep_rtp]

    def save_settings(self):
        """
        Save settings to file.
        """

        settings = {
            "version": self.info_version_en,
            "site": self.info_main_site,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }

        items = (
            "usr_color", "usr_image", "store_loc", "hm_rule", "overflow", "lang", "press_move", "color_sys",
            "show_rgb", "show_hsv", "show_info_pts", "h_range", "s_range", "v_range",
            "wheel_ratio", "volum_ratio", "cubic_ratio", "coset_ratio",
            "rev_direct", "s_tag_radius", "v_tag_radius", "zoom_step", "move_step", "rand_num", "circle_dist",
            "positive_wid", "negative_wid", "wheel_ed_wid",
            "positive_color", "negative_color", "wheel_ed_color",
            "stab_column", # "main_win_state", "main_win_geometry",
            "max_history_files", "max_history_steps", "export_grid_extns", "export_swatch_ctp", "r_prefix", "rgb_prefix", "hec_prefix", "lst_prefix",
            "win_on_top", "font_size", "font_weight", "font_family", "bakgd_id", "style_id", "white_illuminant", "white_observer", "export_ase_type",
            "shortcut_keymaps",
        )

        for item in items:
            value = getattr(self, item)
            settings[item] = value

        if self.store_loc:
            try:
                with open(os.sep.join((self.resources, "settings.json")), "w", encoding="utf-8") as sf:
                    json.dump(settings, sf, ensure_ascii=False)

            except Exception as err:
                if self.global_log:
                    print(err)

                self.store_loc = True
        else:
            try:
                with open(os.sep.join((self.usr_store, "settings.json")), "w", encoding="utf-8") as sf:
                    json.dump(settings, sf, ensure_ascii=False)

                with open(os.sep.join((self.resources, "settings.json")), "w", encoding="utf-8") as sf:
                    json.dump({"store_loc": False, "lang": self.lang}, sf, ensure_ascii=False)

            except Exception as err:
                if self.global_log:
                    print(err)

    def modify_settings(self, item, value):
        items = {
            "usr_color": lambda vl: self.pfmt_path(vl, self.usr_color),
            "usr_image": lambda vl: self.pfmt_path(vl, self.usr_image),
            "store_loc": lambda vl: self.pfmt_value(vl, bool, self.store_loc),
            "hm_rule": lambda vl: self.pfmt_str_in_list(vl, self.global_hm_rules, self.hm_rule),
            "overflow": lambda vl: self.pfmt_str_in_list(vl, self.global_overflows, self.overflow),
            "lang": lambda vl: self.pfmt_str_in_list(vl, [x[1] for x in self.usr_langs], self.lang),
            "press_move": lambda vl: self.pfmt_value(vl, bool, self.press_move),
            "color_sys": lambda vl: self.pfmt_num_in_scope(vl, (0, 3), int, self.color_sys),
            "show_rgb": lambda vl: self.pfmt_value(vl, bool, self.show_rgb),
            "show_hsv": lambda vl: self.pfmt_value(vl, bool, self.show_hsv),
            "show_info_pts": lambda vl: self.pfmt_info_list(vl, self.show_hsv),
            "h_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 360.0), float, self.h_range),
            "s_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 1.0), float, self.s_range),
            "v_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 1.0), float, self.v_range),
            "wheel_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.wheel_ratio),
            "volum_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.volum_ratio),
            "cubic_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.cubic_ratio),
            "coset_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.coset_ratio),
            "rev_direct": lambda vl: self.pfmt_value(vl, bool, self.rev_direct),
            "s_tag_radius": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 0.2), float, self.s_tag_radius),
            "v_tag_radius": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 0.2), float, self.v_tag_radius),
            "zoom_step": lambda vl: self.pfmt_num_in_scope(vl, (1.0, 10.0), float, self.zoom_step),
            "move_step": lambda vl: self.pfmt_num_in_scope(vl, (1, 100), int, self.move_step),
            "rand_num": lambda vl: self.pfmt_num_in_scope(vl, (0, 1000000000), int, self.rand_num),
            "circle_dist": lambda vl: self.pfmt_num_in_scope(vl, (0, 50), int, self.circle_dist),
            "positive_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.positive_wid),
            "negative_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.negative_wid),
            "wheel_ed_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.wheel_ed_wid),
            "positive_color": lambda vl: self.pfmt_rgb_color(vl, self.positive_color),
            "negative_color": lambda vl: self.pfmt_rgb_color(vl, self.negative_color),
            "wheel_ed_color": lambda vl: self.pfmt_rgb_color(vl, self.wheel_ed_color),
            "stab_column": lambda vl: self.pfmt_num_in_scope(vl, (1, 12), int, self.stab_column),
            "stab_ucells": lambda vl: self.pfmt_stab_ucells(vl),
            "main_win_state": lambda vl: self.pfmt_value(vl, str, ""),
            "main_win_geometry": lambda vl: self.pfmt_value(vl, str, ""),
            "max_history_files": lambda vl: self.pfmt_num_in_scope(vl, (0, 1000), int, self.max_history_files),
            "max_history_steps": lambda vl: self.pfmt_num_in_scope(vl, (0, 1000), int, self.max_history_steps),
            "export_grid_extns": lambda vl: check_file_name(vl),
            "export_swatch_ctp": lambda vl: self.pfmt_str_in_list(vl, ("rgb", "hsv", "cmyk", "lab", "gray"), self.export_swatch_ctp),
            "r_prefix": lambda vl: self.pfmt_prefix(vl, 2, self.r_prefix),
            "rgb_prefix": lambda vl: self.pfmt_prefix(vl, 3, self.rgb_prefix),
            "hec_prefix": lambda vl: self.pfmt_prefix(vl, 2, self.hec_prefix),
            "lst_prefix": lambda vl: self.pfmt_prefix(vl, 3, self.lst_prefix),
            "win_on_top": lambda vl: self.pfmt_value(vl, bool, self.win_on_top),
            "font_size": lambda vl: self.pfmt_num_in_scope(vl, (4, 64), int, self.font_size),
            "font_weight": lambda vl: self.pfmt_num_in_scope(vl, (1, 9), int, self.font_weight),
            "font_family": lambda vl: check_nonempt_str_lst(vl),
            "bakgd_id": lambda vl: self.pfmt_num_in_scope(vl, (0, 16), int, self.bakgd_id),
            "style_id": lambda vl: self.pfmt_num_in_scope(vl, (0, 16), int, self.style_id),
            "white_illuminant": lambda vl: self.pfmt_num_in_scope(vl, (0, 19), int, self.white_illuminant),
            "white_observer": lambda vl: self.pfmt_num_in_scope(vl, (0, 1), int, self.white_observer),
            "export_ase_type": lambda vl: self.pfmt_str_in_list(vl, ("spot", "global", "process"), self.export_ase_type),
            "shortcut_keymaps": lambda vl: self.pfmt_shortcut_keymaps(vl, self.shortcut_keymaps),
        }

        if item in items:
            setattr(self, item, items[item](value))

            if item in ("circle_dist", "positive_wid", "negative_wid"):
                self.dep_circle_dist_2 = self.circle_dist ** 2
                self.dep_circle_dist_wid = self.circle_dist + (self.positive_wid + self.negative_wid) * 2
                self.dep_circle_dist_wid_2 = self.dep_circle_dist_wid ** 2

            elif item == "color_sys":
                self.dep_rtp = self.color_sys % 2
                self.dep_wtp = self.color_sys // 2
                self.dep_wtp_s, self.dep_wtp_n = (("s", 1), ("v", 2))[self.dep_rtp]
                self.dep_wtp_rev_s, self.dep_wtp_rev_n = (("v", 2), ("s", 1))[self.dep_rtp]
                self.sys_color_set.set_color_system(self.dep_wtp)

            elif item == "lang":
                if self.lang == "zh":
                    self.info_main_site = "https://eigenmiao.com/yanhuo"
                    self.info_aucc_site = "https://eigenmiao.com/yanhuo/support.html"
                    self.info_dissc_site = "https://eigenmiao.com/yanhuo/discuss.html"

                elif self.lang in ("eo", "ru", "ja", "fr", "de", "es"):
                    self.info_main_site = "https://eigenmiao.com/yanhuo/{}.html".format(self.lang)
                    self.info_aucc_site = "https://eigenmiao.com/rickrack/support.html"
                    self.info_dissc_site = "https://eigenmiao.com/rickrack/discuss.html"

                else:
                    self.info_main_site = "https://eigenmiao.com/rickrack"
                    self.info_aucc_site = "https://eigenmiao.com/rickrack/support.html"
                    self.info_dissc_site = "https://eigenmiao.com/rickrack/discuss.html"

    def backup_settings(self, settings_file):
        """
        Move settings.json as settings_bak.json when load settings failed.

        Args:
          settings_file - string. settings file path.
        """

        if os.path.isfile(settings_file):
            if os.path.isfile(settings_file[:-5] + "_bak.json"):
                os.remove(settings_file[:-5] + "_bak.json")

            os.rename(settings_file, settings_file[:-5] + "_bak.json")

    def load_settings(self, settings_file):
        """
        Modify default settings by user settings.

        Args:
          settings_file - string. settings file path.
        """

        uss = {}

        if os.path.isfile(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as sf:
                    uss = json.load(sf)

            except Exception as err:
                self.load_settings_failed = 1
                self.backup_settings(settings_file)

        if isinstance(uss, dict) and uss:
            if "version" in uss:
                vid = self.check_version_x(uss["version"])

                if vid < 3:
                    uss["circle_dist"] = 16
                    uss["font_size"] = 16
                    uss["font_family"] = ["Noto Sans", "Noto Sans SC", "Noto Sans TC", "Noto Sans JP"]

                if vid == 0 or vid > 3:
                    self.load_settings_failed = 2
                    self.backup_settings(settings_file)
                    uss = {}

            else:
                self.load_settings_failed = 3
                self.backup_settings(settings_file)
                uss = {}

            if "style_id" in uss and "bakgd_id" not in uss:
                uss["bakgd_id"] = 0

            for item in uss:
                self.modify_settings(item, uss[item])

    def pfmt_path(self, value, default):
        """
        Parse directory path.
        """

        ans = str(value)

        if os.path.isdir(ans):
            return ans

        return default

    def pfmt_info_list(self, value, default):
        """
        [0-3, 0-3, 0-3]
        """

        if isinstance(value, (tuple, list)) and len(value) > 2:
            w, i, b = value[:3]

            if not (isinstance(w, int) and 0 <= w < 4):
                w = default[0]

            if not (isinstance(i, int) and 0 <= i < 4):
                i = default[1]

            if not (isinstance(b, int) and 0 <= b < 4):
                b = default[2]

            return [w, i, b]
        return default

    def pfmt_num_pair_in_scope(self, value, scope, dtype, default):
        """
        Parse number pair in scope.
        """

        try:
            ans = (dtype(value[0]), dtype(value[1]))

        except Exception as err:
            ans = None

        if ans != None and scope[0] <= ans[0] <= scope[1] and scope[0] <= ans[1] <= scope[1] and ans[0] <= ans[1]:
            return ans

        return default

    def pfmt_str_in_list(self, value, lst, default):
        """
        Parse string in list.
        """

        ans = str(value)

        if ans in lst:
            return ans

        return default

    def pfmt_num_in_scope(self, value, scope, dtype, default):
        """
        Parse number in scope.
        """

        try:
            ans = dtype(value)

        except Exception as err:
            ans = None

        if ans != None and scope[0] <= ans <= scope[1]:
            return ans

        return default

    def pfmt_value(self, value, dtype, default):
        """
        Parse value in designed dtype.
        """

        try:
            ans = dtype(value)

        except Exception as err:
            ans = None

        if ans != None:
            return ans

        return default

    def pfmt_file_name(self, value, default):
        """
        Parse string without special chars.
        """

        name_stri = re.split(r"[\v\a\f\n\r\t!@#$%^&\*]", str(value))

        while "" in name_stri:
            name_stri.remove("")

        if name_stri:
            name_stri = name_stri[0].lstrip().rstrip()

        else:
            name_stri = ""

        if name_stri:
            return name_stri

        return default

    def pfmt_rgb_color(self, value, default):
        """
        Parse value in designed color.
        """

        try:
            ans = (int(value[0]), int(value[1]), int(value[2]))

        except Exception as err:
            ans = None

        if ans != None and  0 <= ans[0] <= 255 and 0 <= ans[2] <= 255 and 0 <= ans[2] <= 255:
            return ans

        return default

    def pfmt_stab_ucells(self, value):
        """
        Parse value in designed color.
        """

        stab_ucells = []
        try:
            for cslst in value:
                colors = []

                for color in cslst[0]:
                    ans = (float(color[0]), float(color[1]), float(color[2]))

                    if 0.0 <= ans[0] <= 360.0 and 0.0 <= ans[2] <= 1.0 and 0.0 <= ans[2] <= 1.0:
                        colors.append(ans)

                    else:
                        break

                hm_rule = str(cslst[1])

                if hm_rule not in self.global_hm_rules:
                    hm_rule = ""

                if len(colors) == 5 and hm_rule:
                    cr_name = "" if len(cslst) < 3 else str(cslst[2])
                    cr_desc = "" if len(cslst) < 4 else str(cslst[3])
                    cr_time = (-1.0, -1.0) if len(cslst) < 5 else (float(cslst[4][0]), float(cslst[4][1]))
                    stab_ucells.append((tuple(colors), hm_rule, cr_name, cr_desc, cr_time))

        except Exception as err:
            if self.global_log:
                print(err)

        print(b"\xd1\xe6\xbb\xf0\xca\xae\xb6\xfe\xbe\xed\xa3\xac\xb1\xbe\xd5\xf7\xdf\xf7\xba\xaf\xca\xfd".decode("gbk"))
        print()
        return stab_ucells

    def pfmt_prefix(self, prefix, length, default):
        """
        Parse r g b prefix.
        """

        if isinstance(prefix, (tuple, list)) and len(prefix) == length:
            is_a_prefix = True

            for stri in prefix:
                if not isinstance(stri, str):
                    is_a_prefix = False
                    break

            if is_a_prefix:
                return tuple(prefix)

        return default

    def pfmt_shortcut_keymaps(self, value, default):
        """
        Parse shortcut keymaps.
        """

        if isinstance(value, (tuple, list)) and isinstance(default, (tuple, list)) and len(value) == len(default):
            shortcuts = []
            used_names = []

            for skey_idx in range(len(default)):
                if isinstance(value[skey_idx], (tuple, list)):
                    cked_names = [check_key(name) for name in value[skey_idx]]

                else:
                    cked_names = default[skey_idx]

                rved_names = []

                for name in cked_names:
                    if name and name not in used_names:
                        used_names.append(name)
                        rved_names.append(name)

                shortcuts.append(tuple(rved_names))
            return tuple(shortcuts)

        return default

    @classmethod
    def check_version_x(cls, version):
        """
        Check if settings file version is compatible.
        """

        ans = re.match(r"^v.+?-x(\d+)d.+?s.+-.*", str(version))

        if ans:
            return int(ans.group(1))

        elif re.match(r"^v2\.[12].*", str(version)):
            return 1

        else:
            return 0

    @classmethod
    def check_version_d(cls, version):
        """
        Check if color depot file version is compatible.
        """

        ans = re.match(r"^v.+?-x.+?d(\d+)s.+-.*", str(version))

        if ans:
            return int(ans.group(1))

        elif re.match(r"^v2\.[12].*", str(version)):
            return 1

        else:
            return 0

    @classmethod
    def check_version_s(cls, version):
        """
        Check if color set file version is compatible.
        """

        ans = re.match(r"^v.+?-x.+?d.+?s(\d+).*-.*", str(version))

        if ans:
            return int(ans.group(1))

        elif re.match(r"^v2\.[12].*", str(version)):
            return 1

        else:
            return 0

    def check_temp_dir(self):
        """
        Check if temporary directory valid.
        """

        return self.global_temp_dir and self.global_temp_dir.isValid() and os.path.isdir(self.global_temp_dir.path())

    def remove_temp_dir(self):
        """
        Remove temporary directory.
        """

        if not self.global_temp_dir:
            return

        temp_dir = self.global_temp_dir.path()
        self.global_temp_dir.remove()

        if os.path.isdir(temp_dir):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)

            except Exception as err:
                pass

class TestArgs(unittest.TestCase):
    """
    Test Args object.
    """

    def test_check_version_x(self):
        items = (
            ("v2.2.8-pre", 1),
            ("v2.3.0-x2d1s1-pre", 2),
            ("v2.3.0-x1d2s1-pre", 1),
            ("v2.3.0-x1d1s2-pre", 1),
            ("v2.3.0-x12d1s1-pre", 12),
            ("v2.3.0-x1d12s1-pre", 1),
            ("v2.3.0-x1d1s12-pre", 1),
            ("v2.3.0-x123d1s1-pre", 123),
            ("v2.3.0-x1d123s1-pre", 1),
            ("v2.3.0-x1d1s123-pre", 1),
            ("v2.3.0-x2d1s1k3-pre", 2),
            ("v2.3.0-x1d2s1k3-pre", 1),
            ("v2.3.0-x1d1s2k3-pre", 1),
            ("v2.3.0-x12d1s1k3p4-pre", 12),
            ("v2.3.0-x1d12s1k3p4-pre", 1),
            ("v2.3.0-x1d1s12k3p4-pre", 1),
            ("v2.3.0-x123d1s1r-pre", 123),
            ("v2.3.0-x1d123s1r-pre", 1),
            ("v2.3.0-x1d1s123r-pre", 1),
            ("v2.3.0-x2-pre", 0),
            ("v2.3.0-x1-pre", 0),
            ("v2.3.0-x1-pre", 0),
            ("v2.3.0-x12d1-pre", 0),
            ("v2.3.0-x1d12-pre", 0),
            ("v2.3.0-x1d1s-pre", 0),
            ("v2.3.0-x123r-pre", 0),
            ("v2.3.0-x1d1r-pre", 0),
            ("v2.3.0-x1d1r-pre", 0),
        )

        for itm, ans in items:
            self.assertEqual(Args.check_version_x(itm), ans, msg=itm)

    def test_check_version_d(self):
        items = (
            ("v2.2.8-pre", 1),
            ("v2.3.0-x2d1s1-pre", 1),
            ("v2.3.0-x1d2s1-pre", 2),
            ("v2.3.0-x1d1s2-pre", 1),
            ("v2.3.0-x12d1s1-pre", 1),
            ("v2.3.0-x1d12s1-pre", 12),
            ("v2.3.0-x1d1s12-pre", 1),
            ("v2.3.0-x123d1s1-pre", 1),
            ("v2.3.0-x1d123s1-pre", 123),
            ("v2.3.0-x1d1s123-pre", 1),
            ("v2.3.0-x2d1s1k3-pre", 1),
            ("v2.3.0-x1d2s1k3-pre", 2),
            ("v2.3.0-x1d1s2k3-pre", 1),
            ("v2.3.0-x12d1s1k3p4-pre", 1),
            ("v2.3.0-x1d12s1k3p4-pre", 12),
            ("v2.3.0-x1d1s12k3p4-pre", 1),
            ("v2.3.0-x123d1s1r-pre", 1),
            ("v2.3.0-x1d123s1r-pre", 123),
            ("v2.3.0-x1d1s123r-pre", 1),
            ("v2.3.0-d1-pre", 0),
            ("v2.3.0-d2-pre", 0),
            ("v2.3.0-d1-pre", 0),
            ("v2.3.0-x12d1-pre", 0),
            ("v2.3.0-x1d12-pre", 0),
            ("v2.3.0-x1d1s-pre", 0),
            ("v2.3.0-23d1r-pre", 0),
            ("v2.3.0-d123r-pre", 0),
            ("v2.3.0-d1s1r-pre", 0),
        )

        for itm, ans in items:
            self.assertEqual(Args.check_version_d(itm), ans, msg=itm)

    def test_check_version_s(self):
        items = (
            ("v2.2.8-pre", 1),
            ("v2.3.0-x2d1s1-pre", 1),
            ("v2.3.0-x1d2s1-pre", 1),
            ("v2.3.0-x1d1s2-pre", 2),
            ("v2.3.0-x12d1s1-pre", 1),
            ("v2.3.0-x1d12s1-pre", 1),
            ("v2.3.0-x1d1s12-pre", 12),
            ("v2.3.0-x123d1s1-pre", 1),
            ("v2.3.0-x1d123s1-pre", 1),
            ("v2.3.0-x1d1s123-pre", 123),
            ("v2.3.0-x2d1s1k3-pre", 1),
            ("v2.3.0-x1d2s1k3-pre", 1),
            ("v2.3.0-x1d1s2k3-pre", 2),
            ("v2.3.0-x12d1s1k3p4-pre", 1),
            ("v2.3.0-x1d12s1k3p4-pre", 1),
            ("v2.3.0-x1d1s12k3p4-pre", 12),
            ("v2.3.0-x123d1s1r-pre", 1),
            ("v2.3.0-x1d123s1r-pre", 1),
            ("v2.3.0-x1d1s123r-pre", 123),
            ("v2.3.0-s1-pre", 0),
            ("v2.3.0-s1-pre", 0),
            ("v2.3.0-s2-pre", 0),
            ("v2.3.0-d1s1-pre", 0),
            ("v2.3.0-12s1-pre", 0),
            ("v2.3.0-1s12-pre", 0),
            ("v2.3.0-d1s1r-pre", 0),
            ("v2.3.0-23s1r-pre", 0),
            ("v2.3.0-s123r-pre", 0),
        )

        for itm, ans in items:
            self.assertEqual(Args.check_version_s(itm), ans, msg=itm)

if __name__ == "__main__":
    unittest.main()
