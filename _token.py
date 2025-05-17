class Token:
    def __init__(self, content, type, line):
        self.content = content
        self.type = type
        self.line = line
        self.is_first = False
        self.is_last = False

    # This function is used to mark the token as a keyword.
    # This is used in the screener.    
    def make_keyword(self):
        self.type = "<KEYWORD>" 
        
    def make_first_token(self):
        self.is_first = True
        
    # This function is used to mark the token as the last token.
    # Marking the last token is important for the parsing process.    
    def make_last_token(self):
        self.is_last = True
        
   