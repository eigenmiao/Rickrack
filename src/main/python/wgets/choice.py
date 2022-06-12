# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

Copyright (c) 2019-2022 by Eigenmiao. All Rights Reserved.
"""

from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from cguis.resource import view_rc
from ricore.check import check_file_name


class Choice(QDialog):
    def __init__(self, wget, args):
        """
        Init settings.
        """

        super().__init__(wget, Qt.WindowCloseButtonHint)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        self.setObjectName("Choice")
        self.resize(300, 200)

        choice_grid_layout = QGridLayout(self)

        self.choice_label = QLabel(self)
        choice_grid_layout.addWidget(self.choice_label, 0, 0, 1, 1)
        self.choice_label.setWordWrap(True)

        self.choice_btn = QPushButton(self)
        choice_grid_layout.addWidget(self.choice_btn, 1, 0, 1, 1)
        self.choice_btn.clicked.connect(self.apply_choice)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def apply_choice(self):
        """
        Apply current choice of color.
        """

        self._args.sys_choice_stat = []
        self.hide()

    def showup(self):
        """
        Initialize and show.
        """

        self.update_text()
        self.show()

    # ---------- ---------- ---------- Event Funcs ---------- ---------- ---------- #

    def closeEvent(self, event):
        """
        Actions before close dialog.
        """

        self.apply_choice()
        event.accept()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.setWindowTitle(self._choice_descs[0])

        if self._args.sys_choice_stat:
            if len(self._args.sys_choice_stat) > 1:
                pre_text = self._choice_descs[1].join(self._args.sys_choice_stat[:-1])
                end_text = self._args.sys_choice_stat[-1]

                if self._args.lang[:2].lower() in ("zh", "ja", "ko"):
                    if check_file_name(pre_text[-1]):
                        pre_text = pre_text + " "

                    if check_file_name(end_text[0]):
                        end_text = " " + end_text

                    if check_file_name(end_text[-1]):
                        end_text = end_text + " "

                text = pre_text + self._choice_descs[2] + end_text

            else:
                text = self._args.sys_choice_stat[0]

                if self._args.lang[:2].lower() in ("zh", "ja", "ko"):
                    if check_file_name(text[-1]):
                        text = text + " "

            text += self._choice_descs[3]

        else:
            text = ""

        self.choice_label.setText(text)
        self.choice_btn.setText(self._choice_descs[4])

        self.choice_label.setAlignment(Qt.AlignCenter)

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._choice_descs = (
            _translate("Choice", "Choice"),
            _translate("Info", ", "),
            _translate("Info", " and "),
            _translate("Choice", " wanna set of colors."),
            _translate("Choice", "It seeems well"),
        )
