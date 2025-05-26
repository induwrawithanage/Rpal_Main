class TreeNode:
    def __init__(self, value):
        self.value = value
        self.depth = 0
        self.childList = []  
  
def preorderTraversal(root):
    if root is None:
        return
    mySta = [(root, 0)]  # (node, depth)
    while mySta:
        node, depth = mySta.pop()
        print("." * depth + node.value)
        # Push children in reverse order so left-most child is processed first
        for child in reversed(node.childList):
            mySta.append((child, depth + 1))
