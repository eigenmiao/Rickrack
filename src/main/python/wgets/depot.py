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

import re
import os
import json
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QFrame, QShortcut, QMenu, QAction, QDialog, QDialogButtonBox, QPushButton, QApplication, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QMimeData, QPoint, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QCursor, QKeySequence, QPixmap, QImage, QIcon, QDrag
from cguis.design.info_dialog import Ui_InfoDialog
from cguis.resource import view_rc
from ricore.color import FakeColor, Color
from ricore.export import export_list
from ricore.transpt import get_link_tag
from ricore.grid import norm_grid_locations, norm_grid_list, norm_grid_values
from ricore.check import check_image_desc, fmt_im_time


class Info(QDialog, Ui_InfoDialog):
    """
    Info object based on QDialog. Init color set information.
    """

    def __init__(self, wget, args):
        """
        Init information.
        """

        super().__init__(wget, Qt.WindowCloseButtonHint)
        self.setupUi(self)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        self._clone = None
        self._unit_cell = UnitCell(self.colors, self._args)

        color_grid_layout = QGridLayout(self.colors)
        color_grid_layout.setContentsMargins(1, 1, 1, 1)
        color_grid_layout.addWidget(self._unit_cell)

        # init buttons.
        self.buttonBox.clear()

        self._btn_1 = QPushButton()
        self._btn_1.clicked.connect(self.application)
        self.buttonBox.addButton(self._btn_1, QDialogButtonBox.AcceptRole)

        self._btn_2 = QPushButton()
        self._btn_2.clicked.connect(self.close)
        self.buttonBox.addButton(self._btn_2, QDialogButtonBox.RejectRole)

        self._btn_3 = QPushButton()
        self._btn_3.clicked.connect(self.update_values)
        self.buttonBox.addButton(self._btn_3, QDialogButtonBox.ApplyRole)

        self._btn_4 = QPushButton()
        self._btn_4.clicked.connect(self.reset_values)
        self.buttonBox.addButton(self._btn_4, QDialogButtonBox.ResetRole)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def clone_cell(self, unit_cell):
        if isinstance(unit_cell, UnitCell) and len(unit_cell.color_set) == 5 and None not in self._unit_cell.color_set:
            self._clone = unit_cell

            self._unit_cell.color_set = unit_cell.color_set

            if unit_cell.grid_list[0]:
                self._unit_cell.grid_list = [["FFFFFF",], ["",]]

            else:
                self._unit_cell.grid_list = [[], []]

            self._unit_cell.update()

            if unit_cell.name:
                self.name_ledit.setText(unit_cell.name)

            else:
                self.name_ledit.setText(self._cell_descs[0])

            if unit_cell.desc:
                self.desc_tedit.setText(unit_cell.desc)

            else:
                color_signs = []

                for i in (2, 1, 0, 3, 4):
                    sign = Color.sign(self._unit_cell.color_set[i].hsv)
                    color_signs.append(self._color_descs[sign[0]] + self._color_descs[sign[1] + 10])

                desc_context = self._cell_descs[2].format(*color_signs) + "\n"

                if unit_cell.grid_list[0]:
                    if len(unit_cell.grid_list[0]) > 5:
                        list_out_signs = [Color.sign(Color.hec2hsv(coitem)) for coitem in unit_cell.grid_list[0][:5]]
                        list_out_colors = [self._color_descs[snitem[0]] + self._color_descs[snitem[1] + 10] for snitem in list_out_signs]

                        for i in range(5):
                            if len(unit_cell.grid_list[1]) > i and unit_cell.grid_list[1][i]:
                                list_out_colors[i] = unit_cell.grid_list[1][i]

                        list_out_text = self._cell_descs[4].join(list_out_colors) + self._cell_descs[6]

                    elif len(unit_cell.grid_list[0]) > 1:
                        list_out_signs = [Color.sign(Color.hec2hsv(coitem)) for coitem in unit_cell.grid_list[0]]
                        list_out_colors = [self._color_descs[snitem[0]] + self._color_descs[snitem[1] + 10] for snitem in list_out_signs]

                        for i in range(len(unit_cell.grid_list[0])):
                            if len(unit_cell.grid_list[1]) > i and unit_cell.grid_list[1][i]:
                                list_out_colors[i] = unit_cell.grid_list[1][i]

                        list_out_text = self._cell_descs[4].join(list_out_colors[:-1]) + self._cell_descs[5] + list_out_colors[-1]

                    elif len(unit_cell.grid_list[0]) == 1:
                        one_sign = Color.sign(Color.hec2hsv(unit_cell.grid_list[0][0]))
                        list_out_text = self._color_descs[one_sign[0]] + self._color_descs[one_sign[1] + 10]

                    else:
                        list_out_text = ""

                    desc_context = desc_context + self._cell_descs[3].format(list_out_text) + "\n"

                else:
                    desc_context = desc_context + self._cell_descs[7]

                self.desc_tedit.setText(desc_context)

            self.hm_rule_label.setText(self._rule_descs[self._args.global_hm_rules.index(unit_cell.hm_rule)])

            if unit_cell.cr_time[0] < 0:
                time_str = self._cell_descs[1]

            else:
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unit_cell.cr_time[0]))

            if unit_cell.cr_time[1] < 0:
                time_str += "\n{}".format(self._cell_descs[1])

            else:
                time_str += "\n{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unit_cell.cr_time[1])))

            self.cr_time_label.setText(time_str)

        else:
            self._clone = None

            self._unit_cell.color_set = []
            self._unit_cell.update()

            self.name_ledit.setText(self._cell_descs[8])
            self.desc_tedit.setText(self._cell_descs[9])
            self.cr_time_label.setText(self._cell_descs[1] + "\n" + self._cell_descs[1])
            self.hm_rule_label.setText(self._rule_descs[self._args.global_hm_rules.index(self._args.hm_rule)])

    def application(self):
        """
        Modify the values.
        """

        if self._clone:
            name = re.split(r"[\v\a\f\n\r\t]", str(self.name_ledit.text()))
            desc = re.split(r"[\v\a\f]", str(self.desc_tedit.toPlainText()))

            while "" in name:
                name.remove("")

            if name:
                name = name[0].lstrip().rstrip()

            else:
                name = ""

            while "" in desc:
                desc.remove("")

            if desc:
                desc = desc[0].lstrip().rstrip()

            else:
                desc = ""

            if name != self._clone.name or desc != self._clone.desc:
                self._clone.name = name
                self._clone.desc = desc
                self._clone.cr_time = (self._clone.cr_time[0], time.time())

    def update_values(self):
        """
        For button apply.
        """

        self.application()
        self.clone_cell(self._clone)

    def reset_values(self):
        """
        For button reset.
        """

        self.clone_cell(self._clone)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.setWindowTitle(self._dialog_descs[0])
        self._btn_1.setText(self._dialog_descs[1])
        self._btn_2.setText(self._dialog_descs[2])
        self._btn_3.setText(self._dialog_descs[3])
        self._btn_4.setText(self._dialog_descs[4])

        self.retranslateUi(self)

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._dialog_descs = (
            _translate("Info", "Information"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
            _translate("Info", "Apply"),
            _translate("Info", "Reset"),
        )

        self._cell_descs = (
            _translate("Info", "Rickrack Color Set"),
            _translate("Info", "Unknown"),
            _translate("Info", "This color set includes: {}, {}, {}, {} and {}."),
            _translate("Info", "A fixed color board is attached, including: {}."),
            _translate("Info", ", "),
            _translate("Info", " and "),
            _translate("Info", " etc."),
            _translate("Info", "A gradient color board is attached."),
            _translate("Info", "Uninitialized Color Set"),
            _translate("Info", "Double Click The Blank Set to Initialize."),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )

        self._color_descs = (
            _translate("Rickrack", "Deep "),
            _translate("Rickrack", "Snow "),
            _translate("Rickrack", "Heavy "),
            _translate("Rickrack", "Dull "),
            _translate("Rickrack", "Grey "),
            _translate("Rickrack", "Pale "),
            _translate("Rickrack", "Light "),
            _translate("Rickrack", "Bright "),
            _translate("Rickrack", "Dark "),
            _translate("Rickrack", "Vivid "),
            _translate("Rickrack", "Black"),
            _translate("Rickrack", "White"),
            _translate("Rickrack", "Red"),
            _translate("Rickrack", "Yellow"),
            _translate("Rickrack", "Green"),
            _translate("Rickrack", "Cyan"),
            _translate("Rickrack", "Blue"),
            _translate("Rickrack", "Magenta"),
            _translate("Rickrack", "Orange"),
            _translate("Rickrack", "Pink"),
        )


class UnitCell(QWidget):
    """
    UnitCell objet based on QWidget. Init an unit cell in depot.
    """

    def __init__(self, wget, args, hsv_set=[], hm_rule="", name="", desc="", cr_time=(0, 0), grid_locations=[], grid_assitlocs=[], grid_list=[], grid_values={}):
        """
        Init empty unit cell.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self.activated = False

        name_stri = re.split(r"[\v\a\f\n\r\t]", str(name))
        desc_stri = re.split(r"[\v\a\f]", str(desc))

        while "" in name_stri:
            name_stri.remove("")

        if name_stri:
            name_stri = name_stri[0].lstrip().rstrip()

        else:
            name_stri = ""

        while "" in desc_stri:
            desc_stri.remove("")

        if desc_stri:
            desc_stri = desc_stri[0].lstrip().rstrip()

        else:
            desc_stri = ""

        self.name = name_stri
        self.desc = desc_stri

        self.cr_time = fmt_im_time(cr_time)

        self.update_colors(hsv_set, hm_rule, grid_locations, grid_assitlocs, grid_list, grid_values, update_time=False)

    def update_colors(self, hsv_set, hm_rule, grid_locations, grid_assitlocs, grid_list, grid_values, update_time=True):
        self.color_set = []

        for hsv in hsv_set:
            if hsv == None:
                self.color_set.append(None)

            else:
                self.color_set.append(FakeColor(Color.hsv2rgb(hsv), hsv, Color.hsv2hec(hsv)))

        self.color_set = tuple(self.color_set)
        self.hm_rule = str(hm_rule)

        if hsv_set:
            self.grid_locations, self.grid_assitlocs = norm_grid_locations(grid_locations, grid_assitlocs)
            self.grid_list = norm_grid_list(grid_list) # ["000000", "FF0000", "00FF00", "0000FF", "FFFF00", "00FFFF"]
            self.grid_values = norm_grid_values(grid_values)

        else:
            self.grid_locations = []
            self.grid_assitlocs = []
            self.grid_list = [[], []]
            self.grid_values = {}

        if update_time:
            self.cr_time = fmt_im_time((self.cr_time[0], time.time()))

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        cs_wid = int(min(self.width(), self.height()) * self._args.coset_ratio / 2)

        cs_boxes = (
            (self.width() / 2 - cs_wid, self.height() / 2 - cs_wid, cs_wid, cs_wid),
            (self.width() / 2, self.height() / 2 - cs_wid, cs_wid, cs_wid),
            (self.width() / 2 - cs_wid, self.height() / 2, cs_wid, cs_wid),
            (self.width() / 2, self.height() / 2, cs_wid, cs_wid),
            (self.width() / 2 - cs_wid / 2, self.height() / 2 - cs_wid / 2, cs_wid, cs_wid),
        )

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self.activated:
            curr_box = (self._args.negative_wid, self._args.negative_wid, self.width() - self._args.negative_wid * 2, self.height() - self._args.negative_wid * 2)

            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))
            painter.setBrush(QColor(*self._args.wheel_ed_color))
            painter.drawRoundedRect(*curr_box, self.width() / 9, self.height() / 9)

            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))

        else:
            painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

        for idx in range(5):
            if len(self.color_set) == 5:
                painter.setBrush(QColor(*self.color_set[4 - idx].rgb))

            else:
                painter.setBrush(QBrush(Qt.NoBrush))

            painter.drawRoundedRect(*cs_boxes[idx], cs_wid / 9, cs_wid / 9)

        if self.grid_list[0]:
            painter.drawEllipse(*cs_boxes[idx])

        if self.activated and self._args.sys_link_colors[1] and len(self.color_set) == 5:
            link_square_left, link_square_right, link_wid, link_line_start, link_line_end = get_link_tag(cs_boxes[4])

            painter.setBrush(QBrush(Qt.NoBrush))
            painter.drawRoundedRect(*link_square_left, link_wid, link_wid)
            painter.drawRoundedRect(*link_square_right, link_wid, link_wid)
            painter.drawLine(QPoint(*link_line_start), QPoint(*link_line_end))

        painter.end()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        if self.name:
            self.setToolTip(self.name)

        else:
            self.setToolTip(self._cell_descs[0])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._cell_descs = (
            _translate("Info", "Rickrack Color Set"),
        )


class Depot(QWidget):
    """
    Depot object based on QWidget. Init a color set depot in workarea.
    """

    ps_update = pyqtSignal(bool)
    ps_export = pyqtSignal(int)
    ps_status_changed = pyqtSignal(tuple)
    ps_dropped = pyqtSignal(tuple)
    ps_appended = pyqtSignal(tuple)
    ps_linked = pyqtSignal(bool)
    ps_history_backup = pyqtSignal(bool)
    ps_undo = pyqtSignal(bool)
    ps_open_image_url = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init color set depot.
        """

        super().__init__(wget)

        # set name ids.
        wget.setProperty("class", "WorkArea")

        # load args.
        self._args = args
        self._drop_file = None
        self._left_click = False
        self._drag_file = False
        self._double_click = False
        self._start_hig = None
        self._start_pt = None
        self._current_idx = None
        self._fetched_cell = None
        self._press_key = 0
        self._connected_keymaps = {}

        # load translations.
        self._func_tr_()

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea(self)
        self._scroll_area.setProperty("class", "WorkArea")
        self._scroll_area.setFrameShape(QFrame.Box)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)
        grid_layout.addWidget(self._scroll_area)

        self._scroll_bar = self._scroll_area.verticalScrollBar()

        self._scroll_contents = QWidget()
        self._scroll_contents.setProperty("class", "WorkArea")
        self._scroll_grid_layout = QGridLayout(self._scroll_contents)
        self._scroll_grid_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setWidget(self._scroll_contents)

        self.initialize()

        self._info = Info(self, self._args)

        self.create_menu()
        self.update_text()

        # shortcut is updated by _setup_skey in main.py.
        # self.update_skey()

        # stab_column is changed with the changing of interface size. this code is reused.
        self._stab_column_wid = None

        self._pl_wid = 0
        self._tot_rows = 0

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        self._pl_wid = int((self.width() - (self._scroll_bar.width() * 1.25)) / self._args.stab_column)
        self._tot_rows = len(self._args.stab_ucells) // self._args.stab_column if len(self._args.stab_ucells) % self._args.stab_column == 0 else len(self._args.stab_ucells) // self._args.stab_column + 1

        if not self._stab_column_wid:
            self._stab_column_wid = int(self._pl_wid)

        height = self._pl_wid * self._tot_rows
        height = height if height > self._scroll_area.height() else self._scroll_area.height()

        self._scroll_contents.setMinimumSize(self._pl_wid * self._args.stab_column, height)
        self._scroll_contents.setMaximumSize(self._pl_wid * self._args.stab_column, height)

        for i in range(self._tot_rows):
            for j in range(self._args.stab_column):
                idx = self._args.stab_column * i + j

                if idx < len(self._args.stab_ucells) and isinstance(self._args.stab_ucells[idx], UnitCell):
                    self._args.stab_ucells[idx].setGeometry(self._pl_wid * j, self._pl_wid * i, self._pl_wid, self._pl_wid)

        status_idx = self._current_idx

        if status_idx == None:
            status_idx = 0

        else:
            status_idx = status_idx + 1

        self.ps_status_changed.emit((self._tot_rows, self._args.stab_column, len(self._args.stab_ucells) - 1, status_idx))

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self._press_key = 1
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Control:
            self._press_key = 2
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Space:
            self._press_key = 3
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Alt:
            self._press_key = 4
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        else:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        self._press_key = 0
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.ignore()

    def mousePressEvent(self, event):
        point = np.array((event.x() - self._scroll_contents.x(), event.y() - self._scroll_contents.y()))

        col = point[0] // self._pl_wid
        row = point[1] // self._pl_wid

        if self._press_key == 2 and event.button() == Qt.LeftButton:
            color_list = []

            for unit_cell in self._args.stab_ucells[:-1]:
                if isinstance(unit_cell, UnitCell):
                    color_list.append((unit_cell.color_set, unit_cell.hm_rule, unit_cell.name, unit_cell.desc, unit_cell.cr_time, unit_cell.grid_locations, unit_cell.grid_assitlocs, unit_cell.grid_list, unit_cell.grid_values))

            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "depot"}
            color_dict["palettes"] = export_list(color_list)
            color_path = os.sep.join((self._args.global_temp_dir.path(), "Rickrack_Depot_{}.dpc".format(abs(hash(str(color_dict))))))

            with open(color_path, "w", encoding="utf-8") as f:
                json.dump(color_dict, f, indent=4, ensure_ascii=False)

            self._drag_file = True

            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setUrls([QUrl.fromLocalFile(color_path)])
            drag.setMimeData(mimedata)
            pixmap = QPixmap(":/images/images/file_depot_128.png")
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            self._drag_file = False

            # color link will be invalided by code below.
            # self._press_key = 0
            # self.setCursor(QCursor(Qt.ArrowCursor))

        elif col <= self._args.stab_column:
            idx = self._args.stab_column * row + col

            if event.button() == Qt.MidButton or (self._press_key == 3 and event.button() == Qt.LeftButton):
                if event.button() == Qt.MidButton:
                    self.setCursor(QCursor(Qt.ClosedHandCursor))

                self._start_hig = self._scroll_bar.value() + event.y()

            elif idx < len(self._args.stab_ucells):
                self.activate_idx(idx)

                if self._fetched_cell:
                    self._args.stab_ucells[self._current_idx] = self._fetched_cell
                    self._fetched_cell = None

                    self._left_click = False
                    self._start_pt = None

                elif event.button() == Qt.LeftButton and idx < len(self._args.stab_ucells) - 1:
                    self._left_click = True
                    self._start_pt = np.array((event.x(), event.y()))

                    self._fetched_cell = self._args.stab_ucells[self._current_idx]
                    self._args.stab_ucells[self._current_idx] = None

                    self._fetched_cell.raise_()

            else:
                self.activate_idx(None)

        else:
            self.activate_idx(None)

        event.accept()

    def mouseMoveEvent(self, event):
        if self._double_click:
            event.accept()

        elif self._press_key == 1 and self._left_click:
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "set"}
            color_dict["palettes"] = export_list([(self._fetched_cell.color_set, self._fetched_cell.hm_rule, self._fetched_cell.name, self._fetched_cell.desc, self._fetched_cell.cr_time, self._fetched_cell.grid_locations, self._fetched_cell.grid_assitlocs, self._fetched_cell.grid_list, self._fetched_cell.grid_values),])
            color_path = os.sep.join((self._args.global_temp_dir.path(), "Rickrack_Set_{}.dps".format(abs(hash(str(color_dict))))))

            with open(color_path, "w", encoding="utf-8") as f:
                json.dump(color_dict, f, indent=4, ensure_ascii=False)

            self._drag_file = True

            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setUrls([QUrl.fromLocalFile(color_path)])
            drag.setMimeData(mimedata)
            pixmap = QPixmap(":/images/images/file_set_128.png")
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            self._args.stab_ucells[self._current_idx] = self._fetched_cell
            self._fetched_cell = None

            self._left_click = False
            self._start_pt = None

            self._drag_file = False
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))

            self.update()
            event.accept()

        elif self._left_click:
            point = (event.x(), event.y())
            pl_wid_5 = self._pl_wid / 5

            if isinstance(self._start_pt, np.ndarray) and np.sum((self._start_pt - point) ** 2) < pl_wid_5 ** 2:
                # fixed icon in small region.
                event.ignore()

            else:
                x, y = point
                x = x if x > pl_wid_5 else pl_wid_5
                x = x if x < self.width() - pl_wid_5 else self.width() - pl_wid_5
                y = y if y > pl_wid_5 else pl_wid_5
                y = y if y < self.height() - pl_wid_5 else self.height() - pl_wid_5
                x = int(x) - self._scroll_contents.x()
                y = int(y) - self._scroll_contents.y()

                self._start_pt = None

                col = x // self._pl_wid
                row = y // self._pl_wid

                if col <= self._args.stab_column:
                    idx = self._args.stab_column * row + col

                    if idx < len(self._args.stab_ucells) - 1:
                        self._args.stab_ucells.pop(self._current_idx)
                        self._current_idx = idx

                        self._args.stab_ucells.insert(idx, None)

                self._fetched_cell.setGeometry(x - self._pl_wid / 2, y - self._pl_wid / 2, self._pl_wid, self._pl_wid)

                self.update()
                event.accept()

        elif self._start_hig != None:
            self._scroll_bar.setValue(self._start_hig - event.y())

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if self._start_hig:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self._start_hig = None

        if self._left_click:
            if isinstance(self._fetched_cell, UnitCell):
                self._args.stab_ucells[self._current_idx] = self._fetched_cell

            self._fetched_cell = None
            self._left_click = False
            self._start_pt = None

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._double_click = True
            point = (event.x() - self._scroll_contents.x(), event.y() - self._scroll_contents.y())

            col = point[0] // self._pl_wid
            row = point[1] // self._pl_wid

            if col <= self._args.stab_column:
                idx = self._args.stab_column * row + col

                if idx < len(self._args.stab_ucells):
                    self.activate_idx(idx)

                    if idx == len(self._args.stab_ucells) - 1:
                        self.attach_set()

                    else:
                        self.import_set()

                else:
                    self.activate_idx(None)

            else:
                self.activate_idx(None)

            self._double_click = False
            event.accept()

        else:
            event.ignore()

    def dragEnterEvent(self, event):
        # drag file out from depot.
        if self._drag_file:
            event.ignore()
            return

        try:
            depot_file = event.mimeData().urls()[0].toLocalFile()

        except Exception as err:
            event.ignore()
            return

        if depot_file.split(".")[-1].lower() in ("dpc", "dps", "json", "txt", "aco", "ase", "gpl", "xml"):
            self._drop_file = depot_file
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if self._drop_file:
            if self._drop_file.split(".")[-1].lower() in ("dpc", "json"):
                self.ps_dropped.emit((self._drop_file, False))

            else:
                self.ps_appended.emit((self._drop_file, False))

            self._drop_file = None

            event.accept()

        else:
            event.ignore()

    def resizeEvent(self, event):
        if self._stab_column_wid:
            wid = self.width()

            stab_column = int(wid / self._stab_column_wid)
            stab_column = 1 if stab_column < 1 else stab_column

            if stab_column != self._args.stab_column:
                self._args.modify_settings("stab_column", stab_column)

            self.update()

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def initialize(self):
        """
        Initialize Depot from self._args.stab_ucells list.
        """

        unit_cells = []

        for cset in self._args.stab_ucells:
            unit_cell = UnitCell(self._scroll_contents, self._args, *cset)
            unit_cells.append(unit_cell)

            self._scroll_grid_layout.addWidget(unit_cell)

        empty_cell = UnitCell(self._scroll_contents, self._args)
        unit_cells.append(empty_cell)

        self._scroll_grid_layout.addWidget(empty_cell)

        self._args.stab_ucells = unit_cells
        self._current_idx = None

        self.ps_history_backup.emit(True)

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell._func_tr_()
                unit_cell.update_text()

    def activate_idx(self, idx):
        """
        Activate unit cell at idx and set current idx to idx.
        """

        # current idx is None if all unit cells are not selected.
        # current idx is a serial number in range len(self._args.stab_ucells) if any unit cell is selected.
        # firstly deactivate old unit cell at current idx.
        if self._current_idx != None and isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].activated = False
            self._args.stab_ucells[self._current_idx].update()

        # then change current idx to given idx.
        self._current_idx = idx

        if self._current_idx != None:
            self._current_idx = self._current_idx if self._current_idx > 0 else 0
            self._current_idx = self._current_idx if self._current_idx < len(self._args.stab_ucells) -1 else len(self._args.stab_ucells) - 1

        # finally activate new unit cell at current idx.
        if self._current_idx != None and isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].activated = True
            self._args.stab_ucells[self._current_idx].update()

            upp_pos = self._scroll_contents.y() + self._args.stab_ucells[self._current_idx].y()
            low_pos = self._scroll_contents.y() + self._args.stab_ucells[self._current_idx].y() + self._args.stab_ucells[self._current_idx].height()

            if upp_pos <= 0:
                self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].y())

            elif low_pos >= self._scroll_area.height():
                # similar to the expression in func page_end.
                # please modify synchronously if necessary.
                self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].y() + self._pl_wid - self._scroll_area.height())

        status_idx = self._current_idx

        if status_idx == None:
            status_idx = 0

        else:
            status_idx = status_idx + 1

        self.ps_status_changed.emit((self._tot_rows, self._args.stab_column, len(self._args.stab_ucells) - 1, status_idx))

        # clone_cell into info window, thus can change the info dynamically. (recovered)
        # similar to set_context in update_select_idx in board.py.
        if self._current_idx == None:
            self._info.hide()

        else:
            self._info.clone_cell(self._args.stab_ucells[self._current_idx])

    def move(self, shift_x, shift_y):
        """
        Select unit cell around current idx unit cell (leftward, rightward, uppward and downward).
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None:
            self.activate_idx(0)

        elif shift_x < 0:
            self.activate_idx(self._current_idx - 1)

        elif shift_x > 0:
            self.activate_idx(self._current_idx + 1)

        elif shift_y < 0:
            self.activate_idx(self._current_idx - self._args.stab_column)

        elif shift_y > 0:
            self.activate_idx(self._current_idx + self._args.stab_column)

    def zoom(self, ratio):
        """
        Increase or decrease columns for display.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        stab_column = self._args.stab_column

        if True: # self._args.rev_direct:
            if ratio > 1:
                stab_column = stab_column - 1

            elif ratio < 1:
                stab_column = stab_column + 1

        else:
            if ratio > 1:
                stab_column = stab_column + 1

            elif ratio < 1:
                stab_column = stab_column - 1

        self._args.modify_settings("stab_column", stab_column)

        # stab_column is changed with the changing of interface size. this code is reused.
        self._stab_column_wid = None

        self.update()

    '''
    def home(self):
        """
        Locate current unit cell.
        """

        if not self.isVisible():
            return

        if self._current_idx == None:
            self._scroll_bar.setValue(0)
            self.update()

        else:
            self.activate_idx(self._current_idx)
        '''

    def home(self):
        """
        Home scroll page.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._scroll_bar.value() < self._pl_wid:
            self.activate_idx(0)

        else:
            self._scroll_bar.setValue(0)

        self.update()

    def page_up(self):
        """
        Up scroll page.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        self._scroll_bar.setValue(self._scroll_bar.value() - self._scroll_area.height())
        self.update()

    def page_down(self):
        """
        Down scroll page.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        self._scroll_bar.setValue(self._scroll_bar.value() + self._scroll_area.height())
        self.update()

    def page_end(self):
        """
        End scroll page.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        # similar to the expression in func activate_idx.
        # please modify synchronously if necessary.
        if self._scroll_bar.value() > self._args.stab_ucells[len(self._args.stab_ucells) - 1].y() - self._scroll_area.height():
            self.activate_idx(len(self._args.stab_ucells) - 1)

        else:
            self._scroll_bar.setValue(self._scroll_contents.height())

        self.update()

    def insert_set(self):
        """
        Insert current color set (combine attach_set and import_set funcs).
        """

        if self._current_idx == len(self._args.stab_ucells) - 1:
            self.attach_set()

        else:
            self.import_set()

    def delete_set(self):
        """
        Delete current color set from depot.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].close()
            self._args.stab_ucells.pop(self._current_idx)

            self._args.stab_ucells[self._current_idx].activated = True
            self.activate_idx(self._current_idx)
            self.update()

    def confirm_delete_set(self):
        """
        Act delete_set with confirmation.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        self.prompt(self._operation_warns[3], self.delete_set)

    def link_set(self, link):
        """
        Link set with result.

        Args:
            link (bool): whether linked.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        self._args.sys_link_colors[1] = bool(link)
        self.ps_linked.emit(True)

    def import_set(self, rev_import=False):
        """
        Import current color set into color wheel.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)

            if self._press_key in (2, 4) or rev_import:
                self._args.stab_ucells[self._current_idx].update_colors([i.hsv for i in self._args.sys_color_set], self._args.hm_rule, self._args.sys_grid_locations, self._args.sys_grid_assitlocs, self._args.sys_grid_list, self._args.sys_grid_values)

                if self._info.isVisible():
                    self._info.update_values()

            elif self._press_key == 1:
                self.attach_set(location_idx=self._current_idx)

            else:
                self._args.sys_color_set.recover(self._args.stab_ucells[self._current_idx].color_set)
                self._args.hm_rule = str(self._args.stab_ucells[self._current_idx].hm_rule)
                self._args.sys_grid_locations, self._args.sys_grid_assitlocs = norm_grid_locations(self._args.stab_ucells[self._current_idx].grid_locations, self._args.stab_ucells[self._current_idx].grid_assitlocs)
                self._args.sys_grid_list = norm_grid_list(self._args.stab_ucells[self._current_idx].grid_list)
                self._args.sys_grid_values = dict(self._args.stab_ucells[self._current_idx].grid_values)

                self._args.sys_activated_assit_idx = -1

                self._args.sys_assit_color_locs = [[None for j in self._args.sys_grid_assitlocs[i]] for i in range(5)]

                self.ps_update.emit(True)
                self.ps_history_backup.emit(True)

                image_url, full_loc = check_image_desc(self._args.stab_ucells[self._current_idx].desc)

                if image_url:
                    self.ps_open_image_url.emit((image_url, full_loc))

            # link and unlink.
            if self._press_key == 2:
                self.link_set(not self._args.sys_link_colors[1])

            elif self._args.sys_link_colors[1]:
                self.link_set(False)

    def export_set(self):
        """
        Export current color set from depot.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)
            self.ps_export.emit(self._current_idx)

    def detail_set(self):
        """
        Show info of color set (unit cell) at current idx.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)

            # self._info.clone_cell is completed by self.activate_idx above. (recovered)
            # self._info.clone_cell(self._args.stab_ucells[self._current_idx])
            self._info.show()

    def attach_set(self, color_list=None, location_idx=-1):
        """
        Attach current color set from wheel or color list from file into depot.
        """

        if not self.isVisible():
            return

        if isinstance(self._fetched_cell, UnitCell) or self._left_click:
            return

        # Arg color_list with None or False represent add color set from wheel instead of discard.
        if color_list:
            hsv_set = tuple(color_list[0][i].hsv for i in range(5))
            unit_cell = UnitCell(self._scroll_contents, self._args, hsv_set, color_list[1], color_list[2], color_list[3], color_list[4], color_list[5], color_list[6], color_list[7], color_list[8])

        else:
            hsv_set = tuple(self._args.sys_color_set[i].hsv for i in range(5))
            unit_cell = UnitCell(self._scroll_contents, self._args, hsv_set, self._args.hm_rule, "", "", (time.time(), time.time()), self._args.sys_grid_locations, self._args.sys_grid_assitlocs, self._args.sys_grid_list, self._args.sys_grid_values)

        self._scroll_grid_layout.addWidget(unit_cell)

        # normalize location_idx.
        loc_idx = -1
        if isinstance(location_idx, (int, np.int_)):
            loc_idx = int(location_idx)
            loc_idx = -1 if loc_idx < 0 else loc_idx
            loc_idx = -1 if loc_idx > len(self._args.stab_ucells) - 2 else loc_idx

        location_cell = self._args.stab_ucells[loc_idx]
        location_cell.activated = False

        unit_cell._func_tr_()
        unit_cell.update_text()
        unit_cell.activated = False

        # set geometry to prevent go to head when activate_idx() below.
        unit_cell.setGeometry(location_cell.geometry())

        total_len = len(self._args.stab_ucells)
        self._args.stab_ucells = self._args.stab_ucells[:loc_idx] + [unit_cell,] + self._args.stab_ucells[loc_idx:]

        self.update()

        #
        # add judge activate_list to prevent press_act error.
        # activate current index to update info.
        self.activate_idx((total_len + loc_idx) % total_len)

    def detail_state(self):
        """
        Esc refer to close self._info if it is visible in main window.
        """

        return self._info.isVisible()

    def hide_detail(self):
        """
        Hide the info window.
        Esc refer to close self._info if it is visible (return True) in main window.
        """

        if self._info.isVisible():
            self._info.hide()

            return True

        else:
            return False

    def clean_up(self):
        """
        Delete all unit cells except empty cell.
        """

        for unit_cell in self._args.stab_ucells[:-1]:
            if isinstance(unit_cell, UnitCell):
                unit_cell.close()

        self._args.stab_ucells = self._args.stab_ucells[-1:]
        self._args.stab_ucells[0].activated = False
        self._current_idx = None

        self.update()

    def update_index(self):
        """
        Link colors with cube table here.
        """

        # similar code segment in method self.import_set with self._press_key == 2.
        if self._args.sys_link_colors[1] and isinstance(self._args.stab_ucells[self._current_idx], UnitCell) and self._current_idx < len(self._args.stab_ucells) - 1:
            self._args.stab_ucells[self._current_idx].update_colors([i.hsv for i in self._args.sys_color_set], self._args.hm_rule, self._args.sys_grid_locations, self._args.sys_grid_assitlocs, self._args.sys_grid_list, self._args.sys_grid_values)

            if self._info.isVisible():
                self._info.update_values()

        self.update()

    def clipboard_in(self):
        """
        Load depot from clipboard.
        """

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                depot_file = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if depot_file.split(".")[-1].lower() in ("dpc", "json") and os.path.isfile(depot_file):
                    self.ps_dropped.emit((depot_file, False))

            elif depot_file.split(".")[-1].lower() in ("dps", "json", "txt", "aco", "ase", "gpl", "xml") and os.path.isfile(depot_file):
                    self.ps_appended.emit((depot_file, False))

        else:
            try:
                color_dict = json.loads(clipboard.text(), encoding="utf-8")

            except Exception as err:
                return

            if isinstance(color_dict, dict) and "type" in color_dict and "palettes" in color_dict:
                if color_dict["type"] == "depot":
                    self.ps_dropped.emit((color_dict, True))

                elif color_dict["type"] == "set":
                    self.ps_appended.emit((color_dict, True))

    def clipboard_cur(self, ctp):
        """
        Set the rgb, hsv or hec (hex code) of current color set as the clipboard data by shortcut Ctrl + r, h or x.
        """

        def _func_():
            data_lst = []

            if self._current_idx == None or self._args.stab_ucells[self._current_idx] == None or self._current_idx >= len(self._args.stab_ucells) - 1:
                for i in (2, 1, 0, 3, 4):
                    color = self._args.sys_color_set[i].getti(ctp)

                    if ctp == "hec":
                        color = self._args.hec_prefix[0] + str(color) + self._args.hec_prefix[1]

                    else:
                        color = self._args.rgb_prefix[1].join([self._args.r_prefix[0] + str(color[coi]) + self._args.r_prefix[1] for coi in range(3)])
                        color = self._args.rgb_prefix[0] + color + self._args.rgb_prefix[2]

                    data_lst.append(color)

            else:
                for i in (2, 1, 0, 3, 4):
                    color = getattr(self._args.stab_ucells[self._current_idx].color_set[i], ctp)

                    if ctp == "hec":
                        color = self._args.hec_prefix[0] + str(color) + self._args.hec_prefix[1]

                    else:
                        color = self._args.rgb_prefix[1].join([self._args.r_prefix[0] + str(color[coi]) + self._args.r_prefix[1] for coi in range(3)])
                        color = self._args.rgb_prefix[0] + color + self._args.rgb_prefix[2]

                    data_lst.append(color)

            data = self._args.lst_prefix[1].join(data_lst)
            data = self._args.lst_prefix[0] + data + self._args.lst_prefix[2]

            mimedata = QMimeData()
            mimedata.setText(data)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mimedata)

        return _func_

    def update_all(self):
        """
        Update all unit cells and self.
        """

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell.update()

        self.update()

    def prompt(self, text, accept_action):
        box = QMessageBox(self)
        box.setWindowTitle(self._operation_warns[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)

        box.addButton(self._operation_warns[1], QMessageBox.AcceptRole)
        box.addButton(self._operation_warns[2], QMessageBox.RejectRole)

        if box.exec_() == 0:
            accept_action()

    # ---------- ---------- ---------- Menu ---------- ---------- ---------- #

    def create_menu(self):
        """
        Create a right clicked menu.
        """

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self._menu = QMenu(self)

        #   _translate("Depot", "Undo"), # 0
        #   _translate("Depot", "Redo"), # 1
        self._action_undo = QAction(self)
        self._action_undo.triggered.connect(lambda: self.ps_undo.emit(True))
        self._menu.addAction(self._action_undo)

        self._action_redo = QAction(self)
        self._action_redo.triggered.connect(lambda: self.ps_undo.emit(False))
        self._menu.addAction(self._action_redo)

        #   _translate("Depot", "Paste"), # 5
        self._action_paste = QAction(self)
        self._action_paste.triggered.connect(self.clipboard_in)
        self._menu.addAction(self._action_paste)

        #   _translate("Depot", "Copy RGB"), # 2
        #   _translate("Depot", "Copy HSV"), # 3
        #   _translate("Depot", "Copy Hex Code"), # 4
        self._action_copy_rgb = QAction(self)
        self._action_copy_rgb.triggered.connect(self.clipboard_cur("rgb"))
        self._menu.addAction(self._action_copy_rgb)

        self._action_copy_hsv = QAction(self)
        self._action_copy_hsv.triggered.connect(self.clipboard_cur("hsv"))
        self._menu.addAction(self._action_copy_hsv)

        self._action_copy_hec = QAction(self)
        self._action_copy_hec.triggered.connect(self.clipboard_cur("hec"))
        self._menu.addAction(self._action_copy_hec)

        #   _translate("Depot", "Zoom In"), # 6
        #   _translate("Depot", "Zoom Out"), # 7
        self._action_zoom_in = QAction(self)
        self._action_zoom_in.triggered.connect(lambda: self.zoom(self._args.zoom_step))
        self._menu.addAction(self._action_zoom_in)

        self._action_zoom_out = QAction(self)
        self._action_zoom_out.triggered.connect(lambda: self.zoom(1 / self._args.zoom_step))
        self._menu.addAction(self._action_zoom_out)

        #   _translate("Depot", "Replace Color (DK)"), # 8
        #   _translate("Depot", "Rev-Replace Color (Alt+DK)"), # 16
        self._action_import = QAction(self)
        self._action_import.triggered.connect(self.import_set)
        self._menu.addAction(self._action_import)

        self._action_rev_import = QAction(self)
        self._action_rev_import.triggered.connect(lambda: self.import_set(rev_import=True))
        self._menu.addAction(self._action_rev_import)

        #   _translate("Depot", "Export Color Set"), # 9
        self._action_export = QAction(self)
        self._action_export.triggered.connect(self.export_set)
        self._menu.addAction(self._action_export)

        #   _translate("Depot", "Insert Color Set  (Shift+DK)"), # 10
        self._action_attach_beside = QAction(self)
        self._action_attach_beside.triggered.connect(lambda: self.attach_set(location_idx=self._current_idx))
        self._menu.addAction(self._action_attach_beside)

        #   _translate("Depot", "Append Color Set"), # 11
        self._action_attach_append = QAction(self)
        self._action_attach_append.triggered.connect(self.attach_set)
        self._menu.addAction(self._action_attach_append)

        #   _translate("Depot", "Delete Color Set"), # 12
        self._action_delete = QAction(self)
        self._action_delete.triggered.connect(self.delete_set)
        self._menu.addAction(self._action_delete)

        #   _translate("Depot", "Link with Result (Ctrl+DK)"), # 14
        #   _translate("Depot", "Un-Link with Result (Ctrl+DK)"), # 15
        self._action_link = QAction(self)
        self._action_link.triggered.connect(lambda: self.link_set(not self._args.sys_link_colors[1]))
        self._menu.addAction(self._action_link)

        #   _translate("Depot", "Show Detail"), # 13
        self._action_detail = QAction(self)
        self._action_detail.triggered.connect(self.detail_set)
        self._menu.addAction(self._action_detail)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        # normal actions delete.
        if self._current_idx == None or self._args.stab_ucells[self._current_idx] == None or self._current_idx >= len(self._args.stab_ucells) - 1:
            self._action_copy_rgb.setVisible(False)
            self._action_copy_hsv.setVisible(False)
            self._action_copy_hec.setVisible(False)
            self._action_import.setVisible(False)
            self._action_rev_import.setVisible(False)
            self._action_export.setVisible(False)
            self._action_delete.setVisible(False)
            self._action_detail.setVisible(False)
            self._action_attach_beside.setVisible(False)
            self._action_link.setVisible(False)

        else:
            self._action_copy_rgb.setVisible(True)
            self._action_copy_hsv.setVisible(True)
            self._action_copy_hec.setVisible(True)
            self._action_import.setVisible(True)
            self._action_rev_import.setVisible(True)
            self._action_export.setVisible(True)
            self._action_delete.setVisible(True)
            self._action_detail.setVisible(True)
            self._action_attach_beside.setVisible(True)
            self._action_link.setVisible(True)

        self._menu.exec_(QCursor.pos())

    # ---------- ---------- ---------- Shortcut ---------- ---------- ---------- #

    def update_skey(self):
        """
        Set depot shortcuts.
        """

        for skey in self._args.shortcut_keymaps[39]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.delete_set)

        for skey in self._args.shortcut_keymaps[40]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.confirm_delete_set)

        for skey in self._args.shortcut_keymaps[38]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.insert_set)

        for skey in self._args.shortcut_keymaps[41]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.detail_set)

        for skey in self._args.shortcut_keymaps[20]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_cur("rgb"))

        for skey in self._args.shortcut_keymaps[21]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_cur("hsv"))

        for skey in self._args.shortcut_keymaps[22]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_cur("hec"))

        for skey in self._args.shortcut_keymaps[45]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_cur("hec"))

        for skey in self._args.shortcut_keymaps[46]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_in)

        for skey in self._args.shortcut_keymaps[36]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.page_up)

        for skey in self._args.shortcut_keymaps[37]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.page_down)

        for skey in self._args.shortcut_keymaps[35]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.page_end)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_action_text(self):
        #   _translate("Depot", "Undo"), # 0
        #   _translate("Depot", "Redo"), # 1
        self._action_undo.setText(self._action_descs[0])
        self._action_redo.setText(self._action_descs[1])

        #   _translate("Depot", "Copy RGB"), # 2
        #   _translate("Depot", "Copy HSV"), # 3
        #   _translate("Depot", "Copy Hex Code"), # 4
        self._action_copy_rgb.setText(self._action_descs[2])
        self._action_copy_hsv.setText(self._action_descs[3])
        self._action_copy_hec.setText(self._action_descs[4])

        #   _translate("Depot", "Paste"), # 5
        self._action_paste.setText(self._action_descs[5])

        #   _translate("Depot", "Zoom In"), # 6
        #   _translate("Depot", "Zoom Out"), # 7
        self._action_zoom_in.setText(self._action_descs[6])
        self._action_zoom_out.setText(self._action_descs[7])

        #   _translate("Depot", "Replace Color (DK)"), # 8
        #   _translate("Depot", "Rev-Replace Color (Alt+DK)"), # 16
        self._action_import.setText(self._action_descs[8])
        self._action_rev_import.setText(self._action_descs[16])

        #   _translate("Depot", "Export Color Set"), # 9
        self._action_export.setText(self._action_descs[9])

        #   _translate("Depot", "Insert Color Set  (Shift+DK)"), # 10
        self._action_attach_beside.setText(self._action_descs[10])

        #   _translate("Depot", "Append Color Set"), # 11
        self._action_attach_append.setText(self._action_descs[11])

        #   _translate("Depot", "Delete Color Set"), # 12
        self._action_delete.setText(self._action_descs[12])

        #   _translate("Depot", "Show Detail"), # 13
        self._action_detail.setText(self._action_descs[13])

        #   _translate("Depot", "Link with Result (Ctrl+DK)"), # 14
        #   _translate("Depot", "Un-Link with Result (Ctrl+DK)"), # 15
        if self._args.sys_link_colors[1]:
            self._action_link.setText(self._action_descs[15])

        else:
            self._action_link.setText(self._action_descs[14])

    def update_text(self):
        self.update_action_text()

        self._info._func_tr_()
        self._info.update_text()

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell._func_tr_()
                unit_cell.update_text()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Wheel", "Undo"), # 0
            _translate("Wheel", "Redo"), # 1
            _translate("Depot", "Copy RGB"), # 2
            _translate("Depot", "Copy HSV"), # 3
            _translate("Depot", "Copy Hex Code"), # 4
            _translate("Wheel", "Paste"), # 5
            _translate("Board", "Zoom In"), # 6
            _translate("Board", "Zoom Out"), # 7
            _translate("Depot", "Replace Color (DK)"), # 8
            _translate("Depot", "Export Color Set"), # 9
            _translate("Depot", "Insert Color Set  (Shift+DK)"), # 10
            _translate("Depot", "Append Color Set"), # 11
            _translate("Depot", "Delete Color Set"), # 12
            _translate("Depot", "Show Detail"), # 13
            _translate("Depot", "Link with Result (Ctrl+DK)"), # 14
            _translate("Depot", "Un-Link with Result (Ctrl+DK)"), # 15
            _translate("Depot", "Rev-Replace Color (Alt+DK)"), # 16
        )

        self._operation_warns = (
            _translate("Info", "Warning"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
            _translate("Info", "The selected color set will be removed from depot."),
        )
