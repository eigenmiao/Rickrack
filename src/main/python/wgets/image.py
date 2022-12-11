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
import sys
import time
import numpy as np
from PIL import Image as PImage
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QMessageBox, QFileDialog, QShortcut, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QRect, QPoint, QMimeData
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QCursor, QKeySequence
from cguis.resource import view_rc
from clibs.image3c import Image3C
from ricore.transpt import get_outer_box
from ricore.color import Color


class Image(QWidget):
    """
    Image object based on QWidget. Init a image pannel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_image_changed = pyqtSignal(bool)
    ps_status_changed = pyqtSignal(tuple)
    ps_recover_channel = pyqtSignal(bool)
    ps_modify_rule = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init Image pannel.
        """

        super().__init__(wget)

        # set name ids.
        wget.setProperty("class", "WorkArea")

        # load args.
        self._args = args
        self._categories = set()
        self._drop_image = None
        self._start_pt = None
        self._enhance_lock = False
        self._home_image = False
        self._pressing_key = 0
        self._croping_img = False
        self._locating_img = False
        self._resized_img_pos = None
        self._locating_colors = False
        self._color_locations = [None, None, None, None, None]
        self._connected_keymaps = {}

        # load translations.
        self._func_tr_()

        # init qt args.
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

        self._image3c = Image3C(self._args.global_temp_dir)
        self._image3c.ps_describe.connect(self.update_loading_label)
        self._image3c.ps_proceses.connect(self.update_loading_bar)
        self._image3c.ps_finished.connect(self.loading_finished)
        self._image3c.ps_enhanced.connect(self.enhance_finished)
        self._image3c.ps_extracts.connect(self.extract_finished)

        # shortcut is updated by _setup_skey in main.py.
        # self.update_skey()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if not self._image3c.img_data:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.show()

            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid, Qt.PenStyle(Qt.DashLine)))
            painter.setBrush(QColor(*self._args.wheel_ed_color))

            self._tip_box = (self.width() * 0.2, self.height() * 0.2, self.width() * 0.6, self.height() * 0.6)
            radius = min(self.width() * 0.1, self.height() * 0.1)
            painter.drawRoundedRect(*self._tip_box, radius, radius)

            self._tip_label.setGeometry(QRect(*self._tip_box))

            self._tip_label.setText(self._action_descs[0])
            self._tip_label.setAlignment(Qt.AlignCenter)

        elif self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self._loading_bar.show()
            self._ico_label.show()
            self._tip_label.show()

            bar_wid = self.width() * 0.8
            bar_hig = self.height() * 0.1

            self._loading_bar.setGeometry((self.width() - bar_wid) / 2, self.height() * 0.88, bar_wid, bar_hig)
            self._tip_label.setGeometry((self.width() - bar_wid) / 2, self.height() * 0.76, bar_wid, bar_hig)

            img_wid = min(self.width() * 0.8, self.height() * 0.6)

            resized_pix = QPixmap.fromImage(self._ico)
            resized_pix.setDevicePixelRatio(self._ico.width() / img_wid)

            self._ico_label.setPixmap(resized_pix)
            self._ico_label.setGeometry((self.width() - img_wid) / 2, (self.height() * 0.76 - img_wid) / 2, img_wid, img_wid)

        else:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.hide()

            if not self._image3c.display:
                self._image3c.load_image(self._args.sys_category, self._args.sys_channel)

            if self._image3c.display:
                if not self._resized_img_pos:
                    self.home()
                    self._home_image = False

                # display resized image as background.
                self._resized_img_pos[0] = self.width() - 2 if self._resized_img_pos[0] > self.width() - 2 else self._resized_img_pos[0]
                self._resized_img_pos[0] = 2 - self._resized_img_pos[2] if self._resized_img_pos[0] < 2 - self._resized_img_pos[2] else self._resized_img_pos[0]
                self._resized_img_pos[1] = self.height() - 2 if self._resized_img_pos[1] > self.height() - 2 else self._resized_img_pos[1]
                self._resized_img_pos[1] = 2 - self._resized_img_pos[3] if self._resized_img_pos[1] < 2 - self._resized_img_pos[3] else self._resized_img_pos[1]

                # aspect ratio mode: IgnoreAspectRatio, KeepAspectRatio and KeepAspectRatioByExpanding.
                resized_pix = QPixmap.fromImage(self._image3c.display)
                resized_pix.setDevicePixelRatio(self._image3c.display.width() / self._resized_img_pos[2])

                painter.drawPixmap(*self._resized_img_pos, resized_pix)

                # display locating circles.
                idx_seq = list(range(5))
                idx_seq = idx_seq[self._args.sys_activated_idx + 1: ] + idx_seq[: self._args.sys_activated_idx + 1]

                for idx in idx_seq:
                    if self._color_locations[idx]:
                        pt_xy = np.array((self._color_locations[idx][0] * self._resized_img_pos[2] + self._resized_img_pos[0], self._color_locations[idx][1] * self._resized_img_pos[3] + self._resized_img_pos[1]))
                        pt_rgb = self._args.sys_color_set[idx].rgb

                        pt_box = get_outer_box(pt_xy, self._args.circle_dist + (self._args.positive_wid + self._args.negative_wid) * 2)

                        if self._pressing_key == 3:
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

                        if self._pressing_key == 3:
                            painter.setPen(QPen(Qt.black, self._args.negative_wid))
                            painter.setBrush(QBrush(Qt.NoBrush))

                        else:
                            if idx == self._args.sys_activated_idx:
                                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                            else:
                                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

                            painter.setBrush(QColor(*pt_rgb))

                        painter.drawEllipse(*pt_box)

                if isinstance(self._croping_img, tuple):
                    sted_croping = self.get_sorted_croping()

                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))

                    self.draw_twopt_rect(painter, 0, 0, sted_croping[0], self.height())
                    self.draw_twopt_rect(painter, sted_croping[2], 0, self.width(), self.height())
                    self.draw_twopt_rect(painter, sted_croping[0], 0, sted_croping[2], sted_croping[1])
                    self.draw_twopt_rect(painter, sted_croping[0], sted_croping[3], sted_croping[2], self.height())

                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                    painter.drawLine(QPoint(sted_croping[0] + self.x(), 0), QPoint(sted_croping[0] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_croping[1] + self.y()), QPoint(self.width(), sted_croping[1] + self.y()))

                    painter.drawLine(QPoint(sted_croping[2] + self.x(), 0), QPoint(sted_croping[2] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_croping[3] + self.y()), QPoint(self.width(), sted_croping[3] + self.y()))

                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format((self._croping_img[2] - self._resized_img_pos[0]) * 100 / self._resized_img_pos[2]), "{:.1f}".format((self._croping_img[3] - self._resized_img_pos[1]) * 100 / self._resized_img_pos[3])))

                elif isinstance(self._locating_img, tuple):
                    sted_locating = self.get_sorted_locating()

                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))

                    painter.drawRect(0, 0, self.width(), self.height())

                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                    painter.drawLine(QPoint(sted_locating[0] + self.x(), 0), QPoint(sted_locating[0] + self.x(), self.height()))
                    painter.drawLine(QPoint(0, sted_locating[1] + self.y()), QPoint(self.width(), sted_locating[1] + self.y()))

                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format((self._locating_img[0] - self._resized_img_pos[0]) * 100 / self._resized_img_pos[2]), "{:.1f}".format((self._locating_img[1] - self._resized_img_pos[1]) * 100 / self._resized_img_pos[3])))

                elif self._croping_img or self._locating_img:
                    painter.setPen(QPen(Qt.NoPen))
                    painter.setBrush(QColor(255, 255, 255, 160))

                    painter.drawRect(0, 0, self.width(), self.height())

                elif self._color_locations[self._args.sys_activated_idx]:
                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format(self._color_locations[self._args.sys_activated_idx][0] * 100), "{:.1f}".format(self._color_locations[self._args.sys_activated_idx][1] * 100), Color.sign(self._args.sys_color_set[self._args.sys_activated_idx].hsv)))

                else:
                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0]))

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and self._image3c.display:
            self._pressing_key = 3
            self.setCursor(QCursor(Qt.ClosedHandCursor))

            event.accept()
            self.update()

        else:
            self._pressing_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        if self._pressing_key:
            self._pressing_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))

            event.ignore()
            self.update()

    def mouseDoubleClickEvent(self, event):
        if not self._image3c.img_data and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._tip_box[0] < p_x < (self._tip_box[0] + self._tip_box[2]) and self._tip_box[1] < p_y < (self._tip_box[1] + self._tip_box[3]):
                self.open_image_dialog()

                event.accept()
                self.update()

            else:
                event.ignore()

    def dragEnterEvent(self, event):
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
        if self._drop_image:
            self.open_image(self._drop_image)
            self._drop_image = None

            event.accept()

        else:
            event.ignore()

    def wheelEvent(self, event):
        if self._image3c.display:
            point = (event.x(), event.y())
            ratio = (event.angleDelta() / 120).y()

            if ratio:
                ratio = ratio * self._args.zoom_step if ratio > 0 else -1 * ratio / self._args.zoom_step

            else:
                ratio = 1

            self.zoom(ratio, point)

            event.accept()
            # self.update() is completed by self.zoom.
            # self.update()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        if self._image3c.display and self._resized_img_pos:
            if event.button() == Qt.MidButton or (self._pressing_key == 3 and event.button() == Qt.LeftButton):
                if event.button() == Qt.MidButton:
                    self.setCursor(QCursor(Qt.ClosedHandCursor))

                self._start_pt = (event.x(), event.y())

                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self._croping_img:
                self._croping_img = (
                    event.x() - self.x(),
                    event.y() - self.y(),
                    event.x() - self.x(),
                    event.y() - self.y(),
                )

                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self._locating_img:
                self._locating_img = (
                    event.x() - self.x(),
                    event.y() - self.y(),
                )

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton and self._croping_img:
                self._croping_img = False

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton and self._locating_img:
                self._locating_img = False

                event.accept()
                self.update()

            elif not (self._pressing_key or self._croping_img or self._locating_img):
                point = np.array((event.x(), event.y()))
                already_accept = False

                for idx in range(5):
                    if self._color_locations[idx] and np.linalg.norm(point - np.array(self._color_locations[idx]) * np.array(self._resized_img_pos[2:]) - np.array(self._resized_img_pos[:2])) < self._args.circle_dist + (self._args.positive_wid + self._args.negative_wid) * 2:
                        self._args.sys_activated_idx = idx
                        already_accept = True

                        break

                if event.button() == Qt.LeftButton and (((self._args.press_move or not self._color_locations[self._args.sys_activated_idx]) and self._resized_img_pos[0] < point[0] < self._resized_img_pos[0] + self._resized_img_pos[2] and self._resized_img_pos[1] < point[1] < self._resized_img_pos[1] + self._resized_img_pos[3]) or already_accept):
                    loc = [(point[0] - self._resized_img_pos[0]) / self._resized_img_pos[2], (point[1] - self._resized_img_pos[1]) / self._resized_img_pos[3]]
                    loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
                    loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
                    loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
                    loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

                    self._color_locations[self._args.sys_activated_idx] = tuple(loc)
                    self.modify_color_loc()

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
        if self._start_pt:
            point = (event.x(), event.y())

            if self._args.rev_direct:
                self.move(self._start_pt[0] - point[0], self._start_pt[1] - point[1])

            else:
                self.move(point[0] - self._start_pt[0], point[1] - self._start_pt[1])

            self._start_pt = point

            event.accept()
            # self.update() is completed by self.move.
            # self.update()

        elif self._croping_img:
            self._croping_img = (
                self._croping_img[0],
                self._croping_img[1],
                event.x() - self.x(),
                event.y() - self.y(),
            )

            event.accept()
            self.update()

        elif self._locating_img:
            self._locating_img = (
                event.x() - self.x(),
                event.y() - self.y(),
            )

            event.accept()
            self.update()

        elif self._locating_colors:
            point = np.array((event.x(), event.y()))

            loc = [(point[0] - self._resized_img_pos[0]) / self._resized_img_pos[2], (point[1] - self._resized_img_pos[1]) / self._resized_img_pos[3]]
            loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
            loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
            loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
            loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

            self._color_locations[self._args.sys_activated_idx] = tuple(loc)
            self.modify_color_loc()

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._pressing_key = 0
        self._locating_colors = False
        self._start_pt = None

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def init_icon(self):
        """
        if self._args.style_id < 5:
            self._ico = QImage(":/images/images/icon_grey_1024.png")
        """

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

        croping = list(self._croping_img)

        min_wid_rto = 10
        min_hig_rto = 10

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

        locating = list(self._locating_img)

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

        if relative_loc[0] > 1.0 or relative_loc[1] > 1.0 or relative_loc[2] < 0.0 or relative_loc[3] < 0.0:
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

        if not (self.isVisible() and self._image3c.display and self._resized_img_pos):
            return

        if center == "default":
            center = (self.width() / 2, self.height() / 2)

        x, y, wid, hig = self._resized_img_pos

        img_wid = self._image3c.display.size().width()
        img_hig = self._image3c.display.size().height()

        if img_wid < self.width() and img_hig < self.height():
            max_wid = self.width() * 2
            max_hig = self.height() * 2

        elif img_wid < self.width() * 4 and img_hig < self.height() * 4:
            max_wid = self.width() * 6
            max_hig = self.height() * 6

        elif img_wid < self.width() * 8 and img_hig < self.height() * 8:
            max_wid = self.width() * 10
            max_hig = self.height() * 10

        else:
            max_wid = img_wid
            max_hig = img_hig

        # min_wid = 24
        # min_hig = 24

        if wid * ratio > max_wid or hig * ratio > max_hig:
            norm_ratio = min(max_wid / wid, max_hig / hig)

        elif wid * ratio < 24 or hig * ratio < 24:
            norm_ratio = max(24 / wid, 24 / hig)

        else:
            norm_ratio = ratio

        x = (x - center[0]) * norm_ratio + center[0]
        y = (y - center[1]) * norm_ratio + center[1]

        self._resized_img_pos = [int(round(x)), int(round(y)), int(round(wid * norm_ratio)), int(round(hig * norm_ratio))]
        self._home_image = False

        self.update()

    def move(self, shift_x, shift_y):
        """
        Move displayed image.
        """

        if not (self.isVisible() and self._image3c.display and self._resized_img_pos):
            return

        x, y, wid, hig = self._resized_img_pos

        if self._args.rev_direct:
            x = x - shift_x
            y = y - shift_y

        else:
            x = x + shift_x
            y = y + shift_y

        self._resized_img_pos = [x, y, wid, hig]
        self._home_image = False

        self.update()

    def home(self):
        """
        Home displayed image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._home_image:
            self._image3c.load_image(self._args.sys_category, self._args.sys_channel)

        img_wid = self._image3c.display.size().width()
        img_hig = self._image3c.display.size().height()

        ratio = min(self.width() / img_wid, self.height() / img_hig)

        self._resized_img_pos = [
            int(round((self.width() - img_wid * ratio) / 2)),
            int(round((self.height() - img_hig * ratio) / 2)),
            int(round(img_wid * ratio)),
            int(round(img_hig * ratio)),
        ]

        self._home_image = not self._home_image

        self.update()

    def open_image_dialog(self):
        """
        Open a image dialog.
        """

        if not self.isVisible():
            return

        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
        cb_file = QFileDialog.getOpenFileName(None, self._action_descs[1], self._args.usr_image, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
            self.open_image(cb_file[0])

        else:
            # closed without open a file.
            return

    def open_image(self, image, script=""):
        """
        Open a image.
        """

        if isinstance(script, tuple) and (not self.isVisible()):
            return

        if script and (not self._image3c.img_data):
            return

        if self._image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if not self._args.check_temp_dir():
            self.warning(self._image_errs[2])
            return

        if not isinstance(script, tuple):
            try:
                img_data = PImage.open(image)

            except Exception as err:
                self.warning(self._image_errs[4])
                return

            self._image3c.img_data = img_data

        self._categories = set()

        self._args.sys_category = 0
        self._args.sys_channel = 0
        self.ps_image_changed.emit(True)

        self._color_locations = [None, None, None, None, None]
        self._image3c.display = None

        self._image3c.ori_display_data = None
        self._image3c.res_display_data = None
        self._image3c.rev_display_data = None

        self._image3c.rgb_data = None
        self._image3c.hsv_data = None

        if isinstance(script, tuple):
            if script[0] in ("ZOOM", "CROP"):
                self._resized_img_pos = None

            self._image3c.run_args = script
            self._image3c.run_category = "init"
            self._image3c.start()

        else:
            self._resized_img_pos = None

            self._image3c.run_args = None

            self._image3c.run_category = "init"
            self._image3c.start()

        self.update()

    def open_category(self):
        """
        Open this image in other category.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if not self._image3c.img_data:
            return

        if not self._args.check_temp_dir():
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[2])
            return

        if self._enhance_lock:
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[1])
            return

        self._image3c.display = None

        self._image3c.ori_display_data = None
        self._image3c.res_display_data = None
        self._image3c.rev_display_data = None

        if self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self._image3c.run_category = self._args.sys_category
            self._image3c.start()

        self.update()

    def extract_image(self, values):
        """
        Extract a set of colors from image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        self._image3c.run_args = (self._args.rand_num, values)
        self._image3c.run_category = "extract"
        self._image3c.start()

        self.update()

    def enhance_image(self, values):
        """
        Modify r, g or (and) b values to enhance or inverse the contrast of image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if values[0][:5] == "cover":
            cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
            cb_file = QFileDialog.getOpenFileName(None, self._action_descs[3], self._args.usr_image, filter=cb_filter)

            if cb_file[0]:
                self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
                values = list(values) + [os.path.abspath(cb_file[0])]

            else:
                # closed without open a file.
                return

        self._enhance_lock = True

        self._image3c.run_args = values[1:]
        self._image3c.run_category = values[0]
        self._image3c.start()

        self.update()

    def cancel_croping_or_locating(self):
        """
        Cancel the croping or locating actions.
        Esc refer to cancel them if they are activated (return True) in main window.
        """

        if self._croping_img or self._locating_img:
            self._croping_img = False
            self._locating_img = False

            self.update()

            return True

        else:
            return False

    def crop_image(self, value):
        """
        Crop image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._locating_img:
            return

        if self._image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if value:
            if isinstance(self._croping_img, tuple):
                revised_croping_value = self.get_revised_croping_in_img()

                if revised_croping_value:
                    self.open_image("", ("CROP", revised_croping_value))

                else:
                    self._croping_img = False

            else:
                self._croping_img = True

        else:
            self._croping_img = False

        self.update()

    def replace_color(self, value):
        """
        Replace color.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if self._croping_img:
            return

        if value[0]:
            if isinstance(self._locating_img, tuple):
                shape = self._image3c.rgb_data.shape
                revised_locating_value = self.get_revised_locating_in_img()

                if revised_locating_value and value[4]:
                    # using old algorithm.
                    #
                    rgb = self._image3c.rgb_data[int(revised_locating_value[1] * (shape[0] - 1))][int(revised_locating_value[0] * (shape[1] - 1))]
                    separ = []
                    fact = []

                    if value[0] == 1:
                        for i in range(3):
                            if self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] > rgb[i]:
                                separ.append(rgb[i] - rgb[i] * value[3])
                                fact.append((self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] - rgb[i]) / (255 - (rgb[i] - 0.00001))) # divide by zero error.

                            else:
                                separ.append(rgb[i] + 0.00001 + (255.0 - rgb[i]) * value[3])
                                fact.append((rgb[i] - self._args.sys_color_set[self._args.sys_activated_idx].rgb[i]) / (rgb[i] + 0.00001)) # divide by zero error.

                        self._image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2])
                        self._image3c.run_category = "enhance_rgb"

                    elif value[0] == 2:
                        point = Color(rgb, tp="rgb")
                        angle = self._args.sys_color_set[self._args.sys_activated_idx].ref_h(point.h)

                        hsv = list(point.hsv)

                        if angle > 0.0:
                            hsv[0] = float(hsv[0]) - 1E-4

                        elif angle < 0.0:
                            hsv[0] = float(hsv[0]) + 1E-4

                        else:
                            hsv[0] = float(hsv[0])

                        separ.append(hsv[0])
                        fact.append(abs(angle) / 180.0 * value[3])

                        if self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] > hsv[1]:
                            separ.append(hsv[1] - hsv[1] * value[3])
                            fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] - hsv[1]) / (1.0 - hsv[1]))

                        else:
                            separ.append(hsv[1] + 0.00001 + (1.0 - hsv[1]) * value[3])
                            fact.append((hsv[1] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[1]) / hsv[1])

                        if self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] > hsv[2]:
                            separ.append(hsv[2] - hsv[2] * value[3])
                            fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] - hsv[2]) / (1.0 - hsv[2]))

                        else:
                            separ.append(hsv[2] + 0.00001 + (1.0 - hsv[1]) * value[3])
                            fact.append((hsv[2] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[2]) / hsv[2])

                        self._image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2])
                        self._image3c.run_category = "enhance_hsv"

                    self._image3c.start()

                    self._enhance_lock = True

                elif revised_locating_value:
                    # using new algorithm.
                    #
                    rgb = self._image3c.rgb_data[int(revised_locating_value[1] * (shape[0] - 1))][int(revised_locating_value[0] * (shape[1] - 1))]

                    fact = []

                    if value[0] == 1:
                        for i in range(3):
                            if self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] > rgb[i]:
                                fori = (self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] - rgb[i]) / (255.0 - (rgb[i] - 0.00001)) # divide by zero error.
                                fact.append(fori * value[3])

                            else:
                                fori = (rgb[i] - self._args.sys_color_set[self._args.sys_activated_idx].rgb[i]) / (rgb[i] + 0.00001) # divide by zero error.
                                fact.append(fori * value[3])

                        self._image3c.run_args = ((0, 1, 2), tuple(rgb), tuple(fact), value[1], value[2])
                        self._image3c.run_category = "enhance_rgb"

                    elif value[0] == 2:
                        point = Color(rgb, tp="rgb")
                        angle = self._args.sys_color_set[self._args.sys_activated_idx].ref_h(point.h)

                        hsv = list(point.hsv)

                        if angle > 0.0:
                            hsv[0] = float(hsv[0]) - 1E-4

                        elif angle < 0.0:
                            hsv[0] = float(hsv[0]) + 1E-4

                        else:
                            hsv[0] = float(hsv[0])

                        fact.append(abs(angle) / 180.0 * value[3])

                        if self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] > hsv[1]:
                            fori = (self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] - hsv[1]) / (1.0 - (hsv[1] - 0.00001))
                            fact.append(fori * value[3])

                        else:
                            fori = (hsv[1] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[1]) / (hsv[1] + 0.00001)
                            fact.append(fori * value[3])

                        if self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] > hsv[2]:
                            fori = (self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] - hsv[2]) / (1.0 - (hsv[2] - 0.00001))
                            fact.append(fori * value[3])

                        else:
                            fori = (hsv[2] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[2]) / (hsv[2] + 0.00001)
                            fact.append(fori * value[3])

                        self._image3c.run_args = ((0, 1, 2), tuple(hsv), tuple(fact), value[1], value[2])
                        self._image3c.run_category = "enhance_hsv"

                    self._image3c.start()

                    self._enhance_lock = True

                else:
                    self._locating_img = False

            else:
                self._locating_img = True

        else:
            self._locating_img = False

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
        self._locating_img = False
        self._home_image = False

        self.update()

    def extract_finished(self, value):
        """
        Enhance finished.
        """

        self._args.hm_rule = "custom"
        self.ps_modify_rule.emit(True)

        self._color_locations = value

        for i in range(5):
            rgb = self._image3c.rgb_data[int(value[i][1] * (self._image3c.rgb_data.shape[0] - 1))][int(value[i][0] * (self._image3c.rgb_data.shape[1] - 1))]

            color = Color(rgb, tp="rgb", overflow=self._args.sys_color_set.get_overflow())
            self._args.sys_color_set.modify(self._args.hm_rule, i, color, do_sync=False)

        self.ps_color_changed.emit(True)
        # similar to modify_color_loc,
        # update_color_loc() is completed by 
        # self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color()) in main.py.

        self._home_image = False

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
        self._home_image = False

        self.update()

    def modify_color_loc(self):
        """
        Modify color set by overlabel. 
        """

        loc = self._color_locations[self._args.sys_activated_idx]

        if loc:
            shape = self._image3c.rgb_data.shape
            rgb = self._image3c.rgb_data[int(loc[1] * (shape[0] - 1))][int(loc[0] * (shape[1] - 1))]

            if not (rgb == self._args.sys_color_set[self._args.sys_activated_idx].rgb).all():
                color = Color(rgb, tp="rgb", overflow=self._args.sys_color_set.get_overflow())
                self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

        self.ps_color_changed.emit(True)
        # update_color_loc() is completed by 
        # self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color()) in main.py.

    def update_color_loc(self):
        """
        Update color set by overlabel. 
        """

        for idx in range(5):
            loc = self._color_locations[idx]

            if loc:
                shape = self._image3c.rgb_data.shape
                rgb = self._image3c.rgb_data[int(loc[1] * (shape[0] - 1))][int(loc[0] * (shape[1] - 1))]

                if not (rgb == self._args.sys_color_set[idx].rgb).all():
                    self._color_locations[idx] = None

        self.update()

    def freeze_image(self, value):
        """
        Freeze current image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        load_image = self._image3c.save_load_data(self._image3c.display)

        if load_image:
            self.open_image(load_image)

        else:
            self.warning(self._image_errs[5])

    def print_image(self, value):
        """
        Exec print image.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        name = "{}".format(time.strftime("Rickrack_Image_%Y_%m_%d.png", time.localtime()))

        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff *.webp);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff);; {} (*.webp)".format(*self._extend_descs)
        cb_file = QFileDialog.getSaveFileName(None, self._action_descs[2], os.sep.join((self._args.usr_image, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self._image3c.display.save(cb_file[0])

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
            load_image = self._image3c.save_load_data(clipboard.imageData())

            if load_image:
                self.open_image(load_image)

    def clipboard_img(self):
        """
        Set the image as the clipboard data by Ctrl + c.
        """

        if not (self.isVisible() and self._image3c.display):
            return

        mimedata = QMimeData()
        mimedata.setImageData(QPixmap.fromImage(self._image3c.display))

        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mimedata)

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._image_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._image_errs[3], QMessageBox.AcceptRole)

        box.exec_()

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

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Image", "Double click here to open an image."),
            _translate("Image", "Open"),
            _translate("Image", "Print"),
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
