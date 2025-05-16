class Tree_Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.level = 0

def preorder_traversal(node):
    if node is None:
        return
    print("." * node.level + str(node.value))
    for child in node.children:
        child.level = node.level + 1
        preorder_traversal(child)