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

from PySide2.QtCore import QThread, Signal
from socketserver import TCPServer
from ricore.server_req import Request


class ResultServer(QThread):
    """
    ResultServer object.
    """

    ps_iset = Signal(str)
    ps_oset = Signal(str)
    ps_idpt = Signal(str)
    ps_odpt = Signal(str)
    ps_cidx = Signal(tuple)
    ps_star = Signal(bool)
    ps_exit = Signal(bool)

    def __init__(self, args, port=None):
        """
        Init ResultServer object by port.
        """

        super().__init__()

        self.req = Request
        self.req.args = args
        self.req.ps_iset = self.ps_iset
        self.req.ps_oset = self.ps_oset
        self.req.ps_idpt = self.ps_idpt
        self.req.ps_odpt = self.ps_odpt
        self.req.ps_cidx = self.ps_cidx
        self.req.ps_star = self.ps_star
        self.req.ps_exit = self.ps_exit

        self._port = port
        self._server = None

    def run(self):
        """
        Start running in thread.
        """

        try:
            self._server = TCPServer(("localhost", self._port), self.req)

        except Exception as err:
            self._server = None

        if self._server:
            self._server.serve_forever()
