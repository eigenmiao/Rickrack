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

from PyQt5.QtWidgets import QWidget, QRadioButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize


class Channel(QWidget):
    """
    Channel object based on QWidget. Init a channel in channel.
    """

    ps_channel_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init channel.
        """

        super().__init__(wget)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._backups = ()
        self._func_tr_()
        channel_grid_layout = QGridLayout(self)
        channel_grid_layout.setContentsMargins(0, 0, 0, 0)
        channel_grid_layout.setHorizontalSpacing(0)
        channel_grid_layout.setVerticalSpacing(0)
        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        channel_grid_layout.addWidget(scroll_area)
        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(3, 9, 3, 3)
        scroll_grid_layout.setHorizontalSpacing(3)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)
        self._category_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._category_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(16)
        scroll_grid_layout.addWidget(self._category_gbox, 0, 1, 1, 1)
        self._category_btns = []

        for i in range(8):
            btn = QRadioButton(self._category_gbox)
            gbox_grid_layout.addWidget(btn, i, 0, 1, 1)
            btn.clicked.connect(self.modify_category(i))
            self._category_btns.append(btn)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 8, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 8, 1, 1, 1)
        self._channel_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._channel_gbox)
        gbox_grid_layout.setContentsMargins(3, 12, 3, 12)
        gbox_grid_layout.setHorizontalSpacing(3)
        gbox_grid_layout.setVerticalSpacing(16)
        scroll_grid_layout.addWidget(self._channel_gbox, 1, 1, 1, 1)
        self._channel_btns = []

        for i in range(7):
            btn = QRadioButton(self._channel_gbox)
            gbox_grid_layout.addWidget(btn, i, 0, 1, 1)
            btn.clicked.connect(self.modify_channel(i))
            self._channel_btns.append(btn)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 7, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 7, 1, 1, 1)
        self.reset()

    def sizeHint(self):
        return QSize(250, 90)

    def reset(self):
        self._category_btns[self._args.sys_category].setChecked(True)
        self._channel_btns[self._args.sys_channel].setChecked(True)
        self.update_text()

    def modify_category(self, idx):
        """
        Modify stored category set by btn.
        """

        def _func_(value):
            self._backups = (self._args.sys_category, self._args.sys_channel)
            self._args.sys_category = idx
            self.ps_channel_changed.emit(True)
            self.update_text()

        return _func_

    def modify_channel(self, idx):
        """
        Modify stored channel set by btn.
        """

        def _func_(value):
            self._backups = (self._args.sys_category, self._args.sys_channel)
            self._args.sys_channel = idx
            self.ps_channel_changed.emit(True)

        return _func_

    def recover(self):
        """
        Recover sys_category and sys_channel from backups.
        """

        self._args.sys_category, self._args.sys_channel = self._backups
        self.reset()

    def update_text(self):
        self._category_gbox.setTitle(self._gbox_descs[0])
        self._channel_gbox.setTitle(self._gbox_descs[1])

        for i in range(8):
            self._category_btns[i].setText(self._category_descs[i])

        if self._args.sys_category in range(4):
            for i in range(7):
                self._channel_btns[i].setText(self._channel_descs[i])

        else:
            for i in range(7):
                self._channel_btns[i].setText(self._channel_descs[i + 7])

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._gbox_descs = (
            _translate("Channel", "Category"),
            _translate("Channel", "Channel"),
        )

        self._category_descs = (
            _translate("Channel", "Norm RGB"),
            _translate("Channel", "Vtcl RGB"),
            _translate("Channel", "Horz RGB"),
            _translate("Channel", "Finl RGB"),
            _translate("Channel", "Norm HSV"),
            _translate("Channel", "Vtcl HSV"),
            _translate("Channel", "Horz HSV"),
            _translate("Channel", "Finl HSV"),
        )

        self._channel_descs = (
            _translate("Channel", "Full RGB"),
            _translate("Channel", "Chnnel R"),
            _translate("Channel", "Chnnel G"),
            _translate("Channel", "Chnnel B"),
            _translate("Channel", "Not R"),
            _translate("Channel", "Not G"),
            _translate("Channel", "Not B"),
            _translate("Channel", "Full HSV"),
            _translate("Channel", "Chnnel H"),
            _translate("Channel", "Chnnel S"),
            _translate("Channel", "Chnnel V"),
            _translate("Channel", "Not H"),
            _translate("Channel", "Not S"),
            _translate("Channel", "Not V"),
        )

