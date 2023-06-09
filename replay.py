# @File: replay.py
# @Author: Aoran Li
# @Last Edit Date: 2023-03-31

from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue

class ReplayTracker:

    def __init__(self):
        self.replay_tracker = CircularQueue(10000)   # Used to store replay operations
        self.replay = False   # Used to determine if replay is active

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        self.replay = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        # Add the action to the replay tracker
        self.replay_tracker.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """
        """
        Best Complexity: O(1)
        Worst Complexity: O(1)
        """
        # If the replay tracker is empty, return True
        if self.replay_tracker.is_empty():
            return True
        # Pop the last action from the replay tracker
        action = self.replay_tracker.serve()
        # If the action is an undo, undo_apply the action to the grid
        if action[1]:
            action[0].undo_apply(grid)
        # Otherwise, redo_apply the action to the grid
        else:
            action[0].redo_apply(grid)
        return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

