from TreeNode import *
from Parser import *

# The getST function takes a file name as input and returns a getSTd tree.
def getST(file_name):
    ast = parse(file_name)
    st = genarateST(ast)
    
    return st

# The genarateST function takes a root node as input and returns a getSTd tree.
def genarateST(root):
    i = 0
    while i < len(root.childList):
        genarateST(root.childList[i])
        i += 1


    match root.value:
        case "let" if root.childList[0].value == "=":
            child0 = root.childList[0]
            child1 = root.childList[1]

            root.childList[1] = child0.childList[1]
            root.childList[0].childList[1] = child1
            root.childList[0].value = "lambda"
            root.value = "gamma"

        case "where" if root.childList[1].value == "=":
            child0 = root.childList[0]
            child1 = root.childList[1]

            root.childList[0] = child1.childList[1]
            root.childList[1].childList[1] = child0
            root.childList[1].value = "lambda"
            root.childList[0], root.childList[1] = root.childList[1], root.childList[0]
            root.value = "gamma"

        case "function_form":
            expression = root.childList.pop()

            currentN = root
            for i in range(len(root.childList) - 1):
                lambdaN = TreeNode("lambda")
                child = root.childList.pop(1)
                lambdaN.childList.append(child)
                currentN.childList.append(lambdaN)
                currentN = lambdaN

            currentN.childList.append(expression)
            root.value = "="

        case "gamma" if len(root.childList) > 2:
            expression = root.childList.pop()

            currentN = root
            for i in range(len(root.childList) - 1):
                lambdaN = TreeNode("lambda")
                child = root.childList.pop(1)
                lambdaN.childList.append(child)
                currentN.childList.append(lambdaN)
                currentN = lambdaN

            currentN.childList.append(expression)

        case "within" if root.childList[0].value == root.childList[1].value == "=":
            child0 = root.childList[1].childList[0]
            child1 = TreeNode("gamma")

            child1.childList.append(TreeNode("lambda"))
            child1.childList.append(root.childList[0].childList[1])
            child1.childList[0].childList.append(root.childList[0].childList[0])
            child1.childList[0].childList.append(root.childList[1].childList[1])

            root.childList[0] = child0
            root.childList[1] = child1
            root.value = "="

        case "@":
            expression = root.childList.pop(0)
            identifier = root.childList[0]

            gammaN = TreeNode("gamma")
            gammaN.childList.append(identifier)
            gammaN.childList.append(expression)

            root.childList[0] = gammaN
            root.value = "gamma"

        case "and":
            child0 = TreeNode(",")
            child1 = TreeNode("tau")

            for child in root.childList:
                child0.childList.append(child.childList[0])
                child1.childList.append(child.childList[1])

            root.childList.clear()
            root.childList.append(child0)
            root.childList.append(child1)
            root.value = "="

        case "rec":
            temp = root.childList.pop()
            temp.value = "lambda"

            gammaN = TreeNode("gamma")
            gammaN.childList.append(TreeNode("<Y*>"))
            gammaN.childList.append(temp)

            root.childList.append(temp.childList[0])
            root.childList.append(gammaN)
            root.value = "="


    return root