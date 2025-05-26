class Stack:
    def __init__(self, type):
        self.stack = []
        self.type = type      
    
    def __getitem__(self, index):
        return self.stack[index]
    
    def __setitem__(self, index, value):
        self.stack[index] = value
        
    def __reversed__(self):
        return reversed(self.stack)
    # The following function returns the size of the stack.
    def size(self):
        return len(self.stack)
    
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    # The following function lets you check whether the stack is empty.
    def is_empty(self):
        return len(self.stack) == 0