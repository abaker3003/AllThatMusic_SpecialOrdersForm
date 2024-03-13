import sys
import customtkinter
import tkinter.ttk
import tkinter 

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList():
    def __init__(self, objs=None):
        self.head = None
        self.tail = None
        if objs is not None:
            for obj in objs:
                self.append(obj)

    def append(self, data):
        new_node = Node(data)
        new_node.prev = self.tail
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
