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

import copy
import hashlib


class History(object):
    """
    History object. Undo and redo operations.
    """

    def __init__(self, args):
        """
        Init history.
        """

        self._args = args

        self._curr_idx = 0
        self._history_line = []

        self._moving = False
        self._recording = False

    def backup(self):
        """
        Create a history step.
        """

        if self._moving:
            return

        if self._curr_idx != len(self._history_line) - 1:
            self._curr_idx = self._curr_idx if self._curr_idx < len(self._history_line) else len(self._history_line) - 1
            self._history_line = self._history_line[:self._curr_idx + 1]

        if len(self._history_line) > self._args.max_history_steps:
            self._curr_idx = self._curr_idx - (len(self._history_line) - self._args.max_history_steps)
            self._history_line = self._history_line[len(self._history_line) - self._args.max_history_steps: ]

        step_md5 = ""
        step_md5 = step_md5 + hashlib.md5(str(self._args.hm_rule).encode("utf-8")).hexdigest()[:10]
        step_md5 = step_md5 + hashlib.md5(str(self._args.sys_color_set).encode("utf-8")).hexdigest()[:10]
        step_md5 = step_md5 + hashlib.md5(str(self._args.sys_grid_locations).encode("utf-8")).hexdigest()[:10]
        step_md5 = step_md5 + hashlib.md5(str(self._args.sys_grid_assitlocs).encode("utf-8")).hexdigest()[:10]
        step_md5 = step_md5 + hashlib.md5(str(self._args.sys_grid_list).encode("utf-8")).hexdigest()[:10]
        step_md5 = step_md5 + hashlib.md5(str(self._args.sys_grid_values).encode("utf-8")).hexdigest()[:10]
        step_md5 = hashlib.md5(step_md5.encode("utf-8")).hexdigest()[:10]

        # display info.
        # print("{} / {} -> {}".format(self._curr_idx, len(self._history_line), step_md5))

        if len(self._history_line) > 0 and step_md5 == self._history_line[-1][1]:
            return

        self._recording = True

        step = []

        # color set.
        step.append(str(self._args.hm_rule))
        step.append(self._args.sys_color_set.backup())

        # grid values.
        step.append(copy.deepcopy(self._args.sys_grid_locations))
        step.append(copy.deepcopy(self._args.sys_grid_assitlocs))
        step.append(copy.deepcopy(self._args.sys_grid_list))
        step.append(copy.deepcopy(self._args.sys_grid_values))

        # image values.
        step.append(copy.deepcopy(self._args.sys_color_locs))
        step.append(copy.deepcopy(self._args.sys_assit_color_locs))

        self._curr_idx = self._curr_idx + 1
        self._history_line.append((tuple(step), step_md5))

        self._recording = False

    def undo(self):
        """
        Move backward.
        """

        if self._recording:
            return

        if self._curr_idx <= 0:
            self._curr_idx = 0

            return

        self._moving = True

        self._curr_idx = self._curr_idx - 1
        step = self._history_line[self._curr_idx][0]

        # color set.
        self._args.hm_rule = str(step[0])
        self._args.sys_color_set.recover(step[1])

        # grid values.
        self._args.sys_grid_locations = copy.deepcopy(step[2])
        self._args.sys_grid_assitlocs = copy.deepcopy(step[3])
        self._args.sys_grid_list = copy.deepcopy(step[4])
        self._args.sys_grid_values = copy.deepcopy(step[5])

        # image values.
        self._args.sys_color_locs = copy.deepcopy(step[6])
        self._args.sys_assit_color_locs = copy.deepcopy(step[7])

        self._moving = False

    def redo(self):
        """
        Move foreward.
        """

        if self._recording:
            return

        if self._curr_idx >= len(self._history_line) - 1:
            self._curr_idx = len(self._history_line) - 1

            return

        self._moving = True

        self._curr_idx = self._curr_idx + 1
        step = self._history_line[self._curr_idx][0]

        # color set.
        self._args.hm_rule = str(step[0])
        self._args.sys_color_set.recover(step[1])

        # grid values.
        self._args.sys_grid_locations = copy.deepcopy(step[2])
        self._args.sys_grid_assitlocs = copy.deepcopy(step[3])
        self._args.sys_grid_list = copy.deepcopy(step[4])
        self._args.sys_grid_values = copy.deepcopy(step[5])

        # image values.
        self._args.sys_color_locs = copy.deepcopy(step[6])
        self._args.sys_assit_color_locs = copy.deepcopy(step[7])

        self._moving = False
