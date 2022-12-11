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
from ricore.color import Color
from ricore.transpt import get_link_tag


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

        # load args.
        self._args = args
        self._idx = idx

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        rto = (1.0 - self._args.cubic_ratio) / 2

        self._box = (self.width() * rto, self.height() * rto, self.width() * self._args.cubic_ratio, self.height() * self._args.cubic_ratio)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self._idx == self._args.sys_activated_idx:
            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid * 1.5))

        else:
            painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid * 1.5))

        painter.setBrush(QColor(*self._args.sys_color_set[self._idx].rgb))
        painter.drawRect(*self._box)

        if self._idx == self._args.sys_activated_idx and (self._args.sys_link_colors[0] or self._args.sys_link_colors[1]):
            link_box = (self._box[0], self._box[1], self._box[2] / 3.0, self._box[3] / 3.0)
            link_square_left, link_square_right, link_wid, link_line_start, link_line_end = get_link_tag(link_box)

            painter.setBrush(QBrush(Qt.NoBrush))
            painter.drawRoundedRect(*link_square_left, link_wid, link_wid)
            painter.drawRoundedRect(*link_square_right, link_wid, link_wid)
            painter.drawLine(QPoint(*link_line_start), QPoint(*link_line_end))

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                self._args.sys_activated_idx = self._idx

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
                dialog = QColorDialog.getColor(QColor(*self._args.sys_color_set[self._idx].rgb))

                if dialog.isValid():
                    color = Color((dialog.red(), dialog.green(), dialog.blue()), tp="rgb", overflow=self._args.sys_color_set.get_overflow())
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

        # set attr.
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        # load args.
        self._args = args
        self._idx = idx

        # init qt args.
        cube_grid_layout = QGridLayout(self.cube_color)
        cube_grid_layout.setContentsMargins(0, 0, 0, 0)
        cube_grid_layout.setHorizontalSpacing(0)
        cube_grid_layout.setVerticalSpacing(0)

        self.square = Square(self.cube_color, self._args, self._idx)
        cube_grid_layout.addWidget(self.square)

        for tp in ("r", "g", "b"):
            getattr(self, "hs_rgb_{}".format(tp)).wheelEvent = lambda event: event.ignore()

        for tp in ("h", "s", "v"):
            getattr(self, "hs_hsv_{}".format(tp)).wheelEvent = lambda event: event.ignore()

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.cube_color.width()
        self.cube_color.setMinimumHeight(wid * 0.618)
        self.cube_color.setMaximumHeight(wid * 0.618)


class CubeTable(QWidget):
    """
    CubeTable object based on QWidget. Init color cube table in result.
    """

    ps_color_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init color cube table.
        """

        super().__init__(wget)

        # set attr.
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        # load args.
        self._args = args
        self._updated_colors = False

        # init qt args.
        self.setMinimumSize(640, 10)

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
            self._cubes[idx].square.ps_index_changed.connect(lambda x: self.update_index())

            for ctp in ("r", "g", "b"):
                obj = getattr(self._cubes[idx], "hs_rgb_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "direct", ctp))
                obj = getattr(self._cubes[idx], "sp_rgb_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "frdire", ctp))

            for ctp in ("h", "s", "v"):
                obj = getattr(self._cubes[idx], "hs_hsv_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "indire", ctp))
                obj = getattr(self._cubes[idx], "dp_hsv_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "frdire", ctp))

            self._cubes[idx].le_hec.textChanged.connect(self.modify_color(idx, "direct", "hec"))

        self.modify_box_visibility()

    def sizeHint(self):
        return QSize(600, 150)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def modify_color(self, idx, kword, ctp):
        """
        Modify stored color set by slide and box name and value.
        """

        def _func_(value):
            if self._updated_colors:
                return

            if ctp == "hec":
                try:
                    value = Color.fmt_hec(value)

                except Exception as err:
                    return

            self._updated_colors = True

            color = Color(self._args.sys_color_set[idx], tp="color", overflow=self._args.sys_color_set.get_overflow())
            if kword == "direct" or kword == "frdire":
                color.setti(value, ctp)

            else:
                color.setti(value / 1E3, ctp)

            self._args.sys_color_set.modify(self._args.hm_rule, idx, color)

            if kword == "frdire":
                self.update_color(skip_dp=(idx, ctp))

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
            for lc_ctp in ("r", "g", "b"):
                obj = getattr(self._cubes[lc_idx], "hs_rgb_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))

                if not (skip_dp and skip_dp[0] == lc_idx and skip_dp[1] == lc_ctp):
                    obj = getattr(self._cubes[lc_idx], "sp_rgb_{}".format(lc_ctp))
                    obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))

            for lc_ctp in ("h", "s", "v"):
                obj = getattr(self._cubes[lc_idx], "hs_hsv_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp) * 1E3)

                if not (skip_dp and skip_dp[0] == lc_idx and skip_dp[1] == lc_ctp):
                    obj = getattr(self._cubes[lc_idx], "dp_hsv_{}".format(lc_ctp))
                    obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))

            self._cubes[lc_idx].le_hec.setText(self._args.sys_color_set[lc_idx].getti("hec"))

        self.update_index()

        self._updated_colors = False

    def update_index(self):
        """
        Update color activated index.
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

    def create_set(self):
        """
        Create stored color set by create button.
        """

        self._args.sys_color_set.initialize()
        self._args.sys_color_set.create(self._args.hm_rule)
        self.update_color()

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

    def active_by_num(self, idx):
        """
        Set activated idx by shortcut 1, 2, 3, 4 and 5.
        """

        def _func_():
            self._args.sys_activated_idx = idx
            self.update_index()

        return _func_
