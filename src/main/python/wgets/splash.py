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
from PySide2.QtWidgets import QSplashScreen
from PySide2.QtGui import QPixmap, QImage
from cguis.resource import view_rc


class DPSplash(QSplashScreen):
    """
    Show image when loading.
    """

    def __init__(self, resources, sys_argv):
        """
        Init splash.
        """

        display_lang = "en"

        if sys_argv["lang"]:
            if sys_argv["lang"][:2].lower() in ("zh", "ja", "ko"):
                display_lang = "zh"

        else:
            try:
                default_locale = str(locale.getdefaultlocale()[0])

            except Exception as err:
                default_locale = ""

            if len(default_locale) > 1 and default_locale[:2].lower() in ("zh", "ja", "ko"):
                display_lang = "zh"

            else:
                try:
                    with open(os.sep.join((resources, "settings.json")), "r", encoding="utf-8") as sf:
                        uss = json.load(sf)

                    if isinstance(uss, dict) and "lang" in uss and str(uss["lang"])[:2].lower() in ("zh", "ja", "ko"):
                        display_lang = "zh"

                except Exception as err:
                    pass

        super().__init__()

        design_pix = QPixmap.fromImage(QImage(":/images/images/design_{}.png".format(display_lang)))
        design_pix.setDevicePixelRatio(2)

        self.setPixmap(design_pix)

    def mousePressEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def enterEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
