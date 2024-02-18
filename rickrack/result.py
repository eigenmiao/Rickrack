# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more infomation 
about Rickrack.

Copyright (c) 2019-2023 by Eigenmiao. All Rights Reserved.
"""

import numpy as np
from rickrack.color import Color


class Box(object):
    """
    Box object. Storing a color and a name.
    """

    def __init__(self, color, name):
        self._color = str(color)
        self._name = str(name)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __getitem__(self, idx):
        """
        Get color item in color grid.

        Args:
            idx (int or float): color index in grid.
        """

        if idx in (0, "color"):
            return Color(self._color, tp=CTP.hec)

        elif idx in (1, "name"):
            return str(self._name)

    def __str__(self):
        """
        Str format.
        """

        return "Box({}: {})".format(self._name, self._color)

    def __repr__(self):
        """
        Repr format.
        """

        return str(self)

    # ---------- ---------- ---------- Properties ---------- ---------- ---------- #

    @property
    def color(self):
        return Color(self._color, tp=CTP.hec)

    @property
    def name(self):
        return str(self._name)


class Grid(object):
    """
    Grid object. Storing color grid.
    """

    def __init__(self, color_grid, name_grid, grid_size):
        """
        Init Grid ojbect.

        Args:
            color_grid (tuple or list): hex code color list.
            name_grid (tuple or list): name list.
            grid_size (tuple, or list): grid size.
        """

        if not isinstance(color_grid, (tuple, list)):
            raise ValueError("Color grid is not a list: {}".format(color_grid))

        if not isinstance(name_grid, (tuple, list)):
            raise ValueError("Name grid is not a list: {}".format(name_grid))

        if isinstance(grid_size, int) and grid_size >= 0:
            self._grid_size = (int(grid_size),)

        elif isinstance(grid_size, (tuple, list)) and len(grid_size) == 1 and isinstance(grid_size[0], int) and grid_size[0] >= 0:
            self._grid_size = (int(grid_size[0]),)

        elif isinstance(grid_size, (tuple, list)) and len(grid_size) == 2 and isinstance(grid_size[0], int) and isinstance(grid_size[1], int) and grid_size[0] >= 0 and grid_size[1] >= 0:
            self._grid_size = (int(grid_size[0]), int(grid_size[1]))

        else:
            raise ValueError("Grid size is not a number list: {}".format(grid_size))

        if len(self._grid_size) == 1:
            color_grid = ["FFFFFF" if i >= len(color_grid) else Color.fmt_hec(color_grid[i]) for i in range(self._grid_size[0])]
            name_grid = ["RR-{}".format(i + 1) if i >= len(name_grid) else str(name_grid[i]) for i in range(self._grid_size[0])]

        else:
            color_grid = [["FFFFFF" if i * self._grid_size[1] + j >= len(color_grid) else Color.fmt_hec(color_grid[i * self._grid_size[1] + j]) for j in range(self._grid_size[1])] for i in range(self._grid_size[0])]
            name_grid = [["RR-{}-{}".format(i + 1, j + 1) if i * self._grid_size[1] + j >= len(name_grid) else str(name_grid[i * self._grid_size[1] + j]) for j in range(self._grid_size[1])] for i in range(self._grid_size[0])]

        self._color_grid = np.array(color_grid, dtype=str).reshape(grid_size)
        self._name_grid = np.array(name_grid, dtype=str).reshape(grid_size)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __getitem__(self, idx):
        """
        Get color item in color grid.

        Args:
            idx (int or float): color index in grid.
        """

        curr_color = self._color_grid[idx]
        curr_name = self._name_grid[idx]

        if isinstance(curr_color, str) and isinstance(curr_name, str):
            return Box(curr_color, curr_name)

        elif isinstance(curr_color, np.ndarray) and isinstance(curr_name, np.ndarray):
            curr_size = curr_color.shape
            curr_color = curr_color.reshape(-1).tolist()
            curr_name = curr_name.reshape(-1).tolist()

            return Grid(curr_color, curr_name, curr_size)

    def __str__(self):
        """
        Str format.
        """

        return "Grid(size {})".format("x".join([str(i) for i in self.size]))

    def __repr__(self):
        """
        Repr format.
        """

        return str(self)

    # ---------- ---------- ---------- Properties ---------- ---------- ---------- #

    @property
    def T(self):
        curr_color = self._color_grid.T
        curr_name = self._name_grid.T

        curr_size = curr_color.shape
        curr_color = curr_color.reshape(-1).tolist()
        curr_name = curr_name.reshape(-1).tolist()

        return Grid(curr_color, curr_name, curr_size)

    @property
    def size(self):
        return self._grid_size

    @property
    def shape(self):
        return self.size

    @property
    def values(self):
        return self._color_grid.reshape(-1).tolist(), self._name_grid.reshape(-1).tolist()

    @property
    def grid(self):
        return Grid(*self.h_line.values, self.size)

    @property
    def h_line(self):
        curr_color = self._color_grid.reshape(-1).tolist()
        curr_name = self._name_grid.reshape(-1).tolist()

        return Grid(curr_color, curr_name, len(curr_color))

    @property
    def v_line(self):
        curr_color = self._color_grid.T.reshape(-1).tolist()
        curr_name = self._name_grid.T.reshape(-1).tolist()

        return Grid(curr_color, curr_name, len(curr_color))


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

        self._result = {
            "rule": "Custom",
            "index": 0,
            "colors": Grid([], [], 5),
            "refs": Grid([], [], 5),
            "grid": Grid([], [], (1, 1)),
        }

        if "rule" in color_result:
            self._result["rule"] = str(color_result["rule"])

        if "index" in color_result:
            self._result["index"] = int(color_result["index"])

        if "colors" in color_result:
            curr_colors = color_result["colors"]

            if isinstance(curr_colors, Grid):
                self._result["colors"] = curr_colors.h_line

            else:
                raise ValueError("Invalid colors: {}.".format(curr_colors))

        if "refs" in color_result:
            curr_colors = color_result["refs"]

            if isinstance(curr_colors, Grid):
                self._result["refs"] = curr_colors.h_line

            else:
                raise ValueError("Invalid ref colors: {}.".format(curr_colors))

        if "grid" in color_result:
            curr_colors = color_result["grid"]

            if isinstance(curr_colors, Grid):
                self._result["grid"] = curr_colors.grid

            else:
                raise ValueError("Invalid color grid: {}.".format(curr_colors))

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

        plain_text += "Full Colors:\n  {}\n".format(self._result["refs"])
        plain_text += "Color Grid ...:\n  {}\n".format(self._result["grid"])

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
        colors = [self._result["colors"][i] for i in (2, 1, 0, 3, 4)]
        return Grid([i[0].hec for i in colors], [i[1] for i in colors], 5)

    @property
    def selected_color(self):
        return self._result["colors"][self._result["index"]]

    @property
    def full_colors(self):
        return self._result["refs"]

    @property
    def color_grid(self):
        return self._result["grid"]

    @property
    def cset(self):
        return self.colors

    @property
    def cset_in_order(self):
        return self.colors_in_order

    @property
    def refs(self):
        return self.full_colors

    @property
    def grid(self):
        return self.color_grid
