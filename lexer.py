from enum import Enum, auto

class TokenType(Enum):
    ULSHANAKAN = auto() # улшăнакан (переменная)
    KALAR = auto()      # кăлар (печать)
    EGER = auto()       # эгер (если)
    PULSAN = auto()     # пулсан (то)
    URAH = auto()       # урăх (иначе)
    SEHET = auto()      # сехет (пока)

    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    ASSIGN = auto()     # =
    PLUS = auto()       # +
    MINUS = auto()      # -
    MUL = auto()        # *
    DIV = auto()        # /
    EQ = auto()         # ==
    NEQ = auto()        # !=
    LT = auto()         # <
    GT = auto()         # >
    
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    SEMICOLON = auto()  # ;
    EOF = auto()

KEYWORDS = {
    "улшăнакан": TokenType.ULSHANAKAN,
    "кăлар": TokenType.KALAR,
    "эгер": TokenType.EGER,
    "пулсан": TokenType.PULSAN,
    "урăх": TokenType.URAH,
    "сехет": TokenType.SEHET,
}

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.source[self.pos]

            if char in ' \t\r':
                self.pos += 1
                continue
            if char == '\n':
                self.line += 1
                self.pos += 1
                continue

            if char.isdigit():
                val = ""
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    val += self.source[self.pos]
                    self.pos += 1
                tokens.append(Token(TokenType.NUMBER, int(val), self.line))
                continue

            if char in ('"', "'"):
                quote = char
                self.pos += 1
                start = self.pos
                while self.pos < len(self.source) and self.source[self.pos] != quote:
                    self.pos += 1
                val = self.source[start:self.pos]
                self.pos += 1
                tokens.append(Token(TokenType.STRING, val, self.line))
                continue

            if char.isalpha() or char in 'ăĕçÿĂĔÇŸ_':
                ident = ""
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] in 'ăĕçÿĂĔÇŸ_'):
                    ident += self.source[self.pos]
                    self.pos += 1
                ttype = KEYWORDS.get(ident.lower(), TokenType.IDENTIFIER)
                tokens.append(Token(ttype, ident, self.line))
                continue

            if char == '=':
                if self.peek() == '=':
                    self.pos += 2
                    tokens.append(Token(TokenType.EQ, "==", self.line))
                else:
                    self.pos += 1
                    tokens.append(Token(TokenType.ASSIGN, "=", self.line))
                continue

            if char == '!':
                if self.peek() == '=':
                    self.pos += 2
                    tokens.append(Token(TokenType.NEQ, "!=", self.line))
                else:
                    raise SyntaxError(f"Йăнăш: '!' символ хыçĕнчен '=' кĕтetçĕ (йĕр {self.line})")
                continue

            symbols = {'+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MUL, '/': TokenType.DIV,
                       '<': TokenType.LT, '>': TokenType.GT, '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                       '{': TokenType.LBRACE, '}': TokenType.RBRACE, ';': TokenType.SEMICOLON}
            
            if char in symbols:
                tokens.append(Token(symbols[char], char, self.line))
                self.pos += 1
                continue

            raise SyntaxError(f"Пĕлмен символ: '{char}' (йĕр {self.line})")

        tokens.append(Token(TokenType.EOF, "", self.line))
        return tokens

    def peek(self):
        return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else ''