# RPAL Compiler (Python Implementation)

This project is an **RPAL (Right-reference Pedagogic Algorithmic Language) compiler** implemented in Python.  
It supports lexical analysis, parsing, Abstract Syntax Tree (AST) generation, Standardization (ST), and execution of RPAL programs.

---

## 📌 Features
- **Lexical Analysis**: Tokenizes the input RPAL source file.  
- **Parser**: Builds the syntax structure from tokens.  
- **AST Generation**: Produces the Abstract Syntax Tree for the program.  
- **Standardization (ST)**: Converts the AST into a standardized form.  
- **Execution**: Runs RPAL programs and prints the evaluated results.  

---

## 🛠️ Prerequisites
- Python 3.11 or above
- A text editor **VS Code** (optional)

---

## 🚀 Usage

Navigate to the project folder in your terminal before running commands.

### 1. Print the lexical analysis (tokens)
```bash
python myrpal.py -l file_name
```
### 2.Run the program and print result
```bash
python myrpal.py test_cases/add   
```
### 3. Print the Abstract Syntax Tree (AST)
```bash
python myrpal.py -ast test_cases/add
```
### 4. Print the Standardized Tree (ST)
```bash
python myrpal.py -st test_cases/add  


