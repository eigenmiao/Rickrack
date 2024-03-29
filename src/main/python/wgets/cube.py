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

from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QScrollArea, QFrame, QColorDialog, QApplication
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QMimeData, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from cguis.design.scroll_cube import Ui_ScrollCube
from ricore.color import Color, CTP
from ricore.transpt import get_link_tag, get_outer_box
from ricore.grid import gen_assit_color, gen_assit_args


class Square(QWidget):
    """
    Square objet based on QWidget. Init a color square in cube.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_index_changed = pyqtSignal(bool)

    def __init__(self, wget, args, idx):
        """
        Init color square.
        """

        super().__init__(wget)
        self._args = args
        self._idx = idx

    def paintEvent(self, event):
        if False: # self._args.sys_activated_assit_idx > len(self._args.sys_grid_assitlocs[self._args.sys_activated_idx]):
            self._args.sys_activated_assit_idx = -1

        rto = (1.0 - self._args.cubic_ratio) / 2
        self._box = (int(self.width() * rto) + self._args.positive_wid, self._args.positive_wid, int(self.width() * self._args.cubic_ratio - self._args.positive_wid * 2), self.height() - self._args.positive_wid * 2)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QColor(*self._args.sys_color_set[self._idx].rgb))
        painter.drawRect(*self._box)
        assit_len = len(self._args.sys_grid_assitlocs[self._idx])
        assit_w = self._box[2] / (assit_len + 1)
        assit_h = self._box[3] * 0.382
        start_w = self._box[0] + assit_w
        start_h = self._box[3] - assit_h
        self._assit_boxes = []
        self._assit_idx_seq = list(range(len(self._args.sys_grid_assitlocs[self._idx])))

        if self._args.sys_activated_assit_idx >= 0:
            self._assit_idx_seq = self._assit_idx_seq[self._args.sys_activated_assit_idx + 1: ] + self._assit_idx_seq[: self._args.sys_activated_assit_idx + 1]

        for assit_idx in self._assit_idx_seq:
            assit_box = (start_w + assit_w * assit_idx, start_h, assit_w, assit_h)
            assit_color = gen_assit_color(self._args.sys_color_set[self._idx], *self._args.sys_grid_assitlocs[self._idx][assit_idx][2:6])
            assit_frame_color = self._args.positive_color if self._idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx else self._args.negative_color
            self._assit_boxes.append(assit_box)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(*assit_color.rgb))
            painter.drawRect(*assit_box)

            if self._idx == self._args.sys_activated_idx and assit_idx == self._args.sys_activated_assit_idx:
                painter.setPen(QPen(QColor(*assit_frame_color), self._args.positive_wid))
                painter.setBrush(Qt.NoBrush)
                painter.drawRect(*assit_box)

            if not self._args.sys_grid_assitlocs[self._idx][assit_idx][5]:
                dot_box = get_outer_box((assit_box[0] + assit_box[2] / 5, assit_box[1] + assit_box[3] / 5), self._args.negative_wid)
                painter.setPen(QPen(Qt.NoPen))
                painter.setBrush(QBrush(QColor(*assit_frame_color)))
                painter.drawEllipse(*dot_box)

        if self._idx == self._args.sys_activated_idx:
            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

        else:
            painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(*self._box)

        if self._idx == self._args.sys_activated_idx and (self._args.sys_link_colors[0] or self._args.sys_link_colors[1]):
            link_box = (self._box[0], self._box[1], self._box[2] / 3.0, self._box[3] / 3.0)
            link_square_left, link_square_right, link_wid, link_line_start, link_line_end = get_link_tag(link_box)
            painter.setBrush(QBrush(Qt.NoBrush))
            painter.drawRoundedRect(*link_square_left, link_wid, link_wid)
            painter.drawRoundedRect(*link_square_right, link_wid, link_wid)
            painter.drawLine(QPoint(*link_line_start), QPoint(*link_line_end))

        painter.end()

    def mousePressEvent(self, event):
        if event.button() in (Qt.LeftButton, Qt.RightButton):
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                self._args.sys_activated_assit_idx = -1

                for seq_idx in range(len(self._assit_idx_seq)):
                    assit_box = self._assit_boxes[seq_idx]

                    if assit_box[0] < p_x < (assit_box[0] + assit_box[2]) and assit_box[1] < p_y < (assit_box[1] + assit_box[3]):
                        self._args.sys_activated_idx = self._idx
                        self._args.sys_activated_assit_idx = self._assit_idx_seq[seq_idx]
                        break

                if self._args.sys_activated_assit_idx < 0:
                    self._args.sys_activated_idx = self._idx
                    self._args.sys_activated_assit_idx = -1

                self.ps_index_changed.emit(True)
                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                if self._idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                    curr_color = gen_assit_color(self._args.sys_color_set[self._idx], *self._args.sys_grid_assitlocs[self._idx][self._args.sys_activated_assit_idx][2:6])

                else:
                    curr_color = self._args.sys_color_set[self._idx]

                dialog = QColorDialog.getColor(QColor(*curr_color.rgb))

                if dialog.isValid():
                    color = Color((dialog.red(), dialog.green(), dialog.blue()), tp=CTP.rgb, overflow=self._args.sys_color_set.get_overflow())

                    if self._idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                        self._args.sys_grid_assitlocs[self._idx][self._args.sys_activated_assit_idx][2:5] = gen_assit_args(self._args.sys_color_set[self._idx], color, self._args.sys_grid_assitlocs[self._idx][self._args.sys_activated_assit_idx][5])

                    else:
                        self._args.sys_color_set.modify(self._args.hm_rule, self._idx, color)

                    self.ps_color_changed.emit(True)
                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

class Cube(QWidget, Ui_ScrollCube):
    """
    Cube object based on QWidget. Init a color cube in table.
    """

    def __init__(self, wget, args, idx):
        """
        Init color cube.
        """

        super().__init__(wget)
        self.setupUi(self)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._idx = idx
        cube_grid_layout = QGridLayout(self.cube_color)
        cube_grid_layout.setContentsMargins(0, 0, 0, 0)
        cube_grid_layout.setHorizontalSpacing(0)
        cube_grid_layout.setVerticalSpacing(0)
        self.square = Square(self.cube_color, self._args, self._idx)
        cube_grid_layout.addWidget(self.square)
        self.hs_rgb = (self.hs_rgb_r, self.hs_rgb_g, self.hs_rgb_b)
        self.sp_rgb = (self.sp_rgb_r, self.sp_rgb_g, self.sp_rgb_b)
        self.hs_hsv = (self.hs_hsv_h, self.hs_hsv_s, self.hs_hsv_v)
        self.dp_hsv = (self.dp_hsv_h, self.dp_hsv_s, self.dp_hsv_v)

        for i in range(3):
            self.hs_rgb[i].wheelEvent = lambda event: event.ignore()
            self.hs_hsv[i].wheelEvent = lambda event: event.ignore()

    def paintEvent(self, event):
        wid = self.cube_color.width() * self._args.cubic_ratio
        self.cube_color.setMinimumHeight(wid * 0.618)
        self.cube_color.setMaximumHeight(wid * 0.618)

class CubeTable(QWidget):
    """
    CubeTable object based on QWidget. Init color cube table in result.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_history_backup = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init color cube table.
        """

        super().__init__(wget)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._updated_colors = False
        self.setMinimumSize(120, 10)
        cube_grid_layout = QGridLayout(self)
        cube_grid_layout.setContentsMargins(0, 0, 0, 0)
        cube_grid_layout.setHorizontalSpacing(0)
        cube_grid_layout.setVerticalSpacing(0)
        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        cube_grid_layout.addWidget(scroll_area)
        scroll_contents = QWidget()
        scroll_horizontal_layout = QHBoxLayout(scroll_contents)
        scroll_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(scroll_contents)
        self._cubes = (
            Cube(scroll_contents, args, 0),
            Cube(scroll_contents, args, 1),
            Cube(scroll_contents, args, 2),
            Cube(scroll_contents, args, 3),
            Cube(scroll_contents, args, 4),
        )

        self.update_color()

        for idx in (2, 1, 0, 3, 4):
            scroll_horizontal_layout.addWidget(self._cubes[idx])
            self._cubes[idx].square.ps_color_changed.connect(lambda x: self.update_color())
            self._cubes[idx].square.ps_color_changed.connect(lambda x: self.ps_history_backup.emit(True))
            self._cubes[idx].square.ps_index_changed.connect(lambda x: self.update_color())

            for ctp_idx in range(3):
                obj = self._cubes[idx].hs_rgb[ctp_idx]
                obj.valueChanged.connect(self.modify_color(idx, "direct", CTP.r + ctp_idx))
                obj.mouseReleaseEvent = lambda event: self.ps_history_backup.emit(True)
                obj = self._cubes[idx].sp_rgb[ctp_idx]
                obj.valueChanged.connect(self.modify_color(idx, "frdire", CTP.r + ctp_idx))

            for ctp_idx in range(3):
                obj = self._cubes[idx].hs_hsv[ctp_idx]
                obj.valueChanged.connect(self.modify_color(idx, "indire", CTP.h + ctp_idx))
                obj.mouseReleaseEvent = lambda event: self.ps_history_backup.emit(True)
                obj = self._cubes[idx].dp_hsv[ctp_idx]
                obj.valueChanged.connect(self.modify_color(idx, "frdire", CTP.h + ctp_idx))

            self._cubes[idx].le_hec.textChanged.connect(self.modify_color(idx, "frdire", CTP.hec))
        self.modify_box_visibility()

    def sizeHint(self):
        return QSize(600, 200)

    def resizeEvent(self, event):
        wid = self.geometry().width()

        if wid < 650 and self._cubes[0].sp_rgb_r.isVisible():
            for idx in (2, 1, 0, 3, 4):
                for ctp_idx in range(3):
                    obj = self._cubes[idx].sp_rgb[ctp_idx]
                    obj.setVisible(False)

                for ctp_idx in range(3):
                    obj = self._cubes[idx].dp_hsv[ctp_idx]
                    obj.setVisible(False)

        if wid > 650 and not self._cubes[0].sp_rgb_r.isVisible():
            for idx in (2, 1, 0, 3, 4):
                for ctp_idx in range(3):
                    obj = self._cubes[idx].sp_rgb[ctp_idx]
                    obj.setVisible(True)

                for ctp_idx in range(3):
                    obj = self._cubes[idx].dp_hsv[ctp_idx]
                    obj.setVisible(True)

        event.ignore()

    def modify_color(self, idx, kword, ctp):
        """
        Modify stored color set by slide and box name and value.
        """

        def _func_(value):
            if self._updated_colors:
                return

            if ctp == CTP.hec:
                value = Color.stri2color(value)

            if value == None:
                return

            self._updated_colors = True
            color = Color(self._args.sys_color_set[idx], tp=CTP.color, overflow=self._args.sys_color_set.get_overflow())

            if ctp == CTP.hec:
                color.setti(value, tp=CTP.color)

            else:
                if kword == "direct" or kword == "frdire":
                    color.setti(value, ctp)

                else:
                    color.setti(value / 1E3, ctp)

            self._args.sys_color_set.modify(self._args.hm_rule, idx, color)

            if kword == "frdire":
                self.update_color(skip_dp=(idx, ctp))
                self.ps_history_backup.emit(True)

            else:
                self.update_color()

            self._updated_colors = False
        return _func_

    def update_color(self, skip_dp=None):
        """
        Update all colors.
        """

        self._updated_colors = True

        for lc_idx in range(5):
            if lc_idx == self._args.sys_activated_idx and self._args.sys_activated_assit_idx >= 0:
                curr_color = gen_assit_color(self._args.sys_color_set[lc_idx], *self._args.sys_grid_assitlocs[lc_idx][self._args.sys_activated_assit_idx][2:6])

            else:
                curr_color = self._args.sys_color_set[lc_idx]

            curr_hec = curr_color.getti(CTP.hec)
            curr_hsv = curr_color.getti(CTP.hsv)

            if curr_hec == self._cubes[lc_idx].le_hec.text() and curr_hsv[1] > 0.01 and 0.99 > curr_hsv[2] > 0.01:
                continue

            if not (skip_dp and skip_dp[0] == lc_idx and skip_dp[1] == CTP.hec):
                self._cubes[lc_idx].le_hec.setText(curr_hec)

            for lc_ctp_idx in range(3):
                lc_ctp = CTP.r + lc_ctp_idx
                obj = self._cubes[lc_idx].hs_rgb[lc_ctp_idx]
                obj.setValue(curr_color.getti(lc_ctp))

                if not (skip_dp and skip_dp[0] == lc_idx and skip_dp[1] == lc_ctp):
                    obj = self._cubes[lc_idx].sp_rgb[lc_ctp_idx]
                    obj.setValue(curr_color.getti(lc_ctp))

            for lc_ctp_idx in range(3):
                lc_ctp = CTP.h + lc_ctp_idx
                obj = self._cubes[lc_idx].hs_hsv[lc_ctp_idx]
                obj.setValue(curr_hsv[lc_ctp_idx] * 1E3)

                if not (skip_dp and skip_dp[0] == lc_idx and skip_dp[1] == lc_ctp):
                    obj = self._cubes[lc_idx].dp_hsv[lc_ctp_idx]
                    obj.setValue(curr_hsv[lc_ctp_idx])

        self.update_index()
        self._updated_colors = False

    def update_index(self):
        """
        Update color activated index. Undertake func update_color.
        """

        for lc_idx in range(5):
            self._cubes[lc_idx].update()

        self.ps_color_changed.emit(True)

    def modify_rule(self):
        """
        Modify stored color set by rule selection.
        """

        self._args.sys_color_set.create(self._args.hm_rule)
        self.update_color()
        self.ps_history_backup.emit(True)

    def create_set(self, direct=False):
        """
        Create stored color set by create button.
        """

        if not direct and True in [bool(i) for i in self._args.sys_grid_assitlocs]:
            self._args.sys_grid_assitlocs = [[], [], [], [], []]
            self._args.sys_assit_color_locs = [[], [], [], [], []]
            self._args.sys_activated_assit_idx = -1

        else:
            self._args.sys_color_set.initialize()
            self._args.sys_color_set.create(self._args.hm_rule)

        self.update_color()
        self.ps_history_backup.emit(True)

    def modify_box_visibility(self):
        """
        Modify the visibility of hsv or rgb cbox.
        """

        for i in range(5):
            self._cubes[i].gbox_hsv.setVisible(self._args.show_hsv)
            self._cubes[i].gbox_rgb.setVisible(self._args.show_rgb)

    def update_all(self):
        """
        Update five cubes and cube table.
        """

        for lc_idx in range(5):
            self._cubes[lc_idx].update()

        self.update()

    def clipboard_act(self, ctp):
        """
        Set the rgb, hsv or hec (hex code) of activated tag color as the clipboard data by shortcut r, h or c.
        """

        def _func_():
            color = self._args.sys_color_set[self._args.sys_activated_idx].getti(ctp)

            if ctp == CTP.hec:
                color = self._args.hec_prefix[0] + str(color) + self._args.hec_prefix[1]

            else:
                color = self._args.rgb_prefix[1].join([self._args.r_prefix[0] + str(color[coi]) + self._args.r_prefix[1] for coi in range(3)])
                color = self._args.rgb_prefix[0] + color + self._args.rgb_prefix[2]

            mimedata = QMimeData()
            mimedata.setText(color)
            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mimedata)

        return _func_

    def active_by_num(self, idx):
        """
        Set activated idx by shortcut 1, 2, 3, 4 and 5.
        """

        def _func_():
            self._args.sys_activated_idx = idx
            self._args.sys_activated_assit_idx = -1
            self.update_index()

        return _func_
