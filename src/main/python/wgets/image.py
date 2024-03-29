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
import numpy as np
from PIL import ImageQt
from PIL import Image as PImage
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QMessageBox, QFileDialog, QShortcut, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QRect, QPoint, QMimeData
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QCursor, QKeySequence, QPolygon
from cguis.resource import view_rc
from clibs.image3c import Image3C
from ricore.color import Color, CTP
from ricore.transpt import get_outer_box, get_outer_circles
from ricore.grid import gen_assit_color, gen_assit_args


class Image(QWidget):
    """
    Image object based on QWidget. Init a image pannel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_image_changed = pyqtSignal(bool)
    ps_status_changed = pyqtSignal(tuple)
    ps_recover_channel = pyqtSignal(bool)
    ps_modify_rule = pyqtSignal(bool)
    ps_assit_pt_changed = pyqtSignal(bool)
    ps_history_backup = pyqtSignal(bool)
    ps_undo = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init Image pannel.
        """

        super().__init__(wget)
        wget.setProperty("class", "WorkArea")
        self._args = args
        self._categories = set()
        self._start_pt = None
        self._enhance_lock = False
        self._home_image = False
        self._croping_img = False
        self._croping_img_loc = None
        self._locating_img = False
        self._locating_img_loc = None
        self._resized_img_pos = None
        self._locating_colors = False
        self._connected_keymaps = {}
        self.init_key()
        self._func_tr_()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)
        self._tip_label = QLabel(self)
        self._tip_label.setWordWrap(True)
        self._loading_bar = QProgressBar(self)
        self._loading_bar.setTextVisible(False)
        self._loading_bar.setMaximum(100)
        self._loading_bar.setValue(0)
        self._ico = None
        self.init_icon()
        self._ico_label = QLabel(self)
        self.image3c = Image3C(self._args.global_temp_dir, (self._args.d_error, self._args.d_info, self._args.d_action))
        self.image3c.ps_describe.connect(self.update_loading_label)
        self.image3c.ps_proceses.connect(self.update_loading_bar)
        self.image3c.ps_finished.connect(self.loading_finished)
        self.image3c.ps_enhanced.connect(self.enhance_finished)
        self.image3c.ps_extracts.connect(self.extract_finished)
        self._outer_circles = None
        self.create_menu()
        self.update_action_text()

    def paintEvent(self, event):
        if False: # self._args.sys_activated_assit_idx > len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]):
            self._args.sys_activated_assit_idx = -1
            self.ps_color_changed()

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if not self.image3c.img_data:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.show()
            alpha = 255 if self._args.style_id < 5 else 120
            painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid, Qt.PenStyle(Qt.DashLine)))
            painter.setBrush(QColor(*self._args.negative_color, alpha))
            self._tip_box = (self.width() * 0.2, self.height() * 0.2, self.width() * 0.6, self.height() * 0.6)
            radius = int(min(self.width() * 0.1, self.height() * 0.1))
            painter.drawRoundedRect(*self._tip_box, radius, radius)
            self._tip_label.setGeometry(QRect(*self._tip_box))
            self._tip_label.setText(self._open_descs[0])
            self._tip_label.setAlignment(Qt.AlignCenter)

        elif self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self._loading_bar.show()
            self._ico_label.show()
            self._tip_label.show()
            bar_wid = int(self.width() * 0.8)
            bar_hig = int(self.height() * 0.1)
            self._loading_bar.setGeometry((self.width() - bar_wid) / 2, self.height() * 0.88, bar_wid, bar_hig)
            self._tip_label.setGeometry((self.width() - bar_wid) / 2, self.height() * 0.76, bar_wid, bar_hig)
            img_wid = int(min(self.width() * 0.8, self.height() * 0.6))
            resized_pix = self._ico.scaled(img_wid * self.devicePixelRatioF(), img_wid * self.devicePixelRatioF(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            resized_pix = QPixmap.fromImage(resized_pix)
            resized_pix.setDevicePixelRatio(self.devicePixelRatioF())
            self._ico_label.setPixmap(resized_pix)
            self._ico_label.setGeometry((self.width() - img_wid) / 2, (self.height() * 0.76 - img_wid) / 2, img_wid, img_wid)

        else:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.hide()

            if not self.image3c.display:
                self.image3c.load_image(self._args.sys_category, self._args.sys_channel)

            else:
                if not isinstance(self._resized_img_pos, np.ndarray):
                    self.home()
                    self._home_image = False

                self._resized_img_pos[0] = int(self.width() - 2 if self._resized_img_pos[0] > self.width() - 2 else self._resized_img_pos[0])
                self._resized_img_pos[1] = int(self.height() - 2 if self._resized_img_pos[1] > self.height() - 2 else self._resized_img_pos[1])

                if self._resized_img_pos[0] < 2 - self._resized_img_pos[2]:
                    self._resized_img_pos[0] = int(2 - self._resized_img_pos[2])

                if self._resized_img_pos[1] < 2 - self._resized_img_pos[3]:
                    self._resized_img_pos[1] = int(2 - self._resized_img_pos[3])

                resized_pix = QPixmap.fromImage(self.image3c.display)
                resized_pix.setDevicePixelRatio(self.image3c.display.width() / self._resized_img_pos[2])
                painter.drawPixmap(*self._resized_img_pos, resized_pix)
                idx_seq = list(range(5))
                idx_seq = idx_seq[self._args.sys_activated_idx + 1: ] + idx_seq[: self._args.sys_activated_idx + 1]

                for idx in idx_seq:
                    if self._args.sys_color_locs[idx]:
                        pt_xy = np.array((self._args.sys_color_locs[idx][0] * self._resized_img_pos[2] + self._resized_img_pos[0], self._args.sys_color_locs[idx][1] * self._resized_img_pos[3] + self._resized_img_pos[1]), dtype=int)
                        pt_rgb = self._args.sys_color_set[idx].rgb

                    else:
                        continue

                    assit_idx_seq = list(range(len(self._args.sys_grid_assitlocs[idx])))

                    if idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                        assit_idx_seq = assit_idx_seq[self._args.sys_activated_assit_idx + 1: ] + assit_idx_seq[: self._args.sys_activated_assit_idx + 1]

                    for assit_idx in assit_idx_seq:
                        if self._args.sys_assit_color_locs[idx][assit_idx]:
                            assit_pt_xy = np.array((self._args.sys_assit_color_locs[idx][assit_idx][0] * self._resized_img_pos[2] + self._resized_img_pos[0], self._args.sys_assit_color_locs[idx][assit_idx][1] * self._resized_img_pos[3] + self._resized_img_pos[1]), dtype=int)
                            assit_pt_rgb = gen_assit_color(self._args.sys_color_set[idx], *self._args.sys_grid_assitlocs[idx][assit_idx][2:6]).rgb
                            pt_box = get_outer_box(assit_pt_xy, self._args.circle_dist)
                            assit_frame_color = (0, 0, 0)

                            if self._press_key == 3:
                                painter.setBrush(QBrush(Qt.NoBrush))

                            else:
                                if idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx:
                                    assit_frame_color = self._args.positive_color

                                else:
                                    assit_frame_color = self._args.negative_color

                                painter.setBrush(QColor(*assit_pt_rgb))
                            painter.setPen(QPen(QColor(*assit_frame_color), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                            painter.drawLine(QPoint(*pt_xy), QPoint(*assit_pt_xy))
                            painter.setPen(QPen(QColor(*assit_frame_color), self._args.negative_wid))
                            painter.drawEllipse(*pt_box)

                            if not self._args.sys_grid_assitlocs[idx][assit_idx][5]:
                                dot_box = get_outer_box(assit_pt_xy, self._args.negative_wid * 2 / 3)
                                painter.setPen(QPen(Qt.NoPen))
                                painter.setBrush(QBrush(QColor(*assit_frame_color)))
                                painter.drawEllipse(*dot_box)

                    if self._args.sys_color_locs[idx]:
                        pt_xy = np.array((self._args.sys_color_locs[idx][0] * self._resized_img_pos[2] + self._resized_img_pos[0], self._args.sys_color_locs[idx][1] * self._resized_img_pos[3] + self._resized_img_pos[1]), dtype=int)
                        pt_rgb = self._args.sys_color_set[idx].rgb
                        pt_box = get_outer_box(pt_xy, self._args.dep_circle_dist_wid)

                        if self._press_key == 3:
                            painter.setPen(QPen(Qt.white, self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                            painter.setBrush(QBrush(Qt.NoBrush))

                        else:
                            if idx == self._args.sys_activated_idx:
                                painter.setPen(QPen(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2]), self._args.positive_wid))
                                painter.setBrush(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 128))

                            else:
                                painter.setPen(QPen(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 128), self._args.negative_wid, Qt.PenStyle(Qt.DashLine)))
                                painter.setBrush(QColor(255 - pt_rgb[0], 255 - pt_rgb[1], 255 - pt_rgb[2], 64))

                        painter.drawEllipse(*pt_box)
                        pt_box = get_outer_box(pt_xy, self._args.circle_dist)

                        if self._press_key == 3:
                            painter.setPen(QPen(Qt.black, self._args.negative_wid))
                            painter.setBrush(QBrush(Qt.NoBrush))

                        else:
                            if idx == self._args.sys_activated_idx:
                                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                            else:
                                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

                            painter.setBrush(QColor(*pt_rgb))
                        painter.drawEllipse(*pt_box)

                if isinstance(self._croping_img_loc, tuple):
                    sted_croping = self.get_sorted_croping()
                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))
                    self.draw_twopt_rect(painter, 0, 0, sted_croping[0], self.height())
                    self.draw_twopt_rect(painter, sted_croping[2], 0, self.width(), self.height())
                    self.draw_twopt_rect(painter, sted_croping[0], 0, sted_croping[2], sted_croping[1])
                    self.draw_twopt_rect(painter, sted_croping[0], sted_croping[3], sted_croping[2], self.height())
                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))
                    painter.drawLine(QPoint(sted_croping[0] + self.x(), 0), QPoint(sted_croping[0] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_croping[1] + self.y()), QPoint(self.width(), sted_croping[1] + self.y()))
                    painter.drawLine(QPoint(sted_croping[2] + self.x(), 0), QPoint(sted_croping[2] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_croping[3] + self.y()), QPoint(self.width(), sted_croping[3] + self.y()))
                    self.ps_status_changed.emit((self.image3c.rgb_data.shape[1], self.image3c.rgb_data.shape[0], "{:.1f}".format((self._croping_img_loc[2] - self._resized_img_pos[0]) * 100 / self._resized_img_pos[2]), "{:.1f}".format((self._croping_img_loc[3] - self._resized_img_pos[1]) * 100 / self._resized_img_pos[3])))

                elif isinstance(self._locating_img_loc, tuple):
                    sted_locating = self.get_sorted_locating()
                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))
                    painter.drawRect(0, 0, self.width(), self.height())
                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))
                    painter.drawLine(QPoint(sted_locating[0] + self.x(), 0), QPoint(sted_locating[0] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_locating[1] + self.y()), QPoint(self.width(), sted_locating[1] + self.y()))
                    self.ps_status_changed.emit((self.image3c.rgb_data.shape[1], self.image3c.rgb_data.shape[0], "{:.1f}".format((self._locating_img_loc[0] - self._resized_img_pos[0]) * 100 / self._resized_img_pos[2]), "{:.1f}".format((self._locating_img_loc[1] - self._resized_img_pos[1]) * 100 / self._resized_img_pos[3])))

                elif self._croping_img or self._locating_img:
                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))
                    painter.drawRect(0, 0, self.width(), self.height())

                elif self._args.sys_activated_assit_idx >= 0 and self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx]:
                    curr_color = gen_assit_color(self._args.sys_color_set[self._args.sys_activated_idx], *self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2:6])
                    curr_loc = self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx]
                    self.ps_status_changed.emit((self.image3c.rgb_data.shape[1], self.image3c.rgb_data.shape[0], "{:.1f}".format(curr_loc[0] * 100), "{:.1f}".format(curr_loc[1] * 100), Color.sign(curr_color.hsv)))

                elif self._args.sys_color_locs[self._args.sys_activated_idx]:
                    self.ps_status_changed.emit((self.image3c.rgb_data.shape[1], self.image3c.rgb_data.shape[0], "{:.1f}".format(self._args.sys_color_locs[self._args.sys_activated_idx][0] * 100), "{:.1f}".format(self._args.sys_color_locs[self._args.sys_activated_idx][1] * 100), Color.sign(self._args.sys_color_set[self._args.sys_activated_idx].hsv)))

                else:
                    self.ps_status_changed.emit((self.image3c.rgb_data.shape[1], self.image3c.rgb_data.shape[0]))

            if self._outer_circles:
                frame_color = self._args.negative_color

                if self._outer_circles[0] == self._args.sys_activated_idx and (self._outer_circles[1] == self._args.sys_activated_assit_idx or self._outer_circles[1] == -1):
                    frame_color = self._args.positive_color

                if self._outer_circles[5] == 0:
                    painter.setPen(QPen(QColor(*frame_color, ), self._args.negative_wid * 2/3))
                    painter.setBrush(QBrush(QColor(*frame_color, 120)))

                else:
                    painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                    painter.setBrush(Qt.NoBrush)

                outer_circle = self._outer_circles[4][0]
                painter.drawEllipse(*outer_circle[0])

                for line in outer_circle[1:]:
                    painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

                if len(self._outer_circles[4]) > 2:
                    if self._outer_circles[5] == 1:
                        painter.setPen(QPen(QColor(*frame_color, ), self._args.negative_wid * 2/3))
                        painter.setBrush(QBrush(QColor(*frame_color, 120)))

                    else:
                        painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                        painter.setBrush(Qt.NoBrush)

                    outer_circle = self._outer_circles[4][1]
                    painter.drawEllipse(*outer_circle[0])

                    for line in outer_circle[1:]:
                        painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

                    if self._outer_circles[5] == 2:
                        painter.setPen(QPen(QColor(*frame_color, ), self._args.negative_wid * 2/3))
                        painter.setBrush(QBrush(QColor(*frame_color, 120)))

                    else:
                        painter.setPen(QPen(QColor(*frame_color, 100), self._args.negative_wid * 2/3))
                        painter.setBrush(Qt.NoBrush)

                    outer_circle = self._outer_circles[4][2]
                    painter.drawEllipse(*outer_circle[0])

                    if not (self._outer_circles[1] < len(self._args.sys_grid_assitlocs[self._outer_circles[0]]) and self._args.sys_grid_assitlocs[self._outer_circles[0]][self._outer_circles[1]][5]):
                        line = outer_circle[1]
                        painter.drawLine(QPoint(*line[0]), QPoint(*line[1]))

                    poly = QPolygon([QPoint(*i) for i in outer_circle[2]])
                    painter.drawPolygon(poly)

        painter.end()

    def keyPressEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if event.key() == Qt.Key_Space and self.image3c.display:
            self._press_key = 3
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            event.accept()
            self.update()

        elif event.key() == Qt.Key_Control and self.image3c.display:
            self._press_key = 2
            event.accept()

        else:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if self._press_key:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()
            self.update()

    def mouseDoubleClickEvent(self, event):
        if not self.image3c.img_data and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._tip_box[0] < p_x < (self._tip_box[0] + self._tip_box[2]) and self._tip_box[1] < p_y < (self._tip_box[1] + self._tip_box[3]):
                self.open_image_dialog()
                event.accept()
                self.update()

        elif self.image3c.img_data and event.button() == Qt.LeftButton and self._args.sys_activated_assit_idx >= 0:
            point = (event.x(), event.y())
            assit_color_loc = self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx]

            if assit_color_loc:
                assit_pt_xy = np.array((assit_color_loc[0] * self._resized_img_pos[2] + self._resized_img_pos[0], assit_color_loc[1] * self._resized_img_pos[3] + self._resized_img_pos[1]), dtype=int)

                if np.sum((point - assit_pt_xy) ** 2) < self._args.dep_circle_dist_2:
                    self.ps_assit_pt_changed.emit(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])
                    self.ps_color_changed.emit(True)
                    event.accept()

                else:
                    event.ignore()

            else:
                event.ignore()

        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        try:
            image = event.mimeData().urls()[0].toLocalFile()

        except Exception as err:
            event.ignore()
            return

        if image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff", "webp"):
            self._drop_image = image
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if self._drop_image:
            self.open_image(self._drop_image)
            self._drop_image = None
            event.accept()

        else:
            event.ignore()

    def wheelEvent(self, event):
        if self._outer_circles:
            self._outer_circles = None
            self.update()

        if self.image3c.display:
            point = (event.x(), event.y())
            ratio = (event.angleDelta() / 120).y()

            if ratio:
                ratio = ratio * self._args.zoom_step if ratio > 0 else -1 * ratio / self._args.zoom_step

            else:
                ratio = 1

            self.zoom(ratio, point)
            event.accept()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        if self.image3c.display and isinstance(self._resized_img_pos, np.ndarray):
            if event.button() == Qt.MidButton or (self._press_key == 3 and event.button() == Qt.LeftButton):
                if event.button() == Qt.MidButton:
                    self.setCursor(QCursor(Qt.ClosedHandCursor))

                self._start_pt = (event.x(), event.y())
                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self._croping_img:
                if isinstance(self._croping_img_loc, tuple) and self._croping_img == 1:
                    self._croping_img = 2
                    self._croping_img_loc = (
                        self._croping_img_loc[0],
                        self._croping_img_loc[1],
                        event.x() - self.x(),
                        event.y() - self.y(),
                    )

                else:
                    self._croping_img = 1
                    self._croping_img_loc = (
                        event.x() - self.x(),
                        event.y() - self.y(),
                        event.x() - self.x(),
                        event.y() - self.y(),
                    )

                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self._locating_img:
                self._locating_img = 2
                self._locating_img_loc = (
                    event.x() - self.x(),
                    event.y() - self.y(),
                )

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton and (self._croping_img or self._locating_img):
                self._croping_img = False
                self._croping_img_loc = None
                self._locating_img = False
                self._locating_img_loc = None
                event.accept()
                self.update()

            elif self._press_key in (0, 2) and event.button() == Qt.LeftButton and not (self._croping_img or self._locating_img):
                insert_assit_pt_by_info_tag = False

                if self._press_key == 0 and self._outer_circles and self._outer_circles[5] > -1 and event.button() == Qt.LeftButton:
                    sel_idx, sel_assit_idx, is_in_pt, is_in_assit_pt, circle_locations, sel_info_idx = self._outer_circles
                    self._args.sys_activated_idx = sel_idx
                    self._args.sys_activated_assit_idx = sel_assit_idx

                    if is_in_pt or (is_in_assit_pt and sel_info_idx == 0):
                        insert_assit_pt_by_info_tag = True

                    elif is_in_assit_pt and sel_info_idx == 1:
                        self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx] = None
                        event.accept()
                        return

                    else:
                        self.ps_assit_pt_changed.emit(not self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])
                        self.ps_color_changed.emit(True)

                if insert_assit_pt_by_info_tag or (self._press_key == 2 and self._args.sys_color_locs[self._args.sys_activated_idx]):
                    if self._args.sys_activated_assit_idx < 0:
                        self._args.sys_activated_assit_idx = 0

                    already_selected_assit = False

                    for ci in range(len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]) - self._args.sys_activated_assit_idx):
                        if self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx] == None:
                            already_selected_assit = True
                            break

                        self._args.sys_activated_assit_idx += 1
                    assit_len = len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx])

                    if not already_selected_assit and assit_len < 31:
                        self._args.sys_activated_assit_idx = assit_len
                        self._args.sys_grid_assitlocs[self._args.sys_activated_idx].append([0.1, 0.1, 15, 0, 0, True])
                        self._args.sys_assit_color_locs[self._args.sys_activated_idx].append(None)

                    self.ps_color_changed.emit(True)
                point = np.array((event.x(), event.y()))
                already_accept = False

                for idx in range(5):
                    if self._args.sys_color_locs[idx] and np.sum((point - self._args.sys_color_locs[idx] * self._resized_img_pos[2:] - self._resized_img_pos[:2]) ** 2) < self._args.dep_circle_dist_wid_2:
                        self._args.sys_activated_idx = idx
                        self._args.sys_activated_assit_idx = -1
                        already_accept = True

                    else:
                        curr_locs = self._args.sys_assit_color_locs[idx]

                        for assit_idx in range(len(curr_locs)):
                            if curr_locs[assit_idx] and np.sum((point - curr_locs[assit_idx] * self._resized_img_pos[2:] - self._resized_img_pos[:2]) ** 2) < self._args.dep_circle_dist_wid_2 * 4 / 9:
                                self._args.sys_activated_idx = idx
                                self._args.sys_activated_assit_idx = assit_idx
                                already_accept = True
                                break

                    if already_accept:
                        break

                if self._args.sys_activated_assit_idx >= 0 and (not self._args.sys_color_locs[self._args.sys_activated_idx]):
                    self._args.sys_activated_assit_idx = -1

                select_main_color = not self._args.sys_color_locs[self._args.sys_activated_idx]
                select_assit_colors = self._args.sys_activated_assit_idx >= 0 and (not self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx])

                if event.button() == Qt.LeftButton and (((self._args.press_move or select_main_color or select_assit_colors) and self._resized_img_pos[0] < point[0] < self._resized_img_pos[0] + self._resized_img_pos[2] and self._resized_img_pos[1] < point[1] < self._resized_img_pos[1] + self._resized_img_pos[3]) or already_accept):
                    self._locating_colors = True
                    event.accept()
                    self.update()

                else:
                    event.ignore()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        point = np.array((event.x(), event.y()))

        if isinstance(self._start_pt, np.ndarray) or self._start_pt:
            self._outer_circles = None

            if self._args.rev_direct:
                self.move(self._start_pt[0] - point[0], self._start_pt[1] - point[1])

            else:
                self.move(point[0] - self._start_pt[0], point[1] - self._start_pt[1])

            self._start_pt = point
            event.accept()

        elif self._croping_img == 1 and isinstance(self._croping_img_loc, tuple):
            self._outer_circles = None
            self._croping_img_loc = (
                self._croping_img_loc[0],
                self._croping_img_loc[1],
                event.x() - self.x(),
                event.y() - self.y(),
            )

            event.accept()
            self.update()

        elif self._locating_img in (1, 2):
            self._outer_circles = None
            self._locating_img_loc = (
                event.x() - self.x(),
                event.y() - self.y(),
            )

            event.accept()
            self.update()

        elif self._locating_colors:
            self._outer_circles = None
            loc = [(point[0] - self._resized_img_pos[0]) / self._resized_img_pos[2], (point[1] - self._resized_img_pos[1]) / self._resized_img_pos[3]]
            loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
            loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
            loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
            loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

            if self._args.sys_activated_assit_idx < 0:
                self._args.sys_color_locs[self._args.sys_activated_idx] = tuple(loc)

            else:
                self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx] = tuple(loc)

            self.modify_color_loc()
            event.accept()
            self.update()

        else:
            if self._args.show_info_pts[1] and self._press_key == 0 and (not self._drop_image) and isinstance(self._resized_img_pos, np.ndarray):
                color_locs = np.array([i * self._resized_img_pos[2:4] + self._resized_img_pos[0:2] if isinstance(i, (tuple, list, np.ndarray)) else (-100, -100) for i in self._args.sys_color_locs], dtype=int)
                major = self._args.show_info_pts[1] in (1, 3)
                assit_color_locs = [np.array([j[:2] * self._resized_img_pos[2:4] + self._resized_img_pos[0:2] if isinstance(j, (tuple, list, np.ndarray)) else (-100, -100) for j in i], dtype=int) for i in self._args.sys_assit_color_locs]
                minor = self._args.show_info_pts[1] > 1
                last_count = bool(self._outer_circles)
                self._outer_circles = get_outer_circles(point, self._args.sys_activated_idx, color_locs, assit_color_locs, (self._args.dep_circle_dist_wid) * 1.2, self._args.circle_dist * 1.2, self._args.circle_dist, self._outer_circles, major=major, minor=minor)

                if self._outer_circles or last_count:
                    self.update()

            else:
                self._outer_circles = None

            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._locating_colors = False
        self._start_pt = None

        if self._locating_img == 2:
            self._locating_img = 3

        if event.button() == Qt.LeftButton:
            self.ps_history_backup.emit(True)

        event.ignore()

    def init_key(self):
        self._press_key = 0
        self._drop_image = None

    def init_icon(self):
        self._ico = QImage(":/images/images/icon_trans_1024.png")

    def draw_twopt_rect(self, painter, x0, y0, x1, y1):
        """
        Draw rect by two points.
        """

        if x0 == x1 or y0 == y1:
            return

        painter.drawRect(x0, y0, x1 - x0, y1 - y0)

    def get_sorted_croping(self):
        """
        Sort the croping value from mouse move to standard value.
        """

        croping = list(self._croping_img_loc)
        min_wid_rto = max(10, int(self._resized_img_pos[2] / self.image3c.display.width() * 5))
        min_hig_rto = max(10, int(self._resized_img_pos[2] / self.image3c.display.width() * 5))
        x_lim = (self.x() - min_wid_rto, self.x() + self.width() + min_wid_rto)
        y_lim = (self.y() - min_hig_rto, self.y() + self.height() + min_hig_rto)
        croping[0] = x_lim[0] if croping[0] < x_lim[0] else croping[0]
        croping[0] = x_lim[1] if croping[0] > x_lim[1] else croping[0]
        croping[1] = y_lim[0] if croping[1] < y_lim[0] else croping[1]
        croping[1] = y_lim[1] if croping[1] > y_lim[1] else croping[1]
        croping[2] = x_lim[0] if croping[2] < x_lim[0] else croping[2]
        croping[2] = x_lim[1] if croping[2] > x_lim[1] else croping[2]
        croping[3] = y_lim[0] if croping[3] < y_lim[0] else croping[3]
        croping[3] = y_lim[1] if croping[3] > y_lim[1] else croping[3]

        if croping[0] > croping[2]:
            croping[0], croping[2] = croping[2], croping[0]

        if croping[1] > croping[3]:
            croping[1], croping[3] = croping[3], croping[1]

        if croping[2] - croping[0] < min_wid_rto:
            croping[2] = croping[0] + min_wid_rto

            if croping[2] > x_lim[1]:
                croping[2] = x_lim[1]
                croping[0] = x_lim[1] - min_wid_rto

        if croping[3] - croping[1] < min_hig_rto:
            croping[3] = croping[1] + min_hig_rto

            if croping[3] > y_lim[1]:
                croping[3] = y_lim[1]
                croping[1] = y_lim[1] - min_hig_rto

        return croping

    def get_sorted_locating(self):
        """
        Sort the locating value from mouse move to standard value.
        """

        locating = list(self._locating_img_loc)
        min_wid_rto = 10
        min_hig_rto = 10
        x_lim = (self.x() - min_wid_rto, self.x() + self.width() + min_wid_rto)
        y_lim = (self.y() - min_hig_rto, self.y() + self.height() + min_hig_rto)
        locating[0] = x_lim[0] if locating[0] < x_lim[0] else locating[0]
        locating[0] = x_lim[1] if locating[0] > x_lim[1] else locating[0]
        locating[1] = y_lim[0] if locating[1] < y_lim[0] else locating[1]
        locating[1] = y_lim[1] if locating[1] > y_lim[1] else locating[1]
        return locating

    def get_revised_croping_in_img(self):
        """
        Revise the croping value from mouse move to standard value (relative to full image).
        """

        st_croping = self.get_sorted_croping()
        relative_loc = [
            (st_croping[0] - self._resized_img_pos[0]) / self._resized_img_pos[2],
            (st_croping[1] - self._resized_img_pos[1]) / self._resized_img_pos[3],
            (st_croping[2] - self._resized_img_pos[0]) / self._resized_img_pos[2],
            (st_croping[3] - self._resized_img_pos[1]) / self._resized_img_pos[3],
        ]

        if relative_loc[0] > 1.0 - 1.5 / self.image3c.display.width() or relative_loc[1] > 1.0 - 1.5 / self.image3c.display.height() or relative_loc[2] < 1.5 / self.image3c.display.width() or relative_loc[3] < 1.5 / self.image3c.display.height():
            return None

        else:
            for idx in range(4):
                relative_loc[idx] = 0.0 if relative_loc[idx] < 0.0 else relative_loc[idx]
                relative_loc[idx] = 1.0 if relative_loc[idx] > 1.0 else relative_loc[idx]

            return relative_loc

    def get_revised_locating_in_img(self):
        """
        Revise the locating value from mouse move to standard value (relative to full image).
        """

        st_locating = self.get_sorted_locating()
        relative_loc = [
            (st_locating[0] - self._resized_img_pos[0]) / self._resized_img_pos[2],
            (st_locating[1] - self._resized_img_pos[1]) / self._resized_img_pos[3],
        ]

        for idx in range(2):
            if relative_loc[idx] < 0.0 or relative_loc[idx] > 1.0:
                return None

        return relative_loc

    def zoom(self, ratio, center):
        """
        Zoom displayed image.
        """

        if not (self.isVisible() and self.image3c.display and isinstance(self._resized_img_pos, np.ndarray)):
            return

        if center == "default":
            center = np.array((self.width() / 2, self.height() / 2), dtype=int)

        x, y, wid, hig = self._resized_img_pos
        img_wid = int(self.image3c.display.size().width())
        img_hig = int(self.image3c.display.size().height())

        if img_wid < self.width() and img_hig < self.height():
            max_wid = int(self.width() * 2)
            max_hig = int(self.height() * 2)

        elif img_wid < self.width() * 4 and img_hig < self.height() * 4:
            max_wid = int(self.width() * 6)
            max_hig = int(self.height() * 6)

        elif img_wid < self.width() * 8 and img_hig < self.height() * 8:
            max_wid = int(self.width() * 10)
            max_hig = int(self.height() * 10)

        else:
            max_wid = img_wid
            max_hig = img_hig

        if wid * ratio > max_wid or hig * ratio > max_hig:
            norm_ratio = min(max_wid / wid, max_hig / hig)

        elif wid * ratio < 24 or hig * ratio < 24:
            norm_ratio = max(24 / wid, 24 / hig)

        else:
            norm_ratio = ratio

        x = (x - center[0]) * norm_ratio + center[0]
        y = (y - center[1]) * norm_ratio + center[1]
        self._resized_img_pos = np.array([round(x), round(y), round(wid * norm_ratio), round(hig * norm_ratio)], dtype=int)
        self._home_image = False
        self.update()

    def move(self, shift_x, shift_y):
        """
        Move displayed image.
        """

        if not (self.isVisible() and self.image3c.display and isinstance(self._resized_img_pos, np.ndarray)):
            return

        x, y, wid, hig = self._resized_img_pos

        if self._args.rev_direct:
            x = x - shift_x
            y = y - shift_y

        else:
            x = x + shift_x
            y = y + shift_y

        self._resized_img_pos = np.array([x, y, wid, hig], dtype=int)
        self._home_image = False
        self.update()

    def home(self):
        """
        Home displayed image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if self._home_image:
            self.image3c.load_image(self._args.sys_category, self._args.sys_channel)

        img_wid = int(self.image3c.display.size().width())
        img_hig = int(self.image3c.display.size().height())
        ratio = min(self.width() / img_wid, self.height() / img_hig)
        self._resized_img_pos = np.array([
            round((self.width() - img_wid * ratio) / 2),
            round((self.height() - img_hig * ratio) / 2),
            round(img_wid * ratio),
            round(img_hig * ratio),

        ], dtype=int)
        self._home_image = not self._home_image
        self.update()

    def open_image_dialog(self):
        """
        Open a image dialog.
        """

        if not self.isVisible():
            return

        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
        cb_file = QFileDialog.getOpenFileName(None, self._open_descs[1], self._args.usr_image, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
            self.open_image(cb_file[0])

        else:
            return

    def open_image(self, image, script="", with_full_locs=[], direct=False):
        """
        Open a image.
        """

        if isinstance(script, tuple) and (not self.isVisible() or direct):
            return

        if script and (not self.image3c.img_data):
            return

        if self.image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if not self._args.check_temp_dir():
            self.warning(self._image_errs[2])
            return

        if not isinstance(script, tuple):
            if direct:
                img_data = image

            else:
                try:
                    img_data = PImage.open(image)

                except Exception as err:
                    self.warning(self._image_errs[4] + "\n{}\n{}".format(self._image_errs[8], err))
                    return

            self.image3c.img_data = img_data
            self._args.sys_image_url = image

        self._categories = set()
        self._args.sys_category = 0
        self._args.sys_channel = 0
        self.ps_image_changed.emit(True)
        self._args.sys_activated_assit_idx = -1
        self._args.sys_color_locs = [None, None, None, None, None]
        self._args.sys_assit_color_locs = [[None for j in self._args.sys_grid_assitlocs[i]] for i in range(5)]

        if with_full_locs and len(with_full_locs) == 5:
            for fidx in range(5):
                if len(with_full_locs[fidx]) > 0:
                    self._args.sys_color_locs[fidx] = tuple(with_full_locs[fidx][0]) if with_full_locs[fidx][0] else None

                if len(with_full_locs[fidx]) - 1 == len(self._args.sys_assit_color_locs[fidx]):
                    self._args.sys_assit_color_locs[fidx] = list(with_full_locs[fidx][1:])

        self.image3c.display = None
        self.image3c.ori_display_data = None
        self.image3c.res_display_data = None
        self.image3c.rev_display_data = None
        self.image3c.rgb_data = None
        self.image3c.hsv_data = None

        if isinstance(script, tuple):
            if script[0] in ("ZOOM", "CROP"):
                self._resized_img_pos = None

            self.image3c.run_args = script
            self.image3c.run_category = "init"
            self.image3c.start()

        else:
            self._resized_img_pos = None
            self.image3c.run_args = None
            self.image3c.run_category = "init"
            self.image3c.start()

        self.ps_history_backup.emit(True)
        self.update()

    def open_category(self):
        """
        Open this image in other category.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if not self.image3c.img_data:
            return

        if not self._args.check_temp_dir():
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[2])
            return

        if self._enhance_lock:
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[1])
            return

        self.image3c.display = None
        self.image3c.ori_display_data = None
        self.image3c.res_display_data = None
        self.image3c.rev_display_data = None

        if self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self.image3c.run_category = self._args.sys_category
            self.image3c.start()

        self.update()

    def extract_image(self, values):
        """
        Extract a set of colors from image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if self.image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        self.image3c.run_args = (self._args.rand_num, values, self._args.dep_wtp)
        self.image3c.run_category = "extract"
        self.image3c.start()
        self.update()

    def enhance_image(self, values):
        """
        Modify r, g or (and) b values to cover, enhance or inverse the contrast of image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if self.image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if values[0][:5] == "cover":
            cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
            cb_file = QFileDialog.getOpenFileName(None, self._open_descs[3], self._args.usr_image, filter=cb_filter)

            if cb_file[0]:
                self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
                values = list(values) + [os.path.abspath(cb_file[0])]

            else:
                return

        self._enhance_lock = True
        self.image3c.run_args = values[1:]
        self.image3c.run_category = values[0]
        self.image3c.start()
        self.update()

    def cancel_croping_or_locating(self):
        if self._croping_img or self._locating_img:
            self._croping_img = False
            self._croping_img_loc = None
            self._locating_img = False
            self._locating_img_loc = None
            self.update()
            return True

        else:
            return False

    def crop_image(self, value):
        """
        Crop image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if self._locating_img:
            return

        if self.image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if value:
            if isinstance(self._croping_img_loc, tuple) and self._croping_img == 2:
                revised_croping_value = self.get_revised_croping_in_img()

                if revised_croping_value:
                    self.open_image("", ("CROP", revised_croping_value))

                else:
                    self._croping_img = False
                    self._croping_img_loc = None

            else:
                self._croping_img = 1

        else:
            self._croping_img = False
            self._croping_img_loc = None

        self.update()

    def replace_color(self, value):
        """
        Replace color.
        """

        if not (self.isVisible() and self.image3c.display and isinstance(self.image3c.rgb_data, np.ndarray)):
            return

        if self.image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if self._croping_img:
            return

        if value[0]:
            if isinstance(self._locating_img_loc, tuple):
                shape = self.image3c.rgb_data.shape
                revised_locating_value = self.get_revised_locating_in_img()

                if revised_locating_value:
                    rgb = self.image3c.rgb_data[int(round(revised_locating_value[1] * (shape[0] - 1)))][int(round(revised_locating_value[0] * (shape[1] - 1)))]
                    rgb = np.array(rgb, dtype=float)
                    separ = []
                    fact = []

                    if value[0] == 1:
                        for i in range(3):
                            separ.append(rgb[i])
                            fact.append((self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] - rgb[i]) / 255.0)

                        self.image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2], True, self._args.dep_wtp)
                        self.image3c.run_category = "enhance_rgb"

                    elif value[0] == 2:
                        point = Color(rgb, tp=CTP.rgb)
                        hsv = np.array(point.hsv, dtype=float)

                        if self._args.dep_wtp:
                            angle = Color((Color.spc_rgb2ryb_h(hsv[0]), 1, 1), tp=CTP.hsv).ref_h(Color.spc_rgb2ryb_h(self._args.sys_color_set[self._args.sys_activated_idx].h))

                        else:
                            angle = point.ref_h(self._args.sys_color_set[self._args.sys_activated_idx].h)

                        separ.append(hsv[0])
                        fact.append(angle / 180.0)
                        separ.append(hsv[1])
                        fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] - hsv[1]))
                        separ.append(hsv[2])
                        fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] - hsv[2]))
                        self.image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2], True, self._args.dep_wtp)
                        self.image3c.run_category = "enhance_hsv"

                    self.image3c.start()
                    self._enhance_lock = True

                else:
                    self._locating_img = False
                    self._locating_img_loc = None

            else:
                self._locating_img = True

        else:
            self._locating_img = False
            self._locating_img_loc = None

        self.update()

    def update_loading_label(self, idx):
        """
        Loading descriptions when importing a image.
        """

        self._tip_label.setText(self._image_descs[idx])
        self._tip_label.setAlignment(Qt.AlignCenter)
        self.update()

    def update_loading_bar(self, idx):
        """
        Loading process when importing a image.
        """

        self._loading_bar.setValue(idx)
        self.update()

    def loading_finished(self, idx):
        """
        Loading finished.
        """

        self._categories.add(idx)
        self._croping_img = False
        self._croping_img_loc = None
        self._locating_img = False
        self._locating_img_loc = None
        self._home_image = False
        self.update()

    def extract_finished(self, value):
        """
        Enhance finished.
        """

        self._args.hm_rule = "custom"
        self.ps_modify_rule.emit(True)
        self._args.sys_color_locs = value

        for i in range(5):
            rgb = self.image3c.rgb_data[int(round(value[i][1] * (self.image3c.rgb_data.shape[0] - 1)))][int(round(value[i][0] * (self.image3c.rgb_data.shape[1] - 1)))]
            color = Color(rgb, tp=CTP.rgb, overflow=self._args.sys_color_set.get_overflow())
            self._args.sys_color_set.modify(self._args.hm_rule, i, color, do_sync=False)

        self.ps_color_changed.emit(True)
        self._home_image = False
        self.ps_history_backup.emit(True)
        self.update()

    def enhance_finished(self, idx):
        """
        Enhance finished.
        """

        if idx == 2:
            self.warning(self._image_errs[6])

        if idx == 3:
            self.warning(self._image_errs[7])

        self._enhance_lock = False
        self._locating_img = False
        self._locating_img_loc = None
        self._home_image = False
        self.update()

    def modify_color_loc(self):
        """
        Modify color set by overlabel.
        """

        if not isinstance(self.image3c.rgb_data, np.ndarray):
            return

        if self._args.sys_activated_assit_idx < 0:
            loc = self._args.sys_color_locs[self._args.sys_activated_idx]

        else:
            loc = self._args.sys_assit_color_locs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx]

        if loc:
            shape = self.image3c.rgb_data.shape
            rgb = self.image3c.rgb_data[int(round(loc[1] * (shape[0] - 1)))][int(round(loc[0] * (shape[1] - 1)))]

            if self._args.sys_activated_assit_idx < 0:
                if not (rgb == self._args.sys_color_set[self._args.sys_activated_idx].rgb).all():
                    color = Color(rgb, tp=CTP.rgb, overflow=self._args.sys_color_set.get_overflow())
                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

            else:
                color = Color(rgb, tp=CTP.rgb, overflow=self._args.sys_color_set.get_overflow())
                self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][2:5] = gen_assit_args(self._args.sys_color_set[self._args.sys_activated_idx], color, self._args.sys_grid_assitlocs[self._args.sys_activated_idx][self._args.sys_activated_assit_idx][5])

        self.ps_color_changed.emit(True)

    def update_color_loc(self):
        """
        Update color set by overlabel.
        """

        if not isinstance(self.image3c.rgb_data, np.ndarray):
            return

        for idx in range(5):
            loc = self._args.sys_color_locs[idx]

            if loc:
                shape = self.image3c.rgb_data.shape
                rgb = self.image3c.rgb_data[int(round(loc[1] * (shape[0] - 1)))][int(round(loc[0] * (shape[1] - 1)))]

                if not (rgb == self._args.sys_color_set[idx].rgb).all():
                    self._args.sys_color_locs[idx] = None

            for assit_idx in range(len(self._args.sys_grid_assitlocs[idx])):
                loc = self._args.sys_assit_color_locs[idx][assit_idx]

                if loc:
                    shape = self.image3c.rgb_data.shape
                    rgb = self.image3c.rgb_data[int(round(loc[1] * (shape[0] - 1)))][int(round(loc[0] * (shape[1] - 1)))]
                    curr_color = gen_assit_color(self._args.sys_color_set[idx], *self._args.sys_grid_assitlocs[idx][assit_idx][2:6])

                    if not (rgb == curr_color.rgb).all():
                        self._args.sys_assit_color_locs[idx][assit_idx] = None

        self.update()

    def freeze_image(self, value=None):
        """
        Freeze current image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        if self.image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        load_image = ImageQt.fromqimage(self.image3c.display)

        if load_image:
            self.open_image(load_image, direct=True)

        else:
            self.warning(self._image_errs[5])

    def save_image(self, value=None):
        """
        Exec save image.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        name = "{}".format(time.strftime("Rickrack_Image_%Y_%m_%d.png", time.localtime()))
        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
        cb_file = QFileDialog.getSaveFileName(None, self._open_descs[2], os.sep.join((self._args.usr_image, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            return

        self.image3c.display.save(cb_file[0])

    def clipboard_in(self):
        """
        Load image from clipboard.
        """

        if not self.isVisible():
            return

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                image = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff") and os.path.isfile(image):
                self.open_image(image)

        elif clipboard.hasImage():
            load_image = self.image3c.save_load_data(clipboard.imageData())

            if load_image:
                self.open_image(load_image)

    def clipboard_img(self):
        """
        Set the image as the clipboard data by Ctrl + c.
        """

        if not (self.isVisible() and self.image3c.display):
            return

        mimedata = QMimeData()
        mimedata.setImageData(QPixmap.fromImage(self.image3c.display))
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mimedata)

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._image_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._image_errs[3], QMessageBox.AcceptRole)
        box.exec_()

    def create_menu(self):
        """
        Create a right clicked menu.
        """

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
        self._menu = QMenu(self)
        self._action_undo = QAction(self)
        self._action_undo.triggered.connect(lambda: self.ps_undo.emit(True))
        self._menu.addAction(self._action_undo)
        self._action_redo = QAction(self)
        self._action_redo.triggered.connect(lambda: self.ps_undo.emit(False))
        self._menu.addAction(self._action_redo)
        self._action_reset = QAction(self)
        self._action_reset.triggered.connect(self.home)
        self._menu.addAction(self._action_reset)
        self._action_paste = QAction(self)
        self._action_paste.triggered.connect(self.clipboard_in)
        self._menu.addAction(self._action_paste)
        self._action_open_img = QAction(self)
        self._action_open_img.triggered.connect(self.open_image_dialog)
        self._menu.addAction(self._action_open_img)
        self._action_copy_img = QAction(self)
        self._action_copy_img.triggered.connect(self.clipboard_img)
        self._menu.addAction(self._action_copy_img)
        self._action_freeze_img = QAction(self)
        self._action_freeze_img.triggered.connect(self.freeze_image)
        self._menu.addAction(self._action_freeze_img)
        self._action_save_img = QAction(self)
        self._action_save_img.triggered.connect(self.save_image)
        self._menu.addAction(self._action_save_img)
        self._action_zoom_in = QAction(self)
        self._action_zoom_in.triggered.connect(lambda: self.zoom(self._args.zoom_step, center="default"))
        self._menu.addAction(self._action_zoom_in)
        self._action_zoom_out = QAction(self)
        self._action_zoom_out.triggered.connect(lambda: self.zoom(1 / self._args.zoom_step, center="default"))
        self._menu.addAction(self._action_zoom_out)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        self.update_action_text()

        if self.image3c.display:
            self._action_reset.setVisible(True)
            self._action_copy_img.setVisible(True)
            self._action_zoom_in.setVisible(True)
            self._action_zoom_out.setVisible(True)
            self._action_freeze_img.setVisible(True)
            self._action_save_img.setVisible(True)

        else:
            self._action_reset.setVisible(False)
            self._action_copy_img.setVisible(False)
            self._action_zoom_in.setVisible(False)
            self._action_zoom_out.setVisible(False)
            self._action_freeze_img.setVisible(False)
            self._action_save_img.setVisible(False)

        self._menu.exec_(QCursor.pos())

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

            shortcut.activated.connect(self.clipboard_img)

        for skey in self._args.shortcut_keymaps[46]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()

            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut

            shortcut.activated.connect(self.clipboard_in)

    def update_action_text(self):
        self._action_undo.setText(self._action_descs[0])
        self._action_redo.setText(self._action_descs[1])
        self._action_open_img.setText(self._action_descs[2])
        self._action_copy_img.setText(self._action_descs[3])
        self._action_paste.setText(self._action_descs[4])
        self._action_reset.setText(self._action_descs[5])
        self._action_zoom_in.setText(self._action_descs[6])
        self._action_zoom_out.setText(self._action_descs[7])
        self._action_freeze_img.setText(self._action_descs[8])
        self._action_save_img.setText(self._action_descs[9])

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._action_descs = (
            _translate("Wheel", "Undo"), # 0
            _translate("Wheel", "Redo"), # 1
            _translate("Image", "Open Image"), # 2
            _translate("Image", "Copy Image"), # 3
            _translate("Wheel", "Paste"), # 4
            _translate("Image", "Reset"), # 5
            _translate("Board", "Zoom In"), # 6
            _translate("Board", "Zoom Out"), # 7
            _translate("Image", "Freeze Image"), # 8
            _translate("Image", "Save Image"), # 9
        )

        self._open_descs = (
            _translate("Image", "Double click here to open an image."),
            _translate("Image", "Open"),
            _translate("Image", "Save"),
            _translate("Image", "Cover"),
        )

        self._image_errs = (
            _translate("Image", "Error"),
            _translate("Image", "Could not process image. There is a process of image not finished."),
            _translate("Image", "Could not create temporary dir. Dir is not created."),
            _translate("Image", "OK"),
            _translate("Image", "Could not open image. This image is broken."),
            _translate("Image", "Could not process image. Translation is not completed."),
            _translate("Image", "Could not process image. The size of image is not suitable."),
            _translate("Image", "Could not process image. This image is invalid."),
            _translate("Operation", "Detail:"),
        )

        self._image_descs = (
            _translate("Image", "Finishing."),
            _translate("Image", "Loading RGB data."),
            _translate("Image", "Saving RGB data."),
            _translate("Image", "Loading HSV data."),
            _translate("Image", "Saving HSV data."),
            _translate("Image", "Loading RGB vertical edge data."),
            _translate("Image", "Saving RGB vertical edge data."),
            _translate("Image", "Loading RGB horizontal edge data."),
            _translate("Image", "Saving RGB horizontal edge data."),
            _translate("Image", "Loading RGB final edge data."),
            _translate("Image", "Saving RGB final edge data."),
            _translate("Image", "Loading HSV vertical edge data."),
            _translate("Image", "Saving HSV vertical edge data."),
            _translate("Image", "Loading HSV horizontal edge data."),
            _translate("Image", "Saving HSV horizontal edge data."),
            _translate("Image", "Loading HSV final edge data."),
            _translate("Image", "Saving HSV final edge data."),
            _translate("Image", "Applying filter to image data."),
        )

        self._extend_descs = (
            _translate("Image", "All Acceptable Images"),
            _translate("Image", "PNG Image"),
            _translate("Image", "BMP Image"),
            _translate("Image", "JPG Image"),
            _translate("Image", "TIF Image"),
            _translate("Image", "WEBP Image"),
        )

