import unittest
from binary_search_tree import Test
from binary_search_tree import BinarySearchTree
from binary_search_tree import BinarySearchNode
from binary_search_tree import sample_code


class BinarySearchTree(BinarySearchTree):
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root:
            self.root.insert(value)
        else:
            self.root = BinarySearchNode(value, None)


class BinarySearchNode(BinarySearchNode):
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    #
    # insert
    #
    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BinarySearchNode(value, self)
        elif value >= self.value:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BinarySearchNode(value, self)

    #
    # delete
    #
    def delete_left(self, value):
        if value < self.value:
            if self.left:
                self.left = self.left.delete_left(value)
            else:
                raise ValueError
        elif value > self.value:
            if self.right:
                self.right = self.right.delete_left(value)
            else:
                raise ValueError
        elif value == self.value:
            old_self = self
            if old_self.left:
                # 1. cut left_max.
                left_max = old_self.left.search_max()
                if left_max.left:
                    left_max.left.parent = left_max.parent

                # 2. insert left_max into root.
                self = left_max
                self.left = old_self.left.delete_max()
                if self.left:
                    self.left.parent = self
                self.right = old_self.right
                if self.right:
                    self.right.parent = self
                self.parent = old_self.parent
                # if self.parent:
                #     ...
            else:
                # 1. cut left_max.
                # 2. insert left_max into root.
                self = old_self.right
                if self:
                    self.parent = old_self.parent

            # 3. delete old_self
            old_self.parent = None
            old_self.left = None
            old_self.right = None
        return self

    def delete_right(self, value):
        if value < self.value:
            if self.left:
                self.left = self.left.delete_right(value)
            else:
                raise ValueError
        elif value > self.value:
            if self.right:
                self.right = self.right.delete_right(value)
            else:
                raise ValueError
        elif value == self.value:
            old_self = self
            if old_self.right:
                # 1. cut right_min.
                right_min = old_self.right.search_min()
                if right_min.right:
                    right_min.right.parent = right_min.parent

                # 2. insert right_min into root.
                self = right_min
                self.left = old_self.left
                if self.left:
                    self.left.parent = self
                self.right = old_self.right.delete_min()
                if self.right:
                    self.right.parent = self
                self.parent = old_self.parent
                # if self.parent:
                #     ...

            else:
                # 1. cut right_min.
                # 2. insert right_min into root.
                self = old_self.left
                if self:
                    self.parent = old_self.parent

            # 3. delete old root.
            old_self.parent = None
            old_self.left = None
            old_self.right = None
        return self


class Path(object):
    def __init__(self, root):
        self._current_node = root

    def __next__(self):
        if self._current_node.right:
            self._seek_right_min()
        else:
            self._seek_right_parent()
        return self._current_node.value

    def _seek_right_min(self):
        self._current_node = self._current_node.right
        while self._current_node.left:
            self._current_node = self._current_node.left

    def _seek_right_parent(self):
        try:
            self._current_node = self._current_node.parent
            while self._current_node is self._current_node._parent.righ:
                self._current_node = self._current_node.parent
        except AttributeError:
            raise StopIteration

    def __iter__(self):
        return self


if __name__ == '__main__':
    sample_code()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
