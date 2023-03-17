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

from PySide2.QtWidgets import QWidget, QCheckBox, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy
from PySide2.QtCore import Qt, QSize, Signal, QCoreApplication
from wgets.general import SlideText, RGBHSVCkb


class Mode(QWidget):
    """
    Mode object based on QWidget. Init a mode in mode.
    """

    ps_mode_changed = Signal(bool)
    ps_assistp_changed = Signal(bool)

    def __init__(self, wget, args):
        """
        Init mode.
        """

        super().__init__(wget)

        # set attr.
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        mode_grid_layout = QGridLayout(self)
        mode_grid_layout.setContentsMargins(0, 0, 0, 0)
        mode_grid_layout.setHorizontalSpacing(0)
        mode_grid_layout.setVerticalSpacing(0)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        mode_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(3, 9, 3, 3)
        scroll_grid_layout.setHorizontalSpacing(3)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        # display functional region.
        self._display_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._display_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._display_gbox, 0, 1, 1, 1)

        self._cbox_rgb = QCheckBox(self._display_gbox)
        self._cbox_rgb.setText("RGB")
        gbox_grid_layout.addWidget(self._cbox_rgb, 0, 1, 1, 1)
        self._cbox_rgb.stateChanged.connect(self.modify_state("rgb"))

        self._cbox_hsv = QCheckBox(self._display_gbox)
        self._cbox_hsv.setText("HSV")
        gbox_grid_layout.addWidget(self._cbox_hsv, 1, 1, 1, 1)
        self._cbox_hsv.stateChanged.connect(self.modify_state("hsv"))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)

        """
        -> Tag: This segment is deleted.

        # assistant functional region.
        self._assistp_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._assistp_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._assistp_gbox, 1, 1, 1, 1)

        self.rhc_covalue = RGBHSVCkb(self._assistp_gbox, oneline_mode=False)
        gbox_grid_layout.addWidget(self.rhc_covalue, 0, 1, 1, 1)
        self.rhc_covalue.ps_value_changed.connect(self.emit_assistp)

        self.sdt_covalue = SlideText(self._assistp_gbox, num_range=(-1.0, 1.0), maxlen=360000, interval=36000)
        gbox_grid_layout.addWidget(self.sdt_covalue, 1, 1, 1, 1)
        self.sdt_covalue.ps_value_changed.connect(self.emit_assistp)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        """

        # grid functional region.
        self._gridvls_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._gridvls_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._gridvls_gbox, 2, 1, 1, 1)

        self.rhc_govalue = RGBHSVCkb(self._gridvls_gbox, oneline_mode=True)
        gbox_grid_layout.addWidget(self.rhc_govalue, 0, 1, 1, 1)
        self.rhc_govalue.ps_value_changed.connect(self.modify_grid_value("ctp", tuple))

        self.ckb_rev_grid = QCheckBox(self._gridvls_gbox)
        self.ckb_rev_grid.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_rev_grid, 1, 1, 1, 1)
        self.ckb_rev_grid.stateChanged.connect(self.modify_grid_value("rev_grid", bool))

        self.sdt_col = SlideText(self._gridvls_gbox, num_range=(1, 51), maxlen=50, interval=10, step=1, decimals=0, default_value=9)
        gbox_grid_layout.addWidget(self.sdt_col, 2, 1, 1, 1)
        self.sdt_col.ps_value_changed.connect(self.modify_grid_value("col", int))

        self.sdt_sum_factor = SlideText(self._gridvls_gbox, num_range=(0.0, 5.0), default_value=1.0)
        gbox_grid_layout.addWidget(self.sdt_sum_factor, 3, 1, 1, 1)
        self.sdt_sum_factor.ps_value_changed.connect(self.modify_grid_value("sum_factor", float))

        self.sdt_dim_factor = SlideText(self._gridvls_gbox, num_range=(0.0, 1.0), default_value=1.0)
        gbox_grid_layout.addWidget(self.sdt_dim_factor, 4, 1, 1, 1)
        self.sdt_dim_factor.ps_value_changed.connect(self.modify_grid_value("dim_factor", float))

        self.sdt_assist_factor = SlideText(self._gridvls_gbox, num_range=(0.0, 1.0), default_value=0.6)
        gbox_grid_layout.addWidget(self.sdt_assist_factor, 5, 1, 1, 1)
        self.sdt_assist_factor.ps_value_changed.connect(self.modify_grid_value("assist_factor", float))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 6, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(210, 60)

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

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._display_gbox.setTitle(self._gbox_descs[0])
        self._gridvls_gbox.setTitle(self._gbox_descs[2])

        self.rhc_govalue.set_prefix_text((self._assistp_descs[0], self._assistp_descs[1]))
        self.sdt_col.set_text(self._assistp_descs[3])
        self.sdt_sum_factor.set_text(self._assistp_descs[4])
        self.sdt_dim_factor.set_text(self._assistp_descs[5])
        self.sdt_assist_factor.set_text(self._assistp_descs[6])
        self.ckb_rev_grid.setText(self._assistp_descs[7])

        self.update_mode()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Mode", "Display"),
            _translate("Mode", "Assistant"),
            _translate("Mode", "Grid"),
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
