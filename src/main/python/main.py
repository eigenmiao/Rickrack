# -*- coding: utf-8 -*-

__LICENSE__ = """
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.
"""

__COPYRIGHT__ = """
Copyright (c) 2019-2023 by Eigenmiao. All Rights Reserved.
"""

__WEBSITE__ = """
https://github.com/eigenmiao/Rickrack
"""

__VERSION__ = """
v2.8.40-x3d3s3-stable
"""

__AUTHOR__ = """
Eigenmiao (eigenmiao@outlook.com)
"""

__DATE__ = """
July 23, 2023
"""

__HELP__ = """
INTRODUCTION:
  Rickrack is a free and user-friendly color editor. It is designed to 
  generate a set of harmonious colors from the color wheel or other places. 
  You can share these colors with your friends, or apply them into your 
  creative works.

  See https://eigenmiao.com/rickrack/ for more information.

VERSION:
  Rickrack {version} ({date})

AUTHOR:
  {author}

USAGE:
  Rickrack [OPTION]... [FILE]

OPTION:
  -h, --help        : display this help information.
  -v, --version     : output the version information.
  -t, --temporary   : open software in temporary mode without loading local 
                      settings and history color results. It will discard all 
                      changes on exit.
  -r, --reset=NAME  : reset software functions, where NAME is "settings" (or 
                      "setting"), "layout" (or "geometry"), "set", "depot", 
                      "work" or "all".
  -i, --input=FILE  : open the FILE in software on startup, where FILE is 
                      the file path for input, such as a color set file (or 
                      a color depot file) with extension "dps" (or "dpc").
  -o, --output=FILE : export color results into the FILE on exit, where FILE 
     (--export=FILE)  is the file path for output. Acceptable file extensions 
                      include "dps", "txt", "aco", "ase", "gpl" and "xml". 
                      (Both "--output" and "--export" are avaiable.)
  -w, --window=NUM  : display or hide the seven dock windows in software, 
                      where NUM is a decimal integer less than 128 (0 refers 
                      to hide all windows, and 127 for display all, and 1 for 
                      display Rickrack Result window only).
  -e, --sequence=NUM: similar to "-w" and "--window", but NUM is in binary 
                      type, i.e., 0000000 (or 0) refers to hide all 
                      windows, and 1111111 for display all, and 0000001 
                      (or 1) for display Rickrack Result window only.
  -l, --lang=LANG   : set display language, where LANG is "zh", "en", 
     (--locale=LANG)  "ja", or other self-defined languages. (Both "--lang" 
                      and "--locale" are avaiable.)
  -p, --port=INDEX  : provide color result on local service, where INDEX is 
                      the service port (less than 65536). Here, 0 stands for 
                      not opening the service (by default).

FILE:
  The input tag "-i" or "--input" can be omitted and use command 
  `Rickrack FILE` to open an existed file.
  FILE is the file path for openning, such as color set file, color 
  depot file or an image file with png, jpg, bmp extentions.

CONSOLE OUTPUT:
  The output information is printed on screen by default. The tag "*" 
  indicates the index of selected color before closing the software. The sequence 
  displayed in Rickrack Result window is 2, 1, 0, 3, 4, i.e., the first color in 
  color list is the middle (main) color in Rickrack Result window.
  The information is shown like below:
  ------------------------------------
  + # Name: Console Results
  + # Rule: ...
  + # Time: ...; ...
  + # Index R       G       B       H         S         V         Hex Code
  +   2     ...     ...     ...     ...       ...       ...       ...
  +   1     ...     ...     ...     ...       ...       ...       ...
  + * 0     ...     ...     ...     ...       ...       ...       ...
  +   3     ...     ...     ...     ...       ...       ...       ...
  +   4     ...     ...     ...     ...       ...       ...       ...
  +
  + # Full Colors
  + ...   ...    ...    ...    ...
  + 
  + # Color Grid ...
  + ...   ...    ...
  + ...   ...    ...
  . ...   ...    ...

SERVER OUTPUT:
  The output information is provided on local server (default off).
  The information is shown like below:
  ------------------------------------
  ... rule index ... color set, name ... col ... color grid, name ...

EXAMPLE:
  $> Rickrack
  $> Rickrack -h
  $> Rickrack -t
  $> Rickrack -l zh
  $> Rickrack -i /path/to/myimage.png
  $> Rickrack -i /path/to/mycolors.dps
  $> Rickrack -o /path/to/mycolors.dps
  $> Rickrack -r settings
  $> Rickrack -w 0
  $> 

NOTICE:
* Use command `Rickrack` without any option, and this software will 
  automatically load previous settings and color results from history
  files.

COPYRIGHT:
  {copyright}
""".format(**{"version": __VERSION__[1:-1], "author": __AUTHOR__[1:-1], "copyright": __COPYRIGHT__[1:-1], "date": __DATE__[1:-1]})

import os
import sys
import json
import time
import hashlib
import numpy as np
from getopt import getopt
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QGridLayout, QMessageBox, QShortcut, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QCoreApplication, QTemporaryDir, QUrl, QTranslator, QSettings, QByteArray, QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtGui import QGuiApplication, QIcon, QPixmap, QImage, QDesktopServices, QKeySequence, QFontDatabase
from cguis.design.main_window import Ui_MainWindow
from cguis.resource import view_rc
from clibs.server import ResultServer
from ricore.args import Args
from ricore.color import Color
from ricore.history import History
from ricore.export import export_text
from ricore.check import check_is_num
from ricore.icon import get_icon
from wgets.wheel import Wheel
from wgets.image import Image
from wgets.board import Board
from wgets.depot import Depot
from wgets.cube import CubeTable
from wgets.rule import Rule
from wgets.mode import Mode
from wgets.operation import Operation
from wgets.script import Script
from wgets.channel import Channel
from wgets.transformation import Transformation
from wgets.settings import Settings
from wgets.choice import Choice
from wgets.splash import DPSplash


class Rickrack(QMainWindow, Ui_MainWindow):
    def __init__(self, resources, sys_argv):
        super().__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setAttribute(Qt.WA_InputMethodEnabled)
        self._sys_argv = sys_argv
        reset_all_args = self._sys_argv["reset"] in ("settings", "setting", "all") or self._sys_argv["temporary"]
        self._args = Args(resources, resetall=reset_all_args, uselang=self._sys_argv["lang"])
        self._args.global_temp_dir = QTemporaryDir()
        try:
            geo_args = QSettings(self._args.geometry_args, QSettings.IniFormat)
        except Exception as err:
            geo_args = None
        self._geo_args = geo_args
        self._save_settings_before_close = True
        self._connected_keymaps = {}
        self._curr_view_idx = 0
        self._curr_docks = None
        self._func_tr_()
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)
        self.setMinimumSize(600, 460)
        self._setup_workarea()
        self._setup_result()
        self._setup_rule()
        self._setup_mode()
        self._setup_operation()
        self._setup_script()
        self._setup_channel()
        self._setup_transformation()
        self._setup_settings()
        self.tabifyDockWidget(self.operation_dock_widget, self.script_dock_widget)
        self.tabifyDockWidget(self.mode_dock_widget, self.transformation_dock_widget)
        self.tabifyDockWidget(self.rule_dock_widget, self.channel_dock_widget)
        self.operation_dock_widget.raise_()
        self.mode_dock_widget.raise_()
        self.rule_dock_widget.raise_()
        self.rule_dock_widget.visibilityChanged.connect(lambda x: self.actionRule.setChecked(self.rule_dock_widget.isVisible()))
        self.channel_dock_widget.visibilityChanged.connect(lambda x: self.actionChannel.setChecked(self.channel_dock_widget.isVisible()))
        self.operation_dock_widget.visibilityChanged.connect(lambda x: self.actionOperation.setChecked(self.operation_dock_widget.isVisible()))
        self.script_dock_widget.visibilityChanged.connect(lambda x: self.actionScript.setChecked(self.script_dock_widget.isVisible()))
        self.mode_dock_widget.visibilityChanged.connect(lambda x: self.actionMode.setChecked(self.mode_dock_widget.isVisible()))
        self.transformation_dock_widget.visibilityChanged.connect(lambda x: self.actionTransformation.setChecked(self.transformation_dock_widget.isVisible()))
        self.result_dock_widget.visibilityChanged.connect(lambda x: self.actionResult.setChecked(self.result_dock_widget.isVisible()))
        self.actionOpen.triggered.connect(self._wget_operation.exec_open)
        self.actionSave.triggered.connect(self._wget_operation.exec_save)
        self.actionImport.triggered.connect(self._wget_operation.exec_import)
        self.actionExport.triggered.connect(self._wget_operation.exec_export)
        self.actionOpenImage.triggered.connect(self._ins_open_image)
        self.actionSaveImage.triggered.connect(self._ins_save_image)
        self.actionQuit.triggered.connect(self.close)
        self.actionDirectQuit.triggered.connect(self.close_without_save)
        self.actionCreate.triggered.connect(self._ins_create)
        self.actionLocate.triggered.connect(self._ins_locate)
        self.actionDerive.triggered.connect(self._ins_derive)
        self.actionAttach.triggered.connect(self._ins_attach)
        self.actionSettings.triggered.connect(self._wget_settings.showup)
        self.actionWheel.triggered.connect(self._switch_to_wheel)
        self.actionImage.triggered.connect(self._switch_to_image)
        self.actionBoard.triggered.connect(self._switch_to_board)
        self.actionDepot.triggered.connect(self._switch_to_depot)
        self.actionRule.triggered.connect(self._inner_show_or_hide(self.rule_dock_widget))
        self.actionChannel.triggered.connect(self._inner_show_or_hide(self.channel_dock_widget))
        self.actionOperation.triggered.connect(self._inner_show_or_hide(self.operation_dock_widget))
        self.actionScript.triggered.connect(self._inner_show_or_hide(self.script_dock_widget))
        self.actionMode.triggered.connect(self._inner_show_or_hide(self.mode_dock_widget))
        self.actionTransformation.triggered.connect(self._inner_show_or_hide(self.transformation_dock_widget))
        self.actionResult.triggered.connect(self._inner_show_or_hide(self.result_dock_widget))
        self.actionAll.triggered.connect(self._inner_all_show_or_hide)
        self.actionHomepage.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_main_site)))
        self.actionUpdate.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_update_site)))
        self.actionForum.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_dissc_site)))
        self.actionAbout.triggered.connect(lambda x: self._show_about())
        self.actionInfo.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_aucc_site)))
        self.actionInspired_R.triggered.connect(lambda x: self._change_layout(0))
        self.actionInspired_L.triggered.connect(lambda x: self._change_layout(1))
        self.actionSpecific_R.triggered.connect(lambda x: self._change_layout(2))
        self.actionSpecific_L.triggered.connect(lambda x: self._change_layout(3))
        self.actionConcise_R.triggered.connect(lambda x: self._change_layout(4))
        self.actionConcise_L.triggered.connect(lambda x: self._change_layout(5))
        self._setup_toolbar()
        self._setup_skey()
        self._setup_server()
        self._tr = QTranslator()
        self._app = QApplication.instance()
        self._install_translator()
        self._wget_wheel.setFocus()
        self._load_last_work()
        if self._sys_argv["input"]:
            if self._sys_argv["input"].split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff", "webp"):
                self._switch_to_image()
                self._wget_image.open_image(self._sys_argv["input"])
            else:
                try:
                    with open(self._sys_argv["input"], "r", encoding="utf-8") as f:
                        color_dict = json.load(f)
                except Exception as err:
                    color_dict = None
                if isinstance(color_dict, dict) and "type" in color_dict:
                    if color_dict["type"] == "depot":
                        self._switch_to_depot()
                        self._wget_operation.dp_open(color_dict, direct_dict=True, dp_path=os.path.dirname(os.path.abspath(self._sys_argv["input"])))
                    elif color_dict["type"] == "set":
                        self._wget_operation.dp_import(color_dict, direct_dict=True)
        if self._args.load_settings_failed:
            self._wget_operation.warning(self._wget_operation.main_errs[self._args.load_settings_failed - 1])
        self._default_state = self.saveState()
        self._default_size = self.size()
        self._change_layout()
        self._setup_geometry()
        QApplication.desktop().screenCountChanged.connect(self._setup_geometry)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, on=self._args.win_on_top)
        self.actionRule.setChecked(self.rule_dock_widget.isVisible())
        self.actionChannel.setChecked(self.channel_dock_widget.isVisible())
        self.actionOperation.setChecked(self.operation_dock_widget.isVisible())
        self.actionScript.setChecked(self.script_dock_widget.isVisible())
        self.actionMode.setChecked(self.mode_dock_widget.isVisible())
        self.actionTransformation.setChecked(self.transformation_dock_widget.isVisible())
        self.actionResult.setChecked(self.result_dock_widget.isVisible())
        if self._sys_argv["window"] >= 0:
            self.rule_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 // 2 // 2 // 2 // 2 // 2 % 2))
            self.channel_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 // 2 // 2 // 2 // 2 % 2))
            self.operation_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 // 2 // 2 // 2 % 2))
            self.script_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 // 2 // 2 % 2))
            self.mode_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 // 2 % 2))
            self.transformation_dock_widget.setVisible(bool(self._sys_argv["window"] // 2 % 2))
            self.result_dock_widget.setVisible(bool(self._sys_argv["window"] % 2))
        if os.path.isdir(os.sep.join((resources, "fonts"))):
            for font in os.listdir(os.sep.join((resources, "fonts"))):
                if font.split(".")[-1].lower() in ("ttf", "otf"):
                    QFontDatabase.addApplicationFont(os.sep.join((resources, "fonts", font)))
        self._wheel_icon = None
        self._image_icon = None
        self._board_icon = None
        self._depot_icon = None
        self._sel_wheel_icon = None
        self._sel_image_icon = None
        self._sel_board_icon = None
        self._sel_depot_icon = None
        self._setup_interface_style(change_pn_colors=False)
        self._history = History(self._args)
        self._history.backup()
        self._setup_history()

    def _setup_geometry(self):
        scr_count = QApplication.desktop().screenCount()
        if scr_count >= 0:
            cur_geometry = self.geometry()
            cur_in_window = False
            for sc_idx in range(scr_count):
                scr_geometry = QApplication.desktop().availableGeometry(sc_idx)
                if scr_geometry.x() < cur_geometry.x() < scr_geometry.x() + scr_geometry.width() and scr_geometry.y() < cur_geometry.y() < scr_geometry.y() + scr_geometry.height():
                    cur_in_window = True
                    break
            if not cur_in_window:
                scr_geometry = QApplication.desktop().availableGeometry(0)
                new_x = (scr_geometry.width() - cur_geometry.width()) / 2
                new_y = (scr_geometry.height() - cur_geometry.height()) / 2
                new_x = 0 if new_x < 0 else new_x
                new_y = 0 if new_y < 0 else new_y
                self.setGeometry(new_x, new_y, cur_geometry.width(), cur_geometry.height())

    def _setup_workarea(self):
        def _wheel_status(value):
            color_sign = self._color_descs[value[0]] + self._color_descs[value[1] + 10]
            self.statusbar.showMessage(self._status_descs[4].format(color_sign))

        def _image_status(value):
            if len(value) == 2:
                self.statusbar.showMessage(self._status_descs[1].format(*value))
            elif len(value) == 4:
                self.statusbar.showMessage(self._status_descs[2].format(*value))
            else:
                color_sign = self._color_descs[value[4][0]] + self._color_descs[value[4][1] + 10]
                self.statusbar.showMessage(self._status_descs[5].format(*value[:4], color_sign))

        def _board_status(value):
            if value[0] == 0:
                    self.statusbar.showMessage(self._status_descs[8].format(value[1], value[2], value[3], value[4] + 1))
            elif value[0] == 1:
                self.statusbar.showMessage(self._status_descs[7].format(value[1]))
            else:
                self.statusbar.showMessage(self._status_descs[6])

        def _depot_status(value):
            self.statusbar.showMessage(self._status_descs[3].format(*value))

        def _transfer_image(value):
            self._switch_to_image()
            self._wget_image.open_image(value, direct=True)
        central_widget_grid_layout = QGridLayout(self.central_widget)
        central_widget_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_wheel = Wheel(self.central_widget, self._args)
        self._wget_image = Image(self.central_widget, self._args)
        self._wget_board = Board(self.central_widget, self._args)
        self._wget_depot = Depot(self.central_widget, self._args)
        self._wget_wheel.ps_status_changed.connect(_wheel_status)
        self._wget_image.ps_status_changed.connect(_image_status)
        self._wget_board.ps_status_changed.connect(_board_status)
        self._wget_depot.ps_status_changed.connect(_depot_status)
        self._wget_board.ps_transfer_image.connect(_transfer_image)
        self._wget_wheel.show()
        self._wget_image.hide()
        self._wget_board.hide()
        self._wget_depot.hide()
        central_widget_grid_layout.addWidget(self._wget_wheel)
        central_widget_grid_layout.addWidget(self._wget_image)
        central_widget_grid_layout.addWidget(self._wget_board)
        central_widget_grid_layout.addWidget(self._wget_depot)
        self._wget_image.ps_assit_pt_changed.connect(self._wget_wheel.change_assit_point)
        self._wget_board.ps_assit_pt_changed.connect(self._wget_wheel.change_assit_point)

    def _setup_result(self):
        result_grid_layout = QGridLayout(self.result_dock_contents)
        result_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_cube_table = CubeTable(self.result_dock_contents, self._args)
        result_grid_layout.addWidget(self._wget_cube_table)
        self._wget_wheel.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_wheel.ps_index_changed.connect(lambda x: self._wget_cube_table.update_index())
        self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_board.ps_index_changed.connect(lambda x: self._wget_cube_table.update_index())
        self._wget_board.ps_value_changed.connect(lambda x: self._wget_mode.update_grid_vales())
        self._wget_board.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_image.update_color_loc())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_board.update_index())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_depot.update_index())
        self._wget_board.ps_linked.connect(lambda x: self._wget_cube_table.update_all())
        self._wget_depot.ps_linked.connect(lambda x: self._wget_cube_table.update_all())

    def _setup_history(self):
        self._wget_wheel.ps_history_backup.connect(self._inner_backup)
        self._wget_image.ps_history_backup.connect(self._inner_backup)
        self._wget_board.ps_history_backup.connect(self._inner_backup)
        self._wget_depot.ps_history_backup.connect(self._inner_backup)
        self._wget_cube_table.ps_history_backup.connect(self._inner_backup)
        self._wget_operation.ps_opened.connect(self._inner_backup)
        self._wget_operation.ps_update.connect(self._inner_backup)
        self._wget_wheel.ps_undo.connect(self._inner_undo_or_redo)
        self._wget_image.ps_undo.connect(self._inner_undo_or_redo)
        self._wget_board.ps_undo.connect(self._inner_undo_or_redo)
        self._wget_depot.ps_undo.connect(self._inner_undo_or_redo)

    def _setup_toolbar(self):
        self.toolbar.addAction(self.actionWheel)
        self.toolbar.addAction(self.actionImage)
        self.toolbar.addAction(self.actionBoard)
        self.toolbar.addAction(self.actionDepot)
        separator = QWidget(self)
        separator.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.toolbar.addWidget(separator)
        self.toolbar.addAction(self.actionSettings)
        self.toolbar.addAction(self.actionAbout)

    def _setup_rule(self):
        rule_grid_layout = QGridLayout(self.rule_dock_contents)
        rule_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_rule = Rule(self.rule_dock_contents, self._args)
        rule_grid_layout.addWidget(self._wget_rule)
        self._wget_rule.ps_rule_changed.connect(lambda x: self._wget_cube_table.modify_rule())
        self._wget_image.ps_modify_rule.connect(lambda x: self._wget_rule.update_rule())

    def _setup_mode(self):
        mode_grid_layout = QGridLayout(self.mode_dock_contents)
        mode_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_mode = Mode(self.mode_dock_contents, self._args)
        mode_grid_layout.addWidget(self._wget_mode)
        self._update_info_cbox(0)
        self._wget_mode.ps_mode_changed.connect(lambda x: self._wget_cube_table.modify_box_visibility())
        self._wget_mode.ps_assistp_changed.connect(lambda x: self._wget_board.update())
        self._wget_mode.ps_info_changed.connect(lambda x: self._update_info_args())
        self._wget_mode.ps_color_sys_changed.connect(lambda x: self._wget_wheel.update())
        self._wget_wheel.setMouseTracking(bool(self._args.show_info_pts[0]))
        self._wget_image.setMouseTracking(bool(self._args.show_info_pts[1]))
        self._wget_board.setMouseTracking(bool(self._args.show_info_pts[2]))

    def _setup_operation(self):
        operation_grid_layout = QGridLayout(self.operation_dock_contents)
        operation_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_operation = Operation(self.operation_dock_contents, self._args)
        operation_grid_layout.addWidget(self._wget_operation)

        def _functn(value):
            if self._curr_view_idx == 0:
                if value == 0:
                    self._wget_wheel.insert_assit_point((15 * np.random.random() + 15) * np.random.choice([1,-1]), 0.3 * np.random.random() - 0.15, 0)
                if value == 1:
                    self._ins_create()
                elif value == 2:
                    self._wget_wheel.reset_assit_point()
                elif value == 3:
                    self._switch_to_board()
            elif self._curr_view_idx == 1:
                if value == 0:
                    self._ins_open_image()
                elif value == 1:
                    self._ins_save_image()
                elif value == 2:
                    self._ins_locate()
                elif value == 3:
                    self._switch_to_board()
            elif self._curr_view_idx == 2:
                if value == 0:
                    self._ins_save_image()
                elif value == 1:
                    self._wget_board.clear_or_gen_grid_list()
                elif value == 2:
                    self._wget_board.clear_or_gen_assit_color_list()
                elif value == 3:
                    self._wget_board.reset_locations()
            elif self._curr_view_idx == 3:
                if value == 0:
                    self._wget_depot.import_set()
                if value == 1:
                    self._ins_attach()
                elif value == 2:
                    self._wget_depot.export_set()
                elif value == 3:
                    self._wget_depot.detail_set()
            self._inner_backup()
        self._wget_operation.ps_functn.connect(_functn)
        self._wget_operation.ps_update.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_operation.ps_update.connect(lambda x: self._wget_rule.update_rule())
        self._wget_operation.ps_update.connect(lambda x: self._wget_mode.update_grid_vales())
        self._wget_operation.ps_opened.connect(lambda x: self._wget_depot.initialize())
        self._wget_depot.ps_update.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_depot.ps_update.connect(lambda x: self._wget_rule.update_rule())
        self._wget_depot.ps_update.connect(lambda x: self._wget_mode.update_grid_vales())
        self._wget_depot.ps_export.connect(self._wget_operation.exec_export)
        self._wget_wheel.ps_dropped.connect(lambda x: self._inner_import(x))
        self._wget_board.ps_dropped.connect(lambda x: self._inner_import(x))
        self._wget_depot.ps_dropped.connect(lambda x: self._inner_open(x))
        self._wget_depot.ps_appended.connect(lambda x: self._inner_append(x))
        self._wget_depot.ps_open_image_url.connect(lambda x: self._wget_image.open_image(x[0], with_full_locs=x[1]))
        self._wget_operation.show_import_export()

    def _setup_script(self):
        script_grid_layout = QGridLayout(self.script_dock_contents)
        script_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_script = Script(self.script_dock_contents, self._args)
        script_grid_layout.addWidget(self._wget_script)
        self._wget_script.ps_filter.connect(lambda x: self._wget_image.open_image("", script=x))
        self._wget_script.ps_crop.connect(self._wget_image.crop_image)
        self._wget_script.ps_freeze.connect(self._wget_image.freeze_image)
        self._wget_script.ps_freeze.connect(self._wget_board.freeze_image)
        self._wget_script.ps_print.connect(self._wget_image.save_image)
        self._wget_script.ps_print.connect(self._wget_board.save_image)
        self._wget_script.ps_extract.connect(self._wget_image.extract_image)

    def _setup_channel(self):
        channel_grid_layout = QGridLayout(self.channel_dock_contents)
        channel_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_channel = Channel(self.channel_dock_contents, self._args)
        channel_grid_layout.addWidget(self._wget_channel)
        self._wget_channel.ps_channel_changed.connect(lambda x: self._wget_image.open_category())
        self._wget_image.ps_image_changed.connect(lambda x: self._wget_channel.reset())
        self._wget_image.ps_recover_channel.connect(lambda x: self._wget_channel.recover())

    def _setup_transformation(self):
        transformation_grid_layout = QGridLayout(self.transformation_dock_contents)
        transformation_grid_layout.setContentsMargins(2, 2, 2, 2)
        self._wget_transformation = Transformation(self.transformation_dock_contents, self._args)
        transformation_grid_layout.addWidget(self._wget_transformation)
        self._wget_transformation.ps_home.connect(lambda x: self._wget_image.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_image.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_image.zoom(x, "default"))
        self._wget_transformation.ps_home.connect(lambda x: self._wget_board.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_board.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_board.zoom(x))
        self._wget_transformation.ps_home.connect(lambda x: self._wget_depot.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_depot.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_depot.zoom(x))
        self._wget_transformation.ps_replace.connect(self._wget_image.replace_color)
        self._wget_transformation.ps_enhance.connect(self._wget_image.enhance_image)

    def _setup_settings(self):
        self._wget_settings = Settings(self, self._args)
        self._wget_settings.ps_rule_changed.connect(self._wget_cube_table.modify_rule)
        self._wget_settings.ps_lang_changed.connect(self._install_translator)
        self._wget_settings.ps_skey_changed.connect(self._setup_skey)
        self._wget_settings.ps_settings_changed.connect(self._inner_update)
        self._wget_settings.ps_clean_up.connect(self._wget_depot.clean_up)
        self._wget_settings.ps_restore_layout.connect(lambda: self._change_layout(layout_src=None))
        self._wget_settings.ps_theme_changed.connect(lambda x: self._setup_interface_style(change_pn_colors=x))

    def _setup_server(self):
        if self._sys_argv["port"]:
            self._server = ResultServer(self._args, port=self._sys_argv["port"])
            self._server.ps_iset.connect(lambda x: self._inner_import((x, False)))
            self._server.ps_oset.connect(lambda x: self._wget_operation.dp_export(x, True))
            self._server.ps_idpt.connect(lambda x: self._inner_open((x, False)))
            self._server.ps_odpt.connect(lambda x: self._wget_operation.dp_save(x, True))
            self._server.ps_cidx.connect(lambda x: self._inner_modify_color(*x))
            self._choice_dialog = Choice(self, self._args)
            self._server.ps_star.connect(self._choice_dialog.showup)
            self._server.ps_exit.connect(lambda x: self.close_with_verify() if x else self.close_without_save())
            self._server.start()
        else:
            self._server = None
            self._choice_dialog = None

    def _translate_server(self):
        if self._sys_argv["port"] and self._choice_dialog:
            self._choice_dialog._func_tr_()
            self._choice_dialog.update_text()

    def _update_info_args(self):
        curr_wget = None
        if self._wget_wheel.isVisible():
            curr_wget = self._wget_wheel
            idx = 0
        elif self._wget_image.isVisible():
            curr_wget = self._wget_image
            idx = 1
        elif self._wget_board.isVisible():
            curr_wget = self._wget_board
            idx = 2
        else:
            return
        value = self._wget_mode.get_info()
        self._args.show_info_pts[idx] = value
        self._wget_wheel.setMouseTracking(bool(self._args.show_info_pts[0]))
        self._wget_image.setMouseTracking(bool(self._args.show_info_pts[1]))
        self._wget_board.setMouseTracking(bool(self._args.show_info_pts[2]))

    def _update_info_cbox(self, view_idx=None):
        idx = 0
        if self._wget_image.isVisible():
            idx = 1
        elif self._wget_board.isVisible():
            idx = 2
        value = self._args.show_info_pts[idx]
        self._wget_mode.update_info(value in (1, 3), value > 1)

    def _change_layout(self, layout_src=""):
        if isinstance(layout_src, str) and self._args.geometry_args:
            main_win_layout = 0
            main_win_state = self._geo_args.value('main_win_state', None)
            main_win_geometry = self._geo_args.value('main_win_geometry', None)
        elif isinstance(layout_src, int):
            main_win_layout = layout_src
            main_win_state = QByteArray.fromBase64(bytes(self._args.layouts[layout_src], 'ascii'))
            main_win_geometry = None
        else:
            main_win_layout = 0
            main_win_state = self._default_state
            main_win_geometry = None
            self.resize(self._default_size)
        if main_win_state:
            try:
                self.restoreState(main_win_state)
            except Exception as err:
                pass
        if main_win_geometry:
            try:
                self.restoreGeometry(main_win_geometry)
            except Exception as err:
                pass

    def _load_last_work(self):
        if self._sys_argv["temporary"]:
            return
        if self._args.store_loc:
            store_path = self._args.resources
        else:
            store_path = self._args.usr_store
        if not os.path.isdir(os.sep.join((store_path, "MyColors"))):
            os.makedirs(os.sep.join((store_path, "MyColors")))
        if os.path.isfile(os.sep.join((store_path, "depot.json"))) and self._sys_argv["reset"] not in ("depot", "work", "all"):
            self._wget_operation.dp_open(os.sep.join((store_path, "depot.json")))
        if os.path.isfile(os.sep.join((store_path, "set.json"))) and self._sys_argv["reset"] not in ("set", "work", "all"):
            self._wget_operation.dp_import(os.sep.join((store_path, "set.json")))

    def _inner_backup(self, accept=True):
        self._history.backup()
        self._wget_cube_table.update_color()

    def _inner_undo_or_redo(self, undo=True):
        self._args.sys_activated_assit_idx = -1
        if undo:
            self._history.undo()
            self._wget_rule.update_rule()
            self._wget_cube_table.update_color()
        else:
            self._history.redo()
            self._wget_rule.update_rule()
            self._wget_cube_table.update_color()

    def _inner_modify_color(self, idx, color):
        if idx and idx in range(5):
            self._args.sys_activated_idx = int(idx)
            self._args.sys_activated_assit_idx = -1
        fmt_color = Color(color, tp="hsv", overflow=self._args.sys_color_set.get_overflow())
        self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, fmt_color)
        self._wget_cube_table.update_color()
        self._wget_cube_table.update_index()

    def _switch_to_wheel(self):
        self._curr_view_idx = 0
        if self._sel_wheel_icon:
            self.actionWheel.setIcon(self._sel_wheel_icon)
            self.actionImage.setIcon(self._image_icon)
            self.actionBoard.setIcon(self._board_icon)
            self.actionDepot.setIcon(self._depot_icon)
        self._wget_operation.update_functn_text(0)
        if self._wget_wheel.isVisible():
            self._inner_all_show_or_hide_current()
        self._wget_wheel.show()
        self._wget_image.hide()
        self._wget_board.hide()
        self._wget_board.hide_detail()
        self._wget_depot.hide()
        self._wget_depot.hide_detail()
        # self.statusbar.showMessage(self._status_descs[0])
        self._update_info_cbox(0)
        self._wget_operation.show_import_export()
        self._wget_wheel.init_key()
        self._wget_wheel.setFocus()

    def _switch_to_image(self):
        self._curr_view_idx = 1
        if self._sel_image_icon:
            self.actionWheel.setIcon(self._wheel_icon)
            self.actionImage.setIcon(self._sel_image_icon)
            self.actionBoard.setIcon(self._board_icon)
            self.actionDepot.setIcon(self._depot_icon)
        self._wget_operation.update_functn_text(1)
        if self._wget_image.isVisible():
            self._inner_all_show_or_hide_current()
        self._wget_image.show()
        self._wget_wheel.hide()
        self._wget_board.hide()
        self._wget_board.hide_detail()
        self._wget_depot.hide()
        self._wget_depot.hide_detail()
        # self.statusbar.showMessage(self._status_descs[0])
        self._update_info_cbox(1)
        self._wget_operation.show_import_export()
        self._wget_image.init_key()
        self._wget_image.setFocus()

    def _switch_to_board(self):
        self._curr_view_idx = 2
        if self._sel_board_icon:
            self.actionWheel.setIcon(self._wheel_icon)
            self.actionImage.setIcon(self._image_icon)
            self.actionBoard.setIcon(self._sel_board_icon)
            self.actionDepot.setIcon(self._depot_icon)
        self._wget_operation.update_functn_text(2)
        if self._wget_board.isVisible():
            self._inner_all_show_or_hide_current()
        self._wget_board.show()
        self._wget_wheel.hide()
        self._wget_image.hide()
        self._wget_depot.hide()
        self._wget_depot.hide_detail()
        self._update_info_cbox(2)
        self._wget_operation.show_import_export()
        self._wget_board.init_key()
        self._wget_board.setFocus()

    def _switch_to_depot(self):
        self._curr_view_idx = 3
        if self._sel_depot_icon:
            self.actionWheel.setIcon(self._wheel_icon)
            self.actionImage.setIcon(self._image_icon)
            self.actionBoard.setIcon(self._board_icon)
            self.actionDepot.setIcon(self._sel_depot_icon)
        self._wget_operation.update_functn_text(3)
        if self._wget_depot.isVisible():
            self._inner_all_show_or_hide_current()
        self._wget_depot.show()
        self._wget_wheel.hide()
        self._wget_image.hide()
        self._wget_board.hide()
        self._wget_board.hide_detail()
        # self.statusbar.showMessage(self._status_descs[0])
        self._wget_operation.show_open_and_save()
        self._wget_depot.init_key()
        self._wget_depot.setFocus()

    def _ins_create(self):
        if not self._wget_wheel.isVisible():
            self._switch_to_wheel()
        self._wget_cube_table.create_set(direct=True)

    def _ins_open_image(self):
        if not self._wget_image.isVisible():
            self._switch_to_image()
        self._wget_image.open_image_dialog()

    def _ins_save_image(self):
        if self._wget_image.isVisible():
            self._wget_image.save_image()
        elif self._wget_board.isVisible():
            self._wget_board.save_image()

    def _ins_locate(self):
        if not self._wget_image.isVisible():
            self._switch_to_image()
        if not self._wget_image.image3c.display:
            self._ins_open_image()
        self._wget_image.extract_image(0)

    def _ins_derive(self):
        if not self._wget_board.isVisible():
            self._switch_to_board()
        self._wget_board.reset_locations()

    def _ins_attach(self):
        if not self._wget_depot.isVisible():
            self._switch_to_depot()
        self._wget_depot.attach_set()

    def _inner_update(self):
        self._args.sys_color_set.set_overflow(self._args.overflow)
        self._args.sys_color_set.set_hsv_ranges(self._args.h_range, self._args.s_range, self._args.v_range)
        self._wget_wheel.update()
        self._wget_image.update()
        self._wget_board.update()
        self._wget_depot.update_all()
        self._wget_cube_table.update_all()
        self._wget_cube_table.modify_box_visibility()
        self._wget_rule.update_rule()
        self._wget_mode.update_mode()
        self._update_info_cbox()
        self.update()

    def _inner_show_or_hide(self, wget):
        def _func_():
            if wget.isVisible():
                wget.hide()
            else:
                wget.show()
            # self.statusbar.showMessage(self._status_descs[0])
        return _func_

    def _inner_all_show_or_hide(self):
        if self.rule_dock_widget.isVisible() and self.channel_dock_widget.isVisible() and self.operation_dock_widget.isVisible() and self.script_dock_widget.isVisible() and self.mode_dock_widget.isVisible() and self.transformation_dock_widget.isVisible() and self.result_dock_widget.isVisible():
            self.rule_dock_widget.hide()
            self.channel_dock_widget.hide()
            self.operation_dock_widget.hide()
            self.script_dock_widget.hide()
            self.mode_dock_widget.hide()
            self.transformation_dock_widget.hide()
            self.result_dock_widget.hide()
        else:
            self.rule_dock_widget.show()
            self.channel_dock_widget.show()
            self.operation_dock_widget.show()
            self.script_dock_widget.show()
            self.mode_dock_widget.show()
            self.transformation_dock_widget.show()
            self.result_dock_widget.show()
        # self.statusbar.showMessage(self._status_descs[0])

    def _inner_all_show_or_hide_current(self):
        curr_docks = (
            self.rule_dock_widget.isVisible(),
            self.channel_dock_widget.isVisible(),
            self.operation_dock_widget.isVisible(),
            self.script_dock_widget.isVisible(),
            self.mode_dock_widget.isVisible(),
            self.transformation_dock_widget.isVisible(),
            self.result_dock_widget.isVisible(),
        )
        if True in curr_docks:
            self.rule_dock_widget.hide()
            self.channel_dock_widget.hide()
            self.operation_dock_widget.hide()
            self.script_dock_widget.hide()
            self.mode_dock_widget.hide()
            self.transformation_dock_widget.hide()
            self.result_dock_widget.hide()
            self._curr_docks = curr_docks
        else:
            if True in self._curr_docks:
                self.rule_dock_widget.setVisible(self._curr_docks[0])
                self.channel_dock_widget.setVisible(self._curr_docks[1])
                self.operation_dock_widget.setVisible(self._curr_docks[2])
                self.script_dock_widget.setVisible(self._curr_docks[3])
                self.mode_dock_widget.setVisible(self._curr_docks[4])
                self.transformation_dock_widget.setVisible(self._curr_docks[5])
                self.result_dock_widget.setVisible(self._curr_docks[6])
            else:
                self.rule_dock_widget.show()
                self.channel_dock_widget.show()
                self.operation_dock_widget.show()
                self.script_dock_widget.show()
                self.mode_dock_widget.show()
                self.transformation_dock_widget.show()
                self.result_dock_widget.show()

    def _inner_open(self, depot_file):
        self._wget_operation.dp_open(depot_file[0], direct_dict=depot_file[1])
        self.update()

    def _inner_import(self, set_file):
        self._wget_operation.dp_import(set_file[0], direct_dict=set_file[1])
        self.update()

    def _inner_append(self, set_file):
        color_list = self._wget_operation.dp_import(set_file[0], direct_dict=set_file[1], return_set=True)
        if color_list:
            self._wget_depot.attach_set(color_list=color_list)
        # self.update()

    def _install_translator(self):
        self._app.removeTranslator(self._tr)
        if self._args.lang != "default":
            lang = os.sep.join((self._args.resources, "langs", self._args.lang))
            self._tr.load(lang)
            self._app.installTranslator(self._tr)
        self._func_tr_()
        self._wget_wheel._func_tr_()
        self._wget_image._func_tr_()
        self._wget_board._func_tr_()
        self._wget_depot._func_tr_()
        self._wget_rule._func_tr_()
        self._wget_channel._func_tr_()
        self._wget_operation._func_tr_()
        self._wget_transformation._func_tr_()
        self._wget_mode._func_tr_()
        self._wget_script._func_tr_()
        self._wget_settings._func_tr_()
        self._wget_settings.retranslateUi(self._wget_settings)
        self.retranslateUi(self)
        self._wget_board.update_text()
        self._wget_depot.update_text()
        self._wget_rule.update_text()
        self._wget_channel.update_text()
        self._wget_operation.update_text()
        self._wget_operation.update_functn_text(self._curr_view_idx)
        self._wget_transformation.update_text()
        self._wget_mode.update_text()
        self._wget_script.update_text()
        self._wget_settings.update_text()
        self._translate_server()
        if self._args.lang[:2].lower() in ("zh", "ja", "ko"):
            main_info = "焰火十二卷 {}".format("-".join((self._args.info_version_zh.split("-")[0], self._args.info_version_zh.split("-")[2])))
            if self._sys_argv["port"]:
                port_info = "端口：{}".format(self._sys_argv["port"])
                main_info = self._info_descs[12].format(main_info, port_info)
        else:
            main_info = "Rickrack {}".format("-".join((self._args.info_version_en.split("-")[0], self._args.info_version_en.split("-")[2])))
            if self._sys_argv["port"]:
                port_info = "Port: {}".format(self._sys_argv["port"])
                main_info = self._info_descs[12].format(main_info, port_info)
        self.setWindowTitle(main_info)
        self.setStatusTip(self._status_descs[0])
        self.update()

    def _setup_interface_style(self, change_pn_colors=True):
        curr_positive_color = ( 80,  80,  80)
        curr_negative_color = (245, 245, 245)
        curr_wheel_ed_color = (255, 255, 255)
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        if self._args.style_id == 0:
            qstyle = ""
        else:
            qss_file = os.sep.join((self._args.resources, "styles", "default.qss"))
            if os.path.isfile(qss_file):
                try:
                    with open(qss_file, encoding="utf-8") as qf:
                        qstyle = qf.read()
                except Exception as err:
                    qstyle = ""
            else:
                qstyle = ""
            ffmy = ", ".join(["\"{}\"".format(ff) for ff in self._args.font_family])
            ffmy = ffmy if ffmy else "\"\""
            qstyle = qstyle.replace("$qc_font_family", ffmy)
            qstyle = qstyle.replace("$qc_font_weight", str(self._args.font_weight * 100))
            qstyle = qstyle.replace("$qc_font_size", str(self._args.font_size) + "px")
            if self._args.style_id in (1, 2):
                qc_char = Color.hsv2hec((0, 0, 0.1))
                qc_char_over = Color.hsv2hec((0, 0, 0.0))
                gen_h = 0.0
                gen_s = 0.0
                gen_v = 1.0 - (self._args.style_id - 1) * 0.2
                qc_list = Color.hsv2hec((gen_h, gen_s, gen_v - 0.08))
                qc_list_over = Color.hsv2hec((gen_h, gen_s, gen_v - 0.16))
                qc_list_selected = Color.hsv2hec((gen_h, gen_s, 0.35))
                qc_workarea = Color.hsv2hec((gen_h, gen_s, gen_v))
                qc_workarea_over = Color.hsv2hec((gen_h, gen_s, gen_v - 0.05))
            elif self._args.style_id in (3, 4):
                qc_char = Color.hsv2hec((0, 0, 0.9))
                qc_char_over = Color.hsv2hec((0, 0, 1.0))
                gen_h = 0.0
                gen_s = 0.0
                gen_v = 0.4 - (self._args.style_id - 3) * 0.25
                qc_list = Color.hsv2hec((gen_h, gen_s, gen_v + 0.08))
                qc_list_over = Color.hsv2hec((gen_h, gen_s, gen_v + 0.24))
                qc_list_selected = Color.hsv2hec((gen_h, gen_s, 1.0))
                qc_workarea = Color.hsv2hec((gen_h, gen_s, gen_v))
                qc_workarea_over = Color.hsv2hec((gen_h, gen_s, gen_v + 0.1))
            elif self._args.style_id in (5, 6, 7, 8, 9, 10):
                qc_char = Color.hsv2hec((0, 0, 0.1))
                qc_char_over = Color.hsv2hec((0, 0, 0.0))
                if self._args.style_id % 2 == 1:
                    gen_h = (self._args.style_id - 5) * 60.0 + 25.0
                else:
                    gen_h = (self._args.style_id - 5) * 60.0 - 5.0
                gen_s = 0.05
                gen_v = 1.0
                qc_list = Color.hsv2hec((gen_h + 10.0, gen_s + 0.24, gen_v - 0.02))
                qc_list_over = Color.hsv2hec((gen_h - 10.0, gen_s + 0.32, gen_v - 0.03))
                qc_list_selected = Color.hsv2hec((gen_h - 30.0, gen_s + 0.42, 0.90))
                qc_workarea = "FFFFFF"
                qc_workarea_over = Color.hsv2hec((gen_h + 5.0, gen_s + 0.1, gen_v - 0.01))
            elif self._args.style_id in (11, 12, 13, 14, 15, 16):
                qc_char = Color.hsv2hec((0, 0, 0.9))
                qc_char_over = Color.hsv2hec((0, 0, 1.0))
                if self._args.style_id % 2 == 1:
                    gen_h = (self._args.style_id - 11) * 60.0 + 25.0
                else:
                    gen_h = (self._args.style_id - 11) * 60.0 - 5.0
                gen_s = 1.0
                gen_v = 0.05
                qc_list = Color.hsv2hec((gen_h + 10.0, gen_s - 0.24, gen_v + 0.16))
                qc_list_over = Color.hsv2hec((gen_h - 10.0, gen_s - 0.32, gen_v + 0.36))
                qc_list_selected = Color.hsv2hec((gen_h - 30.0, gen_s - 0.32, 0.64))
                qc_workarea = "000000"
                qc_workarea_over = Color.hsv2hec((gen_h + 5.0, gen_s - 0.1, gen_v + 0.06))
            if self._args.bakgd_id in (1, 2):
                qc_char = Color.hsv2hec((0, 0, 0.1))
                qc_char_over = Color.hsv2hec((0, 0, 0.0))
                gen_h = 0.0
                gen_s = 0.0
                gen_v = 1.0 - (self._args.bakgd_id - 1) * 0.2
                qc_list = Color.hsv2hec((gen_h, gen_s, gen_v - 0.08))
                qc_workarea = Color.hsv2hec((gen_h, gen_s, gen_v))
                qc_workarea_over = Color.hsv2hec((gen_h, gen_s, gen_v - 0.05))
            elif self._args.bakgd_id in (3, 4):
                qc_char = Color.hsv2hec((0, 0, 0.9))
                qc_char_over = Color.hsv2hec((0, 0, 1.0))
                gen_h = 0.0
                gen_s = 0.0
                gen_v = 0.4 - (self._args.bakgd_id - 3) * 0.25
                qc_list = Color.hsv2hec((gen_h, gen_s, gen_v + 0.08))
                qc_workarea = Color.hsv2hec((gen_h, gen_s, gen_v))
                qc_workarea_over = Color.hsv2hec((gen_h, gen_s, gen_v + 0.1))
            elif self._args.bakgd_id in (5, 6, 7, 8, 9, 10):
                qc_char = Color.hsv2hec((0, 0, 0.1))
                qc_char_over = Color.hsv2hec((0, 0, 0.0))
                if self._args.bakgd_id % 2 == 1:
                    gen_h = (self._args.bakgd_id - 5) * 60.0 + 25.0
                else:
                    gen_h = (self._args.bakgd_id - 5) * 60.0 - 5.0
                gen_s = 0.05
                gen_v = 1.0
                qc_list = Color.hsv2hec((gen_h + 10.0, gen_s + 0.24, gen_v - 0.02))
                qc_workarea = "FFFFFF"
                qc_workarea_over = Color.hsv2hec((gen_h + 5.0, gen_s + 0.1, gen_v - 0.01))
            elif self._args.bakgd_id in (11, 12, 13, 14, 15, 16):
                qc_char = Color.hsv2hec((0, 0, 0.9))
                qc_char_over = Color.hsv2hec((0, 0, 1.0))
                if self._args.bakgd_id % 2 == 1:
                    gen_h = (self._args.bakgd_id - 11) * 60.0 + 25.0
                else:
                    gen_h = (self._args.bakgd_id - 11) * 60.0 - 5.0
                gen_s = 1.0
                gen_v = 0.05
                qc_list = Color.hsv2hec((gen_h + 10.0, gen_s - 0.24, gen_v + 0.24))
                qc_workarea = "000000"
                qc_workarea_over = Color.hsv2hec((gen_h + 5.0, gen_s - 0.1, gen_v + 0.06))
            if self._args.style_id < 5:
                forecolor = qc_list_selected
                backcolor = qc_list_selected
                curropc = 0.6
            else:
                forecolor = qc_list_selected
                backcolor = qc_list_over
                curropc = 1.0
            self._sel_wheel_icon = get_icon("wheel", forecolor, backcolor, curropc, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._sel_image_icon = get_icon("image", forecolor, backcolor, curropc, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._sel_board_icon = get_icon("board", forecolor, backcolor, curropc, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._sel_depot_icon = get_icon("depot", forecolor, backcolor, curropc, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._wheel_icon = get_icon("sel_wheel", forecolor, backcolor, 0.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._image_icon = get_icon("sel_image", forecolor, backcolor, 0.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._board_icon = get_icon("sel_board", forecolor, backcolor, 0.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self._depot_icon = get_icon("sel_depot", forecolor, backcolor, 0.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self.actionWheel.setIcon(self._sel_wheel_icon if self._curr_view_idx == 0 else self._wheel_icon)
            self.actionImage.setIcon(self._sel_image_icon if self._curr_view_idx == 1 else self._image_icon)
            self.actionBoard.setIcon(self._sel_board_icon if self._curr_view_idx == 2 else self._board_icon)
            self.actionDepot.setIcon(self._sel_depot_icon if self._curr_view_idx == 3 else self._depot_icon)
            self.actionCreate.setIcon(self._wheel_icon)
            self.actionLocate.setIcon(self._image_icon)
            self.actionDerive.setIcon(self._board_icon)
            self.actionAttach.setIcon(self._depot_icon)
            open_icon = get_icon("open", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            save_icon = get_icon("save", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self.actionOpen.setIcon(open_icon)
            self.actionSave.setIcon(save_icon)
            self.actionOpenImage.setIcon(open_icon)
            self.actionSaveImage.setIcon(save_icon)
            self.actionImport.setIcon(open_icon)
            self.actionExport.setIcon(save_icon)
            self.actionSettings.setIcon(get_icon("settings", forecolor, backcolor, curropc, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionHomepage.setIcon(get_icon("home", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionUpdate.setIcon(get_icon("update", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionForum.setIcon(get_icon("forum", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionQuit.setIcon(get_icon("quit", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionDirectQuit.setIcon(get_icon("quit", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionAbout.setIcon(get_icon("about", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            self.actionInfo.setIcon(get_icon("info", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            layout_l = get_icon("layout_l", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            layout_r = get_icon("layout_r", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            self.actionInspired_L.setIcon(layout_l)
            self.actionSpecific_L.setIcon(layout_l)
            self.actionConcise_L.setIcon(layout_l)
            self.actionInspired_R.setIcon(layout_r)
            self.actionSpecific_R.setIcon(layout_r)
            self.actionConcise_R.setIcon(layout_r)
            for btn_idx in range(7):
                name = ("up", "down", "left", "right", "reset", "zoom_in", "zoom_out")[btn_idx]
                self._wget_transformation.move_btns[btn_idx].setIcon(get_icon(name, forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon))
            curr_positive_color = Color.hec2rgb(qc_list_selected)
            curr_negative_color = Color.hec2rgb(qc_list)
            curr_wheel_ed_color = Color.hec2rgb(qc_workarea_over)
            get_icon("box_up", forecolor, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("box_down", forecolor, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("box_left", forecolor, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("box_right", forecolor, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("sel_up", qc_list_over, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("sel_down", qc_list_over, backcolor, 0.64, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("float", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            get_icon("close", forecolor, backcolor, 1.0, 0.0, self._args.global_temp_dir.path(), app_icon)
            qstyle = qstyle.replace("$qc_workarea_over", "#" + qc_workarea_over)
            qstyle = qstyle.replace("$qc_workarea", "#" + qc_workarea)
            qstyle = qstyle.replace("$qc_char_over", "#" + qc_char_over)
            qstyle = qstyle.replace("$qc_char", "#" + qc_char)
            qstyle = qstyle.replace("$qc_list_selected", "#" + qc_list_selected)
            qstyle = qstyle.replace("$qc_list_over", "#" + qc_list_over)
            qstyle = qstyle.replace("$qc_list", "#" + qc_list)
            qstyle = qstyle.replace("$up_arrow", "/".join([self._args.global_temp_dir.path(), "box_up.svg"]))
            qstyle = qstyle.replace("$down_arrow", "/".join([self._args.global_temp_dir.path(), "box_down.svg"]))
            qstyle = qstyle.replace("$left_arrow", "/".join([self._args.global_temp_dir.path(), "box_left.svg"]))
            qstyle = qstyle.replace("$right_arrow", "/".join([self._args.global_temp_dir.path(), "box_right.svg"]))
            qstyle = qstyle.replace("$sel_up_arrow", "/".join([self._args.global_temp_dir.path(), "sel_up.svg"]))
            qstyle = qstyle.replace("$sel_down_arrow", "/".join([self._args.global_temp_dir.path(), "sel_down.svg"]))
            qstyle = qstyle.replace("$float_arrow", "/".join([self._args.global_temp_dir.path(), "float.svg"]))
            qstyle = qstyle.replace("$close_arrow", "/".join([self._args.global_temp_dir.path(), "close.svg"]))
        if change_pn_colors:
            self._args.modify_settings("positive_color", curr_positive_color)
            self._args.modify_settings("negative_color", curr_negative_color)
            self._args.modify_settings("wheel_ed_color", curr_wheel_ed_color)
            self._wget_settings.setup_colors()
        self._app.setStyleSheet(qstyle)
        self._wget_image.init_icon()

    def _show_about(self):
        if self._args.lang[:2].lower() in ("zh", "ja", "ko"):
            info = "焰火十二卷（调色板软件）"
        else:
            info = "Rickrack (Color Palette Generator)"
        info = "<h2>{}</h2><hr/><p style='line-height:150%;'>".format(info)
        if self._args.lang[:2].lower() in ("zh", "ja", "ko"):
            info += self._info_descs[1].format(self._args.info_version_zh) + "<br/>"
            info += self._info_descs[2].format(self._args.info_author_zh) + "<br/>"
            info += self._info_descs[3].format(self._args.info_date_zh) + "<br/>"
        else:
            info += self._info_descs[1].format(self._args.info_version_en) + "<br/>"
            info += self._info_descs[2].format(self._args.info_author_en) + "<br/>"
            info += self._info_descs[3].format(self._args.info_date_en) + "<br/>"
        info += self._info_descs[4] # + "<br/>"
        info += "</p><hr/><p style='line-height:130%;'>"
        info += self._info_descs[5] + "<br/>"
        info += self._info_descs[10] + "<br/>"
        info += self._info_descs[8].format(QT_VERSION_STR, PYQT_VERSION_STR) # + "<br/>"
        if self._args.lang[:2].lower() not in ("zh", "en"):
            info += "<br/>" + self._info_descs[13]
        info += "</p>"
        info = "<html><body>{}</body></html>".format(info)
        box = QMessageBox(self)
        box.setWindowTitle(self._info_descs[0])
        box.setText(info)
        resized_img = QImage(":/images/images/info_256.png").scaled(128 * self.devicePixelRatioF(), 360 * self.devicePixelRatioF(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        resized_img.setDevicePixelRatio(self.devicePixelRatioF())
        box.setIconPixmap(QPixmap.fromImage(resized_img))
        ok_btn = QPushButton()
        ok_btn.setText(self._info_descs[6])
        box.addButton(ok_btn, QMessageBox.RejectRole)
        box.setDefaultButton(ok_btn)
        visit_btn = QPushButton()
        visit_btn.clicked.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_main_site)))
        visit_btn.setText(self._info_descs[7])
        box.addButton(visit_btn, QMessageBox.AcceptRole)
        aucc_btn = QPushButton()
        aucc_btn.clicked.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_aucc_site)))
        aucc_btn.setText(self._info_descs[11])
        box.addButton(aucc_btn, QMessageBox.AcceptRole)
        aucc_btn = QPushButton()
        aucc_btn.clicked.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_font_site)))
        aucc_btn.setText(self._info_descs[14])
        box.addButton(aucc_btn, QMessageBox.AcceptRole)
        box.exec_()

    def _chg_win_on_top(self):
        self._args.win_on_top = not self._args.win_on_top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, on=self._args.win_on_top)
        if not self.isVisible():
            self.show()

    def close_with_verify(self):
        if self._wget_board.hide_detail() or self._wget_depot.hide_detail():
            return
        if self._wget_image.cancel_croping_or_locating():
            return
        if self._wget_settings.isVisible():
            self._wget_settings.hide()
            return
        self._save_settings_before_close = True
        self.close()

    def close_without_save(self):
        self._save_settings_before_close = False
        self.close()

    def rename(self, source, target):
        if os.path.isfile(target):
            os.remove(target)
        os.rename(source, target)

    def save_main_settings(self):
        if self._args.store_loc:
            store_path = self._args.resources
        else:
            store_path = self._args.usr_store
        if not os.path.isdir(os.sep.join((store_path, "History", "Depots"))):
            os.makedirs(os.sep.join((store_path, "History", "Depots")))
        if os.path.isfile(os.sep.join((store_path, "depot.temp"))):
            os.remove(os.sep.join((store_path, "depot.temp")))
        self._wget_operation.dp_save(os.sep.join((store_path, "depot.temp")), True)
        if os.path.isfile(os.sep.join((store_path, "depot.temp"))):
            if self._args.max_history_files and os.path.isfile(os.sep.join((store_path, "depot.json"))):
                json_hash = ""
                temp_hash = ""
                with open(os.sep.join((store_path, "depot.json")), "rb") as frp:
                    json_hash = hashlib.md5(frp.read()).hexdigest()
                with open(os.sep.join((store_path, "depot.temp")), "rb") as frp:
                    temp_hash = hashlib.md5(frp.read()).hexdigest()
                if json_hash != temp_hash or (not json_hash) or (not temp_hash):
                    for backup_file in os.listdir(os.sep.join((store_path, "History", "Depots"))):
                        if os.path.isfile(os.sep.join((store_path, "History", "Depots", backup_file))):
                            if backup_file[:6] == "depot_" and backup_file[-13:] == "_bak_{:0>3d}.json".format(self._args.max_history_files - 1):
                                os.remove(os.sep.join((store_path, "History", "Depots", backup_file)))
                                continue
                            for i in range(self._args.max_history_files - 1):
                                if os.path.isfile(os.sep.join((store_path, "History", "Depots", backup_file))) and backup_file[:6] == "depot_" and backup_file[-13:] == "_bak_{:0>3d}.json".format(i):
                                    self.rename(os.sep.join((store_path, "History", "Depots", backup_file)), os.sep.join((store_path, "History", "Depots", backup_file[:-13] + "_bak_{:0>3d}.json".format(i + 1))))
                    self.rename(os.sep.join((store_path, "depot.json")), os.sep.join((store_path, "History", "Depots", "depot_{}_bak_000.json".format(time.strftime("%Y%m%d_%H%M%S", time.localtime())))))
                    self.rename(os.sep.join((store_path, "depot.temp")), os.sep.join((store_path, "depot.json")))
            else:
                self.rename(os.sep.join((store_path, "depot.temp")), os.sep.join((store_path, "depot.json")))
        if not os.path.isdir(os.sep.join((store_path, "History", "Sets"))):
            os.makedirs(os.sep.join((store_path, "History", "Sets")))
        if os.path.isfile(os.sep.join((store_path, "set.temp"))):
            os.remove(os.sep.join((store_path, "set.temp")))
        self._wget_operation.dp_export(os.sep.join((store_path, "set.temp")), True)
        if os.path.isfile(os.sep.join((store_path, "set.temp"))):
            if self._args.max_history_files and os.path.isfile(os.sep.join((store_path, "set.json"))):
                json_hash = ""
                temp_hash = ""
                with open(os.sep.join((store_path, "set.json")), "rb") as frp:
                    json_hash = hashlib.md5(frp.read()).hexdigest()
                with open(os.sep.join((store_path, "set.temp")), "rb") as frp:
                    temp_hash = hashlib.md5(frp.read()).hexdigest()
                if json_hash != temp_hash or (not json_hash) or (not temp_hash):
                    for backup_file in os.listdir(os.sep.join((store_path, "History", "Sets"))):
                        if os.path.isfile(os.sep.join((store_path, "History", "Sets", backup_file))):
                            if backup_file[:4] == "set_" and backup_file[-13:] == "_bak_{:0>3d}.json".format(self._args.max_history_files - 1):
                                os.remove(os.sep.join((store_path, "History", "Sets", backup_file)))
                                continue
                            for i in range(self._args.max_history_files - 1):
                                if os.path.isfile(os.sep.join((store_path, "History", "Sets", backup_file))) and backup_file[:4] == "set_" and backup_file[-13:] == "_bak_{:0>3d}.json".format(i):
                                    self.rename(os.sep.join((store_path, "History", "Sets", backup_file)), os.sep.join((store_path, "History", "Sets", backup_file[:-13] + "_bak_{:0>3d}.json".format(i + 1))))
                    self.rename(os.sep.join((store_path, "set.json")), os.sep.join((store_path, "History", "Sets", "set_{}_bak_000.json".format(time.strftime("%Y%m%d_%H%M%S", time.localtime())))))
                    self.rename(os.sep.join((store_path, "set.temp")), os.sep.join((store_path, "set.json")))
            else:
                self.rename(os.sep.join((store_path, "set.temp")), os.sep.join((store_path, "set.json")))
        for backup_file in os.listdir(store_path):
            if os.path.isfile(os.sep.join((store_path, backup_file))) and backup_file[-5:] == ".temp":
                os.remove(os.sep.join((store_path, backup_file)))
        if self._args.geometry_args:
            self._geo_args.setValue('main_win_state', self.saveState())
            self._geo_args.setValue('main_win_geometry', self.saveGeometry())
        self._args.save_settings()

    def _setup_skey(self):
        self.actionHomepage.setShortcuts(self._args.shortcut_keymaps[0])
        self.actionUpdate.setShortcuts(self._args.shortcut_keymaps[1])
        self.actionAbout.setShortcuts(self._args.shortcut_keymaps[2])
        self.actionInfo.setShortcuts(self._args.shortcut_keymaps[50])
        self.actionOpen.setShortcuts(self._args.shortcut_keymaps[6])
        self.actionSave.setShortcuts(self._args.shortcut_keymaps[7])
        self.actionImport.setShortcuts(self._args.shortcut_keymaps[8])
        self.actionExport.setShortcuts(self._args.shortcut_keymaps[9])
        self.actionCreate.setShortcuts(self._args.shortcut_keymaps[10])
        self.actionLocate.setShortcuts(self._args.shortcut_keymaps[11])
        self.actionDerive.setShortcuts(self._args.shortcut_keymaps[12])
        self.actionAttach.setShortcuts(self._args.shortcut_keymaps[13])
        self.actionWheel.setShortcuts(self._args.shortcut_keymaps[52])
        self.actionImage.setShortcuts(self._args.shortcut_keymaps[53])
        self.actionBoard.setShortcuts(self._args.shortcut_keymaps[54])
        self.actionDepot.setShortcuts(self._args.shortcut_keymaps[55])
        self.actionSettings.setShortcuts(self._args.shortcut_keymaps[3])
        self.actionAll.setShortcuts(self._args.shortcut_keymaps[49])
        for skey in self._args.shortcut_keymaps[4]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self.close_with_verify)
        for skey in self._args.shortcut_keymaps[5]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self.close_without_save)
        for skey in self._args.shortcut_keymaps[14]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_cube_table.clipboard_act("rgb"))
        for skey in self._args.shortcut_keymaps[15]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_cube_table.clipboard_act("hsv"))
        for skey in self._args.shortcut_keymaps[16]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_cube_table.clipboard_act("hec"))
        for skey in self._args.shortcut_keymaps[17]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_wheel.clipboard_all("rgb"))
        for skey in self._args.shortcut_keymaps[18]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_wheel.clipboard_all("hsv"))
        for skey in self._args.shortcut_keymaps[19]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_wheel.clipboard_all("hec"))
        for actv_idx, skey_idx in zip(range(5), (25, 24, 23, 26, 27)):
            for skey in self._args.shortcut_keymaps[skey_idx]:
                if skey in self._connected_keymaps:
                    shortcut = self._connected_keymaps[skey]
                    shortcut.disconnect()
                else:
                    shortcut = QShortcut(QKeySequence(skey), self)
                    self._connected_keymaps[skey] = shortcut
                shortcut.activated.connect(self._wget_cube_table.active_by_num(actv_idx))
        for skey in self._args.shortcut_keymaps[28]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.move_up)
        for skey in self._args.shortcut_keymaps[29]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.move_down)
        for skey in self._args.shortcut_keymaps[30]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.move_left)
        for skey in self._args.shortcut_keymaps[31]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.move_right)
        for skey in self._args.shortcut_keymaps[34]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.reset_home)
        for skey in self._args.shortcut_keymaps[32]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.zoom_in)
        for skey in self._args.shortcut_keymaps[33]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._wget_transformation.zoom_out)
        for skey in self._args.shortcut_keymaps[48]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(self._chg_win_on_top)
        for skey in self._args.shortcut_keymaps[47]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(lambda: self._inner_undo_or_redo(True))
        for skey in self._args.shortcut_keymaps[56]:
            if skey in self._connected_keymaps:
                shortcut = self._connected_keymaps[skey]
                shortcut.disconnect()
            else:
                shortcut = QShortcut(QKeySequence(skey), self)
                self._connected_keymaps[skey] = shortcut
            shortcut.activated.connect(lambda: self._inner_undo_or_redo(False))
        self._wget_wheel.update_skey()
        self._wget_image.update_skey()
        self._wget_board.update_skey()
        self._wget_depot.update_skey()

    def closeEvent(self, event):
        if self._sys_argv["output"]:
            self._wget_operation.dp_export(self._sys_argv["output"], True)
        result_text = export_text([(self._args.sys_color_set, self._args.hm_rule, "Console Results", "", (time.time(), time.time()), self._args.sys_grid_locations, self._args.sys_grid_assitlocs, self._args.sys_grid_list, self._args.sys_grid_values),])
        for line in result_text.split("\n"):
            if line and len(line) > 3:
                if line[2] in [str(i) for i in range(10)] and int(line[2]) == self._args.sys_activated_idx:
                    print("+ *{}".format(line[1:]))
                else:
                    print("+ {}".format(line))
            else:
                print("+")
        if self._save_settings_before_close and not self._sys_argv["temporary"]:
            self.save_main_settings()
        self._args.remove_temp_dir()
        self._wget_wheel.close()
        self._wget_image.close()
        self._wget_depot.close()
        event.accept()

    def _func_tr_(self):
        _translate = QCoreApplication.translate
        self._info_descs = (
            _translate("Rickrack", "About"),
            _translate("Rickrack", "Version: {}"),
            _translate("Rickrack", "Author: {}"),
            _translate("Rickrack", "Update: {}"),
            _translate("Rickrack", "All Rights Reserved."),
            _translate("Rickrack", "Rickrack is a free software, which is distributed in the hope that it will be useful, but without any warranty. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License 3.0 (GPL 3.0) for more details."),
            _translate("Rickrack", "OK"),
            _translate("Rickrack", "Visit Website"),
            _translate("Rickrack", "Rickrack uses Qt version {} (PyQt version {}) licensed under GNU General Public License. Please see qt.io/licensing for an overview of Qt licensing."),
            _translate("Rickrack", "All images, documents and translations in Rickrack code repository are licensed under Creative Commons Attribution-NonCommercial-ShareAlike License 4.0 (CC BY-NC-SA 4.0) unless stating additionally."),
            _translate("Rickrack", "Rickrack default uses Noto Sans font family for interface display. These fonts are open-sourced under SIL Open Font License 1.1."),
            _translate("Rickrack", "Support Rickrack!"),
            _translate("Rickrack", "{} ({})"),
            _translate("Rickrack", "The internationalization (i18n) and localization (l10n) of Rickrack are based on Google Translate."),
            _translate("Rickrack", "Download Full Fonts"),
            )
        self._status_descs = (
            _translate("Rickrack", "Ready."),
            _translate("Rickrack", "Image Size: {} x {}."),
            _translate("Rickrack", "Image Size: {} x {}. Position: {} %, {} %."),
            _translate("Rickrack", "Depot Volume: Row {}, Col {}; Total {}, Index {}."),
            _translate("Rickrack", "Current Color: {}."),
            _translate("Rickrack", "Image Size: {} x {}. Position: {} %, {} %. Current Color: {}."),
            _translate("Rickrack", "Hide Control Points (Press Space to Show)."),
            _translate("Rickrack", "Assistant Points Count for Current Control Points: {}."),
            _translate("Rickrack", "Board Volume: Row {}, Col {}; Total {}, Index {}."),
        )
        self._color_descs = (
            _translate("Rickrack", "Deep "),
            _translate("Rickrack", "Snow "),
            _translate("Rickrack", "Heavy "),
            _translate("Rickrack", "Dull "),
            _translate("Rickrack", "Grey "),
            _translate("Rickrack", "Pale "),
            _translate("Rickrack", "Light "),
            _translate("Rickrack", "Bright "),
            _translate("Rickrack", "Dark "),
            _translate("Rickrack", "Vivid "),
            _translate("Rickrack", "Black"),
            _translate("Rickrack", "White"),
            _translate("Rickrack", "Red"),
            _translate("Rickrack", "Yellow"),
            _translate("Rickrack", "Green"),
            _translate("Rickrack", "Cyan"),
            _translate("Rickrack", "Blue"),
            _translate("Rickrack", "Magenta"),
            _translate("Rickrack", "Orange"),
            _translate("Rickrack", "Pink"),
        )
        _QColorDialog = (
            _translate("QColorDialog", "Hu&e:"),
            _translate("QColorDialog", "&Sat:"),
            _translate("QColorDialog", "&Val:"),
            _translate("QColorDialog", "&Red:"),
            _translate("QColorDialog", "&Green:"),
            _translate("QColorDialog", "Bl&ue:"),
            _translate("QColorDialog", "A&lpha channel:"),
            _translate("QColorDialog", "&HTML:"),
            _translate("QColorDialog", "Cursor at %1, %2\nPress ESC to cancel"),
            _translate("QColorDialog", "Select Color"),
            _translate("QColorDialog", "&Pick Screen Color"),
            _translate("QColorDialog", "&Basic colors"),
            _translate("QColorDialog", "&Custom colors"),
            _translate("QColorDialog", "&Add to Custom Colors"),
        )
        _QPlatformTheme = (
            _translate("QPlatformTheme", "OK"),
            _translate("QPlatformTheme", "Save"),
            _translate("QPlatformTheme", "Save All"),
            _translate("QPlatformTheme", "Open"),
            _translate("QPlatformTheme", "&Yes"),
            _translate("QPlatformTheme", "Yes to &All"),
            _translate("QPlatformTheme", "&No"),
            _translate("QPlatformTheme", "N&o to All"),
            _translate("QPlatformTheme", "Abort"),
            _translate("QPlatformTheme", "Retry"),
            _translate("QPlatformTheme", "Ignore"),
            _translate("QPlatformTheme", "Close"),
            _translate("QPlatformTheme", "Cancel"),
            _translate("QPlatformTheme", "Discard"),
            _translate("QPlatformTheme", "Help"),
            _translate("QPlatformTheme", "Apply"),
            _translate("QPlatformTheme", "Reset"),
            _translate("QPlatformTheme", "Restore Defaults"),
        )
        _QLineEdit = (
            _translate("QLineEdit", "&Undo"),
            _translate("QLineEdit", "&Redo"),
            _translate("QLineEdit", "Cu&t"),
            _translate("QLineEdit", "&Copy"),
            _translate("QLineEdit", "&Paste"),
            _translate("QLineEdit", "Delete"),
            _translate("QLineEdit", "Select All"),
        )
        _QAbstractSpinBox = (
            _translate("QAbstractSpinBox", "&Select All"),
            _translate("QAbstractSpinBox", "&Step up"),
            _translate("QAbstractSpinBox", "Step &down"),
        )
if __name__ == "__main__":
    argv_opts, argv_left = getopt(sys.argv[1:], "hvtr:i:o:w:e:l:p:", ["help", "version", "temporary", "reset=", "input=", "output=", "export=", "window=", "sequence=", "lang=", "locale=", "port="])
    sys_argv = {"temporary": False, "reset": "", "input": None, "output": None, "window": -1, "lang": "", "port": None}
    for opt_name,opt_value in argv_opts:
        if opt_name in ("-h", "--help"):
            print("\n+" + "-" * 34 + " Rickrack " + "-" * 34 + "+")
            print(__HELP__)
            sys.exit()
        elif opt_name in ("-v", "--version"):
            print("Rickrack {} ({})\n".format(__VERSION__[1:-1], __DATE__[1:-1]))
            sys.exit()
        elif opt_name in ("-t", "--temporary"):
            sys_argv["temporary"] = True
        elif opt_name in ("-r", "--reset"):
            if opt_value.lower() in ("settings", "setting", "layout", "geometry", "set", "depot", "work", "all"):
                sys_argv["reset"] = opt_value.lower()
        elif opt_name in ("-i", "--input"):
            if os.path.isfile(opt_value):
                sys_argv["input"] = opt_value
        elif opt_name in ("-o", "--output", "--export"):
            if os.path.isdir(os.path.dirname(opt_value)) and opt_value.split(".")[-1] in ("dps", "txt", "aco", "ase", "gpl", "xml"):
                sys_argv["output"] = opt_value
        elif opt_name in ("-w", "--window"):
            if opt_value and check_is_num(opt_value, length=3):
                sys_argv["window"] = int(opt_value)
        elif opt_name in ("-e", "--sequence"):
            if opt_value and check_is_num(opt_value, length=7, scope=("0", "1")):
                num = 0
                for i in range(len(opt_value)):
                    num = num + int(opt_value[len(opt_value) - i - 1]) * 2 ** i
                sys_argv["window"] = num
        elif opt_name in ("-l", "--lang", "--locale"):
            if len(opt_value) > 1:
                sys_argv["lang"] = opt_value
        elif opt_name in ("-p", "--port"):
            if opt_value and check_is_num(opt_value, length=5):
                port = int(opt_value)
                if 0 < port < 65536:
                    sys_argv["port"] = port
    if not sys_argv["input"] and argv_left and os.path.isfile(argv_left[-1]):
        sys_argv["input"] = argv_left[-1]
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    appctxt = ApplicationContext()
    DPS = DPSplash(appctxt.get_resource('.'), sys_argv)
    DPS.show()
    DP = Rickrack(appctxt.get_resource('.'), sys_argv)
    DP.show()
    DPS.finish(DP)
    DPS.deleteLater()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
