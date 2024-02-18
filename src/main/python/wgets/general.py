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

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox, QSlider, QSpacerItem, QSizePolicy, QCheckBox, QPushButton, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication


class NoWheelSlider(QSlider):
    """
    Slider without responding wheel event.
    """

    def __init__(self, wget):
        """
        Init operation.
        """

        super().__init__(wget)

    def wheelEvent(self, event):
        event.ignore()

class NoWheelDoubleSpinBox(QDoubleSpinBox):
    """
    DoubleSpinBox without responding wheel event.
    """

    def __init__(self, wget):
        """
        Init operation.
        """

        super().__init__(wget)

    def wheelEvent(self, event):
        event.ignore()

class SlideText(QWidget):
    """
    Box with a text label, a spin box and a slider.
    """

    ps_value_changed = pyqtSignal(float)

    def __init__(self, wget, num_range=(0.0, 1.0), maxlen=100000, interval=10000, step=1000, decimals=2, default_value=0.0):
        """
        Init operation.
        """

        super().__init__(wget)
        self._num_range = tuple([float(min(num_range)), float(max(num_range))])
        self._maxlen = int(maxlen)
        self._interval = int(interval)
        self._step = int(step)
        self._decimals = int(decimals)
        self._value = float(default_value)
        self._emitting = True
        local_grid_layout = QGridLayout(self)
        local_grid_layout.setContentsMargins(0, 0, 0, 0)
        local_grid_layout.setHorizontalSpacing(2)
        local_grid_layout.setVerticalSpacing(0)
        self.lab_local = QLabel(self)
        local_grid_layout.addWidget(self.lab_local, 0, 0, 1, 1)
        self.dsp_local = NoWheelDoubleSpinBox(self)
        self.dsp_local.setMinimum(self._num_range[0])
        self.dsp_local.setMaximum(self._num_range[1])
        self.dsp_local.setSingleStep(self._step * 1.0 / self._maxlen * (self._num_range[1] - self._num_range[0]))
        self.dsp_local.setDecimals(self._decimals)
        self.dsp_local.setValue(self._value)
        self.dsp_local.setContextMenuPolicy(Qt.NoContextMenu)
        self.dsp_local.setButtonSymbols(QDoubleSpinBox.NoButtons)
        local_grid_layout.addWidget(self.dsp_local, 0, 1, 1, 1)
        self.dsp_local.valueChanged.connect(self.value_changed_from_dsp)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        local_grid_layout.addItem(spacer, 0, 2, 1, 1)
        self.sdr_local = NoWheelSlider(self)
        self.sdr_local.setMinimum(0)
        self.sdr_local.setMaximum(self._maxlen)
        self.sdr_local.setSingleStep(self._step)
        self.sdr_local.setPageStep(0)
        self.sdr_local.setOrientation(Qt.Horizontal)
        self.sdr_local.setTickPosition(NoWheelSlider.TicksAbove)
        self.sdr_local.setTickInterval(self._interval)
        self.sdr_local.setValue(self.value_dsp_to_sdr(self._value))
        local_grid_layout.addWidget(self.sdr_local, 1, 0, 1, 3)
        self.sdr_local.valueChanged.connect(self.value_changed_from_sdr)

    def norm_dsp_value(self, dsp_value):
        """
        Normalize value for dsp_local.
        """

        norm_value = float(dsp_value)
        norm_value = self._num_range[0] if norm_value < self._num_range[0] else norm_value
        norm_value = self._num_range[1] if norm_value > self._num_range[1] else norm_value
        return norm_value

    def norm_sdr_value(self, sdr_value):
        """
        Normalize value for sdr_local.
        """

        norm_value = int(sdr_value)
        norm_value = 0 if norm_value < 0 else norm_value
        norm_value = self._maxlen if norm_value > self._maxlen else norm_value
        return norm_value

    def value_dsp_to_sdr(self, dsp_value):
        """
        Arg sdr_value from self._num_range[0] to self._num_range[1].
        """

        norm_value = self.norm_dsp_value(dsp_value)
        return int((norm_value - self._num_range[0]) / (self._num_range[1] - self._num_range[0]) * self._maxlen)

    def value_sdr_to_dsp(self, sdr_value):
        """
        Arg sdr_value from 0 to self._maxlen.
        """

        norm_value = self.norm_sdr_value(sdr_value)
        return float((norm_value / self._maxlen) * (self._num_range[1] - self._num_range[0]) + self._num_range[0])

    def set_disabled(self, state):
        """
        Set state for tools.
        """

        self.dsp_local.setDisabled(bool(state))
        self.sdr_local.setDisabled(bool(state))

    def set_value(self, value):
        """
        Set value for SlideText.
        """

        norm_value = self.norm_dsp_value(value)
        self._emitting = False
        self._value = norm_value
        self.dsp_local.setValue(self._value)
        self.sdr_local.setValue(self.value_dsp_to_sdr(self._value))
        self._emitting = True

    def get_value(self):
        """
        Get value for SlideText.
        """

        return self._value

    def set_text(self, text):
        self.lab_local.setText(text)

    def set_num_range(self, num_range):
        sdr_value = self.value_dsp_to_sdr(self._value)
        self._emitting = False
        self._num_range = tuple([float(min(num_range)), float(max(num_range))])
        self.dsp_local.setMinimum(self._num_range[0])
        self.dsp_local.setMaximum(self._num_range[1])
        self.dsp_local.setSingleStep(self._step * 1.0 / self._maxlen * (self._num_range[1] - self._num_range[0]))
        self._value = self.value_sdr_to_dsp(sdr_value)
        self.dsp_local.setValue(self._value)
        self._emitting = True

    def get_num_range(self):
        return self._num_range

    def value_changed_from_dsp(self, value):
        """
        Change dsp_local value.
        """

        if value != self._value:
            self._value = self.norm_dsp_value(value)
            self.sdr_local.setValue(self.value_dsp_to_sdr(self._value))

            if self._emitting:
                self.ps_value_changed.emit(self._value)

    def value_changed_from_sdr(self, value):
        """
        Change sdr_local value.
        """

        if value != self.value_dsp_to_sdr(self._value):
            self._value = self.value_sdr_to_dsp(value)
            self.dsp_local.setValue(self._value)

            if self._emitting:
                self.ps_value_changed.emit(self._value)

class RGBHSVCkb(QWidget):
    """
    Box with R, G, B, H, S, V ckeckboxes.
    """

    ps_value_changed = pyqtSignal(tuple)

    def __init__(self, wget, default_values=[], oneline_mode=True):
        """
        Init operation.
        """

        super().__init__(wget)
        self._avi_values = ("r", "g", "b", "h", "s", "v")
        self._values = []
        self._prefix_text = ""
        self._emitting = True

        if default_values and isinstance(default_values, (tuple, list)):
            for vl in default_values:
                if str(vl).lower() in self._avi_values:
                    self._values.append(str(vl).lower())

        self._oneline_mode = bool(oneline_mode)
        local_grid_layout = QGridLayout(self)
        local_grid_layout.setContentsMargins(0, 0, 0, 0)
        local_grid_layout.setHorizontalSpacing(2)
        local_grid_layout.setVerticalSpacing(4)
        self.lab_link = QLabel(self)
        local_grid_layout.addWidget(self.lab_link, 0, 0, 1, 3)
        self.ckb_r = QCheckBox(self)
        self.ckb_r.setText("R")
        self.ckb_r.setChecked("r" in self._values)
        local_grid_layout.addWidget(self.ckb_r, 1, 0, 1, 1)
        self.ckb_r.stateChanged.connect(self.set_value_from_ckb("r"))
        self.ckb_g = QCheckBox(self)
        self.ckb_g.setText("G")
        self.ckb_g.setChecked("g" in self._values)
        local_grid_layout.addWidget(self.ckb_g, 1, 1, 1, 1)
        self.ckb_g.stateChanged.connect(self.set_value_from_ckb("g"))
        self.ckb_b = QCheckBox(self)
        self.ckb_b.setText("B")
        self.ckb_b.setChecked("b" in self._values)
        local_grid_layout.addWidget(self.ckb_b, 1, 2, 1, 1)
        self.ckb_b.stateChanged.connect(self.set_value_from_ckb("b"))
        self.ckb_h = QCheckBox(self)
        self.ckb_h.setText("H")
        self.ckb_h.setChecked("h" in self._values)
        local_grid_layout.addWidget(self.ckb_h, 2, 0, 1, 1)
        self.ckb_h.stateChanged.connect(self.set_value_from_ckb("h"))
        self.ckb_s = QCheckBox(self)
        self.ckb_s.setText("S")
        self.ckb_s.setChecked("s" in self._values)
        local_grid_layout.addWidget(self.ckb_s, 2, 1, 1, 1)
        self.ckb_s.stateChanged.connect(self.set_value_from_ckb("s"))
        self.ckb_v = QCheckBox(self)
        self.ckb_v.setText("V")
        self.ckb_v.setChecked("v" in self._values)
        local_grid_layout.addWidget(self.ckb_v, 2, 2, 1, 1)
        self.ckb_v.stateChanged.connect(self.set_value_from_ckb("v"))

    def inner_set_value(self, name, state):
        """
        Inner func for set value.

        Args:
            name (str): "r", "g", "b", "h", "s" or "v".
            state (bool): box is checked or unchecked.
        """

        norm_name = str(name).lower()

        if norm_name in self._avi_values:
            if state:
                if self._oneline_mode:
                    changed_values = []

                    if norm_name in self._avi_values[:3]:
                        for vl in self._values:
                            if vl in self._avi_values[:3]:
                                changed_values.append(vl)

                    else:
                        for vl in self._values:
                            if vl in self._avi_values[3:]:
                                changed_values.append(vl)

                    self._values = changed_values
                else:
                    self._values = []

                if norm_name not in self._values:
                    self._values.append(norm_name)

            else:
                changed_values = []

                for vl in self._values:
                    if vl != norm_name:
                        changed_values.append(vl)

                self._values = changed_values

        if len(self._values) > 1:
            changed_values = []

            for vl in self._avi_values:
                if vl in self._values:
                    changed_values.append(vl)

            self._values = changed_values

        for vl in self._avi_values:
            ckb = getattr(self, "ckb_{}".format(vl))

            if vl in self._values:
                if not ckb.isChecked():
                    ckb.setChecked(True)

            else:
                if ckb.isChecked():
                    ckb.setChecked(False)

        if self._values:
            self.lab_link.setText(self._prefix_text[1] + " ".join([x.upper() for x in self._values]))

        else:
            self.lab_link.setText(self._prefix_text[0])

    def set_values(self, values):
        self._emitting = False
        self._values = tuple(values)
        self.inner_set_value("", True)
        self._emitting = True

    def set_value_from_ckb(self, value):
        def _func_(state):
            self.inner_set_value(value, state)

            if self._values and self._emitting:
                self.ps_value_changed.emit(tuple(self._values))

        return _func_

    def get_values(self):
        return self._values

    def set_prefix_text(self, text):
        self._prefix_text = text

        if self._values:
            self.lab_link.setText(self._prefix_text[1] + " ".join([x.upper() for x in self._values]))

        else:
            self.lab_link.setText(self._prefix_text[0])

class RGBCMYCkb(QWidget):
    """
    Box with R, G, B, C, M, Y ckeckboxes.
    """

    ps_angle_changed = pyqtSignal(tuple)

    def __init__(self, wget):
        """
        Init operation.
        """

        super().__init__(wget)
        self._avi_values = ("r", "g", "b", "c", "m", "y")
        self._avi_angles = (0, 120, 240, 180, 300, 60)
        self._values = []
        self._angles = []
        self._prefix_text = ""
        self._emitting = True
        local_grid_layout = QGridLayout(self)
        local_grid_layout.setContentsMargins(0, 0, 0, 0)
        local_grid_layout.setHorizontalSpacing(2)
        local_grid_layout.setVerticalSpacing(4)
        self.lab_link = QLabel(self)
        local_grid_layout.addWidget(self.lab_link, 0, 0, 1, 3)
        self.ckb_r = QCheckBox(self)
        self.ckb_r.setText("R")
        self.ckb_r.setChecked("r" in self._values)
        local_grid_layout.addWidget(self.ckb_r, 1, 0, 1, 1)
        self.ckb_r.stateChanged.connect(self.set_angle_from_ckb(0))
        self.ckb_g = QCheckBox(self)
        self.ckb_g.setText("G")
        self.ckb_g.setChecked("g" in self._values)
        local_grid_layout.addWidget(self.ckb_g, 1, 1, 1, 1)
        self.ckb_g.stateChanged.connect(self.set_angle_from_ckb(120))
        self.ckb_b = QCheckBox(self)
        self.ckb_b.setText("B")
        self.ckb_b.setChecked("b" in self._values)
        local_grid_layout.addWidget(self.ckb_b, 1, 2, 1, 1)
        self.ckb_b.stateChanged.connect(self.set_angle_from_ckb(240))
        self.ckb_c = QCheckBox(self)
        self.ckb_c.setText("C")
        self.ckb_c.setChecked("c" in self._values)
        local_grid_layout.addWidget(self.ckb_c, 2, 0, 1, 1)
        self.ckb_c.stateChanged.connect(self.set_angle_from_ckb(180))
        self.ckb_m = QCheckBox(self)
        self.ckb_m.setText("M")
        self.ckb_m.setChecked("m" in self._values)
        local_grid_layout.addWidget(self.ckb_m, 2, 1, 1, 1)
        self.ckb_m.stateChanged.connect(self.set_angle_from_ckb(300))
        self.ckb_y = QCheckBox(self)
        self.ckb_y.setText("Y")
        self.ckb_y.setChecked("y" in self._values)
        local_grid_layout.addWidget(self.ckb_y, 2, 2, 1, 1)
        self.ckb_y.stateChanged.connect(self.set_angle_from_ckb(60))
        self._ckbs = (self.ckb_r, self.ckb_g, self.ckb_b, self.ckb_c, self.ckb_m, self.ckb_y)

    def disable(self):
        for ckb in self._ckbs:
            ckb.setDisabled()

    def enable(self):
        for ckb in self._ckbs:
            ckb.setEnabled()

    def set_angles(self, angles):
        """
        Inner func for set value.

        Args:
            angles (tuple or list): angle list with values in 0, 120, 240, 180, 300 or 60.
        """

        self._angles = []

        for angle_idx in range(6):
            angle = self._avi_angles[angle_idx]
            state = angle in angles

            if self._ckbs[angle_idx].isChecked() != state:
                self._ckbs[angle_idx].setChecked(state)

            if state:
                self._angles.append(self._avi_angles[angle_idx])

        if self._angles:
            self.lab_link.setText(self._prefix_text[1] + " ".join([self._avi_values[self._avi_angles.index(x)].upper() for x in self._angles]))

        else:
            self.lab_link.setText(self._prefix_text[0])

    def set_angle_from_ckb(self, angle):
        def _func_(state):
            if state:
                self._angles.append(angle)

            else:
                self._angles.pop(angle)

            self._angles.sort()

            if self._angles:
                self.lab_link.setText(self._prefix_text[1] + " ".join([self._avi_values[self._avi_angles.index(x)].upper() for x in self._angles]))
                self.ps_angle_changed.emit(tuple(self._angles))

            else:
                self.lab_link.setText(self._prefix_text[0])

        return _func_

    def get_angles(self):
        return self._angles

    def set_prefix_text(self, text):
        self._prefix_text = text

        if self._angles:
            self.lab_link.setText(self._prefix_text[1] + " ".join([self._avi_values[self._avi_angles.index(x)].upper() for x in self._angles]))

        else:
            self.lab_link.setText(self._prefix_text[0])

class FoldingBox(QWidget):
    """
    Box with a button and a group box.
    """

    ps_fbox_updated = pyqtSignal(bool)

    def __init__(self, wget, title=""):
        """
        Init operation.
        """

        super().__init__(wget)
        self._is_expanded = True
        self._title = str(title)
        self._fbox_icons = (None, None)
        local_grid_layout = QGridLayout(self)
        local_grid_layout.setContentsMargins(0, 0, 0, 0)
        local_grid_layout.setHorizontalSpacing(0)
        local_grid_layout.setVerticalSpacing(0)
        self.top_btn = QPushButton(self)
        self.top_btn.setProperty("class", "fbox")
        local_grid_layout.addWidget(self.top_btn, 0, 0, 1, 1)
        self.top_btn.clicked.connect(self.change_state)
        self.gbox = QWidget(self)
        self.gbox.setProperty("class", "gbox")
        local_grid_layout.addWidget(self.gbox, 1, 0, 1, 1)
        self.gbox_grid_layout = QGridLayout(self.gbox)
        self.gbox_grid_layout.setContentsMargins(3, 6, 3, 6)
        self.gbox_grid_layout.setHorizontalSpacing(3)
        self.gbox_grid_layout.setVerticalSpacing(9)
        self.end_btn = QPushButton(self)
        self.end_btn.setProperty("class", "ebox")
        local_grid_layout.addWidget(self.end_btn, 2, 0, 1, 1)
        self.end_btn.clicked.connect(self.change_state)

    @property
    def is_expanded(self):
        return self._is_expanded

    def expand(self):
        self.top_btn.show()
        self.gbox.show()
        self.end_btn.show()
        self._is_expanded = True
        self.update_title()

    def fold(self):
        self.top_btn.show()
        self.gbox.hide()
        self.end_btn.hide()
        self._is_expanded = False
        self.update_title()

    def change_state(self, state=False):
        if self._is_expanded:
            self.fold()

        else:
            self.expand()

    def set_title(self, title):
        self._title = str(title)
        self.update_title()

    def set_icons(self, fbox_icons):
        self._fbox_icons = fbox_icons

    def update_title(self):
        self.top_btn.setText(self._title)

        if self._is_expanded:
            self.top_btn.show()
            self.end_btn.show()

            if self._fbox_icons[1]:
                self.top_btn.setIcon(self._fbox_icons[1])
                self.end_btn.setIcon(self._fbox_icons[1])

        else:
            self.top_btn.show()
            self.end_btn.hide()

            if self._fbox_icons[0]:
                self.top_btn.setIcon(self._fbox_icons[0])

        self.ps_fbox_updated.emit(True)

class SideWidget(QWidget):
    """
    Docker widget template.
    """

    def __init__(self, wget):
        """
        Init SideWidget.
        """

        super().__init__(wget)
        self._sw_func_tr_()
        self._state = False
        self._all_fboxes = ()
        self._fbox_icons = (None, None)
        self._exp_all_btn = QPushButton(self)
        self._exp_all_btn.setProperty("class", "fbox")
        self._exp_all_btn.clicked.connect(self.expand_or_fold_all_fbox)
        gen_grid_layout = QGridLayout(self)
        gen_grid_layout.setContentsMargins(0, 0, 0, 0)
        gen_grid_layout.setHorizontalSpacing(0)
        gen_grid_layout.setVerticalSpacing(0)
        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        gen_grid_layout.addWidget(scroll_area)
        self.scroll_contents = QWidget()
        self.scroll_grid_layout = QGridLayout(self.scroll_contents)
        self.scroll_grid_layout.setContentsMargins(3, 9, 3, 3)
        self.scroll_grid_layout.setHorizontalSpacing(3)
        self.scroll_grid_layout.setVerticalSpacing(3)
        scroll_area.setWidget(self.scroll_contents)
        self.over_spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def set_icons(self, fbox_icons):
        self._fbox_icons = fbox_icons

        for fbox in self._all_fboxes:
            fbox.set_icons(fbox_icons)
            fbox.update_title()

    def expand_or_fold_all_fbox(self, value):
        state = True in self.get_all_expand_states()

        for fbox in self._all_fboxes:
            if state:
                fbox.fold()

            else:
                fbox.expand()

        if state:
            self.over_spacer.changeSize(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

        else:
            self.over_spacer.changeSize(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.sw_update_text(force=True)

    def get_all_expand_states(self):
        return [fbox.is_expanded for fbox in self._all_fboxes]

    def set_all_expand_states(self, states, default=False):
        if isinstance(states, (tuple, list)) and len(states) == len(self._all_fboxes):
            states = [str(i).lower().startswith("t") if isinstance(i, str) else bool(i) for i in states]

        else:
            states = [bool(default), ] * len(self._all_fboxes)

        for fbox, state in zip(self._all_fboxes, states):
            if state:
                fbox.expand()
                self.over_spacer.changeSize(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

            else:
                fbox.fold()

        self.sw_update_text(force=True)

    def connect_by_fboxes(self):
        for fbox in self._all_fboxes:
            fbox.ps_fbox_updated.connect(self.sw_update_text)

    def sw_update_text(self, force=False):
        state = True in self.get_all_expand_states()

        if force or state != self._state:
            self._state = state

            if state:
                if self._fbox_icons[1]:
                    self._exp_all_btn.setIcon(self._fbox_icons[1])

                self._exp_all_btn.setText(self.exp_all_descs[1])
                self.over_spacer.changeSize(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

            else:
                if self._fbox_icons[0]:
                    self._exp_all_btn.setIcon(self._fbox_icons[0])

                self._exp_all_btn.setText(self.exp_all_descs[0])
                self.over_spacer.changeSize(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def _sw_func_tr_(self):
        _translate = QCoreApplication.translate
        self.exp_all_descs = (
            _translate("General", "Expand All Items"),
            _translate("General", "Fold All Items"),
        )

