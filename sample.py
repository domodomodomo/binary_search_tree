import log
from binary_search_tree import BinarySearchTree
# from binary_search_tree_parent import BinarySearchTree


bst = BinarySearchTree()

#
# 1. insert
#
print('### 1. insert')
bst.insert(8)
bst.insert(3)
bst.insert(1)
bst.insert(6)
bst.insert(10)
bst.insert(4)
bst.insert(7)
bst.insert(14)
bst.insert(13)
print(log.output(bst))
print()
"""
              08
      03              10
  01      06              14
        04  07          13
"""

#
# 2. search
#
print('### 2. search')
print(bst.search(13).value)
print()
"""
13
"""

#
# 3. list
#
print('### 3. list')
print(bst.list())
print(bst.list_sequentially())
print()
"""
[1, 3, 4, 6, 7, 8, 10, 13, 14]
"""

#
# 4. delete
#
print('### 4. delete')
bst.delete_right(8)
print(log.output(bst))
print()
"""
              10
      03              14
  01      06      13
        04  07
"""

bst.delete_left(10)
print(log.output(bst))
print()
"""
              07
      03              14
  01      06      13
        04
"""
