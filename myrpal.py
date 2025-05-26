from lexicalAnalyzer import tokenize
from lexicalAnalyzer import screen

#Check whether the input file exists and is readable
import os
with open('add', 'r') as file:
    input_file_path = file.name
    tokens = screen(input_file_path)
    for token in tokens:
        print(token)