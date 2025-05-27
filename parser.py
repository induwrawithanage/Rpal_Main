from lexical_analyzer import screen
from structures import Stack
from TreeNode import *

stack = Stack("AST")

def parse(input_file):
    global tokens
    tokens, has_invalid, invalid_token = screen(input_file)
    # If there are invalid tokens, parsing cannot proceed.
    match has_invalid:
        case True:
            print("Invalid token present")
            exit(1)
        case False:
            E()
            match stack.is_empty():
                case False:
                    root = stack.pop()
                case True:
                    print("Stack is empty")
                    exit(1)
            return root

# This function builds the abstract syntax tree.
def constructAST(node_value, child_count):
    ast_node = TreeNode(node_value)
    ast_node.childList = [None] * child_count
    
    index = 0
    while index < child_count:
        match stack.is_empty():
            case True:
                print("Stack is empty")
                exit(1)
            case False:
                ast_node.childList[child_count - index - 1] = stack.pop()
        index += 1
        
    stack.push(ast_node)


# This function checks and processes the expected token.
def consumeToken(expected_value):
    match tokens[0].content == expected_value:
        case False:
            print("Syntax error")
            exit(1)
        case True:
            match tokens[0].is_last_token:
                case False:
                    del tokens[0]
                case True:
                    match tokens[0].type == ")":
                        case False:
                            tokens[0].type = ")"
                        case True:
                            pass

# This function prints the abstract syntax tree in preorder traversal.
def printAST(tree_root):
    preorderTraversal(tree_root)



############################################################## 
def E():
    switch_token = tokens[0].content
    match switch_token:
        case "let":
            consumeToken("let")
            D()
            if tokens[0].content == "in":
                consumeToken("in")
                E()
                constructAST("let", 2)
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": 'in' expected")
                exit(1)
        case "fn":
            consumeToken("fn")
            n = 0
            for _ in iter(lambda: tokens[0].type in ["<IDENTIFIER>", "("], False):
                Vb()
                n += 1
            if n == 0:
                print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
                exit(1)
            if tokens[0].content == ".":
                consumeToken(".")
                E()
                constructAST("lambda", n + 1)
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": '.' expected")
                exit(1)
        case _:
            Ew()

### --------------------------------------------------------------
def Ew():
    T()    
    match tokens[0].content:
        case "where":
            consumeToken("where")
            Dr()
            constructAST("where", 2)
        case _:
            pass

### --------------------------------------------------------------
def T():
    Ta()
    n = 0
    for _ in iter(lambda: tokens[0].content == ",", False):
        consumeToken(",")
        Ta()
        n += 1
    if n > 0:
        constructAST("tau", n + 1)

### --------------------------------------------------------------      
def Ta():
    Tc()
    for _ in iter(lambda: tokens[0].content == "aug", False):
        consumeToken("aug")
        Tc()
        constructAST("aug", 2)

### --------------------------------------------------------------
def Tc():
    B()
    match tokens[0].content:
        case "->":
            consumeToken("->")
            Tc()
            if tokens[0].content == "|":
                consumeToken("|")
                Tc()
                constructAST("->", 3)
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": '|' expected")
                exit(1)
        case _:
            pass

### --------------------------------------------------------------
def B():
    Bt()
    for _ in iter(lambda: tokens[0].content == "or", False):
        consumeToken("or")
        Bt()
        constructAST("or", 2)

### --------------------------------------------------------------
def Bt():
    Bs()
    for _ in iter(lambda: tokens[0].content == "&", False):
        consumeToken("&")
        Bs()
        constructAST("&", 2)

### --------------------------------------------------------------
def Bs():
    match tokens[0].content:
        case "not":
            consumeToken("not")
            Bp()
            constructAST("not", 1)
        case _:
            Bp()

### --------------------------------------------------------------
def Bp():
    A()
    match tokens[0].content:
        case "gr" | ">":
            consumeToken(tokens[0].content)
            A()
            constructAST("gr", 2)
        case "ge" | ">=":
            consumeToken(tokens[0].content)
            A()
            constructAST("ge", 2)
        case "ls" | "<":
            consumeToken(tokens[0].content)
            A()
            constructAST("ls", 2)
        case "le" | "<=":
            consumeToken(tokens[0].content)
            A()
            constructAST("le", 2)
        case "eq":
            consumeToken(tokens[0].content)
            A()
            constructAST("eq", 2)
        case "ne":
            consumeToken(tokens[0].content)
            A()
            constructAST("ne", 2)
        case _:
            pass

### --------------------------------------------------------------
def A():
    match tokens[0].content:
        case "+":
            consumeToken("+")
            At()
        case "-":
            consumeToken("-")
            At()
            constructAST("neg", 1)
        case _:
            At()
    for _ in iter(lambda: tokens[0].content in ["+", "-"], False):
        match tokens[0].content:
            case "+":
                consumeToken("+")
                At()
                constructAST("+", 2)
            case "-":
                consumeToken("-")
                At()
                constructAST("-", 2)

### --------------------------------------------------------------
def At():
    Af()
    for _ in iter(lambda: tokens[0].content in ["*", "/"], False):
        match tokens[0].content:
            case "*":
                consumeToken("*")
                Af()
                constructAST("*", 2)
            case "/":
                consumeToken("/")
                Af()
                constructAST("/", 2)

#### --------------------------------------------------------------
def Af():
    Ap()
    match tokens[0].content:
        case "**":
            consumeToken("**")
            Af()
            constructAST("**", 2)
        case _:
            pass

### --------------------------------------------------------------    
def Ap():
    R()
    for _ in iter(lambda: tokens[0].content == "@", False):
        consumeToken("@")
        if tokens[0].type == "<IDENTIFIER>":
            constructAST("<ID:" + tokens[0].content + ">", 0)
            consumeToken(tokens[0].content)
            R()
            constructAST("@", 3)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier expected")
            exit(1)

### --------------------------------------------------------------
def R():
    Rn()
    for _ in iter(lambda: tokens[0].type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false", "nil", "(", "dummy"], False):
        Rn()
        constructAST("gamma", 2)

### --------------------------------------------------------------
def Rn():
    value = tokens[0].content
    match tokens[0].type:
        case "<IDENTIFIER>":
            consumeToken(value)
            constructAST("<ID:" + value + ">", 0)
        case "<INTEGER>":
            consumeToken(value)
            constructAST("<INT:" + value + ">", 0)
        case "<STRING>":
            consumeToken(value)
            constructAST("<STR:" + value + ">", 0)
        case _:
            match value:
                case "true" | "false" | "nil" | "dummy":
                    consumeToken(value)
                    constructAST("<" + value + ">", 0)
                case "(":
                    consumeToken("(")
                    E()
                    if tokens[0].content == ")":
                        consumeToken(")")
                    else:
                        print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
                        exit(1)
                case _:
                    print("Syntax error in line " + str(tokens[0].line) + ": Identifier, Integer, String, 'true', 'false', 'nil', 'dummy' or '(' expected")
                    exit(1)

### --------------------------------------------------------------
def D():
    Da()
    match tokens[0].content:
        case "within":
            consumeToken("within")
            D()
            constructAST("within", 2)
        case _:
            pass

### --------------------------------------------------------------
def Da():
    Dr()
    n = 0
    for _ in iter(lambda: tokens[0].content == "and", False):
        consumeToken("and")
        Dr()
        n += 1
    if n > 0:
        constructAST("and", n + 1)

### --------------------------------------------------------------
def Dr():
    match tokens[0].content:
        case "rec":
            consumeToken("rec")
            Db()
            constructAST("rec", 1)
        case _:
            Db()

### --------------------------------------------------------------
def Db():
    value = tokens[0].content
    match value:
        case "(":
            consumeToken("(")
            D()
            if tokens[0].content == ")":
                consumeToken(")")
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
                exit(1)
        case _ if tokens[0].type == "<IDENTIFIER>":
            consumeToken(value)
            constructAST("<ID:" + value + ">", 0)
            if tokens[0].content in [",", "="]:
                Vl()
                consumeToken("=")
                E()
                constructAST("=", 2)
            else:
                n = 0
                for _ in iter(lambda: tokens[0].type in ["<IDENTIFIER>", "("], False):
                    Vb()
                    n += 1
                if n == 0:
                    print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
                    exit(1)
                if tokens[0].content == "=":
                    consumeToken("=")
                    E()
                    constructAST("function_form", n + 2)
                else:
                    print("Syntax error in line " + str(tokens[0].line) + ": '=' expected")
                    exit(1)
        case _:
            print("Syntax error in line " + str(tokens[0].line) + ": '(' or Identifier expected")
            exit(1)

### --------------------------------------------------------------
def Vb():
    value_1 = tokens[0].content
    match tokens[0].type:
        case "<IDENTIFIER>":
            consumeToken(value_1)
            constructAST("<ID:" + value_1 + ">", 0)
        case _ if value_1 == "(":
            consumeToken("(")
            value_2 = tokens[0].content
            match value_2:
                case ")":
                    consumeToken(")")
                    constructAST("()", 0)
                case _ if tokens[0].type == "<IDENTIFIER>":
                    consumeToken(value_2)
                    constructAST("<ID:" + value_2 + ">", 0)
                    Vl()
                    if tokens[0].content == ")":
                        consumeToken(")")
                    else:
                        print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
                        exit(1)
                case _:
                    print("Syntax error in line " + str(tokens[0].line) + ": Identifier or ')' expected")
                    exit(1)
        case _:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
            exit(1)

###     --------------------------------------------------------------
def Vl():
    n = 0
    for _ in iter(lambda: tokens[0].content == ",", False):
        consumeToken(",")
        if tokens[0].type == "<IDENTIFIER>":
            value = tokens[0].content
            consumeToken(value)
            constructAST("<ID:" + value + ">", 0)
            n += 1
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier expected")
            exit(1)
    if n > 0:
        constructAST(",", n + 1)

