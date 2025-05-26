import re
from Token import Token

def tokenize(characters):
    import re

    # If characters is a list of lines, convert it to a single string
    if isinstance(characters, list):
        characters = ''.join(characters)

    token_specification = [
        ('COMMENT',   r'//[^\n]*'),                        # Single-line comment
        ('STRING',    r"'([^'\n]*)'"),                     # String literal
        ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),          # Identifiers
        ('INTEGER',   r'\d+'),                             # Integer literal
        ('OPERATOR',  r'[:=<>~!@#%^&*\-+|/?$.\[\]{}]+'),    # Operators (multi-char supported)
        ('PUNCTUATION', r'[();,]'),                        # Punctuation
        ('NEWLINE',   r'\n'),                              # Line endings
        ('SKIP',      r'[ \t]+'),                          # Skip spaces and tabs
        ('MISMATCH',  r'.'),                               # Any other character (invalid)
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    line_number = 1
    tokens = []
    token_names = []
    line_numbers = []

    for mo in re.finditer(tok_regex, characters):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NEWLINE':
            line_number += 1
            tokens.append(value)
            token_names.append('<DELETE>')
            line_numbers.append(line_number - 1)
        elif kind == 'SKIP':
            tokens.append(value)
            token_names.append('<DELETE>')
            line_numbers.append(line_number)
        elif kind == 'COMMENT':
            tokens.append(value)
            token_names.append('<DELETE>')
            line_numbers.append(line_number)
        elif kind == 'IDENTIFIER':
            tokens.append(value)
            token_names.append('<IDENTIFIER>')
            line_numbers.append(line_number)
        elif kind == 'INTEGER':
            # Detect invalid integers like 123abc
            if re.match(r'\d+[a-zA-Z_]+', value):
                tokens.append(value)
                token_names.append('<INVALID>')
            else:
                tokens.append(value)
                token_names.append('<INTEGER>')
            line_numbers.append(line_number)
        elif kind == 'STRING':
            if value.count("'") == 2:
                tokens.append(value)
                token_names.append('<STRING>')
                line_numbers.append(line_number)
            else:
                print("String is not closed properly.")
                exit(1)
        elif kind == 'OPERATOR':
            tokens.append(value)
            token_names.append('<OPERATOR>')
            line_numbers.append(line_number)
        elif kind == 'PUNCTUATION':
            tokens.append(value)
            token_names.append(value)
            line_numbers.append(line_number)
        elif kind == 'MISMATCH':
            print(f"Invalid character: {value} at line {line_number}")
            exit(1)

    # Wrap tokens into Token objects
    number_of_tokens = len(tokens)

    for i in range(number_of_tokens):
        if i == 0:
            tokens[i] = Token(tokens[i], token_names[i])
            tokens[i].addLine(line_numbers[i])
            tokens[i].genarateFastToken()
        elif i == number_of_tokens - 1:
            if tokens[i] == '\n':
                tokens[i - 1].genarateLastToken()
                tokens.pop()
                token_names.pop()
                line_numbers.pop()
            else:
                tokens[i] = Token(tokens[i], token_names[i])
                tokens[i].addLine(line_numbers[i])
                tokens[i].genarateLastToken()
        else:
            tokens[i] = Token(tokens[i], token_names[i])
            tokens[i].addLine(line_numbers[i])

    return tokens


def screen(input_file_path):
    # List of reserved keywords in RPAL
    rpal_keywords = [
        "let", "in", "where", "rec", "fn", "aug", "or", "not",
        "gr", "ge", "ls", "le", "eq", "ne", "true", "false",
        "nil", "dummy", "within", "and"
    ]
    
    character_buffer = []
    scanned_tokens = []
    has_invalid_token = False
    first_invalid_token = None
    
    try:
        with open(input_file_path, 'r') as file:
            for line in file:
                for char in line:
                    character_buffer.append(char)
            scanned_tokens = tokenize(character_buffer)

    except Exception as error:
        print("An error occurred:", error)
        exit(1)
    
    # Traverse token list in reverse to handle deletions correctly
    for i in range(len(scanned_tokens) - 1, -1, -1):
        current_token = scanned_tokens[i]
        
        # Convert identifiers that match keywords into keyword tokens
        if current_token.type == "<IDENTIFIER>" and current_token.content in rpal_keywords:
            current_token.makeKeyword()
        
        # Remove unnecessary tokens like <DELETE> and newline characters
        if current_token.type == "<DELETE>" or current_token.content == "\n":            
            scanned_tokens.remove(current_token)
        
        # Capture the first invalid token found
        if current_token.type == "<INVALID>" and not has_invalid_token:
            first_invalid_token = current_token
            has_invalid_token = True
            
    # Ensure the last token is marked correctly
    if len(scanned_tokens) > 0:
        scanned_tokens[-1].is_last_token = True
        
    return scanned_tokens, has_invalid_token, first_invalid_token
