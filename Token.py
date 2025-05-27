class Token:
    def __init__(self, content, type):
        self.content = content
        self.type = type
        self.line = 0
        self.is_first_token = False
        self.is_last_token = False

    # Add a line number to the token.
    def addLine(self, line):
        self.line = line

    # This is used to mark the token as the last token.    
    def genarateLastToken(self):
        self.is_last_token = True

    # This is used to mark the token as the first token.
    def genarateFastToken(self):
        self.is_first_token = True
        
    # This is used to mark the token as a keyword.  
    def makeKeyword(self):
        self.type = "<KEYWORD>"