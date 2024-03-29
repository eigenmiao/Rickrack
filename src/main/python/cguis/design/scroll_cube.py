# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\cguis\design\scroll_cube.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScrollCube(object):
    def setupUi(self, ScrollCube):
        ScrollCube.setObjectName("ScrollCube")
        ScrollCube.resize(241, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScrollCube.sizePolicy().hasHeightForWidth())
        ScrollCube.setSizePolicy(sizePolicy)
        ScrollCube.setBaseSize(QtCore.QSize(0, 0))
        ScrollCube.setWindowTitle("Form")
        self.gridLayout = QtWidgets.QGridLayout(ScrollCube)
        self.gridLayout.setContentsMargins(9, 0, 9, 0)
        self.gridLayout.setSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.sharp = QtWidgets.QLabel(ScrollCube)
        self.sharp.setText("#")
        self.sharp.setObjectName("sharp")
        self.gridLayout.addWidget(self.sharp, 1, 1, 1, 1)
        self.le_hec = QtWidgets.QLineEdit(ScrollCube)
        self.le_hec.setMinimumSize(QtCore.QSize(0, 0))
        self.le_hec.setMaximumSize(QtCore.QSize(80, 16777215))
        self.le_hec.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.le_hec.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_hec.setMaxLength(100)
        self.le_hec.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_hec.setObjectName("le_hec")
        self.gridLayout.addWidget(self.le_hec, 1, 2, 1, 1)
        self.gbox_rgb = QtWidgets.QGroupBox(ScrollCube)
        self.gbox_rgb.setTitle("RGB")
        self.gbox_rgb.setObjectName("gbox_rgb")
        self.gbox_rgb_grid_layout = QtWidgets.QGridLayout(self.gbox_rgb)
        self.gbox_rgb_grid_layout.setContentsMargins(8, 8, 8, 8)
        self.gbox_rgb_grid_layout.setSpacing(8)
        self.gbox_rgb_grid_layout.setObjectName("gbox_rgb_grid_layout")
        self.lb_rgb_r = QtWidgets.QLabel(self.gbox_rgb)
        self.lb_rgb_r.setText("R")
        self.lb_rgb_r.setObjectName("lb_rgb_r")
        self.gbox_rgb_grid_layout.addWidget(self.lb_rgb_r, 0, 0, 1, 1)
        self.hs_rgb_r = QtWidgets.QSlider(self.gbox_rgb)
        self.hs_rgb_r.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_rgb_r.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_rgb_r.setMaximum(255)
        self.hs_rgb_r.setPageStep(0)
        self.hs_rgb_r.setOrientation(QtCore.Qt.Horizontal)
        self.hs_rgb_r.setObjectName("hs_rgb_r")
        self.gbox_rgb_grid_layout.addWidget(self.hs_rgb_r, 0, 1, 1, 1)
        self.sp_rgb_r = QtWidgets.QSpinBox(self.gbox_rgb)
        self.sp_rgb_r.setMinimumSize(QtCore.QSize(30, 24))
        self.sp_rgb_r.setMaximumSize(QtCore.QSize(36, 16777215))
        self.sp_rgb_r.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.sp_rgb_r.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sp_rgb_r.setMaximum(255)
        self.sp_rgb_r.setObjectName("sp_rgb_r")
        self.gbox_rgb_grid_layout.addWidget(self.sp_rgb_r, 0, 2, 1, 1)
        self.lb_rgb_g = QtWidgets.QLabel(self.gbox_rgb)
        self.lb_rgb_g.setText("G")
        self.lb_rgb_g.setObjectName("lb_rgb_g")
        self.gbox_rgb_grid_layout.addWidget(self.lb_rgb_g, 1, 0, 1, 1)
        self.hs_rgb_g = QtWidgets.QSlider(self.gbox_rgb)
        self.hs_rgb_g.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_rgb_g.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_rgb_g.setMaximum(255)
        self.hs_rgb_g.setPageStep(0)
        self.hs_rgb_g.setOrientation(QtCore.Qt.Horizontal)
        self.hs_rgb_g.setObjectName("hs_rgb_g")
        self.gbox_rgb_grid_layout.addWidget(self.hs_rgb_g, 1, 1, 1, 1)
        self.sp_rgb_g = QtWidgets.QSpinBox(self.gbox_rgb)
        self.sp_rgb_g.setMinimumSize(QtCore.QSize(30, 24))
        self.sp_rgb_g.setMaximumSize(QtCore.QSize(36, 16777215))
        self.sp_rgb_g.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.sp_rgb_g.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sp_rgb_g.setMaximum(255)
        self.sp_rgb_g.setObjectName("sp_rgb_g")
        self.gbox_rgb_grid_layout.addWidget(self.sp_rgb_g, 1, 2, 1, 1)
        self.lb_rgb_b = QtWidgets.QLabel(self.gbox_rgb)
        self.lb_rgb_b.setText("B")
        self.lb_rgb_b.setObjectName("lb_rgb_b")
        self.gbox_rgb_grid_layout.addWidget(self.lb_rgb_b, 2, 0, 1, 1)
        self.hs_rgb_b = QtWidgets.QSlider(self.gbox_rgb)
        self.hs_rgb_b.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_rgb_b.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_rgb_b.setMaximum(255)
        self.hs_rgb_b.setPageStep(0)
        self.hs_rgb_b.setOrientation(QtCore.Qt.Horizontal)
        self.hs_rgb_b.setObjectName("hs_rgb_b")
        self.gbox_rgb_grid_layout.addWidget(self.hs_rgb_b, 2, 1, 1, 1)
        self.sp_rgb_b = QtWidgets.QSpinBox(self.gbox_rgb)
        self.sp_rgb_b.setMinimumSize(QtCore.QSize(30, 24))
        self.sp_rgb_b.setMaximumSize(QtCore.QSize(36, 16777215))
        self.sp_rgb_b.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.sp_rgb_b.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sp_rgb_b.setMaximum(255)
        self.sp_rgb_b.setObjectName("sp_rgb_b")
        self.gbox_rgb_grid_layout.addWidget(self.sp_rgb_b, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.gbox_rgb, 2, 0, 1, 4)
        self.cube_color = QtWidgets.QWidget(ScrollCube)
        self.cube_color.setMinimumSize(QtCore.QSize(0, 0))
        self.cube_color.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cube_color.setObjectName("cube_color")
        self.gridLayout.addWidget(self.cube_color, 0, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(0, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(0, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.gbox_hsv = QtWidgets.QGroupBox(ScrollCube)
        self.gbox_hsv.setTitle("HSV")
        self.gbox_hsv.setObjectName("gbox_hsv")
        self.gbox_hsv_grid_layout = QtWidgets.QGridLayout(self.gbox_hsv)
        self.gbox_hsv_grid_layout.setContentsMargins(8, 8, 8, 8)
        self.gbox_hsv_grid_layout.setSpacing(8)
        self.gbox_hsv_grid_layout.setObjectName("gbox_hsv_grid_layout")
        self.lb_hsv_h = QtWidgets.QLabel(self.gbox_hsv)
        self.lb_hsv_h.setText("H")
        self.lb_hsv_h.setObjectName("lb_hsv_h")
        self.gbox_hsv_grid_layout.addWidget(self.lb_hsv_h, 0, 0, 1, 1)
        self.hs_hsv_h = QtWidgets.QSlider(self.gbox_hsv)
        self.hs_hsv_h.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_hsv_h.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_hsv_h.setMaximum(359999)
        self.hs_hsv_h.setPageStep(0)
        self.hs_hsv_h.setOrientation(QtCore.Qt.Horizontal)
        self.hs_hsv_h.setObjectName("hs_hsv_h")
        self.gbox_hsv_grid_layout.addWidget(self.hs_hsv_h, 0, 1, 1, 1)
        self.dp_hsv_h = QtWidgets.QDoubleSpinBox(self.gbox_hsv)
        self.dp_hsv_h.setMinimumSize(QtCore.QSize(30, 24))
        self.dp_hsv_h.setMaximumSize(QtCore.QSize(36, 16777215))
        self.dp_hsv_h.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.dp_hsv_h.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dp_hsv_h.setDecimals(3)
        self.dp_hsv_h.setMaximum(360.0)
        self.dp_hsv_h.setObjectName("dp_hsv_h")
        self.gbox_hsv_grid_layout.addWidget(self.dp_hsv_h, 0, 2, 1, 1)
        self.lb_hsv_s = QtWidgets.QLabel(self.gbox_hsv)
        self.lb_hsv_s.setText("S")
        self.lb_hsv_s.setObjectName("lb_hsv_s")
        self.gbox_hsv_grid_layout.addWidget(self.lb_hsv_s, 1, 0, 1, 1)
        self.hs_hsv_s = QtWidgets.QSlider(self.gbox_hsv)
        self.hs_hsv_s.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_hsv_s.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_hsv_s.setMaximum(1000)
        self.hs_hsv_s.setPageStep(0)
        self.hs_hsv_s.setOrientation(QtCore.Qt.Horizontal)
        self.hs_hsv_s.setObjectName("hs_hsv_s")
        self.gbox_hsv_grid_layout.addWidget(self.hs_hsv_s, 1, 1, 1, 1)
        self.dp_hsv_s = QtWidgets.QDoubleSpinBox(self.gbox_hsv)
        self.dp_hsv_s.setMinimumSize(QtCore.QSize(30, 24))
        self.dp_hsv_s.setMaximumSize(QtCore.QSize(36, 16777215))
        self.dp_hsv_s.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.dp_hsv_s.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dp_hsv_s.setDecimals(3)
        self.dp_hsv_s.setMaximum(1.0)
        self.dp_hsv_s.setSingleStep(0.01)
        self.dp_hsv_s.setObjectName("dp_hsv_s")
        self.gbox_hsv_grid_layout.addWidget(self.dp_hsv_s, 1, 2, 1, 1)
        self.lb_hsv_v = QtWidgets.QLabel(self.gbox_hsv)
        self.lb_hsv_v.setText("V")
        self.lb_hsv_v.setObjectName("lb_hsv_v")
        self.gbox_hsv_grid_layout.addWidget(self.lb_hsv_v, 2, 0, 1, 1)
        self.hs_hsv_v = QtWidgets.QSlider(self.gbox_hsv)
        self.hs_hsv_v.setMinimumSize(QtCore.QSize(0, 12))
        self.hs_hsv_v.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hs_hsv_v.setMaximum(1000)
        self.hs_hsv_v.setPageStep(0)
        self.hs_hsv_v.setOrientation(QtCore.Qt.Horizontal)
        self.hs_hsv_v.setObjectName("hs_hsv_v")
        self.gbox_hsv_grid_layout.addWidget(self.hs_hsv_v, 2, 1, 1, 1)
        self.dp_hsv_v = QtWidgets.QDoubleSpinBox(self.gbox_hsv)
        self.dp_hsv_v.setMinimumSize(QtCore.QSize(30, 24))
        self.dp_hsv_v.setMaximumSize(QtCore.QSize(36, 16777215))
        self.dp_hsv_v.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.dp_hsv_v.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dp_hsv_v.setDecimals(3)
        self.dp_hsv_v.setMaximum(1.0)
        self.dp_hsv_v.setSingleStep(0.01)
        self.dp_hsv_v.setObjectName("dp_hsv_v")
        self.gbox_hsv_grid_layout.addWidget(self.dp_hsv_v, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.gbox_hsv, 3, 0, 1, 4)
        self.retranslateUi(ScrollCube)
        QtCore.QMetaObject.connectSlotsByName(ScrollCube)

    def retranslateUi(self, ScrollCube):
        pass
