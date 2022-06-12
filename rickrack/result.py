# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more infomation 
about Rickrack.

Copyright (c) 2019-2022 by Eigenmiao. All Rights Reserved.
"""

from rickrack.color import Color


class Grid(object):
    """
    Grid object. Storing color grid.
    """

    def __init__(self, color_grid):
        """
        Init Grid ojbect.

        Args:
            color_grid (tuple or list): hex code color list.
        """

        self._grid = tuple(color_grid)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __getitem__(self, idx):
        """
        Get color item in color grid.

        Args:
            idx (int or float): color index in grid.
        """

        if isinstance(idx, (tuple, list)):
            if len(idx) > 2:
                return self[idx[0]][idx[1:]]

            else:
                return self[idx[0]][idx[1]]

        elif isinstance(idx, int) and idx < len(self._grid):
            color_line = self._grid[idx]

        elif isinstance(idx, float) and 0 <= idx <= 1:
            color_line = self._grid[int((len(self._grid) - 1) * idx)]

        else:
            color_line = self._grid[idx]

        if isinstance(color_line, str):
            return Color(color_line, tp="hec")

        else:
            return Grid(color_line)

    def __len__(self):
        """
        Length.
        """

        return len(self._grid)

    def __str__(self):
        """
        Str format.
        """

        curr_size = []
        curr_grid = self._grid

        while isinstance(curr_grid, (tuple, list)):
            curr_size.append(len(curr_grid))

            if curr_grid:
                curr_grid = curr_grid[0]

            else:
                curr_grid = None

        if curr_size:
            return "Grid(size {})".format("x".join([str(i) for i in curr_size]))

        else:
            return str(curr_grid)

    def __repr__(self):
        """
        Repr format.
        """

        return str(self)

    # ---------- ---------- ---------- Properties ---------- ---------- ---------- #

    @property
    def grid(self):
        return Grid(self._grid)

    @property
    def value(self):
        return tuple(self._grid)

    @property
    def h_line(self):
        line = []

        for i in range(len(self._grid)):
            for j in range(len(self._grid[0])):
                line.append(self._grid[i][j])

        return Grid(line)

    @property
    def v_line(self):
        line = []

        for j in range(len(self._grid[0])):
            for i in range(len(self._grid)):
                line.append(self._grid[i][j])

        return Grid(line)


class Result(object):
    """
    Result object. Storing rickrack result.
    """

    def __init__(self, color_result):
        """
        Init Result ojbect.

        Args:
            color_result (dict): final result.
        """

        self._result = dict(color_result)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __getitem__(self, idx):
        """
        Get item in result.

        Args:
            idx (int or str): index in result.
        """

        if isinstance(idx, int):
            return self._result["colors"][idx]

        elif isinstance(idx, str):
            return self._result[idx]

        else:
            raise IndexError("Invalid index: {}".format(idx))

    def __str__(self):
        """
        Str format.
        """

        plain_text = ""
        plain_text += "Rule:\n  {}\n".format(self._result["rule"])
        plain_text += "Colors:\n"

        for i in (2, 1, 0, 3, 4):
            if i == self._result["index"]:
                plain_text += " *"

            else:
                plain_text += "  "

            plain_text += str(self._result["colors"][i]) + "\n"

        plain_text += "Color Grid:\n  {}\n".format(self._result["grid"])

        return plain_text

    def __repr__(self):
        """
        Repr format.
        """

        return str(self)

    # ---------- ---------- ---------- Properties ---------- ---------- ---------- #

    @property
    def rule(self):
        return self._result["rule"]

    @property
    def index(self):
        return self._result["index"]

    @property
    def colors(self):
        return self._result["colors"]

    @property
    def colors_in_order(self):
        return tuple([self._result["colors"][i] for i in (2, 1, 0, 3, 4)])

    @property
    def selected_color(self):
        return self._result["colors"][self._result["index"]]

    @property
    def grid(self):
        return self._result["grid"]

    @property
    def grid_h_line(self):
        return self._result["grid"].h_line

    @property
    def grid_v_line(self):
        return self._result["grid"].v_line
