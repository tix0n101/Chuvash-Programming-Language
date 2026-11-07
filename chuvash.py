#!/usr/bin/env python3
import sys
import os

# Добавляем текущую директорию в путь импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser_ast import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Улшăну: chuvash <файл.cht>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Йăнăш: '{filepath}' файл тупăнмарĕ.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(ast)

    except Exception as e:
        print(f"Пĕтĕрÿ йăнăшĕ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()