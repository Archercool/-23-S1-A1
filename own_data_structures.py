# @File: own_data_structures.py
# @Author: Aoran Li
# @Last Edit Date: 2023-03-27

from data_structures.queue_adt import *
from data_structures.abstract_list import *
from data_structures.referential_array import ArrayR, T


class ArrayQueue(Queue[T]):
    MIN_CAPACITY = 1

    def __init__(self,max_capacity:int) -> None:
        super().__init__()
        # Set the capacity of the queue to a maximum of the minimum capacity 
        # and the specified maximum capacity
        self.capacity = max(self.MIN_CAPACITY, max_capacity)
        # Create an array to store the elements in the queue
        self.items = ArrayR(max(self.MIN_CAPACITY,max_capacity))
        # Initialize both the front and rear indexes of the queue to 0
        self.front = 0
        self.rear = 0

    def append(self, item: T) -> None:
        """ 
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        if self.is_full():
            # If the queue is full, raise an exception
            raise Exception("Queue is full")
        # Add the item to the queue and increment the rear index
        self.items[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.length += 1


    def is_full(self) -> bool:
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        return self.length == self.capacity

    def __getitem__(self, index: int) -> T:
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if index < 0 or index >= len(self):
            # If the index is out of range, raise an exception
            raise IndexError("Index out of range")
        # Return the item at the specified index
        return self.items[(self.front + index) % self.capacity]

    def __setitem__(self, index: int, item: T) -> None:
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if index < 0 or index >= len(self):
            # If the index is out of range, raise an exception
            raise IndexError("Index out of range")
        # Set the item at the specified index
        self.items[(self.front + index) % self.capacity] = item

    # Define a method for flipping elements in a queue
    def reverse(self) -> None:
        """ 
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(n)
        """
        i = self.front
        j = (self.rear - 1) % self.capacity
        while i < j:
            # Exchange elements in the queue from both ends until i>=j
            self.items[i], self.items[j] = self.items[j], self.items[i]
            i = (i + 1) % self.capacity
            j = (j - 1) % self.capacity
    

    def serve(self) -> None:
        """ Deletes the element at the queue's front.
        :pre: queue is not empty
        :raises Exception: if the queue is empty
        """
        """
        Best-Case Complexity = O(1)
        Worst-Case Complexity = O(1)
        """
        if self.is_empty():
            # If the queue is empty, raise an exception
            raise Exception("Queue is empty")
        # Delete the element at the front of the queue and increment the front index
        self.front = (self.front + 1) % self.capacity
        self.length -= 1
        




        
                    