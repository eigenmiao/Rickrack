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

import re
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QGroupBox, QGridLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from ricore.check import check_key, check_nonempt_str_lst
from cguis.design.settings_dialog import Ui_SettingsDialog
from cguis.resource import view_rc


class Settings(QDialog, Ui_SettingsDialog):
    """
    Settings object based on QDialog. Init a settings in settings.
    """

    ps_rule_changed = pyqtSignal()
    ps_lang_changed = pyqtSignal()
    ps_skey_changed = pyqtSignal()
    ps_settings_changed = pyqtSignal()
    ps_clean_up = pyqtSignal()
    ps_restore_layout = pyqtSignal()
    ps_theme_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init settings.
        """

        super().__init__(wget, Qt.WindowCloseButtonHint)
        self.setupUi(self)

        # set attr.
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        # load args.
        self._args = args

        self._is_initializing = False

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        # init shortcuts.
        scroll_grid_layout = QGridLayout(self.shortcuts_scroll_contents)

        self._skey_gboxes = []
        self._skey_labels = []
        self._skey_ledits = []
        self._skey_accept = []

        skey_gboxe_layouts = []

        self._skey_distribution = (6, 8, 9, 5, 10, 10)

        g0_seq = (0, 1, 2, 4, 7, 8)
        g5_seq = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10)

        for gbox_id in range(len(self._skey_distribution)):
            skey_gbox = QGroupBox(self.shortcuts_scroll_contents)
            gbox_grid_layout = QGridLayout(skey_gbox)
            scroll_grid_layout.addWidget(skey_gbox, gbox_id, 1, 1, 1)
            self._skey_gboxes.append(skey_gbox)
            skey_gboxe_layouts.append(gbox_grid_layout)

            for curr_id in range(self._skey_distribution[gbox_id]):
                if gbox_id == 0:
                    skey_id = g0_seq[curr_id]

                elif gbox_id == 5:
                    skey_id = g5_seq[curr_id]

                else:
                    skey_id = curr_id

                skey_label = QLabel(skey_gbox)
                skey_label.setMinimumSize(200, 25)
                skey_label.setMaximumSize(400, 40)
                gbox_grid_layout.addWidget(skey_label, skey_id, 0, 1, 1)
                self._skey_labels.append(skey_label)

                for ledit_id in range(3):
                    skey_ledit = QLineEdit(skey_gbox)
                    skey_ledit.setMinimumSize(68, 25)
                    skey_ledit.setMaximumSize(120, 16777215)
                    gbox_grid_layout.addWidget(skey_ledit, skey_id, ledit_id + 1, 1, 1)
                    skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
                    self._skey_ledits.append(skey_ledit)

        # new shortcuts not in range.
        # key no. 48 at line 5, g0.
        skey_label = QLabel(self._skey_gboxes[0])
        skey_label.setMinimumSize(200, 25)
        skey_label.setMaximumSize(400, 40)
        skey_gboxe_layouts[0].addWidget(skey_label, 5, 0, 1, 1)
        self._skey_labels.append(skey_label)

        for ledit_id in range(3):
            skey_ledit = QLineEdit(self._skey_gboxes[0])
            skey_ledit.setMinimumSize(68, 25)
            skey_ledit.setMaximumSize(120, 16777215)
            skey_gboxe_layouts[0].addWidget(skey_ledit, 5, ledit_id + 1, 1, 1)
            skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
            self._skey_ledits.append(skey_ledit)

        # key no. 49 at line 6, g0.
        skey_label = QLabel(self._skey_gboxes[0])
        skey_label.setMinimumSize(200, 25)
        skey_label.setMaximumSize(400, 40)
        skey_gboxe_layouts[0].addWidget(skey_label, 6, 0, 1, 1)
        self._skey_labels.append(skey_label)

        for ledit_id in range(3):
            skey_ledit = QLineEdit(self._skey_gboxes[0])
            skey_ledit.setMinimumSize(68, 25)
            skey_ledit.setMaximumSize(120, 16777215)
            skey_gboxe_layouts[0].addWidget(skey_ledit, 6, ledit_id + 1, 1, 1)
            skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
            self._skey_ledits.append(skey_ledit)

        # key no. 50 at line 3, g0.
        skey_label = QLabel(self._skey_gboxes[0])
        skey_label.setMinimumSize(200, 25)
        skey_label.setMaximumSize(400, 40)
        skey_gboxe_layouts[0].addWidget(skey_label, 3, 0, 1, 1)
        self._skey_labels.append(skey_label)

        for ledit_id in range(3):
            skey_ledit = QLineEdit(self._skey_gboxes[0])
            skey_ledit.setMinimumSize(68, 25)
            skey_ledit.setMaximumSize(120, 16777215)
            skey_gboxe_layouts[0].addWidget(skey_ledit, 3, ledit_id + 1, 1, 1)
            skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
            self._skey_ledits.append(skey_ledit)

        # key no. 51 at line 7, g5.
        skey_label = QLabel(self._skey_gboxes[5])
        skey_label.setMinimumSize(200, 25)
        skey_label.setMaximumSize(400, 40)
        skey_gboxe_layouts[5].addWidget(skey_label, 7, 0, 1, 1)
        self._skey_labels.append(skey_label)

        for ledit_id in range(3):
            skey_ledit = QLineEdit(self._skey_gboxes[5])
            skey_ledit.setMinimumSize(68, 25)
            skey_ledit.setMaximumSize(120, 16777215)
            skey_gboxe_layouts[5].addWidget(skey_ledit, 7, ledit_id + 1, 1, 1)
            skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
            self._skey_ledits.append(skey_ledit)

        # key no. 52-55 at line 5-8, g3.
        for key_id in range(4):
            skey_label = QLabel(self._skey_gboxes[3])
            skey_label.setMinimumSize(200, 25)
            skey_label.setMaximumSize(400, 40)
            skey_gboxe_layouts[3].addWidget(skey_label, key_id + 5, 0, 1, 1)
            self._skey_labels.append(skey_label)

            for ledit_id in range(3):
                skey_ledit = QLineEdit(self._skey_gboxes[3])
                skey_ledit.setMinimumSize(68, 25)
                skey_ledit.setMaximumSize(120, 16777215)
                skey_gboxe_layouts[3].addWidget(skey_ledit, key_id + 5, ledit_id + 1, 1, 1)
                skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
                self._skey_ledits.append(skey_ledit)

        # key no. 56 at line 11, g5.
        skey_label = QLabel(self._skey_gboxes[5])
        skey_label.setMinimumSize(200, 25)
        skey_label.setMaximumSize(400, 40)
        skey_gboxe_layouts[5].addWidget(skey_label, 11, 0, 1, 1)
        self._skey_labels.append(skey_label)

        for ledit_id in range(3):
            skey_ledit = QLineEdit(self._skey_gboxes[5])
            skey_ledit.setMinimumSize(68, 25)
            skey_ledit.setMaximumSize(120, 16777215)
            skey_gboxe_layouts[5].addWidget(skey_ledit, 11, ledit_id + 1, 1, 1)
            skey_ledit.textChanged.connect(self.verify_shortcut_keymaps)
            self._skey_ledits.append(skey_ledit)

        # init comb boxes.
        for lang in self._args.usr_langs:
            self.lang_comb.addItem("")

        for method in self._args.global_hm_rules:
            self.hm_rule_comb.addItem("")

        for overfl in self._args.global_overflows:
            self.overflow_comb.addItem("")

        for ctp in ("rgb", "hsv", "cmyk", "lab", "gray"):
            self.export_swatch_ctp_comb.addItem(ctp.upper())

        for atp in range(3):
            self.export_ase_type_comb.addItem("")

        for wref in range(20):
            self.white_illuminant_comb.addItem("")

        for wref in range(2):
            self.white_observer_comb.addItem("")

        for fweight in range(9):
            self.font_weight_comb.addItem(str((fweight + 1) * 100))

        for bakid in range(17):
            self.bakgd_id_comb.addItem("")

        for styid in range(17):
            self.style_id_comb.addItem("")

        # init clean up button.
        self.clean_up_btn.clicked.connect(lambda x: self.ps_clean_up.emit())
        self.restore_original_btn.clicked.connect(lambda x: self.ps_restore_layout.emit())

        # init buttons.
        self.buttonBox.clear()

        self._btn_1 = QPushButton()
        self._btn_1.clicked.connect(self.application)
        self.buttonBox.addButton(self._btn_1, QDialogButtonBox.AcceptRole)

        self._btn_2 = QPushButton()
        self._btn_2.clicked.connect(self.close)
        self.buttonBox.addButton(self._btn_2, QDialogButtonBox.RejectRole)

        self._btn_3 = QPushButton()
        self._btn_3.clicked.connect(self.update_values)
        self.buttonBox.addButton(self._btn_3, QDialogButtonBox.ApplyRole)

        self._btn_4 = QPushButton()
        self._btn_4.clicked.connect(self.reset_values)
        self.buttonBox.addButton(self._btn_4, QDialogButtonBox.ResetRole)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def setup_colors(self):
        """
        Initialize color dp values by colors in self._args.
        """

        self.positive_color_0_dp.setValue(self._args.positive_color[0])
        self.positive_color_1_dp.setValue(self._args.positive_color[1])
        self.positive_color_2_dp.setValue(self._args.positive_color[2])
        self.negative_color_0_dp.setValue(self._args.negative_color[0])
        self.negative_color_1_dp.setValue(self._args.negative_color[1])
        self.negative_color_2_dp.setValue(self._args.negative_color[2])
        self.wheel_ed_color_0_dp.setValue(self._args.wheel_ed_color[0])
        self.wheel_ed_color_1_dp.setValue(self._args.wheel_ed_color[1])
        self.wheel_ed_color_2_dp.setValue(self._args.wheel_ed_color[2])

    def initialize(self):
        """
        Initialize values of boxes in settings dialog by self._args.
        """

        self._is_initializing = True

        self._skey_accept = []

        for i in range(len(self._args.shortcut_keymaps)):
            keymaps = self._args.shortcut_keymaps[i]

            for j in range(3):
                self._skey_ledits[i * 3 + j].setStyleSheet("")

                if j < len(keymaps):
                    self._skey_ledits[i * 3 + j].setText(keymaps[j])

                else:
                    self._skey_ledits[i * 3 + j].setText("")

        self.usr_color_ledit.setText(self._args.usr_color)
        self.usr_image_ledit.setText(self._args.usr_image)

        self.press_act_cbox.setChecked(self._args.press_act)
        self.store_loc_cbox.setChecked(self._args.store_loc)
        self.win_on_top_cbox.setChecked(self._args.win_on_top)

        self.lang_comb.setCurrentIndex([x[1] for x in self._args.usr_langs].index(self._args.lang))
        self.hm_rule_comb.setCurrentIndex(self._args.global_hm_rules.index(self._args.hm_rule))
        self.overflow_comb.setCurrentIndex(self._args.global_overflows.index(self._args.overflow))
        self.export_swatch_ctp_comb.setCurrentText(self._args.export_swatch_ctp.upper())
        self.export_ase_type_comb.setCurrentIndex(("spot", "global", "process").index(self._args.export_ase_type))
        self.font_weight_comb.setCurrentIndex(self._args.font_weight - 1)
        self.bakgd_id_comb.setCurrentIndex(self._args.bakgd_id)
        self.style_id_comb.setCurrentIndex(self._args.style_id)
        self.white_illuminant_comb.setCurrentIndex(self._args.white_illuminant)
        self.white_observer_comb.setCurrentIndex(self._args.white_observer)

        self.font_family_ledit.setText("; ".join(self._args.font_family))
        self.font_size_sp.setValue(self._args.font_size)

        self.max_history_files_sp.setValue(self._args.max_history_files)
        self.max_history_steps_sp.setValue(self._args.max_history_steps)
        self.export_grid_extns_ledit.setText(self._args.export_grid_extns)

        self.r_prefix_0_ledit.setText(self._args.r_prefix[0].replace("\n", "\\n").replace("\t", "\\t"))
        self.r_prefix_1_ledit.setText(self._args.r_prefix[1].replace("\n", "\\n").replace("\t", "\\t"))

        self.rgb_prefix_0_ledit.setText(self._args.rgb_prefix[0].replace("\n", "\\n").replace("\t", "\\t"))
        self.rgb_prefix_1_ledit.setText(self._args.rgb_prefix[1].replace("\n", "\\n").replace("\t", "\\t"))
        self.rgb_prefix_2_ledit.setText(self._args.rgb_prefix[2].replace("\n", "\\n").replace("\t", "\\t"))

        self.hec_prefix_0_ledit.setText(self._args.hec_prefix[0].replace("\n", "\\n").replace("\t", "\\t"))
        self.hec_prefix_1_ledit.setText(self._args.hec_prefix[1].replace("\n", "\\n").replace("\t", "\\t"))

        self.lst_prefix_0_ledit.setText(self._args.lst_prefix[0].replace("\n", "\\n").replace("\t", "\\t"))
        self.lst_prefix_1_ledit.setText(self._args.lst_prefix[1].replace("\n", "\\n").replace("\t", "\\t"))
        self.lst_prefix_2_ledit.setText(self._args.lst_prefix[2].replace("\n", "\\n").replace("\t", "\\t"))

        self.press_move_cbox.setChecked(self._args.press_move)
        self.show_hsv_cbox.setChecked(self._args.show_hsv)
        self.show_rgb_cbox.setChecked(self._args.show_rgb)

        self.h_range_0_dp.setValue(self._args.h_range[0])
        self.h_range_1_dp.setValue(self._args.h_range[1])
        self.s_range_0_dp.setValue(self._args.s_range[0])
        self.s_range_1_dp.setValue(self._args.s_range[1])
        self.v_range_0_dp.setValue(self._args.v_range[0])
        self.v_range_1_dp.setValue(self._args.v_range[1])

        self.wheel_ratio_dp.setValue(self._args.wheel_ratio)
        self.volum_ratio_dp.setValue(self._args.volum_ratio)
        self.cubic_ratio_dp.setValue(self._args.cubic_ratio)
        self.coset_ratio_dp.setValue(self._args.coset_ratio)

        self.stab_column_dp.setValue(self._args.stab_column)

        self.rev_direct_cbox.setChecked(self._args.rev_direct)

        self.s_tag_radius_dp.setValue(self._args.s_tag_radius)
        self.v_tag_radius_dp.setValue(self._args.v_tag_radius)

        self.zoom_step_dp.setValue(self._args.zoom_step)
        self.move_step_dp.setValue(self._args.move_step)

        self.rand_num_sp.setValue(self._args.rand_num)
        self.circle_dist_sp.setValue(self._args.circle_dist)

        self.positive_wid_sp.setValue(self._args.positive_wid)
        self.negative_wid_sp.setValue(self._args.negative_wid)
        self.wheel_ed_wid_sp.setValue(self._args.wheel_ed_wid)

        self.setup_colors()

        self._is_initializing = False

    def application(self):
        """
        Modify self._args by values of boxes in settings dialog.
        """

        if self._skey_accept:
            self._args.modify_settings("shortcut_keymaps", [(self._skey_accept[i * 3], self._skey_accept[i * 3 + 1], self._skey_accept[i * 3 + 2]) for i in range(len(self._args.shortcut_keymaps))])
            self.ps_skey_changed.emit()

        self._args.modify_settings("usr_color", self.usr_color_ledit.text())
        self._args.modify_settings("usr_image", self.usr_image_ledit.text())

        self._args.modify_settings("press_act", self.press_act_cbox.isChecked())
        self._args.modify_settings("store_loc", self.store_loc_cbox.isChecked())
        self._args.modify_settings("win_on_top", self.win_on_top_cbox.isChecked())

        hm_rule = self._args.hm_rule
        self._args.modify_settings("hm_rule", self._args.global_hm_rules[self.hm_rule_comb.currentIndex()])

        if self._args.hm_rule != hm_rule:
            self.ps_rule_changed.emit()

        self._args.modify_settings("overflow", self._args.global_overflows[self.overflow_comb.currentIndex()])

        lang = self._args.lang
        self._args.modify_settings("lang", self._args.usr_langs[self.lang_comb.currentIndex()][1])

        if self._args.lang != lang:
            self.ps_lang_changed.emit()

        self._args.modify_settings("export_swatch_ctp", self.export_swatch_ctp_comb.currentText().lower())
        self._args.modify_settings("export_ase_type", ("spot", "global", "process")[self.export_ase_type_comb.currentIndex()])

        self._args.modify_settings("white_illuminant", self.white_illuminant_comb.currentIndex())
        self._args.modify_settings("white_observer", self.white_observer_comb.currentIndex())

        new_bakgd_id = self.bakgd_id_comb.currentIndex()
        new_style_id = self.style_id_comb.currentIndex()
        new_font_weight = self.font_weight_comb.currentIndex() + 1
        new_font_size = int(self.font_size_sp.value())
        new_font_family = check_nonempt_str_lst(re.split(r"[\v\a\f\n\r\t\[\]\(\),;:#]", str(self.font_family_ledit.text())))

        if new_bakgd_id != self._args.bakgd_id or new_style_id != self._args.style_id or new_font_weight != self._args.font_weight or new_font_size != self._args.font_size or new_font_family != self._args.font_family:
            if new_bakgd_id == self._args.bakgd_id and new_style_id == self._args.style_id:
                change_pn_colors = False

            else:
                change_pn_colors = True

                self._args.modify_settings("bakgd_id", new_bakgd_id)
                self._args.modify_settings("style_id", new_style_id)

            self._args.modify_settings("font_weight", new_font_weight)
            self._args.modify_settings("font_size", new_font_size)
            self._args.modify_settings("font_family", new_font_family)

            self.ps_theme_changed.emit(change_pn_colors)

        else:
            self._args.modify_settings("positive_color", (self.positive_color_0_dp.value(), self.positive_color_1_dp.value(), self.positive_color_2_dp.value()))
            self._args.modify_settings("negative_color", (self.negative_color_0_dp.value(), self.negative_color_1_dp.value(), self.negative_color_2_dp.value()))
            self._args.modify_settings("wheel_ed_color", (self.wheel_ed_color_0_dp.value(), self.wheel_ed_color_1_dp.value(), self.wheel_ed_color_2_dp.value()))

        self._args.modify_settings("max_history_files", self.max_history_files_sp.value())
        self._args.modify_settings("max_history_steps", self.max_history_steps_sp.value())
        self._args.modify_settings("export_grid_extns", self.export_grid_extns_ledit.text())

        self._args.modify_settings("r_prefix", (self.r_prefix_0_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.r_prefix_1_ledit.text().replace("\\n", "\n").replace("\\t", "\t")))
        self._args.modify_settings("rgb_prefix", (self.rgb_prefix_0_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.rgb_prefix_1_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.rgb_prefix_2_ledit.text().replace("\\n", "\n").replace("\\t", "\t")))
        self._args.modify_settings("hec_prefix", (self.hec_prefix_0_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.hec_prefix_1_ledit.text().replace("\\n", "\n").replace("\\t", "\t")))
        self._args.modify_settings("lst_prefix", (self.lst_prefix_0_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.lst_prefix_1_ledit.text().replace("\\n", "\n").replace("\\t", "\t"), self.lst_prefix_2_ledit.text().replace("\\n", "\n").replace("\\t", "\t")))

        self._args.modify_settings("press_move", self.press_move_cbox.isChecked())
        self._args.modify_settings("show_hsv", self.show_hsv_cbox.isChecked())
        self._args.modify_settings("show_rgb", self.show_rgb_cbox.isChecked())

        self._args.modify_settings("h_range", (self.h_range_0_dp.value(), self.h_range_1_dp.value()))
        self._args.modify_settings("s_range", (self.s_range_0_dp.value(), self.s_range_1_dp.value()))
        self._args.modify_settings("v_range", (self.v_range_0_dp.value(), self.v_range_1_dp.value()))

        self._args.modify_settings("wheel_ratio", self.wheel_ratio_dp.value())
        self._args.modify_settings("volum_ratio", self.volum_ratio_dp.value())
        self._args.modify_settings("cubic_ratio", self.cubic_ratio_dp.value())
        self._args.modify_settings("coset_ratio", self.coset_ratio_dp.value())

        self._args.modify_settings("stab_column", self.stab_column_dp.value())

        self._args.modify_settings("rev_direct", self.rev_direct_cbox.isChecked())

        self._args.modify_settings("s_tag_radius", self.s_tag_radius_dp.value())
        self._args.modify_settings("v_tag_radius", self.v_tag_radius_dp.value())

        self._args.modify_settings("zoom_step", self.zoom_step_dp.value())
        self._args.modify_settings("move_step", self.move_step_dp.value())

        self._args.modify_settings("rand_num", self.rand_num_sp.value())
        self._args.modify_settings("circle_dist", self.circle_dist_sp.value())

        self._args.modify_settings("positive_wid", self.positive_wid_sp.value())
        self._args.modify_settings("negative_wid", self.negative_wid_sp.value())
        self._args.modify_settings("wheel_ed_wid", self.wheel_ed_wid_sp.value())

        self.ps_settings_changed.emit()

    def showup(self):
        """
        Initialize and show.
        """

        self.initialize()
        self.show()

    def update_values(self):
        """
        For button apply.
        """

        self.application()
        self.initialize()

    def reset_values(self):
        """
        For button reset.
        """

        hm_rule = self._args.hm_rule
        lang = self._args.lang

        old_bakgd_id = self._args.bakgd_id
        old_style_id = self._args.style_id
        old_font_weight = self._args.font_weight
        old_font_size = self._args.font_size
        old_font_family = self._args.font_family

        self._args.init_settings()
        self.initialize()

        if self._args.hm_rule != hm_rule:
            self.ps_rule_changed.emit()

        if self._args.lang != lang:
            self.ps_lang_changed.emit()

        self.ps_settings_changed.emit()
        self.ps_theme_changed.emit(True)

    def verify_shortcut_keymaps(self):
        if self._is_initializing:
            return

        self._skey_accept = []

        skey_copies = []

        for i in range(len(self._skey_labels)):
            for j in range(3):
                self._skey_ledits[i * 3 + j].setStyleSheet("color: '#202020'; background-color: '#F9FFDF';")
                skey_copies.append(self._skey_ledits[i * 3 + j].text())

        err_id = []
        used_names = []

        for i in range(len(skey_copies)):
            if not skey_copies[i]:
                self._skey_accept.append("")
                continue

            skey_name = check_key(skey_copies[i])

            if not skey_name:
                self._skey_accept.append("")
                err_id.append(i)

            elif skey_name in self._skey_accept:
                self._skey_accept.append("")

                for copy_id in range(len(skey_copies)):
                    if skey_copies[copy_id] == skey_name and copy_id not in err_id:
                        err_id.append(copy_id)

            else:
                self._skey_accept.append(skey_name)

        for i in err_id:
            self._skey_ledits[i].setStyleSheet("color: '#202020'; background-color: '#FFB6AE';")

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.setWindowTitle(self._dialog_descs[0])
        self._btn_1.setText(self._dialog_descs[1])
        self._btn_2.setText(self._dialog_descs[2])
        self._btn_3.setText(self._dialog_descs[3])
        self._btn_4.setText(self._dialog_descs[4])

        for i in range(len(self._skey_gboxes)):
            self._skey_gboxes[i].setTitle(self._skey_blocks[i])

        for i in range(len(self._skey_labels)):
            self._skey_labels[i].setText(self._skey_seqs[i])

        for idx in range(len(self._args.usr_langs)):
            lang = self._args.usr_langs[idx]
            self.lang_comb.setItemText(idx, self._lang_descs[40].format(self._lang_descs[lang[0]], lang[1].split(".")[0]))

        for idx in range(len(self._args.global_hm_rules)):
            self.hm_rule_comb.setItemText(idx, self._rule_descs[idx])

        for idx in range(len(self._args.global_overflows)):
            self.overflow_comb.setItemText(idx, self._overflow_descs[idx])

        for idx in range(3):
            self.export_ase_type_comb.setItemText(idx, self._ase_descs[idx])

        for idx in range(17):
            self.bakgd_id_comb.setItemText(idx, self._bakgd_descs[idx])

        for idx in range(17):
            self.style_id_comb.setItemText(idx, self._theme_descs[idx])

        for idx in range(20):
            self.white_illuminant_comb.setItemText(idx, self._white_illuminant_descs[idx])

        for idx in range(2):
            self.white_observer_comb.setItemText(idx, self._white_observer_descs[idx])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._dialog_descs = (
            _translate("Settings", "Settings"),
            _translate("Settings", "OK"),
            _translate("Settings", "Cancel"),
            _translate("Settings", "Apply"),
            _translate("Settings", "Reset"),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )

        self._overflow_descs = (
            _translate("Rule", "Cutoff"),
            _translate("Rule", "Return"),
            _translate("Rule", "Repeat"),
        )

        self._bakgd_descs = (
            _translate("Settings", "Colorful"),
            _translate("Settings", "White"),
            _translate("Settings", "Light Grey"),
            _translate("Settings", "Dark Grey"),
            _translate("Settings", "Black"),
            _translate("Settings", "Light Red"),
            _translate("Settings", "Light Yellow"),
            _translate("Settings", "Light Green"),
            _translate("Settings", "Light Cyan"),
            _translate("Settings", "Light Blue"),
            _translate("Settings", "Light Magenta"),
            _translate("Settings", "Dark Red"),
            _translate("Settings", "Dark Yellow"),
            _translate("Settings", "Dark Green"),
            _translate("Settings", "Dark Cyan"),
            _translate("Settings", "Dark Blue"),
            _translate("Settings", "Dark Magenta"),
        )

        self._theme_descs = (
            _translate("Settings", "Default"),
            _translate("Settings", "White"),
            _translate("Settings", "Light Grey"),
            _translate("Settings", "Dark Grey"),
            _translate("Settings", "Black"),
            _translate("Settings", "Light Red"),
            _translate("Settings", "Light Yellow"),
            _translate("Settings", "Light Green"),
            _translate("Settings", "Light Cyan"),
            _translate("Settings", "Light Blue"),
            _translate("Settings", "Light Magenta"),
            _translate("Settings", "Dark Red"),
            _translate("Settings", "Dark Yellow"),
            _translate("Settings", "Dark Green"),
            _translate("Settings", "Dark Cyan"),
            _translate("Settings", "Dark Blue"),
            _translate("Settings", "Dark Magenta"),
        )

        self._skey_blocks = (
            _translate("Settings", "General"),
            _translate("Settings", "Operation"),
            _translate("Settings", "Clipboard"),
            _translate("Settings", "Activation"),
            _translate("Settings", "Transformation"),
            _translate("Settings", "Storage"),
        )

        self._ase_descs = (
            _translate("Settings", "Spot"),
            _translate("Settings", "Global"),
            _translate("Settings", "Process"),
        )

        self._skey_seqs = (
            _translate("Settings", "Homepage"),
            _translate("Settings", "Update"),
            _translate("Settings", "About"),
            _translate("Settings", "Settings"),
            _translate("Settings", "Close"),
            _translate("Settings", "No_Save_Close"),
            _translate("Settings", "Open"),
            _translate("Settings", "Save"),
            _translate("Settings", "Import"),
            _translate("Settings", "Export"),
            _translate("Settings", "Create"),
            _translate("Settings", "Locate"),
            _translate("Settings", "Derive"),
            _translate("Settings", "Attach"),
            _translate("Settings", "Clipboard_Cur_RGB"),
            _translate("Settings", "Clipboard_Cur_HSV"),
            _translate("Settings", "Clipboard_Cur_Hec"),
            _translate("Settings", "Clipboard_All_RGB"),
            _translate("Settings", "Clipboard_All_HSV"),
            _translate("Settings", "Clipboard_All_Hec"),
            _translate("Settings", "Clipboard_Set_RGB"),
            _translate("Settings", "Clipboard_Set_HSV"),
            _translate("Settings", "Clipboard_Set_Hec"),
            _translate("Settings", "Activate_Color_2"),
            _translate("Settings", "Activate_Color_1"),
            _translate("Settings", "Activate_Color_0"),
            _translate("Settings", "Activate_Color_3"),
            _translate("Settings", "Activate_Color_4"),
            _translate("Settings", "Move_Up"),
            _translate("Settings", "Move_Down"),
            _translate("Settings", "Move_Left"),
            _translate("Settings", "Move_Right"),
            _translate("Settings", "Zoom_In"),
            _translate("Settings", "Zoom_Out"),
            _translate("Settings", "Reset_Home"),
            _translate("Settings", "End"),
            _translate("Settings", "PageUp"),
            _translate("Settings", "PageDown"),
            _translate("Settings", "Insert"),
            _translate("Settings", "Delete"),
            _translate("Settings", "Delete_Ver"),
            _translate("Settings", "Show_Info"),
            _translate("Settings", "Switch"),
            _translate("Settings", "Show_Hide"),
            _translate("Settings", "Gen_Clear"),
            _translate("Settings", "Copy"),
            _translate("Settings", "Paste"),
            _translate("Settings", "Withdraw"),
            _translate("Settings", "Win_On_Top"),
            _translate("Settings", "Show_Hide_All"),
            _translate("Settings", "Support Rickrack!"),
            _translate("Settings", "Gen_Assit"),
            _translate("Settings", "Wheel_View"),
            _translate("Settings", "Image_View"),
            _translate("Settings", "Board_View"),
            _translate("Settings", "Depot_View"),
            _translate("Settings", "Redo"),
        )

        self._white_illuminant_descs = (
            _translate("Settings", "A (Incandescent/tungsten)"),
            _translate("Settings", "B (Old direct sunlight at noon)"),
            _translate("Settings", "C (Old daylight)"),
            _translate("Settings", "D50 (ICC profile PCS)"),
            _translate("Settings", "D55 (Mid-morning daylight)"),
            _translate("Settings", "D65 (Daylight, sRGB, Adobe-RGB)"),
            _translate("Settings", "D75 (North sky daylight)"),
            _translate("Settings", "E (Equal energy)"),
            _translate("Settings", "F1 (Daylight Fluorescent)"),
            _translate("Settings", "F2 (Cool fluorescent)"),
            _translate("Settings", "F3 (White Fluorescent)"),
            _translate("Settings", "F4 (Warm White Fluorescent)"),
            _translate("Settings", "F5 (Daylight Fluorescent)"),
            _translate("Settings", "F6 (Lite White Fluorescent)"),
            _translate("Settings", "F7 (Daylight fluorescent, D65 simulator)"),
            _translate("Settings", "F8 (Sylvania F40, D50 simulator)"),
            _translate("Settings", "F9 (Cool White Fluorescent)"),
            _translate("Settings", "F10 (Ultralume 50, Philips TL85)"),
            _translate("Settings", "F11 (Ultralume 40, Philips TL84)"),
            _translate("Settings", "F12 (Ultralume 30, Philips TL83)"),
        )

        self._white_observer_descs = (
            _translate("Settings", "2Ang (CIE 1931)"),
            _translate("Settings", "10Ang (CIE 1964)"),
        )

        self._lang_descs = (
            _translate("Settings", "en"),
            _translate("Settings", "ar"),
            _translate("Settings", "be"),
            _translate("Settings", "bg"),
            _translate("Settings", "ca"),
            _translate("Settings", "cs"),
            _translate("Settings", "da"),
            _translate("Settings", "de"),
            _translate("Settings", "el"),
            _translate("Settings", "es"),
            _translate("Settings", "et"),
            _translate("Settings", "fi"),
            _translate("Settings", "fr"),
            _translate("Settings", "hr"),
            _translate("Settings", "hu"),
            _translate("Settings", "is"),
            _translate("Settings", "it"),
            _translate("Settings", "iw"),
            _translate("Settings", "ja"),
            _translate("Settings", "ko"),
            _translate("Settings", "lt"),
            _translate("Settings", "lv"),
            _translate("Settings", "mk"),
            _translate("Settings", "nl"),
            _translate("Settings", "no"),
            _translate("Settings", "pl"),
            _translate("Settings", "pt"),
            _translate("Settings", "ro"),
            _translate("Settings", "ru"),
            _translate("Settings", "sh"),
            _translate("Settings", "sk"),
            _translate("Settings", "sl"),
            _translate("Settings", "sq"),
            _translate("Settings", "sr"),
            _translate("Settings", "sv"),
            _translate("Settings", "th"),
            _translate("Settings", "tr"),
            _translate("Settings", "uk"),
            _translate("Settings", "zh"),
            _translate("Settings", "default"),
            _translate("Rickrack", "{} ({})"),
        )
