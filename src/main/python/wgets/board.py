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
import re
import json
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QShortcut, QMenu, QAction, QLabel, QDialog, QGridLayout, QPushButton, QDialogButtonBox, QColorDialog, QApplication, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QPoint, QMimeData, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QCursor, QKeySequence, QIcon, QDrag
from cguis.design.box_dialog import Ui_BoxDialog
from ricore.color import Color
from ricore.transpt import get_outer_box, get_link_tag, rotate_point
from ricore.grid import gen_color_grid, norm_grid_locations, norm_grid_values, snap_point, gen_assit_color
from ricore.export import export_list


class ColorBox(QDialog, Ui_BoxDialog):
    """
    ColorBox object based on QDialog. Init color box information.
    """

    ps_value_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init information.
        """

        super().__init__(wget, Qt.WindowCloseButtonHint)
        self.setupUi(self)

        # load args.
        self._args = args

        self._init_idx = -1
        self._default_name = "Rickrack Color Box"

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        # self.setWindowModality(Qt.ApplicationModal)

        color_grid_layout = QGridLayout(self.color_box)
        color_grid_layout.setContentsMargins(1, 1, 1, 1)

        self.box_sqr = BoxSqr(self, self._args, "FFFFFF")
        color_grid_layout.addWidget(self.box_sqr)
        self.box_sqr.ps_color_changed.connect(lambda x: self.hec_ledit.setText("#" + str(x)))

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

        self.hec_ledit.textChanged.connect(self.box_sqr.change_color)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def set_default_name(self, name):
        """
        Set the default name of color box.
        Args:
            name (str): name of color box. default: "Rickrack Color Box".
        """

        self._default_name = str(name)

    def set_context(self, idx):
        """
        Get the index, color and name of color box. Using update_context to update values.
        """

        self._init_idx = idx

        if 0 <= self._init_idx < len(self._args.sys_grid_list[0]):
            self.index_spb.setMinimum(1)
            self.index_spb.setMaximum(len(self._args.sys_grid_list[0]))

            self.hec_ledit.setText("#" + self._args.sys_grid_list[0][self._init_idx])
            self.box_sqr.change_color(self._args.sys_grid_list[0][self._init_idx])

            name = self._args.sys_grid_list[1][self._init_idx]

            if not name:
                name = self._default_name

            self.name_ledit.setText(str(name))

            self.index_spb.setValue(self._init_idx + 1)

        else:
            self._init_idx = len(self._args.sys_grid_list[0])

            self.index_spb.setMinimum(len(self._args.sys_grid_list[0]) + 1)
            self.index_spb.setMaximum(len(self._args.sys_grid_list[0]) + 1)

            self.hec_ledit.setText("#FFFFFF")
            self.box_sqr.change_color("FFFFFF")
            self.name_ledit.setText(self._uninit_descs[0])

            self.index_spb.setValue(len(self._args.sys_grid_list[0]) + 1)

    def application(self):
        """
        Modify the values.
        """

        name = re.split(r"[\v\a\f\n\r\t]", str(self.name_ledit.text()))

        while "" in name:
            name.remove("")

        if name:
            name = name[0].lstrip().rstrip()

        else:
            name = ""

        idx = self.index_spb.value() - 1
        hec_color = self.box_sqr.color.hec

        if idx == len(self._args.sys_grid_list[0]) and self._init_idx == len(self._args.sys_grid_list[0]):
            self._args.sys_grid_list[0].append(hec_color)
            self._args.sys_grid_list[1].append(name)

        elif 0 <= idx < len(self._args.sys_grid_list[0]) and 0 <= self._init_idx < len(self._args.sys_grid_list[0]):
            if idx == self._init_idx:
                self._args.sys_grid_list[0][idx] = hec_color
                self._args.sys_grid_list[1][idx] = name

            else:
                self._args.sys_grid_list[0].pop(self._init_idx)
                self._args.sys_grid_list[1].pop(self._init_idx)

                self._args.sys_grid_list[0].insert(idx, hec_color)
                self._args.sys_grid_list[1].insert(idx, name)

        self.ps_value_changed.emit(True)

    def update_values(self):
        """
        For button apply.
        """

        self.application()
        self.set_context(self._init_idx)

    def reset_values(self):
        """
        For button reset.
        """

        self.set_context(self._init_idx)

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

        self._uninit_descs = (
            _translate("Info", "Uninitialized Color Box"),
        )


class BoxSqr(QWidget):
    """
    Square objet based on QWidget. Init a color square in box.
    """

    ps_color_changed = pyqtSignal(str)

    def __init__(self, wget, args, hec_color):
        """
        Init color square.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self.color = Color(hec_color, tp="hec")

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        rto = (1.0 - self._args.cubic_ratio) / 2

        self._box = [self.width() * rto, self.height() * rto, self.width() * self._args.cubic_ratio, self.height() * self._args.cubic_ratio]

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid * 1.5))

        painter.setBrush(QColor(*self.color.rgb))
        painter.drawRect(*self._box)

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                dialog = QColorDialog.getColor(QColor(*self.color.rgb))

                if dialog.isValid():
                    self.color = Color((dialog.red(), dialog.green(), dialog.blue()), tp="rgb")

                    self.ps_color_changed.emit(self.color.hec)

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def change_color(self, hec_color):
        hec_value = None

        try:
            hec_value = Color.fmt_hec(str(hec_color)[-6:])

        except Exception as err:
            pass

        if hec_value:
            self.color = Color(hec_value, tp="hec")
            self.update()

        else:
            list_color = re.split(r"[\v\a\f\n\r\t\[\]\(\),;:#]", str(hec_color.replace("【", "[").replace("】", "]").replace("（", "(").replace("）", ")").replace("。", ".").replace("，", ",").replace("、", ",").replace("；", ";").replace("：", ":")))

            while "" in list_color:
                list_color.remove("")

            if len(list_color) >= 3:
                list_color = list_color[-3:]

                if "." in list_color[0] or "." in list_color[1] or "." in list_color[2]:
                    hsv_color = None

                    try:
                        hsv_color = Color.fmt_hsv([float(x) for x in list_color])

                    except Exception as err:
                        pass

                    if isinstance(hsv_color, np.ndarray):
                        self.color = Color(hsv_color, tp="hsv")
                        self.update()

                else:
                    rgb_color = None

                    try:
                        rgb_color = Color.fmt_rgb([int(x) for x in list_color])

                    except Exception as err:
                        pass

                    if isinstance(rgb_color, np.ndarray):
                        self.color = Color(rgb_color, tp="rgb")
                        self.update()


class Board(QWidget):
    """
    Board object based on QWidget. Init a gradual board pannel in workarea.
    """

    ps_index_changed = pyqtSignal(bool)
    ps_value_changed = pyqtSignal(bool)
    ps_color_changed = pyqtSignal(bool)
    ps_status_changed = pyqtSignal(tuple)
    ps_dropped = pyqtSignal(tuple)
    ps_linked = pyqtSignal(bool)
    ps_assit_pt_changed = pyqtSignal(bool)
    ps_history_backup = pyqtSignal(bool)
    ps_undo = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init color set depot.
        """

        super().__init__(wget)

        # set name ids.
        wget.setProperty("class", "WorkArea")

        # load args.
        self._args = args
        self._show_points = True
        self._moving_maintp = False
        self._moving_assitp = False
        self._last_moving = 0 # 0 for moving_maintp just now, 1 for moving_assitp just now.
        self._color_grid = []
        self._selecting_idx = -1
        self._last_selecting_idx = -1
        self._connected_keymaps = {}

        self._drag_file = False
        self._drop_file = None
        self._press_key = 0

        # load translations.
        self._func_tr_()

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self._tool_tip_label = QLabel(self)
        self._last_tool_tip_label = QLabel(self)
        self._color_box = ColorBox(self, self._args)
        self._color_box.ps_value_changed.connect(self.update)
        self._color_box.ps_value_changed.connect(lambda: self.ps_history_backup.emit(True))

        self.create_menu()
        self.update_text()

        # shortcut is updated by _setup_skey in main.py.
        # self.update_skey()

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        # norm assit point index.
        if self._args.sys_activated_assit_idx > len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]):
            self._args.sys_activated_assit_idx = -1
            self.ps_color_changed()

        if self._args.sys_grid_list[0] and self._show_points:
            self._show_points = False

        self._cs_wid = int(min(self.width(), self.height()) * self._args.board_ratio)
        self._cs_box = ((self.width() - self._cs_wid) / 2, (self.height() - self._cs_wid) / 2, self._cs_wid, self._cs_wid)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        painter.setBrush(Qt.white)
        painter.drawRect(*self._cs_box)

        idx_seq = list(range(5))
        idx_seq = idx_seq[self._args.sys_activated_idx + 1: ] + idx_seq[: self._args.sys_activated_idx + 1]

        # draw color grid.
        self._color_grid = gen_color_grid(self._args.sys_color_set, self._args.sys_grid_locations, self._args.sys_grid_assitlocs, grid_list=self._args.sys_grid_list, **self._args.sys_grid_values)

        grid_img = QImage(self._color_grid, self._color_grid.shape[1], self._color_grid.shape[0], self._color_grid.shape[1] * 3, QImage.Format_RGB888)
        grid_img = grid_img.scaled(self._cs_box[2], self._cs_box[3], Qt.KeepAspectRatio)

        painter.drawPixmap(*self._cs_box, QPixmap.fromImage(grid_img))

        # draw main points and assistant points.
        if self._args.sys_grid_list[0]:
            if 0 <= self._last_selecting_idx < self._args.sys_grid_values["col"] ** 2:
                sel_wid = 1.0 / self._args.sys_grid_values["col"] * self._cs_wid
                sel_box = ((self._last_selecting_idx % self._args.sys_grid_values["col"]) * sel_wid + self._cs_box[0], (self._last_selecting_idx // self._args.sys_grid_values["col"]) * sel_wid + self._cs_box[1], sel_wid, sel_wid)

                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                painter.setBrush(QBrush(Qt.NoBrush))
                painter.drawRect(*sel_box)

                self._last_tool_tip_label.setGeometry(*sel_box)
                self._last_tool_tip_label.setToolTip(self.get_box_name(self._last_selecting_idx))
                self._last_tool_tip_label.show()

            else:
                self._last_tool_tip_label.hide()

            if 0 <= self._selecting_idx < self._args.sys_grid_values["col"] ** 2:
                sel_wid = 1.0 / self._args.sys_grid_values["col"] * self._cs_wid
                sel_box = ((self._selecting_idx % self._args.sys_grid_values["col"]) * sel_wid + self._cs_box[0], (self._selecting_idx // self._args.sys_grid_values["col"]) * sel_wid + self._cs_box[1], sel_wid, sel_wid)

                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
                painter.setBrush(QBrush(Qt.NoBrush))
                painter.drawRect(*sel_box)

                if self._args.sys_link_colors[0]:
                    link_square_left, link_square_right, link_wid, link_line_start, link_line_end = get_link_tag(sel_box)

                    painter.setBrush(QBrush(Qt.NoBrush))
                    painter.drawRoundedRect(*link_square_left, link_wid, link_wid)
                    painter.drawRoundedRect(*link_square_right, link_wid, link_wid)
                    painter.drawLine(QPoint(*link_line_start), QPoint(*link_line_end))

                self._tool_tip_label.setGeometry(*sel_box)
                self._tool_tip_label.setToolTip(self.get_box_name(self._selecting_idx))
                self._tool_tip_label.show()

            else:
                self._tool_tip_label.hide()

        else:
            for idx in idx_seq:
                pt_xy = np.array((self._args.sys_grid_locations[idx][0] * self._cs_wid + self._cs_box[0], self._args.sys_grid_locations[idx][1] * self._cs_wid + self._cs_box[1]))
                pt_rgb = self._args.sys_color_set[idx].rgb

                # assit sequence. this code is reused in four places.
                assit_idx_seq = list(range(len(self._args.sys_grid_assitlocs[idx])))
                if idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                    assit_idx_seq = assit_idx_seq[self._args.sys_activated_assit_idx + 1: ] + assit_idx_seq[: self._args.sys_activated_assit_idx + 1]

                # assistant points.
                for assit_idx in assit_idx_seq:
                    assit_pt = pt_xy + np.array(self._args.sys_grid_assitlocs[idx][assit_idx][0:2]) * self._cs_wid
                    assit_box = get_outer_box(assit_pt, self._args.circle_dist)
                    assit_frame_color = (255, 255, 255)

                    if self._show_points:
                        if idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx:
                            assit_frame_color = self._args.positive_color

                        else:
                            assit_frame_color = self._args.negative_color

                    painter.setPen(QPen(QColor(*assit_frame_color), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                    painter.drawLine(QPoint(*pt_xy), QPoint(*assit_pt))

                    painter.setPen(QPen(QColor(*assit_frame_color), self._args.negative_wid))

                    assit_color = gen_assit_color(self._args.sys_color_set[idx], *self._args.sys_grid_assitlocs[idx][assit_idx][2:6])
                    assit_color = assit_color.rgb

                    if self._show_points:
                        painter.setBrush(QColor(*assit_color))

                    else:
                        painter.setBrush(QBrush(Qt.NoBrush))

                    painter.drawEllipse(*assit_box)

                    # relative (move-able) or ref (un-move-able) point tag. assit dot box.
                    if not self._args.sys_grid_assitlocs[idx][assit_idx][5]:
                        dot_box = get_outer_box(assit_pt, self._args.negative_wid * 2 / 3)
                        painter.setPen(QPen(Qt.NoPen))
                        painter.setBrush(QBrush(QColor(*assit_frame_color)))
                        painter.drawEllipse(*dot_box)

                # main points.
                pt_box = get_outer_box(pt_xy, self._args.circle_dist + (self._args.positive_wid + self._args.negative_wid) * 2)

                if self._show_points:
                    if idx == self._args.sys_activated_idx:
                        painter.setPen(QPen(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2]), self._args.positive_wid))
                        painter.setBrush(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 128))

                    else:
                        painter.setPen(QPen(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 128), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                        painter.setBrush(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 64))

                else:
                    painter.setPen(QPen(Qt.white, self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                    painter.setBrush(QBrush(Qt.NoBrush))

                painter.drawEllipse(*pt_box)

                pt_box = get_outer_box(pt_xy, self._args.circle_dist)

                if self._show_points:
                    if idx == self._args.sys_activated_idx:
                        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                    else:
                        painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

                    painter.setBrush(QColor(*pt_rgb))

                else:
                    painter.setPen(QPen(Qt.black, self._args.negative_wid))
                    painter.setBrush(QBrush(Qt.NoBrush))

                painter.drawEllipse(*pt_box)

        painter.end()

        if self._args.sys_grid_list[0]:
            self.ps_status_changed.emit((0, self._args.sys_grid_values["col"], self._args.sys_grid_values["col"], len(self._args.sys_grid_list[0]), self._selecting_idx))

        elif self._show_points:
            self.ps_status_changed.emit((1, len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx])))

        else:
            self.ps_status_changed.emit((2,))

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

        elif event.key() == Qt.Key_Alt:
            self._press_key = 4

            if self._args.sys_grid_list[0]:
                self.setCursor(QCursor(Qt.PointingHandCursor))

            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

            event.accept()

        else:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        self._press_key = 0
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = (event.x(), event.y())

            if self._args.sys_grid_list[0]:
                if point[0] < self._cs_box[0] or point[0] > self._cs_box[0] + self._cs_box[2] or point[1] < self._cs_box[1] or point[1] > self._cs_box[1] + self._cs_box[3]:
                    event.ignore()

                else:
                    sel_wid = 1.0 / self._args.sys_grid_values["col"] * self._cs_wid
                    press_idx = int((point[1] - self._cs_box[1]) / sel_wid) * self._args.sys_grid_values["col"] + int((point[0] - self._cs_box[0]) / sel_wid)

                    if press_idx != self._selecting_idx:
                        self._last_selecting_idx = self._selecting_idx
                        self._selecting_idx = press_idx

                        self.update_select_idx()

                    self.insert_point()

                    event.accept()

                    # self.update()
                    # is completed by self.insert_point()

            elif self._show_points and self._args.sys_activated_assit_idx >= 0:
                pt_xy = np.array((self._args.sys_grid_locations[self._args.sys_activated_idx][0] * self._cs_wid + self._cs_box[0], self._args.sys_grid_locations[self._args.sys_activated_idx][1] * self._cs_wid + self._cs_box[1]))
                assit_pt = pt_xy + np.array(self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][0:2]) * self._cs_wid

                if np.linalg.norm(point - assit_pt) < self._args.circle_dist:
                    self.ps_assit_pt_changed.emit(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])
                    self.ps_color_changed.emit(True)
                    event.accept()

                else:
                    event.ignore()

                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        point = np.array((event.x(), event.y()))

        if self._press_key == 1 and event.button() == Qt.LeftButton:
            #
            # Sync to wheel.py.
            # May exist difference.
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "set"}
            color_dict["palettes"] = export_list([(self._args.sys_color_set, self._args.hm_rule, "", "", (time.time(), time.time()), self._args.sys_grid_locations, self._args.sys_grid_assitlocs, self._args.sys_grid_list, self._args.sys_grid_values),])
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

            self._drag_file = False
            self.setCursor(QCursor(Qt.ArrowCursor))

            event.accept()

        elif self._press_key == 2 and event.button() == Qt.LeftButton:
            if (not self._args.sys_grid_list[0]) and self._show_points:
                loc = [(point[0] - self._cs_box[0]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][0], (point[1] - self._cs_box[1]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][1]]
                loc = snap_point(loc, 0.5 / self._args.sys_grid_values["col"])
                loc[0] = -1.0 if loc[0] < -1.0 else loc[0]
                loc[0] =  1.0 if loc[0] >  1.0 else loc[0]
                loc[1] = -1.0 if loc[1] < -1.0 else loc[1]
                loc[1] =  1.0 if loc[1] >  1.0 else loc[1]

                self._args.sys_activated_assit_idx = len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx])
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx].append([loc[0], loc[1], 15, 0.0, 0.0, True])
                self._args.sys_assit_color_locs[self._args.sys_activated_idx].append(None)

                self._moving_assitp = True

                self.ps_value_changed.emit(True)

                # not use self.insert_point()

                event.accept()
                self.update()

        elif self._args.sys_grid_list[0] and self._cs_box[0] < point[0] < self._cs_box[0] + self._cs_box[2] and self._cs_box[1] < point[1] < self._cs_box[1] + self._cs_box[3]:
            sel_wid = 1.0 / self._args.sys_grid_values["col"] * self._cs_wid
            press_idx = int((point[1] - self._cs_box[1]) / sel_wid) * self._args.sys_grid_values["col"] + int((point[0] - self._cs_box[0]) / sel_wid)

            if press_idx != self._selecting_idx:
                self._last_selecting_idx = self._selecting_idx
                self._selecting_idx = press_idx

                self.update_select_idx()

            event.accept()
            self.update()

        elif self._show_points:
            already_accept_main = False
            already_accept_assi = False

            for idx in range(5):
                if np.linalg.norm(point - np.array((self._cs_box[0], self._cs_box[1])) - np.array(self._args.sys_grid_locations[idx]) * self._cs_wid) < self._args.circle_dist + (self._args.positive_wid + self._args.negative_wid) * 2:
                    self._args.sys_activated_idx = idx
                    self._args.sys_activated_assit_idx = -1

                    self.ps_index_changed.emit(True)
                    already_accept_main = True

                else:
                    for assit_idx in range(len(self._args.sys_grid_assitlocs[idx]))[::-1]:
                        if np.linalg.norm(point - np.array((self._cs_box[0], self._cs_box[1])) - (np.array(self._args.sys_grid_locations[idx]) + np.array(self._args.sys_grid_assitlocs[idx][assit_idx][0:2])) * self._cs_wid) < self._args.circle_dist:
                            self._args.sys_activated_idx = idx
                            self._args.sys_activated_assit_idx = assit_idx

                            self.ps_index_changed.emit(True)
                            already_accept_assi = True

                            break

                if already_accept_main or already_accept_assi:
                    break

            if event.button() == Qt.LeftButton:
                # main points.
                if (self._args.press_move and not self._last_moving and not already_accept_assi and self._cs_box[0] < point[0] < self._cs_box[0] + self._cs_box[2] and self._cs_box[1] < point[1] < self._cs_box[1] + self._cs_box[3]) or already_accept_main:
                    loc = [(point[0] - self._cs_box[0]) / self._cs_wid, (point[1] - self._cs_box[1]) / self._cs_wid]
                    loc = snap_point(loc, 0.5 / self._args.sys_grid_values["col"])
                    loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
                    loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
                    loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
                    loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

                    self._args.sys_grid_locations[self._args.sys_activated_idx] = tuple(loc)

                    self._moving_maintp = True
                    self._last_moving = 0

                    event.accept()
                    self.update()

                # assit points.
                elif self._args.sys_grid_assitlocs[self._args.sys_activated_idx] and (self._args.press_move and self._last_moving and not already_accept_main and self._cs_box[0] < point[0] < self._cs_box[0] + self._cs_box[2] and self._cs_box[1] < point[1] < self._cs_box[1] + self._cs_box[3]) or already_accept_assi:
                    loc = [(point[0] - self._cs_box[0]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][0], (point[1] - self._cs_box[1]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][1]]
                    loc = snap_point(loc, 0.5 / self._args.sys_grid_values["col"])
                    loc[0] = -1.0 if loc[0] < -1.0 else loc[0]
                    loc[0] =  1.0 if loc[0] >  1.0 else loc[0]
                    loc[1] = -1.0 if loc[1] < -1.0 else loc[1]
                    loc[1] =  1.0 if loc[1] >  1.0 else loc[1]

                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][0] = loc[0]
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][1] = loc[1]

                    self._moving_assitp = True
                    self._last_moving = 1

                    event.accept()
                    self.update()

                else:
                    event.ignore()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if not self._show_points:
            return

        if self._moving_assitp:
            point = np.array((event.x(), event.y()))

            loc = [(point[0] - self._cs_box[0]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][0], (point[1] - self._cs_box[1]) / self._cs_wid - self._args.sys_grid_locations[self._args.sys_activated_idx][1]]
            loc = snap_point(loc, 0.5 / self._args.sys_grid_values["col"])
            loc[0] = -1.0 if loc[0] < -1.0 else loc[0]
            loc[0] =  1.0 if loc[0] >  1.0 else loc[0]
            loc[1] = -1.0 if loc[1] < -1.0 else loc[1]
            loc[1] =  1.0 if loc[1] >  1.0 else loc[1]

            self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][0] = loc[0]
            self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][1] = loc[1]

            event.accept()
            self.update()

        if self._moving_maintp:
            point = np.array((event.x(), event.y()))

            loc = [(point[0] - self._cs_box[0]) / self._cs_wid, (point[1] - self._cs_box[1]) / self._cs_wid]
            loc = snap_point(loc, 0.5 / self._args.sys_grid_values["col"])
            loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
            loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
            loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
            loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

            self._args.sys_grid_locations[self._args.sys_activated_idx] = tuple(loc)

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._moving_maintp = False
        self._moving_assitp = False

        if event.button() == Qt.LeftButton:
            self.ps_history_backup.emit(True)

        event.ignore()

    def dragEnterEvent(self, event):
        """
        Sync to wheel.py. May exist difference.
        """

        # drag file out from depot.
        if self._drag_file:
            event.ignore()
            return

        try:
            set_file = event.mimeData().urls()[0].toLocalFile()

        except Exception as err:
            event.ignore()
            return

        if set_file.split(".")[-1].lower() in ("dps", "json", "txt", "aco", "ase", "gpl", "xml"):
            self._drop_file = set_file
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Sync to wheel.py. May exist difference.
        """

        if self._drop_file:
            self.ps_dropped.emit((self._drop_file, False))
            self._drop_file = None

            event.accept()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def home(self):
        """
        Home points.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            self._selecting_idx = 0
            self._last_selecting_idx = 0

            self.update()

        else:
            self.reset_locations()

            # self.update()
            # is completed by self.reset_locations().

    def move(self, shift_x, shift_y):
        """
        Move points.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            next_idx = self._selecting_idx

            if shift_x < 0.0:
                next_idx = next_idx - 1

            elif shift_x > 0.0:
                next_idx = next_idx + 1

            if shift_y < 0.0:
                next_idx = next_idx - self._args.sys_grid_values["col"]

            elif shift_y > 0.0:
                next_idx = next_idx + self._args.sys_grid_values["col"]

            if next_idx != self._selecting_idx:
                self._last_selecting_idx = self._selecting_idx
                self._selecting_idx = next_idx

            self.update_select_idx()

        else:
            if self._last_moving:
                loc = list(self._args.sys_grid_assitlocs[self._args.sys_activated_idx][0])

                if shift_x < 0.0:
                    loc[0] = loc[0] - 0.5 / self._args.sys_grid_values["col"]

                elif shift_x > 0.0:
                    loc[0] = loc[0] + 0.5 / self._args.sys_grid_values["col"]

                if shift_y < 0.0:
                    loc[1] = loc[1] - 0.5 / self._args.sys_grid_values["col"]

                elif shift_y > 0.0:
                    loc[1] = loc[1] + 0.5 / self._args.sys_grid_values["col"]

                loc[0] = -1.0 if loc[0] < -1.0 else loc[0]
                loc[0] =  1.0 if loc[0] >  1.0 else loc[0]
                loc[1] = -1.0 if loc[1] < -1.0 else loc[1]
                loc[1] =  1.0 if loc[1] >  1.0 else loc[1]

                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][0][0] = loc[0]
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][0][1] = loc[1]

            else:
                loc = list(self._args.sys_grid_locations[self._args.sys_activated_idx])

                if shift_x < 0.0:
                    loc[0] = loc[0] - 0.5 / self._args.sys_grid_values["col"]

                elif shift_x > 0.0:
                    loc[0] = loc[0] + 0.5 / self._args.sys_grid_values["col"]

                if shift_y < 0.0:
                    loc[1] = loc[1] - 0.5 / self._args.sys_grid_values["col"]

                elif shift_y > 0.0:
                    loc[1] = loc[1] + 0.5 / self._args.sys_grid_values["col"]

                loc[0] = loc[0] % 1.0
                loc[1] = loc[1] % 1.0

                self._args.sys_grid_locations[self._args.sys_activated_idx] = tuple(loc)

        self.update()

    def zoom(self, ratio):
        """
        Zoom points.
        """

        if not self.isVisible():
            return

        if self._args.rev_direct:
            if ratio > 1 and self._args.sys_grid_values["col"] >= 2:
                self._args.sys_grid_values["col"] = int(self._args.sys_grid_values["col"] - 1)

            elif ratio < 1 and self._args.sys_grid_values["col"] <= 50:
                self._args.sys_grid_values["col"] = int(self._args.sys_grid_values["col"] + 1)

        else:
            if ratio > 1 and self._args.sys_grid_values["col"] <= 50:
                self._args.sys_grid_values["col"] = int(self._args.sys_grid_values["col"] + 1)

            elif ratio < 1 and self._args.sys_grid_values["col"] >= 2:
                self._args.sys_grid_values["col"] = int(self._args.sys_grid_values["col"] - 1)

        self.ps_value_changed.emit(True)
        self.ps_history_backup.emit(True)

        self.update()

    def update_select_idx(self):
        """
        Verify and update select_idx and last_select_idx.
        """

        # the verifing of grid_list length and others should be completed by upper level functions.

        max_gidx = min(len(self._args.sys_grid_list[0]), self._args.sys_grid_values["col"] ** 2 - 1)

        self._selecting_idx = 0 if self._selecting_idx < 0 else self._selecting_idx
        self._selecting_idx = max_gidx if self._selecting_idx > max_gidx else self._selecting_idx

        max_gidx = min(len(self._args.sys_grid_list[0]) - 1, self._args.sys_grid_values["col"] ** 2 - 1)

        self._last_selecting_idx = 0 if self._last_selecting_idx < 0 else self._last_selecting_idx
        self._last_selecting_idx = max_gidx if self._last_selecting_idx > max_gidx else self._last_selecting_idx

        # set_context into info window, thus can change the info dynamically. (recovered)
        # similar to clone_cell in activate_idx in depot.py.
        self._color_box.set_context(self._selecting_idx)
        self.ps_history_backup.emit(True)

    def show_or_hide_points(self):
        """
        Show or hide main and assistant points.
        """

        if not self.isVisible():
            return

        if not self._args.sys_grid_list[0]:
            self._show_points = not self._show_points

            self.update()

    def clear_or_gen_grid_list(self):
        """
        Dynamic board <-> Grid list according to the dynamic board.
        """

        if not self.isVisible():
            return

        if self._color_box.isVisible():
            return

        # unlink colors.
        self._args.sys_link_colors[0] = False
        self.ps_linked.emit(True)

        # clean or gen.
        if self._args.sys_grid_list[0]:
            self._show_points = True
            self._args.sys_grid_list = [[], []]

        else:
            self._show_points = False

            grid_list = [[], ["",] * self._args.sys_grid_values["col"] ** 2]

            color_grid = self._color_grid.tolist()

            for i in range(len(color_grid)):
                for j in range(len(color_grid[i])):
                    grid_list[0].append(Color.rgb2hec(color_grid[i][j]))

            self._args.sys_grid_list = grid_list

        self._selecting_idx = -1
        self._last_selecting_idx = -1
        self.ps_history_backup.emit(True)

        self.update()

    def clear_or_gen_assit_color_list(self):
        """
        Dynamic board <-> Assit color list.
        """

        if not self.isVisible():
            return

        if self._color_box.isVisible():
            return

        # unlink colors.
        self._args.sys_link_colors[0] = False
        self.ps_linked.emit(True)

        # clean or gen.
        if self._args.sys_grid_list[0]:
            self._show_points = True
            self._args.sys_grid_list = [[], []]

        else:
            self._show_points = False

            grid_list = [[], []]

            # generate full colors. this code is reused.
            for idx in (2, 1, 0, 3, 4):
                grid_list[0].append(self._args.sys_color_set[idx].hec)
                grid_list[1].append(self._color_descs[0] + " {}".format(idx))

            grid_list[0].append("FFFFFF")
            grid_list[1].append("")

            for idx in (2, 1, 0, 3, 4):
                grid_list[0].append(self._args.sys_color_set[idx].hec)
                grid_list[1].append(self._color_descs[0] + " {}".format(idx))

                for assit_idx in range(len(self._args.sys_grid_assitlocs[idx])):
                    assit_color = gen_assit_color(self._args.sys_color_set[idx], *self._args.sys_grid_assitlocs[idx][assit_idx][2:6])

                    grid_list[0].append(assit_color.hec)
                    grid_list[1].append(self._color_descs[1] + " {}-{}".format(idx, assit_idx))

            self._args.sys_grid_list = grid_list

        self._selecting_idx = -1
        self._last_selecting_idx = -1
        self.ps_history_backup.emit(True)

        self.update()

    def get_box_name(self, idx):
        """
        Get the name of color box at idx in fixed view.
        """

        if idx < 0 or idx > min(len(self._args.sys_grid_list[0]) - 1, self._args.sys_grid_values["col"] ** 2 - 1):
            return ""

        name = self._args.sys_grid_list[1][idx]

        if not name:
            name = self._tip_descs[0]

        return name

    def act_append_color_box(self):
        """
        Append a color box at end.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            self._args.sys_grid_list[0].append(self._args.sys_color_set[self._args.sys_activated_idx].hec)
            self._args.sys_grid_list[1].append("")

            self.update_select_idx()

    def act_append_beside_color_box(self):
        """
        Append a color box beside.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0] and self._selecting_idx < len(self._args.sys_grid_list[0]):
            self._args.sys_grid_list[0] = self._args.sys_grid_list[0][:self._selecting_idx] + [self._args.sys_color_set[self._args.sys_activated_idx].hec,] + self._args.sys_grid_list[0][self._selecting_idx:]
            self._args.sys_grid_list[1] = self._args.sys_grid_list[1][:self._selecting_idx] + ["",] + self._args.sys_grid_list[1][self._selecting_idx:]

            self.update_select_idx()

    def act_rev_insert_color_box(self):
        """
        Insert the result color into a color box.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0] and self._selecting_idx < len(self._args.sys_grid_list[0]):
            self._args.sys_grid_list[0][self._selecting_idx] = self._args.sys_color_set[self._args.sys_activated_idx].hec

            self.update_select_idx()

    def act_insert_color_box(self):
        """
        Insert the color in a color box into the result.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0] and self._selecting_idx < len(self._args.sys_grid_list[0]):
            color = Color(self._args.sys_grid_list[0][self._selecting_idx], tp="hec", overflow=self._args.sys_color_set.get_overflow())
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

            self.ps_color_changed.emit(True)

            self.update_select_idx()

    def link_point(self, link):
        """
        Link point with result.

        Args:
            link (bool): whether linked.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0] and self._selecting_idx < len(self._args.sys_grid_list[0]):
            self._args.sys_link_colors[0] = bool(link)
            self.ps_linked.emit(True)

    def insert_point(self, insert_pt_beside=False):
        """
        Insert a point into assistant list (dynamic view) or grid list (fixed view) without updating color type and value.

        Args:
            insert_pt_beside (bool): whether append a color beside the selected color box. 
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            if self._selecting_idx < self._args.sys_grid_values["col"] ** 2:
                if self._selecting_idx >= len(self._args.sys_grid_list[0]):
                    self.act_append_color_box()

                else:
                    if self._press_key in (2, 4):
                        self.act_rev_insert_color_box()

                    elif self._press_key == 1 or insert_pt_beside:
                        self.act_append_beside_color_box()

                    else:
                        self.act_insert_color_box()

                    # link and unlink.
                    if self._press_key == 2:
                        self.link_point(not self._args.sys_link_colors[0])

                    elif self._args.sys_link_colors[0]:
                        self.link_point(False)

        else:
            # similar to func "insert_assit_point" in wheel.py.
            #
            loc_a, loc_b = 0.1, 0.1

            self._args.sys_activated_assit_idx = len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx])
            self._args.sys_grid_assitlocs[self._args.sys_activated_idx].append([loc_a, loc_b, 15, 0.0, 0.0, True])
            self._args.sys_assit_color_locs[self._args.sys_activated_idx].append(None)

            self.ps_color_changed.emit(True)

        self.update()

    def switch_point(self):
        """
        Switch selected point (self._selecting_idx) with last selected point.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0] and 0 <= self._selecting_idx < len(self._args.sys_grid_list[0]) and 0 <= self._last_selecting_idx < len(self._args.sys_grid_list[0]) and self._selecting_idx != self._last_selecting_idx:
            self._args.sys_grid_list[0][self._selecting_idx], self._args.sys_grid_list[0][self._last_selecting_idx] = self._args.sys_grid_list[0][self._last_selecting_idx], self._args.sys_grid_list[0][self._selecting_idx]
            self._args.sys_grid_list[1][self._selecting_idx], self._args.sys_grid_list[1][self._last_selecting_idx] = self._args.sys_grid_list[1][self._last_selecting_idx], self._args.sys_grid_list[1][self._selecting_idx]

            self.update_select_idx()
            self.update()

    def delete_point(self, direct_delete=False):
        """
        Delete current point from assistant list (dynamic view) or grid list (fixed view) without updating color type and value.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            if len(self._args.sys_grid_list[0]) == 1 and self._args.sys_grid_list[0][0] == "FFFFFF":
                return

            if 0 <= self._selecting_idx < min(self._args.sys_grid_values["col"] ** 2, len(self._args.sys_grid_list[0])):
                if self._args.sys_grid_list[0][self._selecting_idx] == "FFFFFF" or direct_delete:
                    self._args.sys_grid_list[0].pop(self._selecting_idx)
                    self._args.sys_grid_list[1].pop(self._selecting_idx)

                else:
                    self._args.sys_grid_list[0][self._selecting_idx] = "FFFFFF"
                    self._args.sys_grid_list[1][self._selecting_idx] = ""

                self.update_select_idx()

        else:
            if len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]) > self._args.sys_activated_assit_idx >= 0:
                if self._args.sys_activated_assit_idx == 0:
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][1:]
                    self._args.sys_assit_color_locs[self._args.sys_activated_idx] = self._args.sys_assit_color_locs[self._args.sys_activated_idx][1:]

                else:
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][:self._args.sys_activated_assit_idx] + self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx + 1:]
                    self._args.sys_assit_color_locs[self._args.sys_activated_idx] = self._args.sys_assit_color_locs[self._args.sys_activated_idx][:self._args.sys_activated_assit_idx] + self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx + 1:]

                self._args.sys_activated_assit_idx = -1

                self.ps_color_changed.emit(True)

        self.update()

    def confirm_delete_point(self):
        """
        Act delete_point with confirmation.
        """

        if not self.isVisible():
            return

        if self._args.sys_grid_list[0]:
            self.prompt(self._operation_warns[3], lambda: self.delete_point(direct_delete=True))

        else:
            self.prompt(self._operation_warns[4], self.delete_point)

    def detail_point(self):
        """
        Show info of color box at current idx.
        """

        if not self.isVisible():
            return

        if self._selecting_idx < 0 or self._selecting_idx > len(self._args.sys_grid_list[0]) - 1:
            return

        # self.update_select_idx()

        # self._color_box.set_context is completed by self.update_select_idx above. (recovered)
        # self._color_box.set_context(self._selecting_idx)

        if self._args.sys_grid_list[0]:
            self._color_box.show()

    def hide_detail(self):
        """
        Hide the info window.
        Esc refer to close self._color_box if it is visible (return True) in main window.
        """

        if self._color_box.isVisible():
            self._color_box.hide()
            
            return True

        else:
            return False

    def update_index(self):
        """
        The color type and value of current point will be changed when color set index is changed. For self._wget_cube_table.ps_value_changed in main.py.
        Opposite function to update_assitp (deleted because of fake_current_assitp).
        Link colors with cube table here.
        """

        # similar code segment in method self.insert_point with self._press_key == 2.
        if self._args.sys_link_colors[0] and self._args.sys_grid_list[0] and self._selecting_idx < len(self._args.sys_grid_list[0]):
            self._args.sys_grid_list[0][self._selecting_idx] = self._args.sys_color_set[self._args.sys_activated_idx].hec

            self.update_select_idx()

        self.ps_value_changed.emit(True)

        self.update()

    def reset_locations(self):
        """
        Reset point loctions to default values.
        """

        if self._color_box.isVisible():
            return

        if self._args.sys_grid_list[0]:
            self._show_points = True
            self._args.sys_grid_list = [[], []]

        self._args.sys_grid_locations, _ = norm_grid_locations([], [])
        self._args.sys_activated_assit_idx = -1

        self._args.sys_assit_color_locs = [[None for j in self._args.sys_grid_assitlocs[i]] for i in range(5)]

        # reset center.
        for idx in range(5):
            assit_len = len(self._args.sys_grid_assitlocs[idx])

            for assit_idx in range(assit_len):
                self._args.sys_grid_assitlocs[idx][assit_idx][0:2] = rotate_point((0.2, 0), assit_idx / assit_len * 360)

        self._args.sys_grid_values = norm_grid_values({})

        self._selecting_idx = -1
        self._last_selecting_idx = -1

        self.ps_value_changed.emit(True)
        self.ps_history_backup.emit(True)
        self.update()

    def clipboard_in(self):
        """
        Load set from clipboard. Sync to wheel.py. May exist difference.
        """

        if not self.isVisible():
            return

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                set_file = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if set_file.split(".")[-1].lower() in ("dps", "json", "txt", "aco", "ase", "gpl", "xml") and os.path.isfile(set_file):
                self.ps_dropped.emit((set_file, False))
                self.ps_history_backup.emit(True)

        else:
            try:
                color_dict = json.loads(clipboard.text(), encoding="utf-8")

            except Exception as err:
                return

            if isinstance(color_dict, dict) and "type" in color_dict and "palettes" in color_dict:
                if color_dict["type"] == "set":
                    self.ps_dropped.emit((color_dict, True))
                    self.ps_history_backup.emit(True)

    def clipboard_img(self):
        """
        Set the board image as the clipboard data by Ctrl + c.
        """

        if not (self.isVisible() and isinstance(self._color_grid, np.ndarray)):
            return

        grid_img = QImage(self._color_grid, self._color_grid.shape[1], self._color_grid.shape[0], self._color_grid.shape[1] * 3, QImage.Format_RGB888)
        grid_img = grid_img.scaled(self._cs_box[2], self._cs_box[3], Qt.KeepAspectRatio)

        mimedata = QMimeData()
        mimedata.setImageData(QPixmap.fromImage(grid_img))

        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mimedata)

    def clipboard_cur(self, ctp):
        """
        Set the rgb, hsv or hec (hex code) of current color box as the clipboard data by shortcut Ctrl + r, h or x.
        """

        def _func_():
            if self._args.sys_grid_list[0] and 0 <= self._selecting_idx < len(self._args.sys_grid_list[0]):
                color = Color(self._args.sys_grid_list[0][self._selecting_idx], tp="hec").getti(ctp)

            else:
                color = self._args.sys_color_set[self._args.sys_activated_idx].getti(ctp)

            if ctp == "hec":
                color = self._args.hec_prefix[0] + str(color) + self._args.hec_prefix[1]

            else:
                color = self._args.rgb_prefix[1].join([self._args.r_prefix[0] + str(color[coi]) + self._args.r_prefix[1] for coi in range(3)])
                color = self._args.rgb_prefix[0] + color + self._args.rgb_prefix[2]

            mimedata = QMimeData()
            mimedata.setText(color)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mimedata)

        return _func_

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

        #   _translate("Board", "Undo"), # 0
        #   _translate("Board", "Redo"), # 1
        self._action_undo = QAction(self)
        self._action_undo.triggered.connect(lambda: self.ps_undo.emit(True))
        self._menu.addAction(self._action_undo)

        self._action_redo = QAction(self)
        self._action_redo.triggered.connect(lambda: self.ps_undo.emit(False))
        self._menu.addAction(self._action_redo)

        #   _translate("Board", "Reset"), # 2
        self._action_reset = QAction(self)
        self._action_reset.triggered.connect(self.reset_locations)
        self._menu.addAction(self._action_reset)

        #   _translate("Board", "Paste"), # 7
        self._action_paste = QAction(self)
        self._action_paste.triggered.connect(self.clipboard_in)
        self._menu.addAction(self._action_paste)

        #   _translate("Board", "Copy RGB"), # 3
        #   _translate("Board", "Copy HSV"), # 4
        #   _translate("Board", "Copy Hex Code"), # 5
        self._action_copy_rgb = QAction(self)
        self._action_copy_rgb.triggered.connect(self.clipboard_cur("rgb"))
        self._menu.addAction(self._action_copy_rgb)

        self._action_copy_hsv = QAction(self)
        self._action_copy_hsv.triggered.connect(self.clipboard_cur("hsv"))
        self._menu.addAction(self._action_copy_hsv)

        self._action_copy_hec = QAction(self)
        self._action_copy_hec.triggered.connect(self.clipboard_cur("hec"))
        self._menu.addAction(self._action_copy_hec)

        #   _translate("Board", "Copy as Image"), # 6
        self._action_copy_img = QAction(self)
        self._action_copy_img.triggered.connect(self.clipboard_img)
        self._menu.addAction(self._action_copy_img)

        #   _translate("Board", "Zoom In"), # 8
        #   _translate("Board", "Zoom Out"), # 9
        self._action_zoom_in = QAction(self)
        self._action_zoom_in.triggered.connect(lambda: self.zoom(self._args.zoom_step))
        self._menu.addAction(self._action_zoom_in)

        self._action_zoom_out = QAction(self)
        self._action_zoom_out.triggered.connect(lambda: self.zoom(1 / self._args.zoom_step))
        self._menu.addAction(self._action_zoom_out)

        #   _translate("Board", "Insert Ref Point (Ctrl+MV)"), # 10
        #   _translate("Board", "Replace Color (DK)"), # 14
        self._action_insert = QAction(self)
        self._action_insert.triggered.connect(self.insert_point)
        self._menu.addAction(self._action_insert)

        #   _translate("Board", "Fix Ref Point (DK)"), # 12
        #   _translate("Board", "Un-Fix Ref Point (DK)"), # 13
        self._action_fix_pt = QAction(self)
        self._action_fix_pt.triggered.connect(lambda: self.ps_assit_pt_changed.emit(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]) if self._args.sys_activated_assit_idx >= 0 else None)
        self._menu.addAction(self._action_fix_pt)

        #   _translate("Board", "Rev-Replace Color (Alt+DK)"), # 15
        self._action_rev_insert = QAction(self)
        self._action_rev_insert.triggered.connect(self.act_rev_insert_color_box)
        self._menu.addAction(self._action_rev_insert)

        #   _translate("Board", "Delete Ref Point"), # 11
        #   _translate("Board", "Delete Color Box"), # 18
        self._action_delete = QAction(self)
        self._action_delete.triggered.connect(self.delete_point)
        self._menu.addAction(self._action_delete)

        #   _translate("Board", "Insert Color Box (Shift+DK)"), # 16
        self._action_insert_beside = QAction(self)
        self._action_insert_beside.triggered.connect(self.act_append_beside_color_box)
        self._menu.addAction(self._action_insert_beside)

        #   _translate("Board", "Append Color Box"), # 17
        self._action_insert_append = QAction(self)
        self._action_insert_append.triggered.connect(self.act_append_color_box)
        self._menu.addAction(self._action_insert_append)

        #   _translate("Board", "Switch Color Boxes"), # 19
        self._action_switch = QAction(self)
        self._action_switch.triggered.connect(self.switch_point)
        self._menu.addAction(self._action_switch)

        #   _translate("Board", "Show Points"), # 26
        #   _translate("Board", "Hide Points"), # 27
        self._action_hide_pt = QAction(self)
        self._action_hide_pt.triggered.connect(self.show_or_hide_points)
        self._menu.addAction(self._action_hide_pt)

        #   _translate("Board", "Link with Result (Ctrl+DK)"), # 21
        #   _translate("Board", "Un-Link with Result (Ctrl+DK)"), # 22
        self._action_link = QAction(self)
        self._action_link.triggered.connect(lambda: self.link_point(not self._args.sys_link_colors[0]))
        self._menu.addAction(self._action_link)

        #   _translate("Board", "Make Gradient Board"), # 23
        #   _translate("Board", "Make Fixed Board"), # 24
        #   _translate("Board", "Make Ref Board"), # 25
        self._action_fixed_board = QAction(self)
        self._action_fixed_board.triggered.connect(self.clear_or_gen_grid_list)
        self._menu.addAction(self._action_fixed_board)

        self._action_ref_board = QAction(self)
        self._action_ref_board.triggered.connect(self.clear_or_gen_assit_color_list)
        self._menu.addAction(self._action_ref_board)

        #   _translate("Board", "Show Detail"), # 20
        self._action_detail = QAction(self)
        self._action_detail.triggered.connect(self.detail_point)
        self._menu.addAction(self._action_detail)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        self.update_action_text()

        # special actions for delete later.
        self._action_copy_rgb.setVisible(True)
        self._action_copy_hsv.setVisible(True)
        self._action_copy_hec.setVisible(True)
        self._action_insert_beside.setVisible(True)
        self._action_switch.setVisible(True)
        self._action_detail.setVisible(True)
        self._action_link.setVisible(True)
        self._action_fix_pt.setVisible(True)

        # normal actions delete.
        if self._args.sys_grid_list[0]:
            self._action_rev_insert.setVisible(True)
            self._action_insert_beside.setVisible(True)
            self._action_insert_append.setVisible(True)
            self._action_switch.setVisible(True)
            self._action_detail.setVisible(True)
            self._action_link.setVisible(True)
            self._action_ref_board.setVisible(False)
            self._action_hide_pt.setVisible(False)

        else:
            self._action_rev_insert.setVisible(False)
            self._action_insert_beside.setVisible(False)
            self._action_insert_append.setVisible(False)
            self._action_switch.setVisible(False)
            self._action_detail.setVisible(False)
            self._action_link.setVisible(False)
            self._action_ref_board.setVisible(True)
            self._action_hide_pt.setVisible(True)

        if self._args.sys_grid_list[0] or self._show_points:
            self._action_insert.setVisible(True)
            self._action_delete.setVisible(True)

        else:
            self._action_insert.setVisible(False)
            self._action_delete.setVisible(False)

        if not self._args.sys_grid_list[0] and self._show_points:
            self._action_fix_pt.setVisible(True)

        else:
            self._action_fix_pt.setVisible(False)

        # special actions delete here.
        if self._args.sys_grid_list[0] and self._selecting_idx >= len(self._args.sys_grid_list[0]):
            self._action_copy_rgb.setVisible(False)
            self._action_copy_hsv.setVisible(False)
            self._action_copy_hec.setVisible(False)
            self._action_insert_beside.setVisible(False)
            self._action_switch.setVisible(False)
            self._action_detail.setVisible(False)
            self._action_link.setVisible(False)

        if self._args.sys_activated_assit_idx < 0:
            self._action_fix_pt.setVisible(False)

        self._menu.exec_(QCursor.pos())

    # ---------- ---------- ---------- Shortcut ---------- ---------- ---------- #

    def update_skey(self):
        """
        Set board shortcuts.
        """

        for skey in self._args.shortcut_keymaps[39]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.delete_point)

        for skey in self._args.shortcut_keymaps[40]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.confirm_delete_point)

        for skey in self._args.shortcut_keymaps[38]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.insert_point)

        for skey in self._args.shortcut_keymaps[41]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.detail_point)

        for skey in self._args.shortcut_keymaps[42]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.switch_point)

        for skey in self._args.shortcut_keymaps[43]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.show_or_hide_points)

        for skey in self._args.shortcut_keymaps[44]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clear_or_gen_grid_list)

        for skey in self._args.shortcut_keymaps[51]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clear_or_gen_assit_color_list)

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

            shortcut.activated.connect(self.clipboard_img)

        for skey in self._args.shortcut_keymaps[46]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_in)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_action_text(self):
        #   _translate("Board", "Undo"), # 0
        #   _translate("Board", "Redo"), # 1
        self._action_undo.setText(self._action_descs[0])
        self._action_redo.setText(self._action_descs[1])

        #   _translate("Board", "Reset"), # 2
        self._action_reset.setText(self._action_descs[2])

        #   _translate("Board", "Copy RGB"), # 3
        #   _translate("Board", "Copy HSV"), # 4
        #   _translate("Board", "Copy Hex Code"), # 5
        self._action_copy_rgb.setText(self._action_descs[3])
        self._action_copy_hsv.setText(self._action_descs[4])
        self._action_copy_hec.setText(self._action_descs[5])

        #   _translate("Board", "Copy as Image"), # 6
        self._action_copy_img.setText(self._action_descs[6])

        #   _translate("Board", "Paste"), # 7
        self._action_paste.setText(self._action_descs[7])

        #   _translate("Board", "Zoom In"), # 8
        #   _translate("Board", "Zoom Out"), # 9
        self._action_zoom_in.setText(self._action_descs[8])
        self._action_zoom_out.setText(self._action_descs[9])

        #   _translate("Board", "Insert Ref Point (Ctrl+MV)"), # 10
        #   _translate("Board", "Replace Color (DK)"), # 14
        if self._args.sys_grid_list[0]:
            self._action_insert.setText(self._action_descs[14])

        else:
            self._action_insert.setText(self._action_descs[10])

        #   _translate("Board", "Delete Ref Point"), # 11
        #   _translate("Board", "Delete Color Box"), # 18
        if self._args.sys_grid_list[0]:
            self._action_delete.setText(self._action_descs[18])

        else:
            self._action_delete.setText(self._action_descs[11])

        #   _translate("Board", "Fix Ref Point (DK)"), # 12
        #   _translate("Board", "Un-Fix Ref Point (DK)"), # 13
        if self._args.sys_activated_assit_idx >= 0 and self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]:
            self._action_fix_pt.setText(self._action_descs[12])

        else:
            self._action_fix_pt.setText(self._action_descs[13])

        #   _translate("Board", "Rev-Replace Color (Alt+DK)"), # 15
        self._action_rev_insert.setText(self._action_descs[15])

        #   _translate("Board", "Insert Color Box (Shift+DK)"), # 16
        self._action_insert_beside.setText(self._action_descs[16])

        #   _translate("Board", "Append Color Box"), # 17
        self._action_insert_append.setText(self._action_descs[17])

        #   _translate("Board", "Switch Color Boxes"), # 19
        self._action_switch.setText(self._action_descs[19])

        #   _translate("Board", "Show Detail"), # 20
        self._action_detail.setText(self._action_descs[20])

        #   _translate("Board", "Link with Result (Ctrl+DK)"), # 21
        #   _translate("Board", "Un-Link with Result (Ctrl+DK)"), # 22
        if self._args.sys_link_colors[0]:
            self._action_link.setText(self._action_descs[22])

        else:
            self._action_link.setText(self._action_descs[21])

        #   _translate("Board", "Make Gradient Board"), # 23
        #   _translate("Board", "Make Fixed Board"), # 24
        #   _translate("Board", "Make Ref Board"), # 25
        if self._args.sys_grid_list[0]:
            self._action_fixed_board.setText(self._action_descs[23])
            self._action_ref_board.setText(self._action_descs[23])

        else:
            self._action_fixed_board.setText(self._action_descs[24])
            self._action_ref_board.setText(self._action_descs[25])

        #   _translate("Board", "Show Points"), # 26
        #   _translate("Board", "Hide Points"), # 27
        if self._show_points:
            self._action_hide_pt.setText(self._action_descs[27])

        else:
            self._action_hide_pt.setText(self._action_descs[26])

    def update_text(self):
        self.update_action_text()

        self._color_box.set_default_name(self._tip_descs[0])

        self._color_box._func_tr_()
        self._color_box.update_text()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Wheel", "Undo"), # 0
            _translate("Wheel", "Redo"), # 1
            _translate("Board", "Reset"), # 2
            _translate("Board", "Copy RGB"), # 3
            _translate("Board", "Copy HSV"), # 4
            _translate("Board", "Copy Hex Code"), # 5
            _translate("Board", "Copy as Image"), # 6
            _translate("Wheel", "Paste"), # 7
            _translate("Board", "Zoom In"), # 8
            _translate("Board", "Zoom Out"), # 9
            _translate("Board", "Insert Ref Point (Ctrl+MV)"), # 10
            _translate("Board", "Delete Ref Point"), # 11
            _translate("Board", "Fix Ref Point (DK)"), # 12
            _translate("Board", "Un-Fix Ref Point (DK)"), # 13
            _translate("Board", "Replace Color (DK)"), # 14
            _translate("Board", "Rev-Replace Color (Alt+DK)"), # 15
            _translate("Board", "Insert Color Box (Shift+DK)"), # 16
            _translate("Board", "Append Color Box"), # 17
            _translate("Board", "Delete Color Box"), # 18
            _translate("Board", "Switch Color Boxes"), # 19
            _translate("Board", "Show Detail"), # 20
            _translate("Board", "Link with Result (Ctrl+DK)"), # 21
            _translate("Board", "Un-Link with Result (Ctrl+DK)"), # 22
            _translate("Board", "Make Gradient Board"), # 23
            _translate("Board", "Make Fixed Board"), # 24
            _translate("Board", "Make Ref Board"), # 25
            _translate("Board", "Show Points"), # 26
            _translate("Board", "Hide Points"), # 27
        )

        self._recommend_descs = (
            _translate("Rickrack", "{} ({})"),
        )

        self._tip_descs = (
            _translate("Info", "Rickrack Color Box"),
        )

        self._color_descs = (
            _translate("Info", "Main Color"),
            _translate("Info", "Reference Color"),
        )

        self._operation_warns = (
            _translate("Info", "Warning"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
            _translate("Info", "The selected color box will be removed from board."),
            _translate("Info", "The selected assistant point will be removed from board."),
        )
