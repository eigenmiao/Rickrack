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

from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QRadioButton
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QCoreApplication
from wgets.general import SlideText, RGBHSVCkb, FoldingBox, SideWidget


class Mode(SideWidget):
    """
    Mode object based on QWidget. Init a mode in mode.
    """

    ps_mode_changed = pyqtSignal(bool)
    ps_assistp_changed = pyqtSignal(bool)
    ps_info_changed = pyqtSignal(bool)
    ps_color_spc_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init mode.
        """

        super().__init__(wget)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._func_tr_()
        self._color_spc_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._color_spc_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._color_spc_fbox, 1, 1, 1, 1)
        self._color_spc_btns = []

        for i in range(4):
            btn = QRadioButton(self._color_spc_fbox.gbox)
            gbox_grid_layout.addWidget(btn, i, 1, 1, 1)
            btn.clicked.connect(self.modify_color_spc(i))
            self._color_spc_btns.append(btn)

        self._color_spc_btns[self._args.color_spc].setChecked(True)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 4, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 2, 1, 1)
        self._info_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._info_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._info_fbox, 2, 1, 1, 1)
        self._cbox_major = QCheckBox(self._info_fbox.gbox)
        self._cbox_major.setText("Major")
        gbox_grid_layout.addWidget(self._cbox_major, 0, 1, 1, 1)
        self._cbox_major.stateChanged.connect(lambda x: self.ps_info_changed.emit(x))
        self._cbox_minor = QCheckBox(self._info_fbox.gbox)
        self._cbox_minor.setText("Minor")
        gbox_grid_layout.addWidget(self._cbox_minor, 1, 1, 1, 1)
        self._cbox_minor.stateChanged.connect(lambda x: self.ps_info_changed.emit(x))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._display_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._display_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._display_fbox, 3, 1, 1, 1)
        self._cbox_rgb = QCheckBox(self._display_fbox.gbox)
        self._cbox_rgb.setText("RGB")
        gbox_grid_layout.addWidget(self._cbox_rgb, 0, 1, 1, 1)
        self._cbox_rgb.stateChanged.connect(self.modify_state("rgb"))
        self._cbox_hsv = QCheckBox(self._display_fbox.gbox)
        self._cbox_hsv.setText("HSV")
        gbox_grid_layout.addWidget(self._cbox_hsv, 1, 1, 1, 1)
        self._cbox_hsv.stateChanged.connect(self.modify_state("hsv"))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._gridvls_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._gridvls_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._gridvls_fbox, 4, 1, 1, 1)
        self.rhc_govalue = RGBHSVCkb(self._gridvls_fbox.gbox, oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_govalue, 0, 1, 1, 1)
        self.rhc_govalue.ps_value_changed.connect(self.modify_grid_value("ctp", tuple))
        self.ckb_rev_grid = QCheckBox(self._gridvls_fbox.gbox)
        self.ckb_rev_grid.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_rev_grid, 1, 1, 1, 1)
        self.ckb_rev_grid.stateChanged.connect(self.modify_grid_value("rev_grid", bool))
        self.sdt_col = SlideText(self._gridvls_fbox.gbox, num_range=(1, 51), maxlen=50, interval=10, step=1, decimals=0, default_value=9)
        gbox_grid_layout.addWidget(self.sdt_col, 2, 1, 1, 1)
        self.sdt_col.ps_value_changed.connect(self.modify_grid_value("col", int))
        self.sdt_sum_factor = SlideText(self._gridvls_fbox.gbox, num_range=(0.0, 5.0), default_value=1.0)
        gbox_grid_layout.addWidget(self.sdt_sum_factor, 3, 1, 1, 1)
        self.sdt_sum_factor.ps_value_changed.connect(self.modify_grid_value("sum_factor", float))
        self.sdt_dim_factor = SlideText(self._gridvls_fbox.gbox, num_range=(0.0, 1.0), default_value=1.0)
        gbox_grid_layout.addWidget(self.sdt_dim_factor, 4, 1, 1, 1)
        self.sdt_dim_factor.ps_value_changed.connect(self.modify_grid_value("dim_factor", float))
        self.sdt_assist_factor = SlideText(self._gridvls_fbox.gbox, num_range=(0.0, 1.0), default_value=0.6)
        gbox_grid_layout.addWidget(self.sdt_assist_factor, 5, 1, 1, 1)
        self.sdt_assist_factor.ps_value_changed.connect(self.modify_grid_value("assist_factor", float))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 6, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 2, 1, 1)
        self.scroll_grid_layout.addItem(self.over_spacer, 5, 1, 1, 1)
        self._all_fboxes = (self._color_spc_fbox, self._info_fbox, self._display_fbox, self._gridvls_fbox)
        self.scroll_grid_layout.addWidget(self._exp_all_btn, 0, 1, 1, 1)
        self.connect_by_fboxes()
        self.update_text()

    def sizeHint(self):
        return QSize(250, 60)

    def modify_state(self, tag):
        """
        Modify stored shown state set by cbox.
        """

        def _func_(state):
            setattr(self._args, "show_{}".format(tag), bool(state))
            self.ps_mode_changed.emit(True)

        return _func_

    def update_mode(self):
        """
        Update mode cbox by self._args.show_rgb and show_hsv.
        """

        self._cbox_rgb.setChecked(self._args.show_rgb)
        self._cbox_hsv.setChecked(self._args.show_hsv)
        self._color_spc_btns[self._args.color_spc].setChecked(True)

    def modify_color_spc(self, idx):
        """
        Modify stored color system by btn.
        """

        def _func_(value):
            self._args.modify_settings("color_spc", idx)
            self.ps_color_spc_changed.emit(True)

        return _func_

    def get_info(self):
        """
        Get value of cbox of self._args.show_info_pts.
        """

        return int(self._cbox_major.isChecked()) + int(self._cbox_minor.isChecked()) * 2

    def update_info(self, major, minor):
        """
        Update mode cbox by self._args.show_info_pts.
        """

        self._cbox_major.stateChanged.disconnect()
        self._cbox_minor.stateChanged.disconnect()
        self._cbox_major.setChecked(major)
        self._cbox_minor.setChecked(minor)
        self._cbox_major.stateChanged.connect(lambda x: self.ps_info_changed.emit(x))
        self._cbox_minor.stateChanged.connect(lambda x: self.ps_info_changed.emit(x))

    def modify_grid_value(self, name, dtype=float):
        """
        Modify a grid values.
        """

        def _func_(value):
            self._args.sys_grid_values[name] = dtype(value)
            self.ps_assistp_changed.emit(True)

        return _func_

    def update_grid_vales(self):
        """
        Update grid values.
        """

        self.rhc_govalue.set_values(self._args.sys_grid_values["ctp"])
        self.sdt_col.set_value(self._args.sys_grid_values["col"])
        self.sdt_sum_factor.set_value(self._args.sys_grid_values["sum_factor"])
        self.sdt_dim_factor.set_value(self._args.sys_grid_values["dim_factor"])
        self.sdt_assist_factor.set_value(self._args.sys_grid_values["assist_factor"])
        self.ckb_rev_grid.setChecked(self._args.sys_grid_values["rev_grid"])

    def update_text(self):
        self.sw_update_text(force=True)
        self._display_fbox.set_title(self._gbox_descs[0])
        self._gridvls_fbox.set_title(self._gbox_descs[2])
        self._info_fbox.set_title(self._gbox_descs[3])
        self._color_spc_fbox.set_title(self._gbox_descs[4])
        self._cbox_major.setText(self._info_descs[0])
        self._cbox_minor.setText(self._info_descs[1])
        self.rhc_govalue.set_prefix_text((self._assistp_descs[0], self._assistp_descs[1]))
        self.sdt_col.set_text(self._assistp_descs[3])
        self.sdt_sum_factor.set_text(self._assistp_descs[4])
        self.sdt_dim_factor.set_text(self._assistp_descs[5])
        self.sdt_assist_factor.set_text(self._assistp_descs[6])
        self.ckb_rev_grid.setText(self._assistp_descs[7])

        for i in range(4):
            self._color_spc_btns[i].setText(self._color_spc_descs[i])

        self.update_mode()

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._gbox_descs = (
            _translate("Mode", "Display"),
            _translate("Mode", "Assistant"),
            _translate("Mode", "Grid"),
            _translate("Mode", "Info"),
            _translate("Mode", "Color Space"),
        )

        self._info_descs = (
            _translate("Mode", "Show Major Info"),
            _translate("Mode", "Show Minor Info"),
        )

        self._color_spc_descs = (
            _translate("Mode", "RGB Space"),
            _translate("Mode", "Rev RGB Space"),
            _translate("Mode", "RYB Space"),
            _translate("Mode", "Rev RYB Space"),
        )

        self._assistp_descs = (
            _translate("Mode", "Select"),
            _translate("Mode", "Selected: "),
            _translate("Mode", "Value - "),
            _translate("Mode", "Column - "),
            _translate("Mode", "Sum F - "),
            _translate("Mode", "Dim F - "),
            _translate("Mode", "Asst F - "),
            _translate("Mode", "Reverse Grid"),
        )

