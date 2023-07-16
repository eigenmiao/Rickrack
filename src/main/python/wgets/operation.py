# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details.

Please visit https://github.com/eigenmiao/DigitalPalette for more 
infomation about VioletPy.

Copyright (c) 2019-2021 by Eigenmiao. All Rights Reserved.
"""

import os
import time
import json
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from ricore.export import export_list, export_text, export_swatch, export_ase, export_gpl, export_xml, import_text, import_swatch, import_ase, import_gpl, import_xml
from ricore.grid import norm_grid_locations, norm_grid_list, norm_grid_values
from ricore.check import fmt_im_time
from ricore.color import Color


class Operation(QWidget):
    ps_update = pyqtSignal(bool)
    ps_opened = pyqtSignal(bool)
    ps_functn = pyqtSignal(int)

    def __init__(self, wget, args):
        super().__init__(wget)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._func_tr_()
        operation_grid_layout = QGridLayout(self)
        operation_grid_layout.setContentsMargins(0, 0, 0, 0)
        operation_grid_layout.setHorizontalSpacing(0)
        operation_grid_layout.setVerticalSpacing(0)
        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        operation_grid_layout.addWidget(scroll_area)
        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(3, 9, 3, 3)
        scroll_grid_layout.setHorizontalSpacing(3)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)
        self._file_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._file_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._file_gbox, 0, 1, 1, 1)
        self.import_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.import_btn, 0, 1, 1, 1)
        self.import_btn.clicked.connect(self.exec_import)
        self.export_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.export_btn, 1, 1, 1, 1)
        self.export_btn.clicked.connect(self.exec_export)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._view_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._view_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._view_gbox, 1, 1, 1, 1)
        self.functn = []
        self.functn.append(QPushButton(self._view_gbox))
        gbox_grid_layout.addWidget(self.functn[0], 0, 1, 1, 1)
        self.functn[0].clicked.connect(lambda x: self.ps_functn.emit(0))
        self.functn.append(QPushButton(self._view_gbox))
        gbox_grid_layout.addWidget(self.functn[1], 1, 1, 1, 1)
        self.functn[1].clicked.connect(lambda x: self.ps_functn.emit(1))
        self.functn.append(QPushButton(self._view_gbox))
        gbox_grid_layout.addWidget(self.functn[2], 2, 1, 1, 1)
        self.functn[2].clicked.connect(lambda x: self.ps_functn.emit(2))
        self.functn.append(QPushButton(self._view_gbox))
        gbox_grid_layout.addWidget(self.functn[3], 3, 1, 1, 1)
        self.functn[3].clicked.connect(lambda x: self.ps_functn.emit(3))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 4, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 2, 1, 1)
        self.update_text()

    def sizeHint(self):
        return QSize(250, 145)

    def exec_open(self, value):
        cb_filter = "{} (*.dpc; *.json);; {} (*.dpc);; {} (*.json)".format(self._file_descs[7], self._file_descs[4], self._file_descs[0])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[6], self._args.usr_color, filter=cb_filter)
        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))
        else:
            return
        self.dp_open(cb_file[0])

    def dp_open(self, depot_file, direct_dict=False, dp_path=""):
        color_dict = {}
        curr_path = str(dp_path)
        if direct_dict:
            color_dict = depot_file
        else:
            curr_path = os.path.dirname(depot_file)
            try:
                with open(depot_file, "r", encoding="utf-8") as f:
                    color_dict = json.load(f)
            except Exception as err:
                self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
            if not isinstance(color_dict, dict):
                self.warning(self._operation_errs[2])
                return
        if "version" in color_dict:
            vid = self._args.check_version_d(color_dict["version"])
            if vid == 0 or vid > 3:
                self.warning(self._operation_errs[3])
                return
        else:
            self.warning(self._operation_errs[4])
            return
        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "depot":
                color_palettes = color_dict["palettes"]
            elif color_dict["type"] == "set":
                self.warning(self._operation_errs[15])
                return
            else:
                self.warning(self._operation_errs[11])
                return
        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return
        finished_errs = []
        color_list = []
        if not isinstance(color_palettes, (tuple, list)):
            self.warning(self._operation_errs[13] + "\n{}\n{}".format(self._operation_errs[17], "\"{}\" is not a list.".format(str(color_palettes)[:100] + " ...")))
            return
        for color_idx in range(len(color_palettes)):
            color = color_palettes[color_idx]
            hsv_set = []
            broken_errs = []
            if not isinstance(color, dict):
                broken_errs.append("[id {}] {}".format(color_idx + 1, "\"{}\" is not a dict.".format(str(color)[25] + " ...")))
            if broken_errs:
                finished_errs += list(broken_errs)
                continue
            for i in range(5):
                if broken_errs:
                    break
                if "color_{}".format(i) in color:
                    hsv_tuple = (0.0, 0.0, 1.0)
                    if "hsv" in color["color_{}".format(i)]:
                        try:
                            hsv_tuple = Color.fmt_hsv(color["color_{}".format(i)]["hsv"]).tolist()
                        except Exception as err:
                            broken_errs.append("[id {}] {}".format(color_idx + 1, str(err)))
                    elif "rgb" in color["color_{}".format(i)]:
                        try:
                            hsv_tuple = Color.rgb2hsv(color["color_{}".format(i)]["rgb"]).tolist()
                        except Exception as err:
                            broken_errs.append("[id {}] {}".format(color_idx + 1, str(err)))
                    elif "hex_code" in color["color_{}".format(i)]:
                        try:
                            hsv_tuple = Color.hec2hsv(color["color_{}".format(i)]["hex_code"]).tolist()
                        except Exception as err:
                            broken_errs.append("[id {}] {}".format(color_idx + 1, str(err)))
                    elif "hex code" in color["color_{}".format(i)]:
                        try:
                            hsv_tuple = Color.hec2hsv(color["color_{}".format(i)]["hex code"]).tolist()
                        except Exception as err:
                            broken_errs.append("[id {}] {}".format(color_idx + 1, str(err)))
                    else:
                        broken_errs.append("[id {}] hsv value is not found.".format(color_idx + 1))
                    hsv_set.append(tuple(hsv_tuple))
                else:
                    broken_errs.append("[id {}] {}".format(color_idx + 1, "\"color_{}\" is not found in color dict.".format(i)))
            if broken_errs:
                finished_errs += list(broken_errs)
                continue
            if "name" in color:
                cr_name = str(color["name"])
            else:
                cr_name = ""
            if "desc" in color:
                cr_desc = str(color["desc"])
                cr_desc = cr_desc.replace("$curr_path$", curr_path)
                cr_desc = cr_desc.replace("$os_sep$", os.sep)
            else:
                cr_desc = ""
            if "time" in color:
                cr_time = fmt_im_time(color["time"])
            else:
                cr_time = (0, 0)
            if "grid_locations" in color and "grid_assitlocs" in color:
                grid_locations = color["grid_locations"]
                grid_assitlocs = color["grid_assitlocs"]
            else:
                grid_locations = []
                grid_assitlocs = []
            if "grid_list" in color:
                grid_list = color["grid_list"]
            else:
                grid_list = []
            if "grid_values" in color:
                grid_values = color["grid_values"]
            else:
                grid_values = {}
            grid_locations, grid_assitlocs = norm_grid_locations(grid_locations, grid_assitlocs)
            grid_list = norm_grid_list(grid_list)
            grid_values = norm_grid_values(grid_values)
            if len(hsv_set) == 5:
                if "rule" in color and color["rule"] in self._args.global_hm_rules:
                    color_list.append((tuple(hsv_set), color["rule"], cr_name, cr_desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values))
                else:
                    broken_errs.append("[id {}] color rule is not found.".format(color_idx + 1))
            else:
                broken_errs.append("[id {}] colors are not complete.".format(color_idx + 1))
            finished_errs += list(broken_errs)
        if finished_errs:
            self.warning(self._operation_errs[14] + "\n{}\n{}".format(self._operation_errs[17], "; ".join(finished_errs)))
        for unit_cell in self._args.stab_ucells:
            if hasattr(unit_cell, "close"):
                unit_cell.close()
        self._args.stab_ucells = tuple(color_list)
        self.ps_opened.emit(True)

    def exec_save(self, value):
        name = "{}".format(time.strftime("Rickrack_Depot_%Y_%m_%d.dpc", time.localtime()))
        cb_filter = "{} (*.dpc);; {} (*.txt);; {} (*.aco);; {} (*.ase);; {} (*.gpl);; {} (*.xml)".format(self._file_descs[4], self._file_descs[1], self._file_descs[2], self._file_descs[8], self._file_descs[5], self._file_descs[6])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[7], os.sep.join((self._args.usr_color, name)), filter=cb_filter)
        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))
        else:
            return
        self.dp_save(cb_file[0], value)

    def dp_save(self, depot_file, value):
        color_list = []
        for unit_cell in self._args.stab_ucells[:-1]:
            if unit_cell != None:
                color_list.append((unit_cell.color_set, unit_cell.hm_rule, unit_cell.name, unit_cell.desc, unit_cell.cr_time, unit_cell.grid_locations, unit_cell.grid_assitlocs, unit_cell.grid_list, unit_cell.grid_values))
        if depot_file.split(".")[-1].lower() in ("dpc", "json", "temp"):
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "depot"}
            color_dict["palettes"] = export_list(color_list)
            try:
                with open(depot_file, "w", encoding="utf-8") as f:
                    json.dump(color_dict, f, indent=4, ensure_ascii=False)
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif depot_file.split(".")[-1].lower() == "txt":
            try:
                with open(depot_file, "w", encoding="utf-8") as f:
                    f.write("# Rickrack Color Depot Export\n")
                    f.write("# Please refer to website {} for more information.\n".format(self._args.info_main_site))
                    f.write("# Version: {}\n".format(self._args.info_version_en))
                    f.write("# Total: {}\n\n".format(len(color_list)))
                    f.write(export_text(color_list))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif depot_file.split(".")[-1].lower() == "aco":
            try:
                with open(depot_file, "wb") as f:
                    f.write(export_swatch(color_list, ctp=self._args.export_swatch_ctp, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
                if self._args.export_grid_extns:
                    grid_file = depot_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "wb") as f:
                        f.write(export_swatch(color_list, ctp=self._args.export_swatch_ctp, export_grid=True, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif depot_file.split(".")[-1].lower() == "ase":
            try:
                with open(depot_file, "wb") as f:
                    f.write(export_ase(color_list, ctp=self._args.export_swatch_ctp, asetp=self._args.export_ase_type, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
                if self._args.export_grid_extns:
                    grid_file = depot_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "wb") as f:
                        f.write(export_ase(color_list, ctp=self._args.export_swatch_ctp, asetp=self._args.export_ase_type, export_grid=True, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif depot_file.split(".")[-1].lower() == "gpl":
            try:
                with open(depot_file, "w", encoding="utf-8") as f:
                    f.write(export_gpl(color_list))
                if self._args.export_grid_extns:
                    grid_file = depot_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                with open(grid_file, "w", encoding="utf-8") as f:
                    f.write(export_gpl(color_list, export_grid=True))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif depot_file.split(".")[-1].lower() == "xml":
            try:
                with open(depot_file, "w", encoding="utf-8") as f:
                    f.write(export_xml(color_list))
                if self._args.export_grid_extns:
                    grid_file = depot_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                with open(grid_file, "w", encoding="utf-8") as f:
                    f.write(export_xml(color_list, export_grid=True))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        else:
            self.warning(self._operation_errs[10])

    def exec_import(self, value):
        cb_filter = "{} (*.dps; *.json; *.txt; *.aco; *.ase; *.gpl; *.xml);; {} (*.dps);; {} (*.json);; {} (*.txt);; {} (*.aco);; {} (*.ase);; {} (*.gpl);; {} (*.xml)".format(self._file_descs[7], self._file_descs[3], self._file_descs[0], self._file_descs[1], self._file_descs[2], self._file_descs[8], self._file_descs[5], self._file_descs[6])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[0], self._args.usr_color, filter=cb_filter)
        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))
        else:
            return
        self.dp_import(cb_file[0])

    def dp_import(self, set_file, direct_dict=False, return_set=False):
        color_dict = {}
        if direct_dict:
            color_dict = set_file
        elif set_file.split(".")[-1].lower() in ("txt", "aco", "ase", "gpl", "xml"):
            grid_list = []
            name_list = []
            if set_file.split(".")[-1].lower() == "txt":
                try:
                    grid_list, name_list = import_text(set_file)
                except Exception as err:
                    self.warning(self._operation_errs[19] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
            if set_file.split(".")[-1].lower() == "aco":
                try:
                    grid_list, name_list = import_swatch(set_file, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer])
                except Exception as err:
                    self.warning(self._operation_errs[20] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
            if set_file.split(".")[-1].lower() == "ase":
                try:
                    grid_list, name_list = import_ase(set_file, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer])
                except Exception as err:
                    self.warning(self._operation_errs[20] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
            if set_file.split(".")[-1].lower() == "gpl":
                try:
                    grid_list, name_list = import_gpl(set_file)
                except Exception as err:
                    self.warning(self._operation_errs[21] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
            if set_file.split(".")[-1].lower() == "xml":
                try:
                    grid_list, name_list = import_xml(set_file)
                except Exception as err:
                    self.warning(self._operation_errs[22] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
            imp_color_2 = "FFFFFF" if len(grid_list) < 1 else grid_list[0]
            imp_color_1 = "FFFFFF" if len(grid_list) < 2 else grid_list[1]
            imp_color_0 = "FFFFFF" if len(grid_list) < 3 else grid_list[2]
            imp_color_3 = "FFFFFF" if len(grid_list) < 4 else grid_list[3]
            imp_color_4 = "FFFFFF" if len(grid_list) < 5 else grid_list[4]
            color_dict = {
                "version": self._args.info_version_en,
                "type": "set",
                "palettes": [
                    {
                        "rule": "custom",
                        "name": ".".join(os.path.basename(set_file).split(".")[:-1]),
                        "desc": self._import_descs[0].format(set_file),
                        "time": (time.time(), time.time()),
                        "color_2": {"hex_code": imp_color_2,},
                        "color_1": {"hex_code": imp_color_1,},
                        "color_0": {"hex_code": imp_color_0,},
                        "color_3": {"hex_code": imp_color_3,},
                        "color_4": {"hex_code": imp_color_4,},
                        "grid_list": [grid_list, name_list],
                        "grid_values": {"col": np.ceil(np.sqrt(len(grid_list))),},
                    }
                ]
            }
        else:
            with open(set_file, "r", encoding="utf-8") as f:
                try:
                    color_dict = json.load(f)
                except Exception as err:
                    self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return
                if not isinstance(color_dict, dict):
                    self.warning(self._operation_errs[2])
                    return
        if "version" in color_dict:
            vid = self._args.check_version_s(color_dict["version"])
            if vid == 0 or vid > 3:
                self.warning(self._operation_errs[3])
                return
        else:
            self.warning(self._operation_errs[4])
            return
        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "set":
                color_dict = color_dict["palettes"][0]
            elif color_dict["type"] == "depot":
                self.warning(self._operation_errs[16])
                return
            else:
                self.warning(self._operation_errs[11])
                return
        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return
        color_set = []
        for i in range(5):
            if "color_{}".format(i) in color_dict:
                curr_color = Color((0.0, 0.0, 1.0), tp="hsv")
                if "hsv" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hsv"]
                        curr_color = Color(hsv, tp="hsv", overflow=self._args.sys_color_set.get_overflow())
                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return
                elif "rgb" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["rgb"]
                        curr_color = Color(hsv, tp="rgb", overflow=self._args.sys_color_set.get_overflow())
                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return
                elif "hex_code" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hex_code"]
                        curr_color = Color(hsv, tp="hec", overflow=self._args.sys_color_set.get_overflow())
                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return
                elif "hex code" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hex code"]
                        curr_color = Color(hsv, tp="hec", overflow=self._args.sys_color_set.get_overflow())
                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return
                else:
                    self.warning(self._operation_errs[6] + "\n{}\n{}".format(self._operation_errs[17], "hsv"))
                    return
                color_set.append(curr_color)
            else:
                self.warning(self._operation_errs[7] + "\n{}\n{}".format(self._operation_errs[17], "color_{}".format(i)))
                return
        if "rule" in color_dict:
            if color_dict["rule"] in self._args.global_hm_rules:
                grid_locations = []
                grid_assitlocs = []
                grid_list = []
                grid_values = {}
                if "grid_locations" in color_dict and "grid_assitlocs" in color_dict:
                    grid_locations = color_dict["grid_locations"]
                    grid_assitlocs = color_dict["grid_assitlocs"]
                if "grid_list" in color_dict:
                    grid_list = color_dict["grid_list"]
                if "grid_values" in color_dict:
                    grid_values = color_dict["grid_values"]
                grid_locations, grid_assitlocs = norm_grid_locations(grid_locations, grid_assitlocs)
                grid_list = norm_grid_list(grid_list)
                grid_values = norm_grid_values(grid_values)
                if return_set:
                    set_name = ""
                    set_desc = ""
                    set_time = (0, 0)
                    if "name" in color_dict:
                        set_name = str(color_dict["name"])
                    if "desc" in color_dict:
                        set_desc = str(color_dict["desc"])
                    if "time" in color_dict:
                        set_time = fmt_im_time(color_dict["time"])
                    return (color_set, color_dict["rule"], set_name, set_desc, set_time, grid_locations, grid_assitlocs, grid_list, grid_values)
                else:
                    self._args.hm_rule = color_dict["rule"]
                    self._args.sys_color_set.recover(color_set)
                    self._args.sys_grid_locations = grid_locations
                    self._args.sys_grid_assitlocs = grid_assitlocs
                    self._args.sys_grid_list = grid_list
                    self._args.sys_grid_values = grid_values
                    self._args.sys_activated_assit_idx = -1
                    self._args.sys_assit_color_locs = [[None for j in self._args.sys_grid_assitlocs[i]] for i in range(5)]
            else:
                self.warning(self._operation_errs[8] + "\n{}\n{}".format(self._operation_errs[17], color_dict["rule"]))
                return
        else:
            self.warning(self._operation_errs[9] + "\n{}\n{}".format(self._operation_errs[17], "rule"))
            return
        self.ps_update.emit(True)

    def exec_export(self, value):
        name = "{}".format(time.strftime("Rickrack_Set_%Y_%m_%d.dps", time.localtime()))
        cb_filter = "{} (*.dps);; {} (*.txt);; {} (*.aco);; {} (*.ase);; {} (*.gpl);; {} (*.xml)".format(self._file_descs[3], self._file_descs[1], self._file_descs[2], self._file_descs[8], self._file_descs[5], self._file_descs[6])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[1], os.sep.join((self._args.usr_color, name)), filter=cb_filter)
        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))
        else:
            return
        self.dp_export(cb_file[0], value)

    def dp_export(self, set_file, value):
        color_set = None
        hm_rule = None
        desc = ""
        if isinstance(value, bool):
            color_set = self._args.sys_color_set
            hm_rule = self._args.hm_rule
            cr_name = ""
            cr_desc = ""
            cr_time = (time.time(), time.time())
            grid_locations = self._args.sys_grid_locations
            grid_assitlocs = self._args.sys_grid_assitlocs
            grid_list = self._args.sys_grid_list
            grid_values = self._args.sys_grid_values
        else:
            color_set = self._args.stab_ucells[value].color_set
            hm_rule = self._args.stab_ucells[value].hm_rule
            cr_name = self._args.stab_ucells[value].name
            cr_desc = self._args.stab_ucells[value].desc
            cr_time = self._args.stab_ucells[value].cr_time
            grid_locations = self._args.stab_ucells[value].grid_locations
            grid_assitlocs = self._args.stab_ucells[value].grid_assitlocs
            grid_list = self._args.stab_ucells[value].grid_list
            grid_values = self._args.stab_ucells[value].grid_values
        color_list = [(color_set, hm_rule, cr_name, cr_desc, cr_time, grid_locations, grid_assitlocs, grid_list, grid_values),]
        if set_file.split(".")[-1].lower() in ("dps", "json", "temp"):
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "set"}
            color_dict["palettes"] = export_list(color_list)
            if set_file.split(".")[-1].lower() == "temp":
                color_dict["palettes"][0]["time"] = [0, 0]
            try:
                with open(set_file, "w", encoding="utf-8") as f:
                    json.dump(color_dict, f, indent=4, ensure_ascii=False)
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif set_file.split(".")[-1].lower() == "txt":
            try:
                with open(set_file, "w", encoding="utf-8") as f:
                    f.write("# Rickrack Color Set Export\n")
                    f.write("# Please refer to website {} for more information.\n".format(self._args.info_main_site))
                    f.write("# Version: {}\n".format(self._args.info_version_en))
                    f.write("# Total: {}\n\n".format(len(color_list)))
                    f.write(export_text(color_list))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif set_file.split(".")[-1].lower() == "aco":
            try:
                with open(set_file, "wb") as f:
                    f.write(export_swatch(color_list, ctp=self._args.export_swatch_ctp, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
                if self._args.export_grid_extns:
                    grid_file = set_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "wb") as f:
                        f.write(export_swatch(color_list, ctp=self._args.export_swatch_ctp, export_grid=True, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif set_file.split(".")[-1].lower() == "ase":
            try:
                with open(set_file, "wb") as f:
                    f.write(export_ase(color_list, ctp=self._args.export_swatch_ctp, asetp=self._args.export_ase_type, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
                if self._args.export_grid_extns:
                    grid_file = set_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "wb") as f:
                        f.write(export_ase(color_list, ctp=self._args.export_swatch_ctp, asetp=self._args.export_ase_type, export_grid=True, white_ref=self._args.global_white_ref[self._args.white_illuminant][self._args.white_observer]))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif set_file.split(".")[-1].lower() == "gpl":
            try:
                with open(set_file, "w", encoding="utf-8") as f:
                    f.write(export_gpl(color_list))
                if self._args.export_grid_extns:
                    grid_file = set_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "w", encoding="utf-8") as f:
                        f.write(export_gpl(color_list, export_grid=True))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        elif set_file.split(".")[-1].lower() == "xml":
            try:
                with open(set_file, "w", encoding="utf-8") as f:
                    f.write(export_xml(color_list))
                if self._args.export_grid_extns:
                    grid_file = set_file.split(".")
                    grid_file[-2] = grid_file[-2] + self._args.export_grid_extns
                    grid_file = ".".join(grid_file)
                    with open(grid_file, "w", encoding="utf-8") as f:
                        f.write(export_xml(color_list, export_grid=True))
            except Exception as err:
                self.warning(self._operation_errs[23] + "\n{}\n{}".format(self._operation_errs[17], err))
                return
        else:
            self.warning(self._operation_errs[10])

    def show_import_export(self):
        self.import_btn.clicked.disconnect()
        self.export_btn.clicked.disconnect()
        self.import_btn.clicked.connect(self.exec_import)
        self.export_btn.clicked.connect(self.exec_export)
        self.import_btn.setText(self._operation_descs[0])
        self.export_btn.setText(self._operation_descs[1])

    def show_open_and_save(self):
        self.import_btn.clicked.disconnect()
        self.export_btn.clicked.disconnect()
        self.import_btn.clicked.connect(self.exec_open)
        self.export_btn.clicked.connect(self.exec_save)
        self.import_btn.setText(self._operation_descs[6])
        self.export_btn.setText(self._operation_descs[7])

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._operation_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._operation_errs[18], QMessageBox.AcceptRole)
        box.exec_()

    def update_text(self):
        self._file_gbox.setTitle(self._gbox_descs[0])
        self._view_gbox.setTitle(self._gbox_descs[1])
        self.import_btn.setText(self._operation_descs[0])
        self.export_btn.setText(self._operation_descs[1])

    def update_functn_text(self, view_idx=0):
        if view_idx == 0:
            # self.functn[0].show()
            # self.functn[1].show()
            # self.functn[2].show()
            # self.functn[3].hide()
            self.functn[0].setText(self._shortcut_descs[12])
            self.functn[1].setText(self._shortcut_descs[0])
            self.functn[2].setText(self._shortcut_descs[1])
            self.functn[3].setText(self._shortcut_descs[13])
        elif view_idx == 1:
            # self.functn[0].show()
            # self.functn[1].show()
            # self.functn[2].show()
            # self.functn[3].hide()
            self.functn[0].setText(self._shortcut_descs[2])
            self.functn[1].setText(self._shortcut_descs[3])
            self.functn[2].setText(self._shortcut_descs[4])
            self.functn[3].setText(self._shortcut_descs[13])
        elif view_idx == 2:
            # self.functn[0].show()
            # self.functn[1].show()
            # self.functn[2].show()
            # self.functn[3].show()
            self.functn[0].setText(self._shortcut_descs[5])
            self.functn[1].setText(self._shortcut_descs[6])
            self.functn[2].setText(self._shortcut_descs[7])
            self.functn[3].setText(self._shortcut_descs[8])
        elif view_idx == 3:
            # self.functn[0].show()
            # self.functn[1].show()
            # self.functn[2].show()
            # self.functn[3].hide()
            self.functn[1].setText(self._shortcut_descs[9])
            self.functn[2].setText(self._shortcut_descs[10])
            self.functn[3].setText(self._shortcut_descs[11])
            self.functn[0].setText(self._shortcut_descs[14])

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._gbox_descs = (
            _translate("MainWindow", "File"),
            _translate("MainWindow", "View"),
        )
        self._shortcut_descs = (
            _translate("MainWindow", "Create Colors"),
            _translate("Wheel", "Reset"),
            _translate("Image", "Open Image"),
            _translate("Image", "Save Image"),
            _translate("MainWindow", "Locate Colors"),
            _translate("Image", "Save Image"),
            _translate("Board", "Gradient - Fixed"),
            _translate("Board", "Gradient - Ref"),
            _translate("Board", "Reset"),
            _translate("Depot", "Attach Color Set"),
            _translate("Depot", "Export Color Set"),
            _translate("Depot", "Show Detail"),
            _translate("Wheel", "Add More Colors"),
            _translate("Wheel", "Generate Palette"),
            _translate("Depot", "Import Color Set"),
        )
        self._operation_descs = (
            _translate("MainWindow", "Import"),
            _translate("MainWindow", "Export"),
            _translate("MainWindow", "Create"),
            _translate("MainWindow", "Locate"),
            _translate("MainWindow", "Derive"),
            _translate("MainWindow", "Attach"),
            _translate("MainWindow", "Open"),
            _translate("MainWindow", "Save"),
        )
        self._sub_descs = (
            _translate("Rickrack", "{} ({})"),
            _translate("MainWindow", "Wheel"),
            _translate("MainWindow", "Image"),
            _translate("MainWindow", "Board"),
            _translate("MainWindow", "Depot"),
        )
        self._file_descs = (
            _translate("Operation", "Rickrack Json File"),
            _translate("Operation", "Plain Text File"),
            _translate("Operation", "Adobe Swatch File"),
            _translate("Operation", "Rickrack Set File"),
            _translate("Operation", "Rickrack Depot File"),
            _translate("Operation", "GIMP Palette File"),
            _translate("Operation", "Pencil Palette File"),
            _translate("Operation", "All Acceptable Files"),
            _translate("Operation", "Adobe Exchange File"),
        )
        self._import_descs = (
            _translate("Operation", "This color set is imported from file at {}."),
        )
        self._operation_errs = (
            _translate("Operation", "Error"),
            _translate("Operation", "Import color file error. Color file is broken."),
            _translate("Operation", "Import color format error. Data is not in dict type."),
            _translate("Operation", "Import color version error. Version does not match."),
            _translate("Operation", "Import color version error. Version does not exist."),
            _translate("Operation", "Import color set error. Color set is broken."),
            _translate("Operation", "Import color set error. HSV tags do not exist."),
            _translate("Operation", "Import color set error. Color tags do not exist."),
            _translate("Operation", "Import harmony rule error. Rule does not match."),
            _translate("Operation", "Import harmony rule error. Rule does not exist."),
            _translate("Operation", "Export Color file error. Extension does not match."),
            _translate("Operation", "Import color type error. Type does not match."),
            _translate("Operation", "Import color type error. Type does not exist."),
            _translate("Operation", "Import color depot error."),
            _translate("Operation", "Import some color sets into depot error. These color sets are discarded."),
            _translate("Operation", "Import color type error. This is a color set file, please use 'Import'."),
            _translate("Operation", "Import color type error. This is a color depot file, please use 'Open'."),
            _translate("Operation", "Detail:"),
            _translate("Operation", "OK"),
            _translate("Operation", "Import color list from plain text file error."),
            _translate("Operation", "Import color list from Adobe swatch file error."),
            _translate("Operation", "Import color list from GIMP palette file error."),
            _translate("Operation", "Import color list from Pencil palette file error."),
            _translate("Operation", "Export color file error."),
        )
        self.main_errs = (
            _translate("Operation", "Could not load settings. Settings file is broken. Old settings file has been backed up as 'settings_bak.json'."),
            _translate("Operation", "Could not load settings. Version does not match. Old settings file has been backed up as 'settings_bak.json'."),
            _translate("Operation", "Could not load settings. Version does not exist. Old settings file has been backed up as 'settings_bak.json'."),
        )
