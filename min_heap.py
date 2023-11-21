from node import HeapNode


class PriorityMinHeap:
    MAX_SIZE = 20

    def __init__(self):
        self.heap = []
        self.heap_size = 0

    # add new element to the heap
    def push(self, patron_id, priority):
        if self.heap_size < PriorityMinHeap.MAX_SIZE:
            node = HeapNode(patron_id, priority)
            self.heap.append(node)
            self.heap_size += 1
            self.heapify_up(len(self.heap) - 1)

    # remove root element (smallest) and heapify down to readjust heap property
    def pop(self):
        if not self.heap:
            return None

        # swap the root with the last element
        PriorityMinHeap.swap(self.heap, 0, len(self.heap) - 1)
        # pop the last element (root)
        popped = self.heap.pop()
        # heapify down to maintain heap property
        self.heapify_down(0)
        self.heap_size -= 1
        return popped

    # function to swap elements at given positions
    @staticmethod
    def swap(nodes, i, j):
        nodes[i], nodes[j] = nodes[j], nodes[i]

    # Compare two nodes based on priority and timestamp and return true if first has
    # greater priority of arrives first in case of same priority.
    @staticmethod
    def compare_nodes(node1, node2):
        if node1.priority == node2.priority:
            return node1.timestamp < node2.timestamp
        return node1.priority < node2.priority

    # function to fix heap properties while inserting (from index up to the root)
    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if PriorityMinHeap.compare_nodes(self.heap[index], self.heap[parent]):
                PriorityMinHeap.swap(self.heap, parent, index)
                index = parent
            else:
                break

    # function to fix heap properties after deletion from root to leaf
    def heapify_down(self, index):
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < len(self.heap) and PriorityMinHeap.compare_nodes(self.heap[left_child], self.heap[smallest]):
                smallest = left_child

            if right_child < len(self.heap) and PriorityMinHeap.compare_nodes(self.heap[right_child], self.heap[smallest]):
                smallest = right_child

            if smallest != index:
                PriorityMinHeap.swap(self.heap, index, smallest)
                index = smallest
            else:
                break

    # function to return patrons in sorted order without altering original heap
    def get_patrons_sorted(self):
        for x in self.heap:
            yield x.patron_id
