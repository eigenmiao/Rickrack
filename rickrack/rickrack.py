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
v2.9.9-x3d3s3-pre
"""

__AUTHOR__ = """
Eigenmiao (eigenmiao@outlook.com)
"""

__DATE__ = """
February 18, 2024
"""

__HELP__ = """
INTRODUCTION:
  Rickrack-Startup provides the ability to operate Rickrack from the 
  command line or through Python code, allowing you to start it, close it, 
  and obtain color results from Rickrack.

  See https://eigenmiao.com/rickrack/ for more information.

VERSION:
  Rickrack-Startup {version} ({date})

AUTHOR:
  {author}

USAGE:
  rickrack [OPTION]... [FILE]

OPTION:
  -h, --help        : display this help information.
  -v, --version     : output the version information.
  -d, --project=DIR : set the project or software directory for Rickrack. 
     (--dir=DIR)      (Both "--project" and "--dir" are avaiable.)

EXAMPLE:
  $> rickrack
  $> rickrack -h
  $> rickrack -l zh
  $> rickrack -d /PATH/TO/RICKRACK/PROJECT
  $> rickrack -i /path/to/myimage.png
  $> rickrack -i /path/to/mycolors.dps
  $> rickrack -r all
  $> 

PYTHON:
  >> # Use Rickrack module in code.
  >> # This code fragment could be reused.
  >> 
  >> from rickrack import Rickrack
  >> 
  >> # Init Rickrack.
  >> rr = Rickrack()
  >> 
  >> # Display the help information.
  >> dp_proj = "/PATH/TO/RICKRACK/PROJECT"
  >> dp_argv = dict()
  >> dp_argv["help"] = True
  >> 
  >> # Run.
  >> rr.run(dp_argv=dp_argv, dp_proj=dp_proj)
  >> 
  >> # Open a local color set file;
  >> # in temporary mode;
  >> # without any dock window (only work area).
  >> dp_argv = dict()
  >> dp_argv["input"] = "/path/to/mycolors.dps"
  >> dp_argv["temporary"] = True
  >> dp_argv["window"] = "0"
  >> 
  >> # Run.
  >> rr.run(dp_argv=dp_argv, dp_proj=dp_proj)
  >> 
  >> # Display the color set result.
  >> print(rr.result)
  >> 
  >> # Output result into a log file.
  >> # See OUTPUT section in Rickrack help information.
  >> log_file = "/path/to/myresult.log"
  >> rr.dump_log(log_file)
  >> 
  >> # Run in sub-thread mode (start a server).
  >> rr.port = 23333
  >> rr.run(dp_argv=dp_argv, dp_proj=dp_proj)
  >> 
  >> # Get result.
  >> rr.update()
  >> 
  >> # Display the color set result.
  >> color_set = rr.result["colors"]
  >> selected_index = rr.result["index"]
  >> selected_color = color_set[selected_index]
  >> 
  >> print("Hex Code : " + str(selected_color.hec))
  >> print("RGB Color: " + str(selected_color.rgb))
  >> print("HSV Color: " + str(selected_color.hsv))
  >> 

NOTICE:
* In python module, option items in dictionary "dp_argv" are full names 
  without prefix "--", such as "input".

* In python module, it will not output the log file if item "help" or 
  "version" is in dictionary "dp_argv", or running in sub-thread mode with 
  port > 0.

* In python module, it will not output the log file if software is running 
  in sub-thread mode with port > 0.

* Use command `rickrack` or python code "rr.run()" without any option, and 
  this software will automatically load previous settings and color results 
  from history files (see the Rickrack help information).

* For other options (such as "-i" and "--input"), see the OPTION section in 
  the Rickrack help information.

COPYRIGHT:
  {copyright}
""".format(**{"version": __VERSION__[1:-1], "author": __AUTHOR__[1:-1], "copyright": __COPYRIGHT__[1:-1], "date": __DATE__[1:-1]})

__ERROR__ = """
ATTENTION PLEASE! -------------------------------------------------------------+
| Can not find the Rickrack project.                                           |
| Please use option '-d' or '--project' to specify the project directory.      |
| You can download this project from https://eigenmiao.com/rickrack/.          |
+------------------------------------------------------------------------------+
"""

import os
import sys
import json
import time
import types
import socket
import hashlib
from rickrack.color import Color, CTP, OTP
from rickrack.result import Grid, Result
from threading import Thread
from getopt import getopt


def para_dir(path):
    """
    Find project directory at path.

    Args:
        path (str): path for project directory.

    Returns:
        Project folder (str) and name (str).
    """

    spath = str(path)

    if os.path.isfile(spath):
        path_lst = os.path.abspath(os.path.dirname(spath)).split(os.sep)

    elif os.path.isdir(spath):
        path_lst = os.path.abspath(spath).split(os.sep)

    else:
        return None, None

    # go back to root dir of Rickrack.
    if path_lst[-1] == "":
        path_lst = path_lst[:-1]

    """
    if path_lst[-1] == "python":
        path_lst = path_lst[:-1]

    if path_lst[-1] == "main":
        path_lst = path_lst[:-1]

    if path_lst[-1] == "src":
        path_lst = path_lst[:-1]
    """

    allow_lst = ([".", "src", "main", "python", "main.py",], [".", "Rickrack",], [".", "Rickrack.exe",])

    # perfect matching firstly.
    for file_lst in allow_lst:
        if os.path.isfile(os.sep.join(path_lst + file_lst)):
            return os.sep.join(path_lst), os.sep.join(file_lst)

    return None, None

def startup():
    """
    Running Rickrack-Startup.
    """

    dp_proj = ""
    dp_argv = {}

    argv_opts, argv_left = getopt(sys.argv[1:], "hvtr:i:o:w:e:l:p:d:", ["help", "version", "temporary", "reset=", "input=", "output=", "export=", "window=", "sequence=", "lang=", "locale=", "port=", "project=", "dir="])

    for opt_name,opt_value in argv_opts:
        if opt_name in ("-h", "--help"):
            dp_argv["help"] = True

        elif opt_name in ("-v", "--version"):
            dp_argv["version"] = True

        elif opt_name in ("-t", "--temporary"):
            dp_argv["temporary"] = True

        elif opt_name in ("-r", "--reset"):
            dp_argv["reset"] = opt_value

        elif opt_name in ("-i", "--input"):
            dp_argv["input"] = opt_value

        elif opt_name in ("-o", "--output", "--export"):
            dp_argv["output"] = opt_value

        elif opt_name in ("-w", "--window"):
            dp_argv["window"] = opt_value

        elif opt_name in ("-e", "--sequence"):
            dp_argv["sequence"] = opt_value

        elif opt_name in ("-l", "--lang", "--locale"):
            dp_argv["lang"] = opt_value

        elif opt_name in ("-p", "--port"):
            dp_argv["port"] = opt_value

        elif opt_name in ("-d", "--project", "--dir"):
            dp_proj = opt_value

    if argv_left and argv_left[-1]:
        dp_argv["input"] = argv_left[-1]

    rr = Rickrack()
    rr.run(dp_argv=dp_argv, dp_proj=dp_proj)


class Rickrack(object):
    """
    Rickrack object. Running Rickrack and getting result from it.
    """

    def __init__(self, host="localhost", port=0, timeout=0.1, default_color="FFFFFF"):
        """
        Init Rickrack settings.

        Args:
            host (str): localhost. default: "localhost".
            port (int): server port. 0 refers to run software directly, while other numbers refer to run software in a sub-thread with server enabled. default: 0.
            timeout (float): connection timeout. default: 0.1.
            default_color (str): default color to be used if connection failed. default: "FFFFFF".
        """

        self._hash = ""
        self._text = ""
        self._default_color = str(default_color)

        rt_rule = "Custom"
        rt_cidx = 0
        rt_cset = Grid([default_color, default_color, default_color, default_color, default_color], [], 5)
        rt_refs = Grid([], [], 0)
        rt_cgrd = Grid([], [], (0, 0))

        result = {"rule": str(rt_rule), "index": int(rt_cidx), "colors": rt_cset, "refs": rt_refs, "grid": rt_cgrd}
        self._result = Result(result)

        self._host = str(host)
        self._port = int(port)
        self._timeout = float(timeout)
        self._will_disconnect = False

        self.is_started_by_script = False

        self._items_for_render = []

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __getitem__(self, idx):
        """
        Get item in result.

        Args:
            idx (int or str): index in result.
        """

        return self._result[idx]

    def __str__(self):
        """
        Str format.
        """

        return "Rickrack({}:{}, {})".format(self._host, self._port, self._hash)

    def __repr__(self):
        """
        Repr format.
        """

        return str(self)

    # ---------- ---------- ---------- Properties and Setters ---------- ---------- ---------- #

    @property
    def hash(self):
        return str(self._hash)

    @property
    def host(self):
        return str(self._host)

    @host.setter
    def host(self, item):
        self._host = str(item)

    @property
    def port(self):
        return int(self._port)

    @port.setter
    def port(self, item):
        self._port = int(item)

    @property
    def timeout(self):
        return float(self._timeout)

    @timeout.setter
    def timeout(self, item):
        self._timeout = float(item)

    @property
    def result(self):
        return self._result

    @property
    def rule(self):
        return self._result.rule

    @property
    def index(self):
        return self._result.index

    @property
    def colors(self):
        return self._result.colors

    @property
    def colors_in_order(self):
        return self._result.colors_in_order

    @property
    def selected_color(self):
        return self._result.selected_color

    @property
    def full_colors(self):
        return self._result.full_colors

    @property
    def color_grid(self):
        return self._result.color_grid

    @property
    def cset(self):
        return self._result.cset

    @property
    def cset_in_order(self):
        return self._result.cset_in_order

    @property
    def refs(self):
        return self._result.refs

    @property
    def grid(self):
        return self._result.grid

    @property
    def grid_h_line(self):
        return self._result.grid_h_line

    @property
    def grid_v_line(self):
        return self._result.grid_v_line

    @property
    def is_connected(self):
        """
        Check if connected to server.
        """

        if not self._port:
            return False

        try:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            client.close()

        except Exception as err:
            print("Connect to server with port {} faild:\n{}".format(self._port, err))
            return False

        return True

    @property
    def is_choice_available(self):
        """
        Check if color choice confirmed.
        """

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            client.sendall("stat".encode("utf-8"))

            ans = client.recv(1)
            ans = ans.decode("utf-8")

            client.close()

            return ans == "1"

        return False

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def disconnect_after_load(self):
        """
        Disconnect server (set port as 0) after loading log.
        """

        self._will_disconnect = True

    def require_a_choice(self):
        """
        Start a color choice.
        """

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "star{}".format(os.path.basename(sys.argv[0]))
            client.sendall(info.encode("utf-8"))

            client.close()

    def add_items_for_render(self, items, setcolor, color=lambda r: "#" + r.selected_color.hec):
        """
        Add items into list for render.

        Args:
            items (tuple or list): item list for render.
            setcolor (str or function): how to set a color for this item. item inner method name if str, else self-defined setcolor function with item and color as the first and second arguments. for example, "setcolor=lambda item, color: item.set_color(color)".
            color (str or function): set which color for this item. static color if str, else dynamic color generated by function with rickrack result as the first argument. for example, "color=lambda result: "#" + result.selected_color.hec". default: the selected color in software.
        """

        if isinstance(items, (tuple, list)):
            item_lst = tuple(items)

        else:
            item_lst = (items,)

        if isinstance(setcolor, str):
            for item in item_lst:
                assert hasattr(item, setcolor), "item {} doesn't has a setcolor method: {}".format(item, setcolor)

            method = lambda obj, c: getattr(obj, setcolor)(c)

        else:
            method = setcolor

        assert isinstance(method, types.FunctionType), "setcolor is not an available function (name): {}".format(method)

        if isinstance(color, str):
            func = lambda r: color

        else:
            func = color

        assert isinstance(func, types.FunctionType), "color is not an available function (name): {}".format(func)

        self._items_for_render.append((item_lst, method, func))

    def render(self, head=None, tail=None):
        """
        Start a render loop till color choice confirmed.

        Args:
            head (None or function): pretreatment function at the beginning of each loop. default: None.
            tail (None or function): post-treatment function at the ending of each loop. default: None.
        """

        curr_hash = ""
        self.require_a_choice()

        do_first_run = True

        while self.is_connected and (self.is_choice_available or do_first_run):
            do_first_run = False

            if head:
                head()

            self.update()

            if self.hash == curr_hash:
                continue

            curr_hash = self.hash

            for item_lst, method, func in self._items_for_render:
                for item in item_lst:
                    method(item, func(self._result))

            if tail:
                tail()

    def modify_color(self, index, color):
        """
        Modify a color by index and new color.

        Args:
            index (int): color index in color set.
            color (str): color in Color type.
        """

        if self.is_connected:
            if index and index in range(5):
                idx = str(index)

            else:
                idx = "N"

            assert isinstance(color, Color), "color isn't in Color type: {}".format(color)

            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "cidx{}; {}".format(idx, " ".join(["{:.5f}".format(j) for j in color.hsv]))
            client.sendall(info.encode("utf-8"))

            client.close()

    def import_color_set(self, dps_file):
        """
        Import a dps color file into Rickrack.

        Args:
            dps_file (str): dps file for import.
        """

        assert os.path.isfile(dps_file), "import file doesn't exist: {}".format(dps_file)
        assert dps_file[-4:] == ".dps", "import file isn't a dps color file: {}".format(dps_file)

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "iset{}".format(dps_file)
            client.sendall(info.encode("utf-8"))

            client.close()

    def export_color_set(self, dps_file):
        """
        Export a dps color file from Rickrack.

        Args:
            dps_file (str): dps file for export.
        """

        assert os.path.isdir(os.path.dirname(dps_file)), "export dir doesn't exist: {}".format(os.path.dirname(dps_file))
        assert dps_file[-4:] == ".dps", "export file isn't a dps color file: {}".format(dps_file)

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "oset{}".format(dps_file)
            client.sendall(info.encode("utf-8"))

            client.close()

    def open_color_depot(self, dpc_file):
        """
        Open a dpc color file into Rickrack.

        Args:
            dpc_file (str): dpc file for open.
        """

        assert os.path.isfile(dpc_file), "open file doesn't exist: {}".format(dpc_file)
        assert dpc_file[-4:] == ".dpc", "open file isn't a dpc color file: {}".format(dpc_file)

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "idpt{}".format(dpc_file)
            client.sendall(info.encode("utf-8"))

            client.close()

    def save_color_depot(self, dpc_file):
        """
        Save a dpc color file from Rickrack.

        Args:
            dpc_file (str): dpc file for save.
        """

        assert os.path.isdir(os.path.dirname(dpc_file)), "save dir doesn't exist: {}".format(os.path.dirname(dpc_file))
        assert dpc_file[-4:] == ".dpc", "save file isn't a dpc color file: {}".format(dpc_file)

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            info = "odpt{}".format(dpc_file)
            client.sendall(info.encode("utf-8"))

            client.close()

    def update_or_load_or_run(self, log_file, dp_argv={}, dp_proj=""):
        """
        Updating result if software connected, else loading result if log file exists, else running directly.

        Args:
            log_file (str): see method: load_log.
            dp_argv (dict): see method: run.
            dp_proj (str): see method: run.
        """

        if self.is_connected:
            self.update()

        else:
            self.load_or_run(log_file, dp_argv=dp_argv, dp_proj=dp_proj)

    def load_or_update_or_run(self, log_file, dp_argv={}, dp_proj=""):
        """
        Loading result if log file exists, else updating result if software connected, else running directly.

        Args:
            log_file (str): see method: load_log.
            dp_argv (dict): see method: run.
            dp_proj (str): see method: run.
        """

        if os.path.isfile(log_file):
            self.load_log(log_file=log_file)

        else:
            self.update_or_run(dp_argv=dp_argv, dp_proj=dp_proj)

    def update_or_load(self, log_file):
        """
        Updating result if software connected, else loading result from log file.

        Args:
            log_file (str): see method: load_log.
        """

        if self.is_connected:
            self.update()

        else:
            self.load_log(log_file=log_file)

    def load_or_update(self, log_file):
        """
        Loading result if log file exists, else updating result from software connection.

        Args:
            log_file (str): see method: load_log.
        """

        if os.path.isfile(log_file):
            self.load_log(log_file=log_file)

        else:
            self.update()

    def update_or_run(self, dp_argv={}, dp_proj=""):
        """
        Updating result if software connected, else running directly.

        Args:
            dp_argv (dict): see method: run.
            dp_proj (str): see method: run.
        """

        if self.is_connected:
            self.update()

        else:
            self.run(dp_argv=dp_argv, dp_proj=dp_proj)

    def load_or_run(self, log_file, dp_argv={}, dp_proj=""):
        """
        Loading result if log file exists, else running directly.

        Args:
            dp_argv (dict): see method: run.
            dp_proj (str): see method: run.
        """

        if os.path.isfile(log_file):
            self.load_log(log_file=log_file)

        else:
            self.run(dp_argv=dp_argv, dp_proj=dp_proj)

    def update(self):
        """
        Get result from Rickrack server.
        """

        if self.is_connected:
            client = socket.socket()
            client.settimeout(self._timeout)
            client.connect((self._host, self._port))

            client.sendall("data".encode("utf-8"))

            head = client.recv(10)
            head = head.decode("utf-8")

            doc = client.recv(int(head))
            doc = doc.decode("utf-8")

            client.close()

            self._load("+ @ " + doc)

    def run(self, dp_argv={}, dp_proj=""):
        """
        Running Rickrack.
        Note that the sequence of colors in returned color set list doesn't consist with the sequence displayed in Rickrack Result window.
        The sequence displayed in Rickrack Result window is 2, 1, 0, 3, 4 according to the color set list, i.e., the first color in color list is the middle (main) color in Rickrack Result window.

        Args:
            dp_argv (dict): rickrack argv, includes "help", "version", "temporary", "reset", "input", "output", "window", "sequence", "lang" and (or) "port". for example, {"help": True, "reset": "all"}.
            dp_proj (str): rickrack startup argv, project directory.
        """

        if self.is_connected:
            print("Rickrack is already started.")

            return

        if dp_proj:
            dirname, basename = para_dir(dp_proj)

        elif os.path.isfile(os.sep.join([os.path.abspath(os.path.dirname(__file__)), "data.json"])):
            with open(os.sep.join([os.path.abspath(os.path.dirname(__file__)), "data.json"]), "r", encoding="utf-8") as f:
                data = json.load(f)

            if "dp_proj" in data and data["dp_proj"]:
                dirname, basename = para_dir(data["dp_proj"])

            else:
                dirname, basename = None, None

        else:
            dirname, basename = para_dir(".")

        if not dirname or not basename:
            dirname, basename = para_dir(os.path.abspath(os.path.dirname(__file__)))

        if not dirname or not basename:
            print("\n+" + "-" * 30 + " Rickrack-Startup " + "-" * 30 + "+")
            print(__HELP__)
            print(__ERROR__)
            sys.exit()

        os.chdir(dirname)

        with open(os.sep.join([os.path.abspath(os.path.dirname(__file__)), "data.json"]), "w", encoding="utf-8") as f:
            json.dump({"dp_proj": dirname, "dp_exec": basename}, f, indent=4, ensure_ascii=False)

        # run project.
        sdp_argv = dict()

        if dp_argv:
            if isinstance(dp_argv, dict):
                sdp_argv = dp_argv.copy()

            elif isinstance(dp_argv, str):
                sdp_argv[dp_argv] = True

            elif isinstance(dp_argv, (tuple, list, set)):
                for i in dp_argv:
                    sdp_argv[i] = True

        # priority: local port (sdp_argv["port"]) > global port (self._port).
        # global port will be synced by local port if not zero.
        if "port" in sdp_argv:
            if self._port:
                self._port = int(sdp_argv["port"])

        else:
            sdp_argv["port"] = str(self._port)

        run_argv = ""

        for dp_key in sdp_argv:
            if dp_key in ("help", "version", "temporary"):
                run_argv = run_argv + " --{}".format(dp_key)

                if dp_key == "help":
                    print("\n+" + "-" * 30 + " Rickrack-Startup " + "-" * 30 + "+")
                    print(__HELP__)

                elif dp_key == "version":
                    print("Rickrack-Startup {} ({})\n".format(__VERSION__[1:-1], __DATE__[1:-1]))

            else:
                run_argv = run_argv + " --{}=\"{}\"".format(dp_key, sdp_argv[dp_key])

        cmd = ""
        results = ""

        if basename[-3:] == ".py":
            with open(basename, "r", encoding="utf-8") as f:
                f.readline()
                f.readline()
                f.readline()
                line = f.readline()

            if line[:30] == "Real-time Color Kit (Rickrack)":
                cmd = "\"{}\" {}".format(sys.executable, basename + run_argv)

            else:
                print("\n+" + "-" * 30 + " Rickrack-Startup " + "-" * 30 + "+")
                print(__HELP__)
                print(__ERROR__)
                sys.exit()

        else:
            cmd = basename + run_argv

        if self._port:
            dp_thread = RickrackThread()
            dp_thread.cmd = cmd
            dp_thread.start()
            dp_thread.join()

            self.is_started_by_script = True

            while not self.is_connected:
                time.sleep(1)
                print("Waiting for starting Rickrack.")

        else:
            results = os.popen(cmd, "r")

        # get results.
        if results:
            exec_results = results.read()

        else:
            exec_results = ""

        if "help" in sdp_argv or "version" in sdp_argv:
            print(exec_results)

            return

        self._load(exec_results)

    def close(self, save_data=True):
        """
        Close Rickrack.

        Args:
            save_data (bool): if save data before close.
        """

        if self.is_started_by_script and self.is_connected:
            while self.is_connected:
                client = socket.socket()
                client.settimeout(self._timeout)
                client.connect((self._host, self._port))

                info = "exit{}".format(save_data)
                client.sendall(info.encode("utf-8"))

                client.close()

                time.sleep(1)
                print("Waiting for closing Rickrack.")

        self.is_started_by_script = False

    def load_log(self, log_file):
        """
        Loading result from a log file.

        Args:
            log_file (str): log file path.
        """

        assert os.path.isfile(log_file), "load file doesn't exist: {}".format(log_file)

        # disconnect after load.
        if self._will_disconnect:
            self._port = 0

        # load.
        log_text = open(log_file, "r", encoding="utf-8")
        log_text = log_text.read()
        self._load(log_text)

    def dump_log(self, log_file):
        """
        Dumping result into a log file.

        Args:
            log_file (str): file path.
        """

        assert os.path.isdir(os.path.dirname(log_file)), "dump dir doesn't exist: {}".format(os.path.dirname(log_file))

        # dump.
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(self._text)

    # ---------- ---------- ---------- Personal Funcs ---------- ---------- ---------- #

    def _load(self, log_text):
        """
        Load result from log text.

        Args:
            log_text (str): text.
        """

        # calc hash.
        data_hash = hashlib.md5(log_text.encode("utf-8")).hexdigest()[:10]

        if data_hash == self._hash:
            return

        self._hash = data_hash
        self._text = log_text

        # para results.
        rt_rule = "Custom"
        rt_cidx = 0
        rt_cset = ["FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF"]
        rt_cset_name = ["RR-1", "RR-2", "RR-3", "RR-4", "RR-5"]
        rt_refs = []
        rt_refs_name = []
        rt_gcol = 0
        rt_cgrd = []
        rt_cgrd_name = []

        para_full_colors = False
        para_color_grid = False

        for line in log_text.split("\n"):
            if len(line) > 9 and line[0] == "+" and line[2] in (" ", "*", "#"):
                if line[4:] == "Full Colors":
                    para_full_colors = True

                elif line[4:] == "Color Grid ...":
                    para_color_grid = True

                # Color Grid ...
                if para_color_grid:
                    if line[2] == " ":
                        color_line = line[4:].split(" ")
                        rt_gcol = len(color_line)

                        for i in range(len(color_line)):
                            color_line[i] = Color.fmt_hec(color_line[i])

                        rt_cgrd += color_line

                # Full Colors
                elif para_full_colors:
                    if line[2] == " ":
                        color_line = line[4:].split(" ")

                        for i in range(len(color_line)):
                            color_line[i] = Color.fmt_hec(color_line[i])

                        rt_refs = color_line

                else:
                    if line[4] in [str(i) for i in range(5)]:
                        if line[2] == "*":
                            rt_cidx = int(line[4])

                        rt_cset[int(line[4])] = Color.fmt_hec(line[3:].split()[7])

                    elif line[4:8] == "Rule":
                        rt_rule = line[10:].lstrip().rstrip()

                        if rt_rule not in ("Analogous", "Monochromatic", "Triad", "Tetrad", "Pentad", "Complementary", "Shades", "Custom"):
                            rt_rule = "Custom"

            elif len(line) > 9 and line[0] == "+" and line[2] == "@":
                doc = line[4:].split("; ")

                if len(doc) in (5, 6):
                    data_rule, data_index, data_set, data_col, data_grid = doc[:5]
                    data_grid_name = "" if len(doc) < 6 else doc[5]

                    if data_rule in ("Analogous", "Monochromatic", "Triad", "Tetrad", "Pentad", "Complementary", "Shades", "Custom"):
                        rt_rule = data_rule

                    if data_index in [str(i) for i in range(5)]:
                        rt_cidx = int(data_index)

                    rt_gcol = int(data_col)
                    data_set = data_set.split(" ")
                    data_grid = data_grid.split(" ")
                    data_grid_name = data_grid_name.lstrip().rstrip()

                    if data_grid_name:
                        data_grid_name = data_grid_name[1:-1].split('" "')

                    for i in range(5):
                        rt_cset[(2, 1, 0, 3, 4)[i]] = Color.fmt_hec(data_set[i])

                    for i in range(len(data_set) - 6):
                        rt_refs.append(Color.fmt_hec(data_set[i + 6]))

                    for i in range(len(data_grid)):
                        rt_cgrd.append(Color.fmt_hec(data_grid[i]))

                        if data_grid_name:
                            rt_cgrd_name.append(data_grid_name[i])

        rt_cset = Grid(rt_cset, rt_cset_name, 5)
        rt_refs = Grid(rt_refs, rt_refs_name, len(rt_refs))
        rt_cgrd = Grid(rt_cgrd, rt_cgrd_name, (rt_gcol, rt_gcol))

        result = {"rule": str(rt_rule), "index": int(rt_cidx), "colors": rt_cset, "refs": rt_refs, "grid": rt_cgrd}
        result = Result(result)

        self._result = result


class RickrackThread(Thread):
    """
    RickrackThread object. Running Rickrack in sub-thread.
    """

    name = "Rickrack"
    cmd = ""

    def run(self):
        """
        Running command.
        """

        os.popen(self.cmd, "r")


if __name__ == "__main__":
    ans = startup()
