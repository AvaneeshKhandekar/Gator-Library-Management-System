from min_heap import PriorityMinHeap
from node import TreeNode
from tree_helper import TreeHelper, Color


class RedBlackTree:
    def __init__(self):
        self.root = TreeNode.create_empty_node()
        self.color_flip_count = 0
        self.color_count = 0

    # function to insert a new book in the red-black tree
    def insert_book(self, book_id, book_name, author_name, availability_status, borrowed_by=None):
        # create node with given book id and initialize reservation heap
        new_node, reservation_heap = TreeNode(book_id), PriorityMinHeap()

        # update book attributes in the node
        new_node.book_name, new_node.author_name, new_node.availability_status, new_node.borrowed_by, \
            new_node.reservation_heap = book_name, author_name, availability_status, borrowed_by, reservation_heap

        # set left and right as null nodes for balancing tree
        new_node.left = new_node.right = TreeNode.create_empty_node()

        # set color of newly inserted node to red
        new_node.color_changed = TreeHelper.set_color(self, new_node, Color.RED)

        # track nodes while traversing to find insert location
        current_parent, current_node = None, self.root

        # Traverse to find correct location for the new node
        current_parent = TreeHelper.find_insert_location(current_node, current_parent, new_node)

        # update pointers after insert
        TreeHelper.update_pointers_after_insert(self, current_parent, new_node)

        # if tree is empty, new node is the root so color it black
        if new_node.parent is None:
            new_node.color_changed = TreeHelper.set_color(self, new_node, Color.BLACK)
            return

        # if parent of new node is the root stop
        if new_node.parent.parent is None:
            return

        # fix tree properties violated by insert
        TreeHelper.balance_after_insert(self, new_node)

    # function to delete book from tree
    def delete_book(self, book_id):
        # find book to be deleted
        target_node = deleted_book = self.find_book(self.root, book_id)

        # if the book not found, return
        if target_node.is_null():
            return

        successor_node = target_node
        successor_original_color = successor_node.color

        replacement_node, successor_original_color = TreeHelper.find_replacement_node_and_update_pointers(self,
                                                                                                          successor_original_color,
                                                                                                          target_node)

        # if the original color of the successor was black, balance the tree
        if successor_original_color == Color.BLACK:
            TreeHelper.balance_after_delete(self, replacement_node)

        # get patrons from deleted node reservation heap for notification
        heap = deleted_book.reservation_heap
        patrons = []
        while heap.heap_size > 0:
            patrons.append(heap.pop())
        return deleted_book, patrons

    # function to find book with given book id from a give node
    def find_book(self, node, book_id):
        # return in tree is empty or book not found or if book found
        if node.is_null() or book_id == int(node.book_id):
            return node
        # traverse left subtree if book id is less than current node's book id (BST)
        if book_id < int(node.book_id):
            return self.find_book(node.left, book_id)
        # traverse right subtree if book id is greater than current node's book id (BST)
        return self.find_book(node.right, book_id)

    # update book and reservation heap when a patron requests to borrow a book
    def borrow_book(self, patron_id, book_id, priority):
        # find the book in the heap
        book = self.find_book(self.root, int(book_id))
        if book:
            # allot book to patron if book is available
            if book.availability_status == "Yes":
                book.availability_status = "No"
                book.borrowed_by = patron_id
                return book, True
            else:
                # else add patron to reservation heap and update book
                heap = book.reservation_heap
                heap.push(patron_id, priority)
                book.reservation_heap = heap
                return book, False

    # function to update book status when a patron returns it and allot to next patron in priority heap
    def return_book(self, book_id):
        # find book to update
        book = self.find_book(self.root, int(book_id))
        if book:
            heap = book.reservation_heap
            # if book has reservation heap allot book to next patron in priority heap
            if heap.heap_size > 0:
                book.availability_status = "No"
                patron = heap.pop()
                book.borrowed_by = patron.patron_id
                book.reservation_heap = heap
                return book, patron.patron_id
            else:
                # else update book availability to available
                book.availability_status = "Yes"
                book.borrowed_by = None
                return book, None

    # find books with books ids in the given range
    def find_books_in_range(self, node, book_id_1, book_id_2, result):
        if not node.is_null():
            # Traverse left subtree

            self.find_books_in_range(node.left, book_id_1, book_id_2, result)

            # Process the current node
            if book_id_1 <= int(node.book_id) <= book_id_2:
                result.append(node)

            # Traverse right subtree
            self.find_books_in_range(node.right, book_id_1, book_id_2, result)
        return result if result else None

    # return color flips count accounting for initial root color change
    def get_color_flips(self):
        self.color_count += 1
        if self.color_count == 2:
            self.color_flip_count += 1
        return self.color_flip_count

    # function to find the book or books closest to the given book id
    def find_closest_book(self, book_id):
        result = []

        # start from the root
        current = self.root
        closest_lower = None
        closest_higher = None

        while current.book_id is not None:
            # if the current node's book_id is less than the given id update closest_lower and move to the right
            if int(current.book_id) < int(book_id):
                closest_lower = current
                current = current.right
            # if the current node's book_id is greater than the given id, update closest_higher and move to the left
            elif int(current.book_id) > int(book_id):
                closest_higher = current
                current = current.left
            else:
                # if the current node's book_id is equal to the given, no need to search further
                result.append(current)
                return result

        result = TreeHelper.determine_closest_node(book_id, closest_higher, closest_lower, result)

        return result if result else None
