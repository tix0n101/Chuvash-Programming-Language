from lexer import TokenType

class ProgramNode:
    def __init__(self, statements): self.statements = statements
class VarDeclNode:
    def __init__(self, name, expr): self.name, self.expr = name, expr
class AssignNode:
    def __init__(self, name, expr): self.name, self.expr = name, expr
class PrintNode:
    def __init__(self, expr): self.expr = expr
class IfNode:
    def __init__(self, cond, then_b, else_b): self.cond, self.then_b, self.else_b = cond, then_b, else_b
class WhileNode:
    def __init__(self, cond, body): self.cond, self.body = cond, body
class BinaryOpNode:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class LiteralNode:
    def __init__(self, value): self.value = value
class VarRefNode:
    def __init__(self, name): self.name = name
class BlockNode:
    def __init__(self, statements): self.statements = statements

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def cur(self): return self.tokens[self.pos]

    def consume(self, ttype):
        tok = self.cur()
        if tok.type == ttype:
            self.pos += 1
            return tok
        raise SyntaxError(f"Йăнăш: Кĕтнĕ {ttype}, анчах тупнă {tok.type} ('{tok.value}') йĕр {tok.line}")

    def parse(self):
        stmts = []
        while self.cur().type != TokenType.EOF:
            stmts.append(self.parse_statement())
        return ProgramNode(stmts)

    def parse_statement(self):
        tok = self.cur()
        if tok.type == TokenType.ULSHANAKAN:
            self.consume(TokenType.ULSHANAKAN)
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            expr = self.parse_expr()
            self.consume(TokenType.SEMICOLON)
            return VarDeclNode(name, expr)
        elif tok.type == TokenType.KALAR:
            self.consume(TokenType.KALAR)
            self.consume(TokenType.LPAREN)
            expr = self.parse_expr()
            self.consume(TokenType.RPAREN)
            self.consume(TokenType.SEMICOLON)
            return PrintNode(expr)
        elif tok.type == TokenType.EGER:
            self.consume(TokenType.EGER)
            cond = self.parse_expr()
            self.consume(TokenType.PULSAN)
            then_b = self.parse_block()
            else_b = None
            if self.cur().type == TokenType.URAH:
                self.consume(TokenType.URAH)
                else_b = self.parse_block()
            return IfNode(cond, then_b, else_b)
        elif tok.type == TokenType.SEHET:
            self.consume(TokenType.SEHET)
            cond = self.parse_expr()
            self.consume(TokenType.PULSAN)
            body = self.parse_block()
            return WhileNode(cond, body)
        elif tok.type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            expr = self.parse_expr()
            self.consume(TokenType.SEMICOLON)
            return AssignNode(name, expr)
        else:
            raise SyntaxError(f"Паллă мар оператор: '{tok.value}' (йĕр {tok.line})")

    def parse_block(self):
        self.consume(TokenType.LBRACE)
        stmts = []
        while self.cur().type != TokenType.RBRACE and self.cur().type != TokenType.EOF:
            stmts.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return BlockNode(stmts)

    def parse_expr(self):
        return self.parse_equality()

    def parse_equality(self):
        node = self.parse_relational()
        while self.cur().type in (TokenType.EQ, TokenType.NEQ):
            op = self.consume(self.cur().type).value
            node = BinaryOpNode(node, op, self.parse_relational())
        return node

    def parse_relational(self):
        node = self.parse_additive()
        while self.cur().type in (TokenType.LT, TokenType.GT):
            op = self.consume(self.cur().type).value
            node = BinaryOpNode(node, op, self.parse_additive())
        return node

    def parse_additive(self):
        node = self.parse_term()
        while self.cur().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.cur().type).value
            node = BinaryOpNode(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.cur().type in (TokenType.MUL, TokenType.DIV):
            op = self.consume(self.cur().type).value
            node = BinaryOpNode(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        tok = self.cur()
        if tok.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return LiteralNode(tok.value)
        elif tok.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            return LiteralNode(tok.value)
        elif tok.type == TokenType.IDENTIFIER:
            self.consume(TokenType.IDENTIFIER)
            return VarRefNode(tok.value)
        elif tok.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.parse_expr()
            self.consume(TokenType.RPAREN)
            return node
        raise SyntaxError(f"Выраженире йăнăш: '{tok.value}' (йĕр {tok.line})")