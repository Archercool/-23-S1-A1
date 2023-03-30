# @File: grid.py
# @Author: Aoran Li
# @Last Edit Date: 2023-03-28

from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        # x and y are the dimensions.
        if draw_style not in self.DRAW_STYLE_OPTIONS:
            raise ValueError("Invalid draw style.")   # Check whether the drawing style is valid
        self.x = x
        self.y = y
        self.draw_style = draw_style
        self.brush_size = self.DEFAULT_BRUSH_SIZE   # Set the brush size to the default size
        self.initialize(self.x, self.y)
        

    def initialize(self, x, y):
        """
        Best-Case Complexity = O(x*y)
        Worst-Case Complexity = O(x*y)
        """
        # create grid
        self.grid = ArrayR(x)
        for i in range(x):
            row = ArrayR(y)
            for j in range(y):
                # Select the LayerStore class based on the drawing style
                if self.draw_style == Grid.DRAW_STYLE_SET:
                    layer_store = SetLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_ADD:
                    layer_store = AdditiveLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_SEQUENCE:
                    layer_store = SequenceLayerStore()
                row[j] = layer_store
            self.grid[i] = row

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        """
        Best-Case Complexity = O(x*y)
        Worst-Case Complexity = O(x*y)
        """
        # Cycle through each row and column of the grid and 
        # activate special effects on the corresponding layer storage object
        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()
        

    def __getitem__(self, index):
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        # Index to access the content of a Grid object
        return self.grid[index]


