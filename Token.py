class Token:
    def __init__(self, content, type, line):
        self.content = content
        self.type = type
        self.line = line
        self.is_first_token = False
        self.is_last_token = False
    
    # This is used to mark the token as the first token.
    def make_first_token(self):
        self.is_first_token = True
        
    # This is used to mark the token as the last token.    
    def make_last_token(self):
        self.is_last_token = True
        
    # This is used to mark the token as a keyword.  
    def make_keyword(self):
        self.type = "<KEYWORD>"