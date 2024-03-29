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

from PyQt5.QtWidgets import QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from wgets.general import SlideText, FoldingBox, SideWidget


class Script(SideWidget):
    """
    Script object based on QWidget. Init a script in script.
    """

    ps_filter = pyqtSignal(tuple)
    ps_crop = pyqtSignal(bool)
    ps_freeze = pyqtSignal(bool)
    ps_print = pyqtSignal(bool)
    ps_extract = pyqtSignal(int)

    def __init__(self, wget, args):
        """
        Init operation.
        """

        super().__init__(wget)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self._args = args
        self._func_tr_()
        self._filter_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._filter_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._filter_fbox, 2, 1, 1, 1)
        self._filter_btns = []

        for i in range(10):
            btn = QPushButton(self._filter_fbox.gbox)
            self._filter_btns.append(btn)

        gbox_grid_layout.addWidget(self._filter_btns[0], 0, 1, 1, 1)
        self._filter_btns[0].clicked.connect(lambda x: self.ps_filter.emit(("BLUR", None)))
        gbox_grid_layout.addWidget(self._filter_btns[1], 1, 1, 1, 1)
        self._filter_btns[1].clicked.connect(lambda x: self.ps_filter.emit(("CONTOUR", None)))
        gbox_grid_layout.addWidget(self._filter_btns[2], 2, 1, 1, 1)
        self._filter_btns[2].clicked.connect(lambda x: self.ps_filter.emit(("DETAIL", None)))
        gbox_grid_layout.addWidget(self._filter_btns[3], 3, 1, 1, 1)
        self._filter_btns[3].clicked.connect(lambda x: self.ps_filter.emit(("EDGE_ENHANCE", None)))
        gbox_grid_layout.addWidget(self._filter_btns[4], 4, 1, 1, 1)
        self._filter_btns[4].clicked.connect(lambda x: self.ps_filter.emit(("EDGE_ENHANCE_MORE", None)))
        gbox_grid_layout.addWidget(self._filter_btns[5], 5, 1, 1, 1)
        self._filter_btns[5].clicked.connect(lambda x: self.ps_filter.emit(("EMBOSS", None)))
        gbox_grid_layout.addWidget(self._filter_btns[6], 6, 1, 1, 1)
        self._filter_btns[6].clicked.connect(lambda x: self.ps_filter.emit(("FIND_EDGES", None)))
        gbox_grid_layout.addWidget(self._filter_btns[7], 7, 1, 1, 1)
        self._filter_btns[7].clicked.connect(lambda x: self.ps_filter.emit(("SHARPEN", None)))
        gbox_grid_layout.addWidget(self._filter_btns[8], 8, 1, 1, 1)
        self._filter_btns[8].clicked.connect(lambda x: self.ps_filter.emit(("SMOOTH", None)))
        gbox_grid_layout.addWidget(self._filter_btns[9], 9, 1, 1, 1)
        self._filter_btns[9].clicked.connect(lambda x: self.ps_filter.emit(("SMOOTH_MORE", None)))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 10, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 10, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 10, 2, 1, 1)
        self._zoom_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._zoom_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._zoom_fbox, 5, 1, 1, 1)
        self.sdt_zoom = SlideText(self._zoom_fbox.gbox, num_range=(0.0, 3.0), default_value=1.0)
        gbox_grid_layout.addWidget(self.sdt_zoom, 0, 1, 1, 1)
        self.sdt_zoom.ps_value_changed.connect(self.update_zoom)
        self.btn_zoom = QPushButton(self._zoom_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_zoom, 1, 1, 1, 1)
        self.btn_zoom.clicked.connect(lambda x: self.ps_filter.emit(("ZOOM", self.sdt_zoom.get_value())))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._crop_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._crop_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._crop_fbox, 4, 1, 1, 1)
        self.btn_crop = QPushButton(self._crop_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_crop, 0, 1, 1, 1)
        self.btn_crop.clicked.connect(lambda x: self.ps_crop.emit(True))
        self.btn_cancel = QPushButton(self._crop_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_cancel, 1, 1, 1, 1)
        self.btn_cancel.clicked.connect(lambda x: self.ps_crop.emit(False))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._snap_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._snap_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._snap_fbox, 3, 1, 1, 1)
        self.btn_freeze = QPushButton(self._snap_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_freeze, 0, 1, 1, 1)
        self.btn_freeze.clicked.connect(lambda x: self.ps_freeze.emit(True))
        self.btn_print = QPushButton(self._snap_fbox.gbox)
        gbox_grid_layout.addWidget(self.btn_print, 1, 1, 1, 1)
        self.btn_print.clicked.connect(lambda x: self.ps_print.emit(True))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)
        self._extract_fbox = FoldingBox(self.scroll_contents)
        gbox_grid_layout = self._extract_fbox.gbox_grid_layout
        self.scroll_grid_layout.addWidget(self._extract_fbox, 1, 1, 1, 1)
        self._extract_btns = []

        for i in range(6):
            btn = QPushButton(self._extract_fbox.gbox)
            self._extract_btns.append(btn)

        gbox_grid_layout.addWidget(self._extract_btns[0], 0, 1, 1, 1)
        self._extract_btns[0].clicked.connect(lambda x: self.ps_extract.emit(0))
        gbox_grid_layout.addWidget(self._extract_btns[1], 1, 1, 1, 1)
        self._extract_btns[1].clicked.connect(lambda x: self.ps_extract.emit(1))
        gbox_grid_layout.addWidget(self._extract_btns[2], 2, 1, 1, 1)
        self._extract_btns[2].clicked.connect(lambda x: self.ps_extract.emit(2))
        gbox_grid_layout.addWidget(self._extract_btns[3], 3, 1, 1, 1)
        self._extract_btns[3].clicked.connect(lambda x: self.ps_extract.emit(3))
        gbox_grid_layout.addWidget(self._extract_btns[4], 4, 1, 1, 1)
        self._extract_btns[4].clicked.connect(lambda x: self.ps_extract.emit(4))
        gbox_grid_layout.addWidget(self._extract_btns[5], 5, 1, 1, 1)
        self._extract_btns[5].clicked.connect(lambda x: self.ps_extract.emit(5))
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 6, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 6, 2, 1, 1)
        self.scroll_grid_layout.addItem(self.over_spacer, 6, 1, 1, 1)
        self._all_fboxes = (self._filter_fbox, self._zoom_fbox, self._crop_fbox, self._snap_fbox, self._extract_fbox)
        self.scroll_grid_layout.addWidget(self._exp_all_btn, 0, 1, 1, 1)
        self.connect_by_fboxes()
        self.update_text()

    def sizeHint(self):
        return QSize(250, 145)

    def update_zoom(self):
        """
        Update zoom region.
        """

        if self.sdt_zoom.get_value() == 1.0:
            self.btn_zoom.setText(self._zoom_descs[1])

        elif self.sdt_zoom.get_value() < 1.0:
            self.btn_zoom.setText(self._zoom_descs[2])

        else:
            self.btn_zoom.setText(self._zoom_descs[3])

    def update_text(self):
        self.sw_update_text(force=True)
        self._filter_fbox.set_title(self._gbox_descs[0])

        for i in range(10):
            self._filter_btns[i].setText(self._filter_descs[i])

        self._zoom_fbox.set_title(self._gbox_descs[1])
        self.sdt_zoom.set_text(self._zoom_descs[0])
        self.update_zoom()
        self._crop_fbox.set_title(self._gbox_descs[2])
        self.btn_crop.setText(self._crop_descs[0])
        self.btn_cancel.setText(self._crop_descs[1])
        self._snap_fbox.set_title(self._gbox_descs[3])
        self.btn_freeze.setText(self._snap_descs[0])
        self.btn_print.setText(self._snap_descs[1])
        self._extract_fbox.set_title(self._gbox_descs[4])

        for i in range(6):
            self._extract_btns[i].setText(self._extract_descs[i])

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._gbox_descs = (
            _translate("Script", "Filter"),
            _translate("Script", "Zoom"),
            _translate("Script", "Crop"),
            _translate("Script", "Snap"),
            _translate("Script", "Extract"),
        )

        self._extract_descs = (
            _translate("Script", "Bright Colorful"),
            _translate("Script", "Light Colorful"),
            _translate("Script", "Dark Colorful"),
            _translate("Script", "Bright"),
            _translate("Script", "Light"),
            _translate("Script", "Dark"),
        )

        self._filter_descs = (
            _translate("Script", "Blur"),
            _translate("Script", "Contour"),
            _translate("Script", "Detail"),
            _translate("Script", "Edge Enhance"),
            _translate("Script", "Edge Enhance More"),
            _translate("Script", "Emboss"),
            _translate("Script", "Find Edges"),
            _translate("Script", "Sharpen"),
            _translate("Script", "Smooth"),
            _translate("Script", "Smooth More"),
        )

        self._zoom_descs = (
            _translate("Script", "Ratio - "),
            _translate("Script", "Zoom"),
            _translate("Script", "Zoom In"),
            _translate("Script", "Zoom Out"),
        )

        self._crop_descs = (
            _translate("Script", "Crop"),
            _translate("Script", "Cancel"),
        )

        self._snap_descs = (
            _translate("Script", "Freeze Image"),
            _translate("Script", "Save Image"),
        )

