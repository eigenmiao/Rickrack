# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details.

Please visit https://github.com/eigenmiao/DigitalPalette for more 
infomation about DigitalPalette.

Copyright (c) 2019-2021 by Eigenmiao. All Rights Reserved.
"""

import os
import numpy as np
from PIL import Image, ImageFilter
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from ricore.color import Color, CTP
from ricore.image_act import extract_image


class Image3C(QThread):
    ps_proceses = pyqtSignal(int)
    ps_describe = pyqtSignal(int)
    ps_finished = pyqtSignal(int)
    ps_enhanced = pyqtSignal(int)
    ps_extracts = pyqtSignal(list)

    def __init__(self, temp_dir, debug_tools):
        """
        Init image3c with default temp dir.
        """

        super().__init__()
        self._d_error, self._d_info, self._d_action = debug_tools
        self._temp_dir = temp_dir
        self.img_data = None
        self.display = None
        self.rgb_data = None
        self.hsv_data = None
        self.run_args = None
        self.run_category = None
        self.ori_display_data = None
        self.res_display_data = None
        self.rev_display_data = None
        self._rgb_ext_data = None
        self._hsv_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    def run(self):
        """
        Start running in thread.
        """

        self._d_action(500)
        self._d_info(500, self.run_category)
        self._d_info(501, self.run_args)

        if isinstance(self.run_category, int):
            func = getattr(self, "run_{}".format(self.run_category))
            func((0, 100))

        else:
            func = getattr(self, "run_{}".format(self.run_category))
            func((0, 100), self.run_args)

    def run_rgb_extend(self):
        """
        Extend rgb data into extended rgb data for Sobel edge detection.
        """

        if not isinstance(self._rgb_ext_data, np.ndarray):
            self._rgb_ext_data = np.insert(self.rgb_data, 0, self.rgb_data[1, :], axis=0)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, self._rgb_ext_data.shape[0], self._rgb_ext_data[self._rgb_ext_data.shape[0] - 2, :], axis=0)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, 0, self._rgb_ext_data[:, 1], axis=1)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, self._rgb_ext_data.shape[1], self._rgb_ext_data[:, self._rgb_ext_data.shape[1] - 2], axis=1)

    def run_hsv_extend(self):
        """
        Extend rgb data into extended rgb data for Sobel edge detection.
        """

        if not isinstance(self._hsv_ext_data, np.ndarray):
            self._hsv_ext_data = np.insert(self.hsv_data, 0, self.hsv_data[1, :], axis=0)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, self._hsv_ext_data.shape[0], self._hsv_ext_data[self._hsv_ext_data.shape[0] - 2, :], axis=0)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, 0, self._hsv_ext_data[:, 1], axis=1)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, self._hsv_ext_data.shape[1], self._hsv_ext_data[:, self._hsv_ext_data.shape[1] - 2], axis=1)

    def run_init(self, process_scope, script=""):
        """
        Run pre init data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            script (str): (str): BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.
        """

        if isinstance(script, tuple) and script[0] in ("BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE"):
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))
            self.img_data = self.img_data.filter(getattr(ImageFilter, script[0]))

        elif isinstance(script, tuple) and script[0] == "ZOOM":
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))
            ratio = max(5.0 / self.img_data.size[0], 5.0 / self.img_data.size[1], script[1])

            if ratio != 1.0:
                self.img_data = self.img_data.resize((int(round(self.img_data.size[0] * ratio)), int(round(self.img_data.size[1] * ratio))), Image.ANTIALIAS)

        elif isinstance(script, tuple) and script[0] == "CROP":
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))

            if script[1] != (0.0, 0.0, 1.0, 1.0):
                self.img_data = self.img_data.crop((int(round(script[1][0] * self.img_data.size[0])), int(round(script[1][1] * self.img_data.size[1])), int(round(script[1][2] * self.img_data.size[0])), int(round(script[1][3] * self.img_data.size[1]))))

            ratio = max(5.0 / self.img_data.size[0], 5.0 / self.img_data.size[1])

            if ratio > 1.0:
                self.img_data = self.img_data.resize((int(self.img_data.size[0] * ratio), int(self.img_data.size[1] * ratio)), Image.ANTIALIAS)

        else:
            self.ps_describe.emit(1)
            self.ps_proceses.emit(int(process_scope[0]))
            ratio = max(5.0 / self.img_data.size[0], 5.0 / self.img_data.size[1])

            if ratio > 1.0:
                self.img_data = self.img_data.resize((int(self.img_data.size[0] * ratio), int(self.img_data.size[1] * ratio)), Image.ANTIALIAS)

        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.60))
        self.rgb_data = np.array(self.img_data.convert("RGB"), dtype=np.uint8)
        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.80))
        self.save_rgb_full_data(self.rgb_data, 0)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(process_scope[0] + process_scope[1]))

    def run_0(self, process_scope):
        """
        Run normal rgb data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_init((process_scope[0], process_scope[1] * 0.40))
            pro_scope = (process_scope[0] + process_scope[1] * 0.40, process_scope[1] * 0.60)

        else:
            pro_scope = tuple(process_scope)

        self.ps_describe.emit(2)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.60))
        self.save_rgb_chnl_data(self.rgb_data, 0)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_4(self, process_scope):
        """
        Run normal hsv data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        self.ps_describe.emit(3)
        self.ps_proceses.emit(int(pro_scope[0]))
        self.hsv_data = Color.rgb2hsv_array(self.rgb_data)
        self.ps_describe.emit(4)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.60))
        self.save_hsv_chnl_data(self.hsv_data, 4)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_1(self, process_scope):
        """
        Run vertical rgb space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        self.run_rgb_extend()
        self.ps_describe.emit(5)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._rgb_vtl_data = np.zeros((self.rgb_data.shape[0], self.rgb_data.shape[1], 3), dtype=np.uint8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))

        for i in range(self.rgb_data.shape[0]):
            for j in range(self.rgb_data.shape[1]):
                rgb_result = self._rgb_ext_data[i:i + 3, j:j + 3, :] * [[[-1, -1, -1], [0, 0, 0], [1, 1, 1]], [[-2, -2, -2], [0, 0, 0], [2, 2, 2]], [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]]
                rgb_result = rgb_result.sum(axis=(0, 1)) / 4
                self._rgb_vtl_data[i][j] = np.abs(rgb_result).astype(np.uint8)

        self.ps_describe.emit(6)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._rgb_vtl_data, 1)
        self.save_rgb_chnl_data(self._rgb_vtl_data, 1)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_2(self, process_scope):
        """
        Run horizontal rgb space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        self.run_rgb_extend()
        self.ps_describe.emit(7)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._rgb_hrz_data = np.zeros((self.rgb_data.shape[0], self.rgb_data.shape[1], 3), dtype=np.uint8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))

        for i in range(self.rgb_data.shape[0]):
            for j in range(self.rgb_data.shape[1]):
                rgb_result = self._rgb_ext_data[i:i + 3, j:j + 3, :] * [[[-1, -1, -1], [-2, -2, -2], [-1, -1, -1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [2, 2, 2], [1, 1, 1]]]
                rgb_result = rgb_result.sum(axis=(0, 1)) / 4
                self._rgb_hrz_data[i][j] = np.abs(rgb_result).astype(np.uint8)

        self.ps_describe.emit(8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._rgb_hrz_data, 2)
        self.save_rgb_chnl_data(self._rgb_hrz_data, 2)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_3(self, process_scope):
        """
        Run final rgb space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self._rgb_vtl_data, np.ndarray):
            self.run_1((process_scope[0], process_scope[1] * 0.60))
            pro_scope = (process_scope[0] + process_scope[1] * 0.60, process_scope[1] * 0.40)

        else:
            pro_scope = tuple(process_scope)

        if not isinstance(self._rgb_hrz_data, np.ndarray):
            self.run_2((pro_scope[0], pro_scope[1] * 0.50))
            pro_scope = (pro_scope[0] + pro_scope[1] * 0.50, pro_scope[1] * 0.50)

        else:
            pro_scope = tuple(pro_scope)

        self.ps_describe.emit(9)
        self.ps_proceses.emit(int(pro_scope[0]))
        fnl_results = (np.sqrt(self._rgb_vtl_data.astype(np.uint32) ** 2 + self._rgb_hrz_data.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)
        self.ps_describe.emit(10)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(fnl_results, 3)
        self.save_rgb_chnl_data(fnl_results, 3)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._rgb_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None

    def run_5(self, process_scope):
        """
        Run vertical hsv space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        self.run_hsv_extend()
        self.ps_describe.emit(11)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_vtl_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.uint8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))

        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                h_result_0 = abs(self._hsv_ext_data[i + 0][j + 2][0] - self._hsv_ext_data[i + 0][j][0])
                h_result_1 = abs(self._hsv_ext_data[i + 1][j + 2][0] - self._hsv_ext_data[i + 1][j][0])
                h_result_2 = abs(self._hsv_ext_data[i + 2][j + 2][0] - self._hsv_ext_data[i + 2][j][0])
                h_result_0 = 360.0 - h_result_0 if h_result_0 > 180.0 else h_result_0
                h_result_1 = 360.0 - h_result_1 if h_result_1 > 180.0 else h_result_1
                h_result_2 = 360.0 - h_result_2 if h_result_2 > 180.0 else h_result_2
                h_result = h_result_0 + h_result_1 * 2 + h_result_2
                sv_result = self._hsv_ext_data[i:i + 3, j:j + 3, 1:3] * [[[-1, -1], [0, 0], [1, 1]], [[-2, -2], [0, 0], [2, 2]], [[-1, -1], [0, 0], [1, 1]]]
                sv_result = sv_result.sum(axis=(0, 1)).astype(np.float32)
                self._hsv_vtl_data[i][j] = np.array((h_result * 0.3542, abs(sv_result[0]) * 63.75, abs(sv_result[1]) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(12)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._hsv_vtl_data, 5)
        self.save_rgb_chnl_data(self._hsv_vtl_data, 5)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_6(self, process_scope):
        """
        Run horizontal hsv space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        self.run_hsv_extend()
        self.ps_describe.emit(13)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_hrz_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.uint8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))

        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                h_result_0 = abs(self._hsv_ext_data[i + 2][j + 0][0] - self._hsv_ext_data[i][j + 0][0])
                h_result_1 = abs(self._hsv_ext_data[i + 2][j + 1][0] - self._hsv_ext_data[i][j + 1][0])
                h_result_2 = abs(self._hsv_ext_data[i + 2][j + 2][0] - self._hsv_ext_data[i][j + 2][0])
                h_result_0 = 360.0 - h_result_0 if h_result_0 > 180.0 else h_result_0
                h_result_1 = 360.0 - h_result_1 if h_result_1 > 180.0 else h_result_1
                h_result_2 = 360.0 - h_result_2 if h_result_2 > 180.0 else h_result_2
                h_result = h_result_0 + h_result_1 * 2 + h_result_2
                sv_result = self._hsv_ext_data[i:i + 3, j:j + 3, 1:3] * [[[-1, -1], [-2, -2], [-1, -1]], [[0, 0], [0, 0], [0, 0]], [[1, 1], [2, 2], [1, 1]]]
                sv_result = sv_result.sum(axis=(0, 1)).astype(np.float32)
                self._hsv_hrz_data[i][j] = np.array((h_result * 0.3542, abs(sv_result[0]) * 63.75, abs(sv_result[1]) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(14)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._hsv_hrz_data, 6)
        self.save_rgb_chnl_data(self._hsv_hrz_data, 6)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_7(self, process_scope):
        """
        Run final hsv space edge data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self._hsv_vtl_data, np.ndarray):
            self.run_5((process_scope[0], process_scope[1] * 0.60))
            pro_scope = (process_scope[0] + process_scope[1] * 0.60, process_scope[1] * 0.40)

        else:
            pro_scope = tuple(process_scope)

        if not isinstance(self._hsv_hrz_data, np.ndarray):
            self.run_6((pro_scope[0], pro_scope[1] * 0.50))
            pro_scope = (pro_scope[0] + pro_scope[1] * 0.50, pro_scope[1] * 0.50)

        else:
            pro_scope = tuple(pro_scope)

        self.ps_describe.emit(15)
        self.ps_proceses.emit(int(pro_scope[0]))
        fnl_results = (np.sqrt(self._hsv_vtl_data.astype(np.uint32) ** 2 + self._hsv_hrz_data.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)
        self.ps_describe.emit(16)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(fnl_results, 7)
        self.save_rgb_chnl_data(fnl_results, 7)
        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._hsv_ext_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    def save_load_data(self, load_image):
        """
        Save load image from clipboard, etc.

        Args:
            load_image (QImage): display image data.
        """

        i = 0
        image_path = self._temp_dir.path() + os.sep + "load_{}.png"

        while os.path.isfile(image_path.format(i)):
            i += 1

        image_path = image_path.format(i)
        try:
            load_image.save(image_path)

        except Exception as err:
            self._d_error(500, err)
            return None

        if os.path.isfile(image_path):
            return image_path

        else:
            return None

    def save_rgb_full_data(self, rgb_data, prefix):
        """
        Save rgb full channel image (0_0.png for category 0 and 4 and channel 0).

        Args:
            rgb_data (3D array): rgb image array.
            prefix (int): graph category as image name prefix.
        """

        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._temp_dir.path() + os.sep + "{}_0.png".format(prefix))

        if prefix == 0:
            self.ps_finished.emit(0)
            self.ps_finished.emit(40)

        else:
            self.ps_finished.emit(prefix * 10)

    def save_rgb_chnl_data(self, rgb_data, prefix):
        """
        Save r, g, b, not r, not g and not b channel images separately.

        Args:
            rgb_data (3D array): rgb image array.
            prefix (int): graph category as image name prefix.
        """

        z_chl = np.zeros((rgb_data.shape[0], rgb_data.shape[1]), dtype=np.uint8)
        r_chl = np.stack((rgb_data[:, :, 0], z_chl, z_chl), axis=2)
        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 1)
        g_chl = np.stack((z_chl, rgb_data[:, :, 1], z_chl), axis=2)
        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 2)
        b_chl = np.stack((z_chl, z_chl, rgb_data[:, :, 1]), axis=2)
        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 3)
        n_r_chl = np.stack((z_chl, rgb_data[:, :, 1], rgb_data[:, :, 2]), axis=2)
        n_r_chl = QImage(n_r_chl, n_r_chl.shape[1], n_r_chl.shape[0], n_r_chl.shape[1] * 3, QImage.Format_RGB888)
        n_r_chl.save(self._temp_dir.path() + os.sep + "{}_4.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 4)
        n_g_chl = np.stack((rgb_data[:, :, 0], z_chl, rgb_data[:, :, 2]), axis=2)
        n_g_chl = QImage(n_g_chl, n_g_chl.shape[1], n_g_chl.shape[0], n_g_chl.shape[1] * 3, QImage.Format_RGB888)
        n_g_chl.save(self._temp_dir.path() + os.sep + "{}_5.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 5)
        n_b_chl = np.stack((rgb_data[:, :, 0], rgb_data[:, :, 1], z_chl), axis=2)
        n_b_chl = QImage(n_b_chl, n_b_chl.shape[1], n_b_chl.shape[0], n_b_chl.shape[1] * 3, QImage.Format_RGB888)
        n_b_chl.save(self._temp_dir.path() + os.sep + "{}_6.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 6)

    def save_hsv_chnl_data(self, hsv_data, prefix):
        """
        Save h, s, v, not h, not s and not v channel images separately.

        Args:
            hsv_data (3D array): hsv image array.
            prefix (int): graph category as image name prefix.
        """

        ones = np.ones(hsv_data.shape[:2])
        zeros = np.zeros(hsv_data.shape[:2])
        h_chl = Color.hsv2rgb_array(np.stack((hsv_data[:, :, 0], ones, ones), axis=2))
        h_chl = QImage(h_chl, h_chl.shape[1], h_chl.shape[0], h_chl.shape[1] * 3, QImage.Format_RGB888)
        h_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 1)
        s_chl = Color.hsv2rgb_array(np.stack((zeros, hsv_data[:, :, 1], ones), axis=2))
        s_chl = QImage(s_chl, s_chl.shape[1], s_chl.shape[0], s_chl.shape[1] * 3, QImage.Format_RGB888)
        s_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 2)
        v_chl = Color.hsv2rgb_array(np.stack((zeros, ones, hsv_data[:, :, 2]), axis=2))
        v_chl = QImage(v_chl, v_chl.shape[1], v_chl.shape[0], v_chl.shape[1] * 3, QImage.Format_RGB888)
        v_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 3)
        n_h_chl = Color.hsv2rgb_array(np.stack((zeros, hsv_data[:, :, 1], hsv_data[:, :, 2]), axis=2))
        n_h_chl = QImage(n_h_chl, n_h_chl.shape[1], n_h_chl.shape[0], n_h_chl.shape[1] * 3, QImage.Format_RGB888)
        n_h_chl.save(self._temp_dir.path() + os.sep + "{}_4.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 4)
        n_s_chl = Color.hsv2rgb_array(np.stack((hsv_data[:, :, 0], ones, hsv_data[:, :, 2]), axis=2))
        n_s_chl = QImage(n_s_chl, n_s_chl.shape[1], n_s_chl.shape[0], n_s_chl.shape[1] * 3, QImage.Format_RGB888)
        n_s_chl.save(self._temp_dir.path() + os.sep + "{}_5.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 5)
        n_v_chl = Color.hsv2rgb_array(np.stack((hsv_data[:, :, 0], hsv_data[:, :, 1], ones), axis=2))
        n_v_chl = QImage(n_v_chl, n_v_chl.shape[1], n_v_chl.shape[0], n_v_chl.shape[1] * 3, QImage.Format_RGB888)
        n_v_chl.save(self._temp_dir.path() + os.sep + "{}_6.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 6)

    def load_image(self, category, channel):
        """
        Load image with category and channel.

        Args:
            category (int): graph category index.
            channel (int): graph channel index.
        """

        if category in (0, 4) and channel == 0:
            img_path = os.sep.join((self._temp_dir.path(), "0_0.png"))

        else:
            img_path = os.sep.join((self._temp_dir.path(), "{}_{}.png".format(category, channel)))

        if os.path.isfile(img_path):
            try:
                img_data = Image.open(img_path).convert("RGB")

            except Exception as err:
                self._d_error(501, err)
                img_data = None

            if img_data:
                self.ori_display_data = np.array(img_data, dtype=np.uint8)
                self.display = QImage(self.ori_display_data, self.ori_display_data.shape[1], self.ori_display_data.shape[0], self.ori_display_data.shape[1] * 3, QImage.Format_RGB888)
                self.res_display_data = self.ori_display_data
                self.rev_display_data = None

            else:
                self.display = None
                self.res_display_data = None
                self.rev_display_data = None

        else:
            self.display = None

    def run_enhance_rgb(self, process_scope, values):
        """
        Enhance rgb display by factor. Modify r, g or (and) b values to enhance the contrast of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, separation, factor, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, separ, fact, res, sigma, onedir, useryb = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        if isinstance(separ, (int, float)):
            separ = [separ,] * len(reg)

        else:
            separ = list(separ)

        if isinstance(fact, (int, float)):
            fact = [fact,] * len(reg)

        else:
            fact = list(fact)

        sigma = float(sigma)
        sigma = 0.0 if sigma < 0.0 else sigma
        sigma = 1.0 if sigma > 1.0 else sigma

        for k, k_separ, k_fact in zip(reg, separ, fact):
            if abs(k_fact) < 1E-3:
                continue

            data = np.array(display_data[:, :, k], dtype=np.float32)

            if sigma == 0.0:
                expd = np.zeros(data.shape)
                expd[np.where((data < k_separ + 1) & (data > k_separ - 1))] = k_fact

            elif sigma == 1.0:
                expd = np.ones(data.shape) * k_fact

            else:
                expd = 0.001 * (10 ** (4.5 * sigma)) * -1
                expd = np.exp(((data - k_separ) / 255.0) ** 2 / expd) * k_fact

            if onedir:
                data = data + expd * 255.0

            else:
                expd = np.abs(expd)
                selection = np.where(data >= k_separ) if k_separ < 125 else np.where(data > k_separ)
                data = data * (1.0 - expd)
                data[selection] = data[selection] + expd[selection] * 255.0

            data[np.where(data < 0)] = 0
            data[np.where(data > 255)] = 255
            display_data[:, :, k] = np.array(data, dtype=np.uint8)

        self.res_display_data = display_data
        self.rev_display_data = None
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_enhance_hsv(self, process_scope, values):
        """
        Enhance hsv display by factor. Modify h, s or (and) v values to enhance the contrast of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, separation, factor, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, separ, fact, res, sigma, onedir, useryb = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        if isinstance(separ, (int, float)):
            separ = [separ,] * len(reg)

        else:
            separ = list(separ)

        if isinstance(fact, (int, float)):
            fact = [fact,] * len(reg)

        else:
            fact = list(fact)

        sigma = float(sigma)
        sigma = 0.0 if sigma < 0.0 else sigma
        sigma = 1.0 if sigma > 1.0 else sigma

        for k, k_separ, k_fact in zip(reg, separ, fact):
            if abs(k_fact) < 1E-3:
                continue

            data = np.array(display_data[:, :, k], dtype=np.float32)

            if k == 0:
                if useryb:
                    data = Color.spc_rgb2ryb_h_array(data)
                    k_separ = Color.spc_rgb2ryb_h(k_separ)

                data = Color((k_separ, 1.0, 1.0), tp=CTP.hsv).ref_h_array(data)

                if sigma == 0.0:
                    expd = np.zeros(data.shape)
                    expd[np.where((data > -1E-3) & (data < 1E-3))] = k_fact

                elif sigma == 1.0:
                    expd = np.ones(data.shape) * k_fact

                else:
                    expd = 0.001 * (10 ** (4.5 * sigma)) * -1
                    expd = np.exp((data / 180.0) ** 2 / expd) * k_fact

                if onedir:
                    data = data + expd * 180.0 + k_separ

                else:
                    data = data * (1.0 - expd)
                    selection = np.where(data < 0.0)
                    expd[selection] = expd[selection] * -1
                    data = data + expd * 180.0 + k_separ

                if useryb:
                    data = Color.spc_ryb2rgb_h_array(data)

            else:
                if sigma == 0.0:
                    expd = np.zeros(data.shape)
                    expd[np.where((data - k_separ > -1E-3) & (data - k_separ < 1E-3))] = k_fact

                elif sigma == 1.0:
                    expd = np.ones(data.shape) * k_fact

                else:
                    expd = 0.001 * (10 ** (4.5 * sigma)) * -1
                    expd = np.exp((data - k_separ) ** 2 / expd) * k_fact

                if onedir:
                    data = data + expd

                else:
                    expd = np.abs(expd)
                    selection = np.where(data >= k_separ) if k_separ < 0.5 else np.where(data > k_separ)
                    data = data * (1.0 - expd)
                    data[selection] = data[selection] + expd[selection]

                data[np.where(data < 0)] = 0
                data[np.where(data > 1)] = 1

            display_data[:, :, k] = data
        self.rev_display_data = display_data
        display_data = Color.hsv2rgb_array(display_data)
        self.res_display_data = display_data
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_inverse_rgb(self, process_scope, values):
        """
        Inverse rgb display. Modify r, g or (and) b values to inverse the contrast of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        for k in reg:
            display_data[:, :, k] = 255 - display_data[:, :, k]

        self.res_display_data = display_data
        self.rev_display_data = None
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_inverse_hsv(self, process_scope, values):
        """
        Inverse hsv display. Modify h, s or (and) v values to inverse the contrast of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        for k in reg:
            if k == 0:
                display_data[:, :, 0] = display_data[:, :, 0] + 180.0

            else:
                display_data[:, :, k] = 1.0 - display_data[:, :, k]

        self.rev_display_data = display_data
        display_data = Color.hsv2rgb_array(display_data)
        self.res_display_data = display_data
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_cover_rgb(self, process_scope, values):
        """
        Cover rgb display. Modify r, g or (and) b values to cover the channel of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, reserve, path).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res, path = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        if os.path.isfile(path):
            try:
                data = Image.open(path).convert("RGB")
                data = np.array(data, dtype=np.uint8)

            except Exception as err:
                self._d_error(502, err)
                data = None
                self.ps_enhanced.emit(3)

            if isinstance(data, np.ndarray):
                if data.shape == display_data.shape:
                    for k in reg:
                        display_data[:, :, k] = data[:, :, k]

                else:
                    self.ps_enhanced.emit(2)

        else:
            self.ps_enhanced.emit(3)

        self.res_display_data = display_data
        self.rev_display_data = None
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_cover_hsv(self, process_scope, values):
        """
        Cover hsv display. Modify h, s or (and) v values to cover the channel of image.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (region, reserve, path).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res, path = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        if os.path.isfile(path):
            try:
                data = Image.open(path).convert("RGB")
                data = np.array(data, dtype=np.uint8)

            except Exception as err:
                self._d_error(503, err)
                data = None
                self.ps_enhanced.emit(3)

            if isinstance(data, np.ndarray):
                if data.shape == display_data.shape:
                    data = Color.rgb2hsv_array(data)

                    for k in reg:
                        display_data[:, :, k] = data[:, :, k]

                else:
                    self.ps_enhanced.emit(2)

        else:
            self.ps_enhanced.emit(3)

        self.rev_display_data = display_data
        display_data = Color.hsv2rgb_array(display_data)
        self.res_display_data = display_data
        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_extract(self, process_scope, values):
        """
        Extract a set of colors in different extract types.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            values (tuple or list): (random number, color type).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        rand_num, color_type, useryb = values

        if isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = self.ori_display_data

        extracts = extract_image(display_data, rand_num, color_type, useryb=useryb)
        self.ps_extracts.emit(extracts)
