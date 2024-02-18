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
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
