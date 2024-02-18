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

from PyQt5.QtWidgets import QPushButton, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QCoreApplication
from wgets.general import SlideText, RGBHSVCkb, FoldingBox, SideWidget


class Transformation(SideWidget):
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
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._func_tr_()
        self._move_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._move_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._move_fbox, 1, 1, 1, 1)
        self.move_btns = []
        btn = QPushButton(self._move_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_up())
        btn = QPushButton(self._move_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 2, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_down())
        btn = QPushButton(self._move_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 1, 1, 1)
        btn.clicked.connect(lambda x: self.move_left())
        btn = QPushButton(self._move_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 3, 1, 1)
        btn.clicked.connect(lambda x: self.move_right())
        btn = QPushButton(self._move_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 1, 2, 1, 1)
        btn.clicked.connect(lambda x: self.reset_home())
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)
        self._zoom_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._zoom_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._zoom_fbox, 2, 1, 1, 1)
        btn = QPushButton(self._zoom_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 1, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_in())
        btn = QPushButton(self._zoom_fbox.gbox)
        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        self.move_btns.append(btn)
        btn.setStyleSheet("padding: 0px 0px 0px 0px;")
        gbox_grid_layout.addWidget(btn, 0, 3, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_out())
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 1, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 4, 1, 1)
        self._enhance_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._enhance_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._enhance_fbox, 3, 1, 1, 1)
        self.rhc_ehs = RGBHSVCkb(self._enhance_fbox.gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_ehs, 0, 1, 1, 3)
        self.ckb_reserve_ehs = QCheckBox(self._enhance_fbox.gbox)
        self.ckb_reserve_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_ehs, 1, 1, 1, 3)
        self.ckb_reserve_ehs.stateChanged.connect(self.sync_reserve)
        self.ckb_ubox_ehs = QCheckBox(self._enhance_fbox.gbox)
        self.ckb_ubox_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_ubox_ehs, 2, 1, 1, 3)
        self.ckb_onedir = QCheckBox(self._enhance_fbox.gbox)
        self.ckb_onedir.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_onedir, 3, 1, 1, 3)
        self.ckb_onedir.stateChanged.connect(self.change_dir)
        self.sdt_extd_ehs = SlideText(self._enhance_fbox.gbox, num_range=(0.0, 100.0), default_value=100.0)
        gbox_grid_layout.addWidget(self.sdt_extd_ehs, 4, 1, 1, 3)
        self.sdt_extd_ehs.ps_value_changed.connect(self.sync_extd)
        self.sdt_sepr_ehs = SlideText(self._enhance_fbox.gbox, num_range=(0.0, 100.0))
        gbox_grid_layout.addWidget(self.sdt_sepr_ehs, 5, 1, 1, 3)
        self.ckb_ubox_ehs.stateChanged.connect(lambda x: self.sdt_sepr_ehs.set_disabled(x))
        self.sdt_fact_ehs = SlideText(self._enhance_fbox.gbox, num_range=(0.0, 100.0))
        gbox_grid_layout.addWidget(self.sdt_fact_ehs, 6, 1, 1, 3)
        self.btn_enhs = QPushButton(self._enhance_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_enhs, 7, 1, 1, 3)
        self.btn_enhs.clicked.connect(self.emit_enhance)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 8, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 8, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 8, 4, 1, 1)
        self._inverse_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._inverse_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._inverse_fbox, 5, 1, 1, 1)
        self.rhc_inv = RGBHSVCkb(self._enhance_fbox.gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_inv, 0, 1, 1, 3)
        self.ckb_reserve_inv = QCheckBox(self._inverse_fbox.gbox)
        self.ckb_reserve_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_inv, 1, 1, 1, 3)
        self.ckb_reserve_inv.stateChanged.connect(self.sync_reserve)
        self.btn_invs = QPushButton(self._inverse_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_invs, 2, 1, 1, 3)
        self.btn_invs.clicked.connect(self.emit_inverse)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)
        self._replace_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._replace_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._replace_fbox, 4, 1, 1, 1)
        self.ckb_reserve_rep = QCheckBox(self._replace_fbox.gbox)
        self.ckb_reserve_rep.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_rep, 0, 1, 1, 3)
        self.ckb_reserve_rep.stateChanged.connect(self.sync_reserve)
        self.sdt_extd_rep = SlideText(self._replace_fbox.gbox, num_range=(0.0, 100.0), default_value=100.0)
        gbox_grid_layout.addWidget(self.sdt_extd_rep, 2, 1, 1, 3)
        self.sdt_extd_rep.ps_value_changed.connect(self.sync_extd)
        self.btn_replace_rgb = QPushButton(self._replace_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_replace_rgb, 4, 1, 1, 3)
        self.btn_replace_rgb.clicked.connect(lambda x: self.ps_replace.emit((1, self.ckb_reserve_rep.isChecked(), self.sdt_extd_rep.get_value() / 100.0)))
        self.btn_replace_hsv = QPushButton(self._replace_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_replace_hsv, 5, 1, 1, 3)
        self.btn_replace_hsv.clicked.connect(lambda x: self.ps_replace.emit((2, self.ckb_reserve_rep.isChecked(), self.sdt_extd_rep.get_value() / 100.0)))
        self.btn_replace_cancel = QPushButton(self._replace_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_replace_cancel, 6, 1, 1, 3)
        self.btn_replace_cancel.clicked.connect(lambda x: self.ps_replace.emit((0, None, None)))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 7, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 4, 1, 1)
        self._cover_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._cover_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._cover_fbox, 6, 1, 1, 1)
        self.rhc_cov = RGBHSVCkb(self._enhance_fbox.gbox, default_values=("r", "g", "b"), oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_cov, 0, 1, 1, 3)
        self.ckb_reserve_cov = QCheckBox(self._cover_fbox.gbox)
        self.ckb_reserve_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_cov, 1, 1, 1, 3)
        self.ckb_reserve_cov.stateChanged.connect(self.sync_reserve)
        self.btn_cover = QPushButton(self._cover_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_cover, 2, 1, 1, 3)
        self.btn_cover.clicked.connect(self.emit_cover)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)
        self.scroll_grid_layout.addItem(self.over_spacer, 7, 1, 1, 1)
        self._all_fboxes = (self._move_fbox, self._zoom_fbox, self._enhance_fbox, self._inverse_fbox, self._replace_fbox, self._cover_fbox)
        self.scroll_grid_layout.addWidget(self._exp_all_btn, 0, 1, 1, 1)
        self.connect_by_fboxes()
        self.update_text()

    def sizeHint(self):
        return QSize(250, 60)

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

    def change_dir(self, state):
        """
        Change one dir (same direction, -100 - 100) and bin dir (binary direction, 0 - 100).
        """

        val = abs(self.sdt_fact_ehs.get_value())

        if self.ckb_onedir.isChecked():
            self.sdt_fact_ehs.set_num_range((-100.0, 100.0))
            self.sdt_fact_ehs.set_value(val)

        else:
            self.sdt_fact_ehs.set_num_range((0.0, 100.0))
            self.sdt_fact_ehs.set_value(val)

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

            self.ps_enhance.emit(("enhance_rgb", tuple(region), tuple(separ), self.sdt_fact_ehs.get_value() / 100.0, self.ckb_reserve_ehs.isChecked(), self.sdt_extd_ehs.get_value() / 100.0, self.ckb_onedir.isChecked(), self._args.dep_wtp))
        else:
            for vl in checked_values:
                reg = {"h": 0, "s": 1, "v": 2}[vl]
                region.append(reg)
                sepr = self._args.sys_color_set[self._args.sys_activated_idx].hsv[reg]
                separ.append(sepr)

            if not self.ckb_ubox_ehs.isChecked():
                sepr = self.sdt_sepr_ehs.get_value() / 100.0
                separ = (sepr * 360.0, sepr, sepr)

            self.ps_enhance.emit(("enhance_hsv", tuple(region), tuple(separ), self.sdt_fact_ehs.get_value() / 100.0, self.ckb_reserve_ehs.isChecked(), self.sdt_extd_ehs.get_value() / 100.0, self.ckb_onedir.isChecked(), self._args.dep_wtp))

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

    def update_text(self):
        self.sw_update_text(force=True)
        self._move_fbox.set_title(self._gbox_descs[0])
        self._zoom_fbox.set_title(self._gbox_descs[1])
        self.sdt_sepr_ehs.set_text(self._enhance_descs[1])
        self.sdt_fact_ehs.set_text(self._enhance_descs[2])
        self.sdt_extd_ehs.set_text(self._enhance_descs[6])
        self.sdt_extd_rep.set_text(self._enhance_descs[6])
        self.ckb_ubox_ehs.setText(self._enhance_descs[10])
        self.ckb_onedir.setText(self._enhance_descs[11])
        self._replace_fbox.set_title(self._gbox_descs[2])
        self.ckb_reserve_rep.setText(self._enhance_descs[3])
        self.btn_replace_rgb.setText(self._replace_descs[0])
        self.btn_replace_hsv.setText(self._replace_descs[1])
        self.btn_replace_cancel.setText(self._replace_descs[2])
        self._enhance_fbox.set_title(self._gbox_descs[3])
        self.rhc_ehs.set_prefix_text((self._enhance_descs[0], self._enhance_descs[9]))
        self.ckb_reserve_ehs.setText(self._enhance_descs[3])
        self.btn_enhs.setText(self._enhance_descs[4])
        self._inverse_fbox.set_title(self._gbox_descs[4])
        self.rhc_inv.set_prefix_text((self._enhance_descs[0], self._enhance_descs[9]))
        self.ckb_reserve_inv.setText(self._enhance_descs[3])
        self.btn_invs.setText(self._enhance_descs[5])
        self._cover_fbox.set_title(self._gbox_descs[5])
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
            _translate("Transformation", "Same Direction"),
        )

        self._extend_descs = (
            _translate("Image", "All Images"),
            _translate("Image", "PNG Image"),
            _translate("Image", "BMP Image"),
            _translate("Image", "JPG Image"),
            _translate("Image", "TIF Image"),
        )

