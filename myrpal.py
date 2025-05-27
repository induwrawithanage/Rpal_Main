# Description: Main entry point for the RPAL interpreter. 
# This script processes command-line arguments and executes the program based on provided switches.
# Usage: Run in terminal with format: python ./myrpal.py [-l] [-ast] [-st] filename
# -l: Print the source file content
# -ast: Print the abstract syntax tree
# -st: Print the standardized tree
# Note: This file cannot be run directly in an IDE; use the terminal with appropriate arguments.

from Parser import parse
from TreeNode import preorderTraversal
from Standardizer import *
from CSEMachine import *
import sys

def processArg(arguments):
    """Process command-line arguments and execute corresponding actions."""
    # Check if minimum required arguments are provided
    if len(arguments) < 2:
        print("Error: Insufficient arguments. Usage: python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)

    file_name = arguments[-1]  # Last argument is always the filename
    switches = arguments[1:-1] if len(arguments) > 2 else []  # Get switches if present

    # If no switches provided, execute the program directly
    if not switches:
        Result(file_name)
        return

    # Define switch handlers
    switch_handlers = {
        '-l': lambda: printContent(file_name),
        '-ast': lambda: printAST(file_name),
        '-st': lambda: printST(file_name)
    }

    # Validate switches
    valid_switches = {'-l', '-ast', '-st'}
    if not all(switch in valid_switches for switch in switches):
        print("Error: Invalid switch. Usage: python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)

    # Process each switch in order
    for switch in switches:
        if switch == '-ast' and '-st' in switches:
            # Special case: -ast and -st together, show both AST and standardized tree
            ast = parse(file_name)
            preorderTraversal(ast)
            print()
            st = genarateST(ast)
            preorderTraversal(st)
            print()
            sys.exit(0)
        else:
            # Execute individual switch handler
            switch_handlers[switch]()
            print()

def printContent(file_name):
    """Print the contents of the input file."""
    try:
        with open(file_name, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found")
        sys.exit(1)

def printAST(file_name):
    """Print the abstract syntax tree of the input file."""
    try:
        ast = parse(file_name)
        preorderTraversal(ast)
    except Exception as e:
        print(f"Error parsing file '{file_name}': {str(e)}")
        sys.exit(1)

def printST(file_name):
    """Print the standardized tree of the input file."""
    try:
        st = getST(file_name)
        preorderTraversal(st)
        sys.exit(0)
    except Exception as e:
        print(f"Error standardizing file '{file_name}': {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    processArg(sys.argv)