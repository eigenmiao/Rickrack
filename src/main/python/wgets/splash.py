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

import os
import json
import locale
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from cguis.resource import view_rc


class DPSplash(QSplashScreen):
    """
    Show image when loading.
    """

    def __init__(self, resources, sys_argv, debug_tools):
        """
        Init splash.
        """

        d_error, d_info, d_action = debug_tools
        d_action(200)
        d_info(203, resources)
        d_info(200, sys_argv)
        display_lang = "en"

        if sys_argv["lang"]:
            if sys_argv["lang"][:2].lower() in ("zh", "ja", "ko"):
                display_lang = "zh"

        else:
            default_locale = str(locale.getdefaultlocale()[0]).lower()

            if len(default_locale) > 1 and default_locale[:2].lower() in ("zh", "ja", "ko"):
                display_lang = "zh"

            else:
                try:
                    with open(os.sep.join((resources, "settings.json")), "r", encoding="utf-8") as sf:
                        uss = json.load(sf)

                except Exception as err:
                    uss = None
                    d_error(200, err)

                if isinstance(uss, dict) and "lang" in uss and str(uss["lang"])[:2].lower() in ("zh", "ja", "ko"):
                    display_lang = "zh"

                d_info(201, uss)
        super().__init__()
        d_info(205, locale.getdefaultlocale())
        d_info(204, display_lang)
        design_img = QImage(":/images/images/repository_{}.png".format(display_lang)).scaled(480 * 1.2 * self.devicePixelRatioF(), 240 * 1.2 * self.devicePixelRatioF(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        design_img.setDevicePixelRatio(self.devicePixelRatioF())
        d_info(202, self.devicePixelRatioF())
        self.setPixmap(QPixmap.fromImage(design_img))
        d_action(201)

    def mousePressEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def enterEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
