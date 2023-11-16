from enum import Enum


class Color(Enum):
    BLACK = 0
    RED = 1


class TreeHelper:

    # function to set color and increment color flips
    @staticmethod
    def set_color(tree, tree_node, color):
        previous_color = tree_node.color
        tree_node.color = color
        if previous_color != color and tree_node != tree.root:
            tree.color_flip_count += 1

    # determine insert location in tree
    @staticmethod
    def find_insert_location(current_node, current_parent, new_tree_node):
        while not current_node.is_null():
            current_parent = current_node
            #  Traverse to right node until you reach leaf if new node's id is greater than current node
            if int(new_tree_node.book_id) > int(current_node.book_id):
                current_node = current_node.right
            else:
                #  Traverse to left node until you reach leaf if new node's id is smaller than current node
                current_node = current_node.left
        return current_parent

    # update parent pointers after insertion
    @staticmethod
    def update_pointers_after_insert(tree, current_parent, new_tree_node):
        # update parent pointer of new node after finding correct parent for it
        new_tree_node.parent = current_parent
        if current_parent is None:
            #  if tree is empty set new node as root
            tree.root = new_tree_node
        elif int(new_tree_node.book_id) > int(current_parent.book_id):
            # new book id is larger, it goes to the right of parent and updates pointer
            current_parent.right = new_tree_node
        else:
            # new book id is smaller, it goes to the left of parent and updates pointer
            current_parent.left = new_tree_node

    # Balance the tree after insertion
    @staticmethod
    def balance_after_insert(tree, tree_node):
        while tree_node.parent.is_red():
            # if inserted node's parent is left child of grandparent, get right uncle
            if tree_node.parent == tree_node.parent.parent.left:
                tree_node = TreeHelper.handle_parent_left_of_grandparent(tree, tree_node)
            else:
                tree_node = TreeHelper.handle_parent_right_of_grand_parent(tree, tree_node)
            # if new node is root, break
            if tree_node == tree.root:
                break

        # set root node to black
        if tree.root.is_red():
            TreeHelper.set_color(tree, tree.root, Color.BLACK)

    # insert case when new node's parent is right of it's grandparent
    @staticmethod
    def handle_parent_right_of_grand_parent(tree, tree_node):
        # inserted node's parent is right child of grandparent, get left uncle
        uncle = tree_node.parent.parent.left
        if uncle.is_red():
            # update node colors of uncle, parent and grandparent
            TreeHelper.set_color(tree, uncle, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent.parent, Color.RED)
            tree_node = tree_node.parent.parent  # update node to node's grandparent
        else:
            # uncle is black, perform necessary rotations and recolor
            if tree_node == tree_node.parent.left:
                node = tree_node.parent
                TreeHelper.right_rotation(tree, node)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent.parent, Color.RED)
            TreeHelper.left_rotation(tree, tree_node.parent.parent)
        return tree_node

    # insert case when new node's parent is left of it's grandparent
    @staticmethod
    def handle_parent_left_of_grandparent(tree, tree_node):
        # inserted node's parent is left child of grandparent, get right uncle
        uncle = tree_node.parent.parent.right
        if uncle.is_red():
            # update node colors of uncle, parent and grandparent
            TreeHelper.set_color(tree, uncle, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent.parent, Color.RED)
            tree_node = tree_node.parent.parent  # update node to node's grandparent
        else:
            # uncle is black, perform necessary rotations and recolor
            if tree_node == tree_node.parent.right:
                tree_node = tree_node.parent
                TreeHelper.left_rotation(tree, tree_node)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent.parent, Color.RED)
            TreeHelper.right_rotation(tree, tree_node.parent.parent)
        return tree_node

    # function to perform left rotation
    @staticmethod
    #  Function to perform left rotation around pivot node
    def left_rotation(tree, pivot_node):
        # right child of pivot will be the successor
        successor_node = pivot_node.right
        # make the left child of the successor_node the new right child of the pivot_node
        pivot_node.right = successor_node.left

        if not successor_node.left.is_null():
            # update parent pointer of new child if it exists
            successor_node.left.parent = pivot_node

        # update the parent of the successor_node
        successor_node.parent = pivot_node.parent

        if pivot_node.parent is None:
            # If rotation at root, update root
            tree.root = successor_node
        elif pivot_node == pivot_node.parent.left:
            # If rotation around left node of a parent, update parent's left pointer to successor
            pivot_node.parent.left = successor_node
        else:
            # If rotation around right node of a parent, update parent's right pointer to successor
            pivot_node.parent.right = successor_node
        # left rotate pivot node down to the left of successor
        successor_node.left = pivot_node
        # update pivot node parent pointer to successor node
        pivot_node.parent = successor_node

    # function to perform right rotation
    @staticmethod
    def right_rotation(tree, pivot_node):
        # left child of pivot will be the successor
        successor_node = pivot_node.left
        # make the right child of the successor_node the new left child of the pivot_node
        pivot_node.left = successor_node.right
        if not successor_node.right.is_null():
            # update parent pointer of new child if it exists
            successor_node.right.parent = pivot_node

        # update the parent of the successor_node
        successor_node.parent = pivot_node.parent
        if pivot_node.parent is None:
            # If rotation at root, update root
            tree.root = successor_node
        elif pivot_node == pivot_node.parent.right:
            # If rotation around right node of a parent, update parent's right pointer to successor
            pivot_node.parent.right = successor_node
        else:
            # If rotation around left node of a parent, update parent's left pointer to successor
            pivot_node.parent.left = successor_node

        # right rotate pivot node down to the left of successor
        successor_node.right = pivot_node
        # update pivot node parent pointer to successor node
        pivot_node.parent = successor_node

    @staticmethod
    # function to find replacement node and retain color
    def find_replacement_node_and_update_pointers(tree, successor_original_color, target_node):
        # deleted node has no left child, move to the right subtree up
        if target_node.left.is_null():
            replacement_node = target_node.right
            TreeHelper.swap_subtree(tree, target_node, target_node.right)

        # deleted node has no right child, just scoot the left subtree up
        elif target_node.right.is_null():
            replacement_node = target_node.left
            TreeHelper.swap_subtree(tree, target_node, target_node.left)

        # deleted node has wo children, find the successor
        else:
            # in this case find the minimum or left most node of right subtree
            successor_node = TreeHelper.minimum(target_node.right)
            successor_original_color = successor_node.color
            replacement_node = successor_node.right

            # update parent pointers if successor is right child of deleted
            if successor_node.parent == target_node:
                replacement_node.parent = successor_node
            else:
                # if the successor is deeper in the right subtree, update the parent's left pointer
                TreeHelper.swap_subtree(tree, successor_node, successor_node.right)
                successor_node.right = target_node.right
                successor_node.right.parent = successor_node

            TreeHelper.swap_subtree(tree, target_node, successor_node)

            # update left child of successor
            successor_node.left = target_node.left
            successor_node.left.parent = successor_node

            # preserve color of target node in successor
            TreeHelper.set_color(tree, successor_node, target_node.color)
        return replacement_node, successor_original_color

    # function to balance the tree after deletion
    @staticmethod
    def balance_after_delete(tree, tree_node):
        # check current node is not the root and is black
        while tree_node != tree.root and tree_node.is_black():
            # check if node is right child of its parent
            if tree_node == tree_node.parent.right:
                tree_node = TreeHelper.handle_node_black_and_left_sibling(tree, tree_node)
            else:  # node is right child of its parent
                tree_node = TreeHelper.handle_node_black_and_right_sibling(tree, tree_node)
        # set final node color to black
        TreeHelper.set_color(tree, tree_node, Color.BLACK)

    # function to perform rotation and recolor in delete case when deleted node is black and a left child
    @staticmethod
    def handle_node_black_and_right_sibling(tree, tree_node):
        # get right child sibling if node is the left child
        sibling = tree_node.parent.right
        if sibling.is_red():
            # sibling is red perform left rotation and update colors
            TreeHelper.set_color(tree, sibling, Color.BLACK)
            TreeHelper.set_color(tree, sibling.parent, Color.RED)
            TreeHelper.left_rotation(tree, tree_node.parent)
            sibling = tree_node.parent.right

        # both children of sibling are black, update colors and move up the tree
        if sibling.left.is_black() and sibling.right.is_black():
            TreeHelper.set_color(tree, sibling, Color.RED)
            tree_node = tree_node.parent
        else:
            # left child of sibling is black, perform right rotation and update colors
            if sibling.right.is_black():  # right child of sibling is black
                TreeHelper.set_color(tree, sibling.left, Color.BLACK)
                TreeHelper.set_color(tree, sibling, Color.RED)
                TreeHelper.right_rotation(tree, sibling)
                sibling = tree_node.parent.right
            # update colors and perform left rotation to balance the tree
            TreeHelper.set_color(tree, sibling, tree_node.parent.color)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, sibling.right, Color.BLACK)
            TreeHelper.left_rotation(tree, tree_node.parent)
            tree_node = tree.root
        return tree_node

    # function to perform rotation and recolor in delete case when deleted node is black and a right child
    @staticmethod
    def handle_node_black_and_left_sibling(tree, tree_node):
        # get left child sibling if node is right child
        sibling = tree_node.parent.left
        # sibling is red perform right rotation and update colors
        if sibling.is_red():
            TreeHelper.set_color(tree, sibling, Color.BLACK)
            TreeHelper.set_color(tree, tree_node.parent, Color.RED)
            TreeHelper.right_rotation(tree, tree_node.parent)
            sibling = tree_node.parent.left
        # both children of sibling are black, update colors and move up the tree
        if sibling.left.is_black() and sibling.right.is_black():
            TreeHelper.set_color(tree, sibling, Color.RED)
            tree_node = tree_node.parent
        else:
            # right child of sibling is black, perform left rotation and update colors
            if sibling.left.is_black():
                TreeHelper.set_color(tree, sibling.right, Color.BLACK)
                TreeHelper.set_color(tree, sibling, Color.RED)
                TreeHelper.left_rotation(tree, sibling)
                sibling = tree_node.parent.left
            # update colors and perform right rotation to balance the tree
            TreeHelper.set_color(tree, sibling, tree_node.parent.color)
            TreeHelper.set_color(tree, tree_node.parent, Color.BLACK)
            TreeHelper.set_color(tree, sibling.left, Color.BLACK)
            TreeHelper.right_rotation(tree, tree_node.parent)
            tree_node = tree.root
        return tree_node

    # Function to swap & replace subtrees for adjusting parent child relationship
    @staticmethod
    def swap_subtree(tree, old_root, new_root):
        if old_root.parent is None:
            # if old subtree is root of the tree, transplant new subtree root to root
            tree.root = new_root
        elif old_root == old_root.parent.left:
            # if old subtree is left child of parent, transplant new subtree root to parent's left replacing old root
            old_root.parent.left = new_root
        else:
            # if old subtree is right child of parent, transplant new subtree root to parent's right replacing old root
            old_root.parent.right = new_root
        # update parent pointer of new subtree to old subtree's parent
        new_root.parent = old_root.parent

    # Function to return book with the smallest book id in the subtree rooted at node
    @staticmethod
    def minimum(tree_node):
        return TreeHelper.minimum(tree_node.left) if not tree_node.left.is_null() else tree_node

    # function to determine which one is closer if both closest_lower and closest_higher exist
    @staticmethod
    def determine_closest_node(book_id, closest_higher, closest_lower, result):
        if closest_lower is not None and closest_higher is not None:
            distance_lower = abs(int(book_id) - int(closest_lower.book_id))
            distance_higher = abs(int(book_id) - int(closest_higher.book_id))
            # add both books if difference between ids is same
            if distance_lower == distance_higher:
                result.append(closest_lower)
                result.append(closest_higher)
            else:
                # add book which is closer
                closer_node = closest_lower if distance_lower < distance_higher else closest_higher
                result.append(closer_node)
        else:
            # append closest_lower and closest_higher to the result
            if closest_lower is not None:
                result.append(closest_lower)
            if closest_higher is not None:
                result.append(closest_higher)
        return result
