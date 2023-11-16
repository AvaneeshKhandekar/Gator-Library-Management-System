import time

from tree_helper import Color


class TreeNode:

    def __init__(self, book_id: int):
        self.book_id = book_id
        self.parent = self.left = self.right = None
        self.color = Color.RED
        self.book_name = self.author_name = self.availability_status = None
        self.borrowed_by = self.reservation_heap = None

    def is_red(self):
        return self.color == Color.RED

    def is_black(self):
        return self.color == Color.BLACK

    def is_null(self):
        return self.book_id is None

    # create an empty node
    @staticmethod
    def create_empty_node():
        node = TreeNode(0)
        node.book_id = None
        node.color = Color.BLACK
        return node


class HeapNode:
    def __init__(self, patron_id, priority):
        self.patron_id = patron_id
        self.priority = priority
        self.timestamp = time.perf_counter()
