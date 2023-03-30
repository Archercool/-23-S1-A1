# @File: layer_store.py
# @Author: Aoran Li
# @Last Edit Date: 2023-03-28

from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from own_data_structures import *
from data_structures.array_sorted_list import *
from data_structures.bset import *
from layer_util import *
from layers import invert

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        super().__init__()
        self.layer = None   # Store Single Layer
        self.mode = False   # Is the storage special mode active
        
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.layer == layer:
            return False
        else:
            self.layer = layer
            return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.layer is None:
            color = start
        else:
            color = self.layer.apply(start, timestamp, x, y)
        if self.mode:
            return invert.apply(color, timestamp, x, y)   # Invert color if special mode is active
        else:
            return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.layer is None:
            return False
        else:
            self.layer = None
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        # Activate special mode or turn off special mode
        if self.mode:
            self.mode = False
        else:
            self.mode = True

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        super().__init__()
        self.layers = ArrayQueue(10)    # Create an ArrayQueue object to store the layer, 
                                        # with an initial capacity of 10

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        self.layers.append(layer)   # Add a new layer to the end of the queue
        if len(self.layers) > self.layers.capacity:   # If the length of the queue is greater than the capacity
            self.layers.capacity = len(self.layers)*100   # Increase the capacity of the queue
        return True
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        # If the queue is empty, return the starting color
        if len(self.layers) == 0:
            return start
        else:
            color = start
            # Iterate through each layer in the queue and apply it to the color
            for layer in self.layers:
                color = layer.apply(color, timestamp, x, y)
            return color
        

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        if len(self.layers) == 0:   # If the queue is empty, return False
            return False
        else:
            self.layers.serve()   # Remove the first layer in the queue
            return True
        
    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        self.layers.reverse()   # Reverse the order of the layers in the queue
        
class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        super().__init__()
        self.layers = BSet(len(get_layers()))

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        # If the layer is not in the BSet, add it and return True
        if (layer.index + 1) not in self.layers:
            self.layers.add(layer.index + 1)
            return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(logn)
        """
        colour = start
        if self.layers.is_empty():   # If the BSet is empty, return the starting color
            return colour
        # Iterate through each layer in the BSet and apply it to the color
        for i in range(1, int.bit_length(self.layers.elems) + 1):   
            if i in self.layers:
                colour = get_layers().array[i - 1].apply(colour, timestamp, x, y)
        return colour

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(logn)
        """
        if self.layers.is_empty():   # If the BSet is empty,
            return False
        elif (layer.index + 1) in self.layers:   # If the layer is in the BSet, 
            self.layers.remove(layer.index + 1)  #remove it and return True
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        # If the BSet is empty, return False
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        if self.layers.__len__() == 0:
            return False
        else:
            # Create a new ArraySortedList object to store the special layers
            special_layer = ArraySortedList(self.layers.__len__())
            # Iterate through each layer in the BSet and add it to the special layer
            for i in range(1, int.bit_length(self.layers.elems) + 1):
                if i in self.layers:
                    item = ListItem(get_layers().array[i - 1], get_layers().array[i - 1].name)
                    special_layer.add(item)
            # If the length of the special layer is odd, remove the middle one
            if special_layer.__len__() % 2 == 1:
                value = special_layer[special_layer.__len__() // 2].value
            # If the length of the special layer is even, remove the smallest of the middle two names
            else:
                value = special_layer[special_layer.__len__() // 2 - 1].value
            self.layers.remove(value.index + 1)
            