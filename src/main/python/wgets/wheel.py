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
import json
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QShortcut, QApplication
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, pyqtSignal, QMimeData, QPoint, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QRadialGradient, QLinearGradient, QKeySequence, QDrag, QPixmap, QCursor
from cguis.resource import view_rc
from ricore.transpt import get_outer_box, rotate_point_center, get_theta_center
from ricore.color import Color
from ricore.export import export_list


class Wheel(QWidget):
    """
    Wheel object based on QWidget. Init a color wheel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_index_changed = pyqtSignal(bool)
    ps_status_changed = pyqtSignal(tuple)
    ps_dropped = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init color wheel.
        """

        super().__init__(wget)

        # set name ids.
        wget.setProperty("class", "WorkArea")

        # load args.
        self._args = args
        self._backup = self._args.sys_color_set.backup()
        self._drag_file = False
        self._drop_file = None
        self._press_key = 0
        self._connected_keymaps = {}

        # init global args.
        self._pressed_in_wheel = False
        self._pressed_in_bar_1 = False
        self._pressed_in_bar_2 = False

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self.setMinimumSize(QSize(300, 200))

        # shortcut is updated by _setup_skey in main.py.
        # self.update_skey()

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        self._center = np.array((self.width() / 2.0, self.height() / 2.0))
        self._radius = min(self.width(), self.height()) * self._args.wheel_ratio / 2

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # color wheel. hue.
        wheel_box = get_outer_box(self._center, self._radius)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        cgrad = QConicalGradient(*self._center, 0)
        cgrad.setColorAt(0.00000, QColor(255, 0  , 0  ))
        cgrad.setColorAt(0.16667, QColor(255, 0  , 255))
        cgrad.setColorAt(0.33333, QColor(0  , 0  , 255))
        cgrad.setColorAt(0.50000, QColor(0  , 255, 255))
        cgrad.setColorAt(0.66667, QColor(0  , 255, 0  ))
        cgrad.setColorAt(0.83333, QColor(255, 255, 0  ))
        cgrad.setColorAt(1.00000, QColor(255, 0  , 0  ))
        painter.setBrush(cgrad)
        painter.drawEllipse(*wheel_box)

        # color wheel. saturation.
        rgrad = QRadialGradient(*self._center, self._radius)
        rgrad.setColorAt(0.0, Qt.white)
        rgrad.setColorAt(1.0, Qt.transparent)
        painter.setBrush(rgrad)
        painter.drawEllipse(*wheel_box)

        # bars.
        bar_hsv = self._args.sys_color_set[self._args.sys_activated_idx].hsv
        bar_v = bar_hsv[2]
        bar_rgb = Color.hsv2rgb((bar_hsv[0], bar_hsv[1], 1.0))
        self._v_tag_radius = min(self.width(), self.height()) * self._args.v_tag_radius / 2

        re_wid = self.width() * (1 - self._args.wheel_ratio) / 2 * self._args.volum_ratio
        re_wid = self._v_tag_radius * 3 if self._v_tag_radius * 3 < re_wid else re_wid

        bar_1_center = ((self.width() - self._radius * 2) / 4, self.height() / 2)
        self._bar_1_box = (bar_1_center[0] - re_wid / 2, bar_1_center[1] - self.height() * self._args.volum_ratio / 2, re_wid, self.height() * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_1_box[0], self._bar_1_box[1], self._bar_1_box[0], self._bar_1_box[3])
        lgrad.setColorAt(1.0, Qt.white)
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_1_box)

        self._cir_1_center = (bar_1_center[0], self._bar_1_box[1] + self._bar_1_box[3] * bar_v)
        cir_1_box = get_outer_box(self._cir_1_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_1_box)

        bar_2_center = (self.width() - (self.width() - self._radius * 2) / 4, self.height() / 2)
        self._bar_2_box = (bar_2_center[0] - re_wid / 2, bar_2_center[1] - self.height() * self._args.volum_ratio / 2, re_wid, self.height() * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_2_box[0], self._bar_2_box[1], self._bar_2_box[0], self._bar_2_box[3])
        lgrad.setColorAt(1.0, QColor(*bar_rgb))
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_2_box)

        self._cir_2_center = (bar_2_center[0], self._bar_2_box[1] + self._bar_2_box[3] * bar_v)
        cir_2_box = get_outer_box(self._cir_2_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_2_box)

        # color set tags.
        self._tag_center = [None] * 5
        self._tag_radius = min(self.width(), self.height()) * self._args.s_tag_radius / 2

        self._idx_seq = list(range(5))
        self._idx_seq = self._idx_seq[self._args.sys_activated_idx + 1: ] + self._idx_seq[: self._args.sys_activated_idx + 1]

        # lines.
        for idx in self._idx_seq:
            color_center = np.array([self._args.sys_color_set[idx].s * self._radius, 0]) + self._center
            color_center = rotate_point_center(self._center, color_center, self._args.sys_color_set[idx].h)
            self._tag_center[idx] = color_center

            if idx == self._args.sys_activated_idx:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            painter.drawLine(QPoint(*self._center), QPoint(*color_center))

        # dot.
        dot_box = get_outer_box(self._center, self._args.positive_wid)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(QColor(*self._args.positive_color)))
        painter.drawEllipse(*dot_box)

        # circles.
        for idx in self._idx_seq:
            color_box = get_outer_box(self._tag_center[idx], self._tag_radius)

            if idx == self._args.sys_activated_idx:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            painter.setBrush(QColor(*self._args.sys_color_set[idx].rgb))
            painter.drawEllipse(*color_box)

        painter.end()

        self.ps_status_changed.emit(Color.sign(self._args.sys_color_set[self._args.sys_activated_idx].hsv))

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self._press_key = 1
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
        if self._press_key == 1 and event.button() == Qt.LeftButton:
            #
            # Sync to board.py.
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
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))

            event.accept()

        elif event.button() == Qt.LeftButton:
            point = np.array((event.x(), event.y()))
            self._backup = self._args.sys_color_set.backup()

            already_accepted = False

            for idx in self._idx_seq[::-1]:
                if np.linalg.norm(point - self._tag_center[idx]) < self._tag_radius:
                    self._args.sys_activated_idx = idx

                    self.ps_index_changed.emit(True)
                    already_accepted = True

                    event.accept()
                    # self.update() is completed by 
                    # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                    # same below.
                    break

            if already_accepted or (self._args.press_move and np.linalg.norm(point - self._center) < self._radius):
                self._pressed_in_wheel = True

                color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                color.s = np.linalg.norm(point - self._center) / self._radius
                color.h = get_theta_center(self._center, point)

                self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                self.ps_color_changed.emit(True)

                event.accept()
                # self.update() is completed by 
                # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                # same below.

            elif (not already_accepted) and ((self._bar_1_box[0] < point[0] < self._bar_1_box[0] + self._bar_1_box[2] and self._bar_1_box[1] < point[1] < self._bar_1_box[1] + self._bar_1_box[3]) or np.linalg.norm(point - self._cir_1_center) < self._v_tag_radius):
                if np.linalg.norm(point - self._cir_1_center) < self._v_tag_radius or self._args.press_move:
                    self._pressed_in_bar_1 = True

                    v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
                    color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                    color.v = v

                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                    self.ps_color_changed.emit(True)

                    event.accept()

                else:
                    event.ignore()

            elif (not already_accepted) and ((self._bar_2_box[0] < point[0] < self._bar_2_box[0] + self._bar_2_box[2] and self._bar_2_box[1] < point[1] < self._bar_2_box[1] + self._bar_2_box[3]) or np.linalg.norm(point - self._cir_2_center) < self._v_tag_radius):
                if np.linalg.norm(point - self._cir_2_center) < self._v_tag_radius or self._args.press_move:
                    self._pressed_in_bar_2 = True

                    v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
                    color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                    color.v = v

                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                    self.ps_color_changed.emit(True)

                    event.accept()

                else:
                    event.ignore()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        point = np.array((event.x(), event.y()))

        if self._pressed_in_wheel:
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.s = np.linalg.norm(point - self._center) / self._radius
            color.h = get_theta_center(self._center, point)

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_1:
            v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.v = v

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_2:
            v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.v = v

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._press_key = 0

        if self._pressed_in_wheel or self._pressed_in_bar_1 or self._pressed_in_bar_2:
            self._pressed_in_wheel = False
            self._pressed_in_bar_1 = False
            self._pressed_in_bar_2 = False

        event.ignore()

    def dragEnterEvent(self, event):
        """
        Sync to board.py. May exist difference.
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
        Sync to board.py. May exist difference.
        """

        if self._drop_file:
            self.ps_dropped.emit((self._drop_file, False))
            self._drop_file = None

            event.accept()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def clipboard_in(self):
        """
        Load set from clipboard. Sync to board.py. May exist difference.
        """

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                set_file = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if set_file.split(".")[-1].lower() in ("dps", "json", "txt", "aco", "ase", "gpl", "xml") and os.path.isfile(set_file):
                self.ps_dropped.emit((set_file, False))

        else:
            try:
                color_dict = json.loads(clipboard.text(), encoding="utf-8")

            except Exception as err:
                return

            if isinstance(color_dict, dict) and "type" in color_dict and "palettes" in color_dict:
                if color_dict["type"] == "set":
                    self.ps_dropped.emit((color_dict, True))

    def clipboard_all(self, ctp):
        """
        Set the rgb, hsv or hec (hex code) of all result colors as the clipboard data by shortcut Shift + r, h or c.
        """

        def _func_():
            data_lst = []

            for i in (2, 1, 0, 3, 4):
                color = self._args.sys_color_set[i].getti(ctp)

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

    # ---------- ---------- ---------- Shortcut ---------- ---------- ---------- #

    def update_skey(self):
        """
        Set depot shortcuts.
        """

        for skey in self._args.shortcut_keymaps[45]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_all("hec"))

        for skey in self._args.shortcut_keymaps[46]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_in)
