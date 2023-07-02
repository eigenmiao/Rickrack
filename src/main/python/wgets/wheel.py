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
from PyQt5.QtWidgets import QWidget, QShortcut, QMenu, QAction, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QCoreApplication, QSize, pyqtSignal, QMimeData, QPoint, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QRadialGradient, QLinearGradient, QKeySequence, QDrag, QPixmap, QCursor, QPolygon
from cguis.resource import view_rc
from ricore.transpt import get_outer_box, rotate_point_center, get_theta_center, get_outer_circles
from ricore.grid import gen_assit_color
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
    ps_history_backup = pyqtSignal(bool)
    ps_undo = pyqtSignal(bool)

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

        # load translations.
        self._func_tr_()

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self.setMinimumSize(QSize(150, 100))

        # generate point centers and radii.
        # self._center = ...
        # self._radius = ...
        # self._tag_centers = ...
        # self._tag_radii = ...
        # self._assit_tag_centers = ...
        # self._assit_tag_radii = ...
        self.init_pt_centers_and_radii()

        # outer circles.
        self._outer_circles = None

        # shortcut is updated by _setup_skey in main.py.
        # self.update_skey()

        self.create_menu()
        self.update_action_text()

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        # norm assit point index.
        if False: # self._args.sys_activated_assit_idx > len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]):
            self._args.sys_activated_assit_idx = -1
            self.ps_color_changed()

        # generate point centers and radii.
        self.init_pt_centers_and_radii()

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # color wheel. hue.
        wheel_box = get_outer_box(self._center, self._radius)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        cgrad = QConicalGradient(*self._center, 0)

        if self._args.dep_wtp:
            cgrad.setColorAt(0.00000, QColor(255, 0  , 0  ))
            cgrad.setColorAt(0.16667, QColor(255, 0  , 255))
            cgrad.setColorAt(0.33333, QColor(0  , 0  , 255))
            cgrad.setColorAt(0.44444, QColor(0  , 255, 255))
            cgrad.setColorAt(0.55555, QColor(0  , 255, 0  ))
            cgrad.setColorAt(0.66667, QColor(255, 255, 0  ))
            cgrad.setColorAt(1.00000, QColor(255, 0  , 0  ))

        else:
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

        if self._args.dep_rtp:
            rgrad.setColorAt(0.0, Qt.black)

        else:
            rgrad.setColorAt(0.0, Qt.white)

        rgrad.setColorAt(1.0, Qt.transparent)
        painter.setBrush(rgrad)
        painter.drawEllipse(*wheel_box)

        # bars.
        if self._args.sys_activated_assit_idx < 0:
            bar_hsv = self._args.sys_color_set[self._args.sys_activated_idx].hsv

        else:
            bar_hsv = gen_assit_color(self._args.sys_color_set[self._args.sys_activated_idx], *self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2:6]).hsv

        bar_i = bar_hsv[self._args.dep_wtp_rev_n]

        if self._args.dep_rtp:
            bar_rgb_1 = Color.hsv2rgb((bar_hsv[0], 1.0, 1.0))
            bar_end_rgb_1 = Color.hsv2rgb((bar_hsv[0], 0.0, 1.0))
            bar_rgb_2 = Color.hsv2rgb((bar_hsv[0], 1.0, bar_hsv[2]))
            bar_end_rgb_2 = Color.hsv2rgb((bar_hsv[0], 0.0, bar_hsv[2]))

        else:
            bar_rgb_1 = Color.hsv2rgb((bar_hsv[0], 0.0, 1.0))
            bar_end_rgb_1 = Color.hsv2rgb((bar_hsv[0], 0.0, 0.0))
            bar_rgb_2 = Color.hsv2rgb((bar_hsv[0], bar_hsv[1], 1.0))
            bar_end_rgb_2 = Color.hsv2rgb((bar_hsv[0], bar_hsv[1], 0.0))

        self._v_tag_radius = min(self.width(), self.height()) * self._args.v_tag_radius / 2
        self._v_tag_radius_2 = self._v_tag_radius ** 2

        re_wid = int(self.width() * (1 - self._args.wheel_ratio) / 2 * self._args.volum_ratio)

        if self._v_tag_radius * 3 < re_wid:
            re_wid = int(self._v_tag_radius * 3)

        bar_1_center = np.array(((self.width() - self._radius * 2) / 4, self.height() / 2), dtype=int)
        self._bar_1_box = (bar_1_center[0] - re_wid / 2, bar_1_center[1] - self.height() * self._args.volum_ratio / 2, re_wid, self.height() * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_1_box[0], self._bar_1_box[1], self._bar_1_box[0], self._bar_1_box[3])
        lgrad.setColorAt(1.0, QColor(*bar_rgb_1))
        lgrad.setColorAt(0.0, QColor(*bar_end_rgb_1))
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_1_box)

        self._cir_1_center = np.array((bar_1_center[0], self._bar_1_box[1] + self._bar_1_box[3] * bar_i), dtype=int)
        cir_1_box = get_outer_box(self._cir_1_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_1_box)

        bar_2_center = np.array((self.width() - (self.width() - self._radius * 2) / 4, self.height() / 2), dtype=int)
        self._bar_2_box = (bar_2_center[0] - re_wid / 2, bar_2_center[1] - self.height() * self._args.volum_ratio / 2, re_wid, self.height() * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_2_box[0], self._bar_2_box[1], self._bar_2_box[0], self._bar_2_box[3])
        lgrad.setColorAt(1.0, QColor(*bar_rgb_2))
        lgrad.setColorAt(0.0, QColor(*bar_end_rgb_2))
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_2_box)

        self._cir_2_center = np.array((bar_2_center[0], self._bar_2_box[1] + self._bar_2_box[3] * bar_i), dtype=int)
        cir_2_box = get_outer_box(self._cir_2_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_2_box)

        # color set tags.
        self._idx_seq = list(range(5))
        self._idx_seq = self._idx_seq[self._args.sys_activated_idx + 1: ] + self._idx_seq[: self._args.sys_activated_idx + 1]

        # lines.
        for idx in self._idx_seq:
            # main points.
            color_center = self._tag_centers[idx]

            # assit sequence. this code is reused in four places.
            assit_idx_seq = list(range(len(self._args.sys_grid_assitlocs[idx])))

            if idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                assit_idx_seq = assit_idx_seq[self._args.sys_activated_assit_idx + 1: ] + assit_idx_seq[: self._args.sys_activated_assit_idx + 1]

            # assit lines.
            for assit_idx in assit_idx_seq:
                # assit points.
                assit_center = self._assit_tag_centers[idx][assit_idx]

                # draw assit points.
                if idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx:
                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))

                else:
                    painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))

                painter.drawLine(QPoint(*color_center), QPoint(*assit_center))

            # draw main points.
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
            # main points.
            color_box = get_outer_box(self._tag_centers[idx], self._tag_radii)

            # assit sequence. this code is reused in four places.
            assit_idx_seq = list(range(len(self._args.sys_grid_assitlocs[idx])))
            if idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                assit_idx_seq = assit_idx_seq[self._args.sys_activated_assit_idx + 1: ] + assit_idx_seq[: self._args.sys_activated_assit_idx + 1]

            # assit circles.
            for assit_idx in assit_idx_seq:
                # assit points.
                assit_color = gen_assit_color(self._args.sys_color_set[idx], *self._args.sys_grid_assitlocs[idx][assit_idx][2:6])
                assit_box = get_outer_box(self._assit_tag_centers[idx][assit_idx], self._assit_tag_radii)
                assit_frame_color = self._args.positive_color if idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx else self._args.negative_color

                painter.setPen(QPen(QColor(*assit_frame_color), self._args.negative_wid))

                painter.setBrush(QColor(*assit_color.rgb))
                painter.drawEllipse(*assit_box)

                # relative (move-able) or ref (un-move-able) point tag. assit dot box.
                if not self._args.sys_grid_assitlocs[idx][assit_idx][5]:
                    dot_box = get_outer_box(self._assit_tag_centers[idx][assit_idx], self._args.negative_wid * 2 / 3)
                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QBrush(QColor(*assit_frame_color)))
                    painter.drawEllipse(*dot_box)

            # draw main points.
            if idx == self._args.sys_activated_idx:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            painter.setBrush(QColor(*self._args.sys_color_set[idx].rgb))
            painter.drawEllipse(*color_box)

        # outer circles.
        if self._outer_circles:
            frame_color = self._args.negative_color

            if self._outer_circles[0] == self._args.sys_activated_idx and (self._outer_circles[1] == self._args.sys_activated_assit_idx or self._outer_circles[1] == -1):
                frame_color = self._args.positive_color

            # circle 0.
            if self._outer_circles[5] == 0:
                painter.setPen(QPen(QColor(*frame_color, 160), self._args.negative_wid * 2/3))
                painter.setBrush(QBrush(QColor(*frame_color, 120)))

            else:
                painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                painter.setBrush(Qt.NoBrush)

            outer_circle = self._outer_circles[4][0]
            painter.drawEllipse(*outer_circle[0])

            for line in outer_circle[1:]:
                painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

            if len(self._outer_circles[4]) > 2:
                # circle 1.
                if self._outer_circles[5] == 1:
                    painter.setPen(QPen(QColor(*frame_color, 160), self._args.negative_wid * 2/3))
                    painter.setBrush(QBrush(QColor(*frame_color, 120)))

                else:
                    painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                    painter.setBrush(Qt.NoBrush)

                outer_circle = self._outer_circles[4][1]
                painter.drawEllipse(*outer_circle[0])

                for line in outer_circle[1:]:
                    painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

                # circle 2.
                if self._outer_circles[5] == 2:
                    painter.setPen(QPen(QColor(*frame_color, 160), self._args.negative_wid * 2/3))
                    painter.setBrush(QBrush(QColor(*frame_color, 120)))

                else:
                    painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                    painter.setBrush(Qt.NoBrush)

                outer_circle = self._outer_circles[4][2]
                painter.drawEllipse(*outer_circle[0])

                # relative (move-able) or ref (un-move-able) point tag. assit dot box.
                if self._outer_circles[1] < len(self._args.sys_grid_assitlocs[self._outer_circles[0]]) and self._args.sys_grid_assitlocs[self._outer_circles[0]][self._outer_circles[1]][5]:
                    line = outer_circle[1]
                    painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

                poly = QPolygon([QPoint(*i) for i in outer_circle[2]])
                painter.drawPolygon(poly)

        painter.end()

        self.ps_status_changed.emit(Color.sign(self._args.sys_color_set[self._args.sys_activated_idx].hsv))

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def keyPressEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if event.key() == Qt.Key_Shift:
            self._press_key = 1
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Control:
            self._press_key = 2
            event.accept()

        elif event.key() == Qt.Key_Alt:
            self._press_key = 4
            event.accept()

        else:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        self._press_key = 0
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        if self._args.sys_activated_assit_idx >= 0 and event.button() == Qt.LeftButton:
            point = (event.x(), event.y())

            if np.sum((point - self._assit_tag_centers[self._args.sys_activated_idx][self._args.sys_activated_assit_idx]) ** 2) < self._assit_tag_radii_2:
                self.change_assit_point(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])

                self.ps_color_changed.emit(True)
                event.accept()

            else:
                event.ignore()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        point = np.array((event.x(), event.y()))

        if self._press_key == 0 and self._outer_circles and self._outer_circles[5] > -1 and event.button() == Qt.LeftButton:
            sel_idx, sel_assit_idx, is_in_pt, is_in_assit_pt, circle_locations, sel_info_idx = self._outer_circles

            self._args.sys_activated_idx = sel_idx
            self._args.sys_activated_assit_idx = sel_assit_idx

            self.ps_index_changed.emit(True)

            # add a ref color.
            if is_in_pt or (is_in_assit_pt and sel_info_idx == 0):
                self._outer_circles = None

                # max assit len 30.
                ans = self.insert_assit_point(0.0, 0.0, 0.0)
                self._pressed_in_wheel = ans

            # del the ref color.
            elif is_in_assit_pt and sel_info_idx == 1:
                self._outer_circles = None
                self.delete_assit_point()

            # fix or unfix the ref color.
            else:
                self.change_assit_point(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])

            self.ps_color_changed.emit(True)
            event.accept()

        elif self._press_key == 1 and event.button() == Qt.LeftButton:
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
            self.setCursor(QCursor(Qt.ArrowCursor))

            event.accept()

        elif self._press_key == 2 and event.button() == Qt.LeftButton:
            if np.sum((point - self._center) ** 2) < self._radius_2:
                curr_color = self._args.sys_color_set[self._args.sys_activated_idx]

                # revise angle for ryb.
                assit_h = get_theta_center(self._center, point)

                if self._args.dep_wtp:
                    assit_h = Color.sys_ryb2rgb(assit_h)

                delta_point = [assit_h - curr_color.h, 0.0, 0.0]
                delta_point[self._args.dep_wtp_n] = np.linalg.norm(point - self._center) / self._radius - curr_color.hsv[self._args.dep_wtp_n]
                self.insert_assit_point(*delta_point)

                self._pressed_in_wheel = True
                self.ps_color_changed.emit(True)

                event.accept()

        elif event.button() in (Qt.LeftButton, Qt.RightButton):
            self._backup = self._args.sys_color_set.backup()

            already_accepted = False

            for idx in self._idx_seq[::-1]:
                if np.sum((point - self._tag_centers[idx]) ** 2) < self._tag_radii_2:
                    self._args.sys_activated_idx = idx
                    self._args.sys_activated_assit_idx = -1

                    self.ps_index_changed.emit(True)
                    already_accepted = True

                else:
                    for assit_idx in range(len(self._args.sys_grid_assitlocs[idx])):
                        if np.sum((point - self._assit_tag_centers[idx][assit_idx]) ** 2) < self._assit_tag_radii_2:
                            self._args.sys_activated_idx = idx
                            self._args.sys_activated_assit_idx = assit_idx

                            self.ps_index_changed.emit(True)
                            already_accepted = True

                            break

                if already_accepted:
                    event.accept()
                    # self.update() is completed by 
                    # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                    # same below.
                    break

            if event.button() == Qt.RightButton:
                event.ignore()

                return

            if already_accepted or (self._args.press_move and np.sum((point - self._center) ** 2) < self._radius_2):
                self._pressed_in_wheel = True

                event.accept()
                # self.update() is completed by 
                # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                # same below.

            elif (not already_accepted) and ((self._bar_1_box[0] < point[0] < self._bar_1_box[0] + self._bar_1_box[2] and self._bar_1_box[1] < point[1] < self._bar_1_box[1] + self._bar_1_box[3]) or np.sum((point - self._cir_1_center) ** 2) < self._v_tag_radius_2):
                if np.sum((point - self._cir_1_center) ** 2) < self._v_tag_radius_2 or self._args.press_move:
                    self._pressed_in_bar_1 = True

                    event.accept()

                else:
                    event.ignore()

            elif (not already_accepted) and ((self._bar_2_box[0] < point[0] < self._bar_2_box[0] + self._bar_2_box[2] and self._bar_2_box[1] < point[1] < self._bar_2_box[1] + self._bar_2_box[3]) or np.sum((point - self._cir_2_center) ** 2) < self._v_tag_radius_2):
                if np.sum((point - self._cir_2_center) ** 2) < self._v_tag_radius_2 or self._args.press_move:
                    self._pressed_in_bar_2 = True

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
            self._outer_circles = None

            if self._args.sys_activated_assit_idx < 0:
                color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                color.setti(np.linalg.norm(point - self._center) / self._radius, self._args.dep_wtp_s)
                color.h = get_theta_center(self._center, point)

                # gen relative angle for ryb system.
                if self._args.dep_wtp:
                    previous_color_set = self._args.sys_color_set.backup()

                    # revise angle for ryb.
                    color.h = Color.sys_ryb2rgb(color.h)

                    self._args.sys_color_set.recover(self._backup)
                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

                    for main_i in range(5):
                        for assit_i in range(len(self._args.sys_grid_assitlocs[main_i])):
                            if self._args.sys_grid_assitlocs[main_i][assit_i][5]:
                                relative_h = self._args.sys_grid_assitlocs[main_i][assit_i][2]
                                relative_h = previous_color_set[main_i].h + relative_h
                                relative_h = Color.sys_rgb2ryb(relative_h) - Color.sys_rgb2ryb(previous_color_set[main_i].h)
                                relative_h = Color.sys_ryb2rgb(Color.sys_rgb2ryb(self._args.sys_color_set[main_i].h) + relative_h)
                                relative_h = relative_h - self._args.sys_color_set[main_i].h
                                self._args.sys_grid_assitlocs[main_i][assit_i][2] = relative_h

                else:
                    self._args.sys_color_set.recover(self._backup)
                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

            else:
                assit_i = np.linalg.norm(point - self._center) / self._radius
                assit_h = get_theta_center(self._center, point)

                if self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]:
                    curr_color = self._args.sys_color_set[self._args.sys_activated_idx]

                    # revise angle for ryb.
                    if self._args.dep_wtp:
                        delta_h = Color.sys_ryb2rgb(assit_h) - curr_color.h

                    else:
                        delta_h = assit_h - curr_color.h

                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] = delta_h
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_n] = assit_i - curr_color.hsv[self._args.dep_wtp_n]

                else:
                    # revise angle for ryb.
                    if self._args.dep_wtp:
                        assit_h = Color.sys_ryb2rgb(assit_h)

                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] = assit_h
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_n] = assit_i

            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_1:
            self._outer_circles = None

            val = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]

            if self._args.sys_activated_assit_idx < 0:
                color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                color.setti(val, self._args.dep_wtp_rev_s)

                self._args.sys_color_set.recover(self._backup)
                self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

            else:
                if self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]:
                    curr_color = self._args.sys_color_set[self._args.sys_activated_idx]

                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_rev_n] = val - curr_color.hsv[self._args.dep_wtp_rev_n]

                else:
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_rev_n] = val

            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_2:
            self._outer_circles = None

            val = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]

            if self._args.sys_activated_assit_idx < 0:
                color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                color.setti(val, self._args.dep_wtp_rev_s)

                self._args.sys_color_set.recover(self._backup)
                self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

            else:
                if self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]:
                    curr_color = self._args.sys_color_set[self._args.sys_activated_idx]

                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_rev_n] = val - curr_color.hsv[self._args.dep_wtp_rev_n]

                else:
                    self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2 + self._args.dep_wtp_rev_n] = val

            self.ps_color_changed.emit(True)

            event.accept()

        else:
            # outer circles.
            if self._args.show_info_pts[0] and self._press_key == 0 and (not self._drop_file):
                pts = self._tag_centers
                major = self._args.show_info_pts[0] in (1, 3)
                assit_pts = self._assit_tag_centers
                minor = self._args.show_info_pts[0] > 1
                last_count = bool(self._outer_circles)
                self._outer_circles = get_outer_circles(point, self._args.sys_activated_idx, pts, assit_pts, self._tag_radii * 1.2, self._assit_tag_radii * 1.2, self._assit_tag_radii, self._outer_circles, major=major, minor=minor)

                if self._outer_circles or last_count:
                    self.update()

            else:
                self._outer_circles = None

            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

        if self._pressed_in_wheel or self._pressed_in_bar_1 or self._pressed_in_bar_2:
            self._pressed_in_wheel = False
            self._pressed_in_bar_1 = False
            self._pressed_in_bar_2 = False

        if event.button() == Qt.LeftButton:
            self.ps_history_backup.emit(True)

        event.ignore()

    def dragEnterEvent(self, event):
        """
        Sync to board.py. May exist difference.
        """

        if self._outer_circles:
            self._outer_circles = None
            self.update()

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

        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if self._drop_file:
            self.ps_dropped.emit((self._drop_file, False))
            self._drop_file = None

            event.accept()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def init_pt_centers_and_radii(self):
        # color set tags.
        self._center = np.array((self.width() / 2.0, self.height() / 2.0), dtype=int)
        self._radius = int(min(self.width(), self.height()) * self._args.wheel_ratio / 2)
        self._radius_2 = self._radius ** 2

        self._tag_centers = [None] * 5
        self._tag_radii = int(min(self.width(), self.height()) * self._args.s_tag_radius / 2)
        self._tag_radii_2 = self._tag_radii ** 2

        self._assit_tag_centers = [[None] * len(self._args.sys_grid_assitlocs[i]) for i in range(5)]
        self._assit_tag_radii = self._tag_radii * 2 / 3
        self._assit_tag_radii_2 = self._assit_tag_radii ** 2

        # lines.
        for idx in range(5):
            # revise angle for ryb.
            angle = self._args.sys_color_set[idx].h

            if self._args.dep_wtp:
                angle = Color.sys_rgb2ryb(angle)

            # main points.
            color_center = np.array([self._args.sys_color_set[idx].hsv[self._args.dep_wtp_n] * self._radius, 0], dtype=int) + self._center
            color_center = rotate_point_center(self._center, color_center, angle)
            self._tag_centers[idx] = color_center.astype(int)

            # assit lines.
            for assit_idx in range(len(self._args.sys_grid_assitlocs[idx])):
                _, _, assit_h, assit_s, assit_v, assit_relativity = self._args.sys_grid_assitlocs[idx][assit_idx]

                # revise angle for ryb.
                angle = self._args.sys_color_set[idx].h
                assit_angle = assit_h
                sum_angle = angle + assit_angle

                if self._args.dep_wtp:
                    sum_angle = Color.sys_rgb2ryb(sum_angle)
                    assit_angle = Color.sys_rgb2ryb(assit_angle)

                """
                # revise angle for ryb.
                angle = self._args.sys_color_set[idx].h
                assit_angle = assit_h

                if self._args.dep_wtp:
                    angle = Color.sys_rgb2ryb(angle)
                    assit_angle = Color.sys_rgb2ryb(assit_angle)

                sum_angle = angle + assit_angle
                """

                # assit points.
                if assit_relativity:
                    assit_center = np.array([(self._args.sys_color_set[idx].hsv[self._args.dep_wtp_n] + (assit_s, assit_v)[self._args.dep_wtp_n - 1]) * self._radius, 0], dtype=int) + self._center
                    assit_center = rotate_point_center(self._center, assit_center, sum_angle)

                else:
                    assit_center = np.array([(assit_s, assit_v)[self._args.dep_wtp_n - 1] * self._radius, 0], dtype=int) + self._center
                    assit_center = rotate_point_center(self._center, assit_center, assit_angle)

                self._assit_tag_centers[idx][assit_idx] = assit_center.astype(int)

    def reset_assit_point(self):
        """
        Delete all assit points.
        """

        if not self.isVisible():
            return

        self._args.sys_grid_assitlocs = [[], [], [], [], []]
        self._args.sys_assit_color_locs = [[], [], [], [], []]
        self._args.sys_activated_assit_idx = -1

        self.ps_color_changed.emit(True)
        self.update()

    def insert_assit_point(self, delta_h, delta_s, delta_v):
        """
        Insert (Append) an assitant point.

        Args:
            delta_h: increment of h relative to the h of the activated-idx color.
            delta_s: increment of s relative to the s of the activated-idx color.
            delta_v: increment of v relative to the v of the activated-idx color.
        """

        if not self.isVisible():
            return False

        # max assit len 30.
        assit_len = len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx])

        if assit_len > 30:
            return False

        loc_a, loc_b = 0.1, 0.1

        self._args.sys_activated_assit_idx = assit_len
        self._args.sys_grid_assitlocs[self._args.sys_activated_idx].append([loc_a, loc_b, delta_h, delta_s, delta_v, True])
        self._args.sys_assit_color_locs[self._args.sys_activated_idx].append(None)

        self.ps_color_changed.emit(True)
        self.update()

        return True

    def change_assit_point(self, relativity):
        """
        Change the relativity of assit point.
        """

        if len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]) > self._args.sys_activated_assit_idx >= 0:
            if self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5] == bool(relativity):
                return

            if bool(relativity):
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] - self._args.sys_color_set[self._args.sys_activated_idx].h
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][3] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][3] - self._args.sys_color_set[self._args.sys_activated_idx].s
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][4] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][4] - self._args.sys_color_set[self._args.sys_activated_idx].v

            else:
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2] + self._args.sys_color_set[self._args.sys_activated_idx].h
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][3] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][3] + self._args.sys_color_set[self._args.sys_activated_idx].s
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][4] = self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][4] + self._args.sys_color_set[self._args.sys_activated_idx].v

            self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5] = bool(relativity)

            self.ps_color_changed.emit(True)
            self.update()

    def delete_assit_point(self):
        """
        Delete the last assitant point.
        """

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

    def confirm_delete_assit_point(self):
        """
        Act delete_assit_point with confirmation.
        """

        if not self.isVisible():
            return

        self.prompt(self._operation_warns[3], self.delete_assit_point)

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

        #   _translate("Wheel", "Undo"), # 0
        #   _translate("Wheel", "Redo"), # 1
        self._action_undo = QAction(self)
        self._action_undo.triggered.connect(lambda: self.ps_undo.emit(True))
        self._menu.addAction(self._action_undo)

        self._action_redo = QAction(self)
        self._action_redo.triggered.connect(lambda: self.ps_undo.emit(False))
        self._menu.addAction(self._action_redo)

        #   _translate("Board", "Reset"), # 10
        self._action_reset = QAction(self)
        self._action_reset.triggered.connect(self.reset_assit_point)
        self._menu.addAction(self._action_reset)

        #   _translate("Wheel", "Paste"), # 5
        self._action_paste = QAction(self)
        self._action_paste.triggered.connect(self.clipboard_in)
        self._menu.addAction(self._action_paste)

        #   _translate("Wheel", "Copy RGB"), # 2
        #   _translate("Wheel", "Copy HSV"), # 3
        #   _translate("Wheel", "Copy Hex Code"), # 4
        self._action_copy_rgb = QAction(self)
        self._action_copy_rgb.triggered.connect(self.clipboard_all("rgb"))
        self._menu.addAction(self._action_copy_rgb)

        self._action_copy_hsv = QAction(self)
        self._action_copy_hsv.triggered.connect(self.clipboard_all("hsv"))
        self._menu.addAction(self._action_copy_hsv)

        self._action_copy_hec = QAction(self)
        self._action_copy_hec.triggered.connect(self.clipboard_all("hec"))
        self._menu.addAction(self._action_copy_hec)

        #   _translate("Wheel", "Insert Ref Point (Ctrl+MV)"), # 6
        self._action_insert = QAction(self)
        self._action_insert.triggered.connect(lambda: self.insert_assit_point((15 * np.random.random() + 15) * np.random.choice([1,-1]), 0.3 * np.random.random() - 0.15, 0))
        self._menu.addAction(self._action_insert)

        #   _translate("Wheel", "Delete Ref Point"), # 7
        self._action_delete = QAction(self)
        self._action_delete.triggered.connect(self.delete_assit_point)
        self._menu.addAction(self._action_delete)

        #   _translate("Wheel", "Fix Ref Point (DK)"), # 8
        #   _translate("Wheel", "Un-Fix Ref Point (DK)"), # 9
        self._action_fix_pt = QAction(self)
        self._action_fix_pt.triggered.connect(lambda: self.change_assit_point(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]) if self._args.sys_activated_idx >= 0 else None)
        self._menu.addAction(self._action_fix_pt)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        self.update_action_text()

        # normal actions delete.
        if self._args.sys_activated_assit_idx >= 0:
            self._action_delete.setVisible(True)
            self._action_fix_pt.setVisible(True)

        else:
            self._action_delete.setVisible(False)
            self._action_fix_pt.setVisible(False)

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

            shortcut.activated.connect(self.delete_assit_point)

        for skey in self._args.shortcut_keymaps[40]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.confirm_delete_assit_point)

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

        for skey in self._args.shortcut_keymaps[38]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(lambda: self.insert_assit_point((15 * np.random.random() + 15) * np.random.choice([1,-1]), 0.3 * np.random.random() - 0.15, 0))

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_action_text(self):
        #   _translate("Wheel", "Undo"), # 0
        #   _translate("Wheel", "Redo"), # 1
        self._action_undo.setText(self._action_descs[0])
        self._action_redo.setText(self._action_descs[1])

        #   _translate("Board", "Reset"), # 10
        self._action_reset.setText(self._action_descs[10])

        #   _translate("Wheel", "Copy RGB"), # 2
        #   _translate("Wheel", "Copy HSV"), # 3
        #   _translate("Wheel", "Copy Hex Code"), # 4
        self._action_copy_rgb.setText(self._action_descs[2])
        self._action_copy_hsv.setText(self._action_descs[3])
        self._action_copy_hec.setText(self._action_descs[4])

        #   _translate("Wheel", "Paste"), # 5
        self._action_paste.setText(self._action_descs[5])

        #   _translate("Wheel", "Insert Ref Point (Ctrl+MV)"), # 6
        self._action_insert.setText(self._action_descs[6])

        #   _translate("Wheel", "Delete Ref Point"), # 7
        self._action_delete.setText(self._action_descs[7])

        #   _translate("Wheel", "Fix Ref Point (DK)"), # 8
        #   _translate("Wheel", "Un-Fix Ref Point (DK)"), # 9
        if self._args.sys_activated_assit_idx >= 0 and self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5]:
            self._action_fix_pt.setText(self._action_descs[8])

        else:
            self._action_fix_pt.setText(self._action_descs[9])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Wheel", "Undo"), # 0
            _translate("Wheel", "Redo"), # 1
            _translate("Board", "Copy RGB"), # 2
            _translate("Board", "Copy HSV"), # 3
            _translate("Board", "Copy Hex Code"), # 4
            _translate("Wheel", "Paste"), # 5
            _translate("Board", "Insert Ref Point (Ctrl+MV)"), # 6
            _translate("Board", "Delete Ref Point"), # 7
            _translate("Board", "Fix Ref Point (DK)"), # 8
            _translate("Board", "Un-Fix Ref Point (DK)"), # 9
            _translate("Wheel", "Reset"), # 10
        )

        self._operation_warns = (
            _translate("Info", "Warning"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
            _translate("Info", "The selected assistant point will be removed from board."),
        )
