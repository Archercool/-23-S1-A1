# @File: undo.py
# @Author: Aoran Li
# @Last Edit Date: 2023-03-31

from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import *

class UndoTracker:

    def __init__(self):
        self.undo_tracker = ArrayStack(10000)   #Used to store undo operations
        self.redo_tracker = ArrayStack(10000)   #Used to store redo operations

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        if self.undo_tracker.is_full():
            return
        else:
            # Add the action to the undo tracker and clear the redo tracker
            self.undo_tracker.push(action)
            self.redo_tracker.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        if self.undo_tracker.is_empty():
            return None
        else:
            # Pop the last action from the undo tracker and push it to the redo tracker
            undo_operation = self.undo_tracker.pop()
            self.redo_tracker.push(undo_operation)
            undo_operation.undo_apply(grid)
            return undo_operation

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        if self.redo_tracker.is_empty():
            return None
        else:
            # Pop the last action from the redo tracker and push it to the undo tracker
            redo_operation = self.redo_tracker.pop()
            self.undo_tracker.push(redo_operation)
            redo_operation.redo_apply(grid)
            return redo_operation