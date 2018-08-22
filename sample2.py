import graph
import binary_search_tree

n = -1
bst = binary_search_tree.BinarySearchTree()
for i in 8, 3, 1, 6, 10, 4, 7, 14, 13:
    n += 1
    bst.insert(i)
    graph.render(bst, 3, 'img_%02d' % n)

n += 1
bst.delete_left(8)
graph.render(bst, 3, 'img_%02d' % n)

n += 1
bst.delete_right(7)
graph.render(bst, 3, 'img_%02d' % n)


n += 1
bst.delete_right(3)
graph.render(bst, 3, 'img_%02d' % n)
