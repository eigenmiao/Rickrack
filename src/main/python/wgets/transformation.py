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

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QCoreApplication
from wgets.general import SlideText, RGBHSVCkb


class Transformation(QWidget):
    """
    Transformation object based on QWidget. Init a transformation in transformation.
    """

    ps_move = pyqtSignal(tuple)
    ps_zoom = pyqtSignal(float)
    ps_home = pyqtSignal(bool)
    ps_replace = pyqtSignal(tuple)
    ps_enhance = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init transformation.
        """

        super().__init__(wget)

        # set attr.
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        transf_grid_layout = QGridLayout(self)
        transf_grid_layout.setContentsMargins(0, 0, 0, 0)
        transf_grid_layout.setHorizontalSpacing(0)
        transf_grid_layout.setVerticalSpacing(0)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        transf_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(3, 9, 3, 3)
        scroll_grid_layout.setHorizontalSpacing(3)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        # move functional region.
        self._move_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._move_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(6)
        gbox_grid_layout.setVerticalSpacing(6)
        scroll_grid_layout.addWidget(self._move_gbox, 0, 1, 1, 1)

        self._move_btns = []

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_up())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 2, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_down())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 1, 1, 1)
        btn.clicked.connect(lambda x: self.move_left())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 3, 1, 1)
        btn.clicked.connect(lambda x: self.move_right())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 2, 1, 1)
        btn.clicked.connect(lambda x: self.reset_home())

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)

        # zoom functional region.
        self._zoom_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._zoom_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(6)
        gbox_grid_layout.setVerticalSpacing(6)
        scroll_grid_layout.addWidget(self._zoom_gbox, 1, 1, 1, 1)

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 1, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_in())

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self._move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 3, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_out())

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 1, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 4, 1, 1)

        # enhance functional region.
        self._enhance_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._enhance_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._enhance_gbox, 2, 1, 1, 1)

        self.rhc_ehs = RGBHSVCkb(self._enhance_gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_ehs, 0, 1, 1, 3)

        self.ckb_reserve_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_reserve_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_ehs, 1, 1, 1, 3)
        self.ckb_reserve_ehs.stateChanged.connect(self.sync_reserve)

        self.ckb_ubox_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_ubox_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_ubox_ehs, 2, 1, 1, 3)

        self.sdt_extd_ehs = SlideText(self._enhance_gbox, num_range=(0.0, 100.0), default_value=100.0)
        gbox_grid_layout.addWidget(self.sdt_extd_ehs, 3, 1, 1, 3)
        self.sdt_extd_ehs.ps_value_changed.connect(self.sync_extd)

        self.sdt_sepr_ehs = SlideText(self._enhance_gbox, num_range=(0.0, 100.0))
        gbox_grid_layout.addWidget(self.sdt_sepr_ehs, 4, 1, 1, 3)
        self.ckb_ubox_ehs.stateChanged.connect(lambda x: self.sdt_sepr_ehs.set_disabled(x))

        self.sdt_fact_ehs = SlideText(self._enhance_gbox, num_range=(0.0, 100.0))
        gbox_grid_layout.addWidget(self.sdt_fact_ehs, 5, 1, 1, 3)

        self.btn_enhs = QPushButton(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.btn_enhs, 6, 1, 1, 3)
        self.btn_enhs.clicked.connect(self.emit_enhance)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 7, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 4, 1, 1)

        # inverse functional region.
        self._inverse_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._inverse_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._inverse_gbox, 3, 1, 1, 1)

        self.rhc_inv = RGBHSVCkb(self._enhance_gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_inv, 0, 1, 1, 3)

        self.ckb_reserve_inv = QCheckBox(self._inverse_gbox)
        self.ckb_reserve_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_inv, 1, 1, 1, 3)
        self.ckb_reserve_inv.stateChanged.connect(self.sync_reserve)

        self.btn_invs = QPushButton(self._inverse_gbox)
        gbox_grid_layout.addWidget(self.btn_invs, 2, 1, 1, 3)
        self.btn_invs.clicked.connect(self.emit_inverse)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)

        """
        -> Tag: This segment is deleted.

        # replace functional region.
        self._replace_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._replace_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._replace_gbox, 4, 1, 1, 1)

        self.ckb_reserve_rep = QCheckBox(self._replace_gbox)
        self.ckb_reserve_rep.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_rep, 0, 1, 1, 3)
        self.ckb_reserve_rep.stateChanged.connect(self.sync_reserve)

        self.ckb_uold_rep = QCheckBox(self._replace_gbox)
        self.ckb_uold_rep.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_uold_rep, 1, 1, 1, 3)

        self.sdt_extd_rep = SlideText(self._replace_gbox, num_range=(0.0, 100.0), default_value=100.0)
        gbox_grid_layout.addWidget(self.sdt_extd_rep, 2, 1, 1, 3)
        self.sdt_extd_rep.ps_value_changed.connect(self.sync_extd)

        self.sdt_scal_rep = SlideText(self._replace_gbox, num_range=(0.0, 100.0), default_value=100.0)
        gbox_grid_layout.addWidget(self.sdt_scal_rep, 3, 1, 1, 3)

        self.btn_replace_rgb = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_rgb, 4, 1, 1, 3)
        self.btn_replace_rgb.clicked.connect(lambda x: self.ps_replace.emit((1, self.ckb_reserve_rep.isChecked(), self.sdt_extd_rep.get_value() / 100.0, self.sdt_scal_rep.get_value() / 100.0, self.ckb_uold_rep.isChecked())))

        self.btn_replace_hsv = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_hsv, 5, 1, 1, 3)
        self.btn_replace_hsv.clicked.connect(lambda x: self.ps_replace.emit((2, self.ckb_reserve_rep.isChecked(), self.sdt_extd_rep.get_value() / 100.0, self.sdt_scal_rep.get_value() / 100.0, self.ckb_uold_rep.isChecked())))

        self.btn_replace_cancel = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_cancel, 6, 1, 1, 3)
        self.btn_replace_cancel.clicked.connect(lambda x: self.ps_replace.emit((0, None, None)))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 7, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 4, 1, 1)
        """

        # cover functional region.
        self._cover_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._cover_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._cover_gbox, 5, 1, 1, 1)

        self.rhc_cov = RGBHSVCkb(self._enhance_gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_cov, 0, 1, 1, 3)

        self.ckb_reserve_cov = QCheckBox(self._cover_gbox)
        self.ckb_reserve_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_cov, 1, 1, 1, 3)
        self.ckb_reserve_cov.stateChanged.connect(self.sync_reserve)

        self.btn_cover = QPushButton(self._cover_gbox)
        gbox_grid_layout.addWidget(self.btn_cover, 2, 1, 1, 3)
        self.btn_cover.clicked.connect(self.emit_cover)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(210, 60)

    def move_up(self):
        """
        Move image up.
        """

        self.ps_move.emit((0, self._args.move_step * -1))

    def move_down(self):
        """
        Move image down.
        """

        self.ps_move.emit((0, self._args.move_step))

    def move_left(self):
        """
        Move image left.
        """

        self.ps_move.emit((self._args.move_step * -1, 0))

    def move_right(self):
        """
        Move image right.
        """

        self.ps_move.emit((self._args.move_step, 0))

    def reset_home(self):
        self.ps_home.emit(True)

    def zoom_in(self):
        self.ps_zoom.emit(self._args.zoom_step)

    def zoom_out(self):
        self.ps_zoom.emit(1 / self._args.zoom_step)

    def sync_reserve(self, state):
        """
        Sync enhance, inverse and replace reserve boxes.
        """

        if state != self.ckb_reserve_ehs.isChecked():
            self.ckb_reserve_ehs.setChecked(state)

        if state != self.ckb_reserve_inv.isChecked():
            self.ckb_reserve_inv.setChecked(state)

        if state != self.ckb_reserve_rep.isChecked():
            self.ckb_reserve_rep.setChecked(state)

        if state != self.ckb_reserve_cov.isChecked():
            self.ckb_reserve_cov.setChecked(state)

    def sync_extd(self, value):
        """
        Sync enhance and replace extd sdr.
        """

        if self.sdt_extd_ehs.get_value() != value:
            self.sdt_extd_ehs.set_value(value)

        if self.sdt_extd_rep.get_value() != value:
            self.sdt_extd_rep.set_value(value)

    def emit_enhance(self, value):
        """
        Emit enhance.
        """

        region = []
        separ = []

        checked_values = self.rhc_ehs.get_values()

        if not checked_values:
            return

        if checked_values[0] in ("r", "g", "b"):
            for vl in checked_values:
                reg = {"r": 0, "g": 1, "b": 2}[vl]
                region.append(reg)

                sepr = self._args.sys_color_set[self._args.sys_activated_idx].rgb[reg]
                separ.append(sepr)

            if not self.ckb_ubox_ehs.isChecked():
                sepr = self.sdt_sepr_ehs.get_value() / 100.0
                separ = (sepr * 255.0, sepr * 255.0, sepr * 255.0)

            self.ps_enhance.emit(("enhance_rgb", tuple(region), tuple(separ), self.sdt_fact_ehs.get_value() / 100.0, self.ckb_reserve_ehs.isChecked(), self.sdt_extd_ehs.get_value() / 100.0))

        else:
            for vl in checked_values:
                reg = {"h": 0, "s": 1, "v": 2}[vl]
                region.append(reg)

                sepr = self._args.sys_color_set[self._args.sys_activated_idx].hsv[reg]
                separ.append(sepr)

            if not self.ckb_ubox_ehs.isChecked():
                sepr = self.sdt_sepr_ehs.get_value() / 100.0
                separ = (sepr * 360.0, sepr, sepr)

            self.ps_enhance.emit(("enhance_hsv", tuple(region), tuple(separ), self.sdt_fact_ehs.get_value() / 100.0, self.ckb_reserve_ehs.isChecked(), self.sdt_extd_ehs.get_value() / 100.0))

    def emit_inverse(self, value):
        """
        Emit inverse.
        """

        region = set()
        checked_values = self.rhc_inv.get_values()

        if not checked_values:
            return

        if checked_values[0] in ("r", "g", "b"):
            for vl in checked_values:
                region.add({"r": 0, "g": 1, "b": 2}[vl])

            self.ps_enhance.emit(("inverse_rgb", region, self.ckb_reserve_inv.isChecked()))

        else:
            for vl in checked_values:
                region.add({"h": 0, "s": 1, "v": 2}[vl])

            self.ps_enhance.emit(("inverse_hsv", region, self.ckb_reserve_inv.isChecked()))

    def emit_cover(self, value):
        """
        Emit cover.
        """

        region = set()
        checked_values = self.rhc_cov.get_values()

        if not checked_values:
            return

        if checked_values[0] in ("r", "g", "b"):
            for vl in checked_values:
                region.add({"r": 0, "g": 1, "b": 2}[vl])

            self.ps_enhance.emit(("cover_rgb", region, self.ckb_reserve_cov.isChecked()))

        else:
            for vl in checked_values:
                region.add({"h": 0, "s": 1, "v": 2}[vl])

            self.ps_enhance.emit(("cover_hsv", region, self.ckb_reserve_cov.isChecked()))

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._move_gbox.setTitle(self._gbox_descs[0])
        self._zoom_gbox.setTitle(self._gbox_descs[1])

        for i in range(7):
            self._move_btns[i].setText(self._move_descs[i])

        self.sdt_sepr_ehs.set_text(self._enhance_descs[1])
        self.sdt_fact_ehs.set_text(self._enhance_descs[2])
        self.sdt_extd_ehs.set_text(self._enhance_descs[6])
        self.ckb_ubox_ehs.setText(self._enhance_descs[10])

        self._enhance_gbox.setTitle(self._gbox_descs[3])
        self.rhc_ehs.set_prefix_text((self._enhance_descs[0], self._enhance_descs[9]))
        self.ckb_reserve_ehs.setText(self._enhance_descs[3])
        self.btn_enhs.setText(self._enhance_descs[4])

        self._inverse_gbox.setTitle(self._gbox_descs[4])
        self.rhc_inv.set_prefix_text((self._enhance_descs[0], self._enhance_descs[9]))
        self.ckb_reserve_inv.setText(self._enhance_descs[3])
        self.btn_invs.setText(self._enhance_descs[5])

        self._cover_gbox.setTitle(self._gbox_descs[5])
        self.rhc_cov.set_prefix_text((self._enhance_descs[0], self._enhance_descs[9]))
        self.ckb_reserve_cov.setText(self._enhance_descs[3])
        self.btn_cover.setText(self._enhance_descs[8])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Transformation", "Move"),
            _translate("Transformation", "Zoom"),
            _translate("Transformation", "Replace"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
            _translate("Transformation", "Cover"),
        )

        self._move_descs = (
            _translate("Transformation", "U"),
            _translate("Transformation", "D"),
            _translate("Transformation", "L"),
            _translate("Transformation", "R"),
            _translate("Transformation", "H"),
            _translate("Transformation", "I"),
            _translate("Transformation", "O"),
        )

        self._replace_descs = (
            _translate("Transformation", "Replace RGB"),
            _translate("Transformation", "Replace HSV"),
            _translate("Transformation", "Cancel"),
            _translate("Transformation", "Use Old Algorithm"),
        )

        self._enhance_descs = (
            _translate("Transformation", "Link"),
            _translate("Transformation", "Space - "),
            _translate("Transformation", "Factor - "),
            _translate("Transformation", "Reserve Result"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
            _translate("Transformation", "Width - "),
            _translate("Transformation", "Spread - "),
            _translate("Transformation", "Cover"),
            _translate("Transformation", "Linked: "),
            _translate("Transformation", "Use Result Color"),
        )

        self._extend_descs = (
            _translate("Image", "All Images"),
            _translate("Image", "PNG Image"),
            _translate("Image", "BMP Image"),
            _translate("Image", "JPG Image"),
            _translate("Image", "TIF Image"),
        )
