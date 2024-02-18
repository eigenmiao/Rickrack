# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

Copyright (c) 2019-2023 by Eigenmiao. All Rights Reserved.
"""

import os
import time
from ricore.export import get_export_color_list
from socketserver import BaseRequestHandler


class Request(BaseRequestHandler):
    """
    Request object. Provide result by socket server.
    """

    def handle(self):
        """
        Get method.
        """

        if self.client_address[0] not in ("127.0.0.1", "localhost"):
            return

        req = self.request.recv(4)
        req = req.decode("utf-8")
        self.args.d_info(800, req)

        if req == "cidx":
            text = self.request.recv(1024)
            text = text.decode("utf-8")
            self.args.d_info(801, text)
            text = text.split("; ")

            if len(text) > 0 and text[0] and text[0] in [str(i) for i in range(5)]:
                color_idx = int(text[0])

            else:
                color_idx = None

            if len(text) > 1 and text[1]:
                try:
                    color = tuple([float(i) for i in text[1].split(" ")])

                except Exception as err:
                    self.args.d_error(801, err)
                    color = ()

            if len(color) == 3:
                self.ps_cidx.emit((color_idx, color))

        elif req == "star":
            text = self.request.recv(1024)
            text = text.decode("utf-8")
            self.args.d_info(801, text)
            text = text.lstrip().rstrip()

            if text:
                self.args.sys_choice_stat.append(text)
                self.ps_star.emit(True)

        elif req == "stat":
            text = str(int(bool(self.args.sys_choice_stat)))
            self.request.sendall(text.encode("utf-8"))
            self.args.d_info(802, text)

        elif req == "iset":
            path = self.request.recv(1024)
            self.args.d_info(801, path)
            path = path.decode("utf-8")
            path = path.lstrip().rstrip()

            if os.path.isfile(path) and path[-4:] == ".dps":
                self.ps_iset.emit(path)

        elif req == "oset":
            path = self.request.recv(1024)
            self.args.d_info(801, path)
            path = path.decode("utf-8")
            path = path.lstrip().rstrip()

            if os.path.isdir(os.path.dirname(path)) and path[-4:] == ".dps":
                self.ps_oset.emit(path)

        elif req == "idpt":
            path = self.request.recv(1024)
            self.args.d_info(801, path)
            path = path.decode("utf-8")
            path = path.lstrip().rstrip()

            if os.path.isfile(path) and path[-4:] == ".dpc":
                self.ps_idpt.emit(path)

        elif req == "odpt":
            path = self.request.recv(1024)
            self.args.d_info(801, path)
            path = path.decode("utf-8")
            path = path.lstrip().rstrip()

            if os.path.isdir(os.path.dirname(path)) and path[-4:] == ".dpc":
                self.ps_odpt.emit(path)

        elif req == "data":
            rule = self.args.hm_rule[0].upper() + self.args.hm_rule[1:]
            main_color_list, main_cname_list = get_export_color_list([(self.args.sys_color_set, self.args.hm_rule, "RR", "", (time.time(), time.time()), self.args.sys_grid_locations, self.args.sys_grid_assitlocs, self.args.sys_grid_list, self.args.sys_grid_values),], export_grid=False, useryb=self.args.dep_wtp)
            grid_color_list, grid_cname_list = get_export_color_list([(self.args.sys_color_set, self.args.hm_rule, "RR", "", (time.time(), time.time()), self.args.sys_grid_locations, self.args.sys_grid_assitlocs, self.args.sys_grid_list, self.args.sys_grid_values),], export_grid=True, useryb=self.args.dep_wtp)
            text = ""
            text += "{}; ".format(rule)
            text += "{}; ".format(self.args.sys_activated_idx)
            text += "{}; ".format(" ".join([i.hec for i in main_color_list]))
            text += "{}; ".format(self.args.sys_grid_values["col"])
            text += "{}; ".format(" ".join([i.hec for i in grid_color_list]))

            if self.args.sys_grid_list[0]:
                text += " ".join(['"{}"'.format(i) for i in grid_cname_list])

            text = text
            text = "{:10d}".format(len(text)) + text
            self.request.sendall(text.encode("utf-8"))
            self.args.d_info(802, text)

        elif req == "exit":
            text = self.request.recv(1)
            text = text.decode("utf-8")
            self.ps_exit.emit(text in ("T", "1"))
