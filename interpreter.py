class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Паллă мар улшăнакан: '{name}'")

    def set(self, name, val):
        self.vars[name] = val

    def assign(self, name, val):
        if name in self.vars:
            self.vars[name] = val
            return
        if self.parent:
            self.parent.assign(name, val)
            return
        raise NameError(f"Паллă мар улшăнакан: '{name}'")

class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def interpret(self, program):
        for stmt in program.statements:
            self.eval_stmt(stmt, self.global_env)

    def eval_stmt(self, stmt, env):
        from parser_ast import (VarDeclNode, AssignNode, PrintNode, IfNode, WhileNode, BlockNode)
        
        if isinstance(stmt, VarDeclNode):
            val = self.eval_expr(stmt.expr, env)
            env.set(stmt.name, val)
        elif isinstance(stmt, AssignNode):
            val = self.eval_expr(stmt.expr, env)
            env.assign(stmt.name, val)
        elif isinstance(stmt, PrintNode):
            val = self.eval_expr(stmt.expr, env)
            print(val)
        elif isinstance(stmt, IfNode):
            cond = self.eval_expr(stmt.cond, env)
            if cond:
                self.eval_block(stmt.then_b, env)
            elif stmt.else_b:
                self.eval_block(stmt.else_b, env)
        elif isinstance(stmt, WhileNode):
            while self.eval_expr(stmt.cond, env):
                self.eval_block(stmt.body, env)

    def eval_block(self, block, parent_env):
        env = Environment(parent_env)
        for stmt in block.statements:
            self.eval_stmt(stmt, env)

    def eval_expr(self, expr, env):
        from parser_ast import LiteralNode, VarRefNode, BinaryOpNode
        if isinstance(expr, LiteralNode):
            return expr.value
        elif isinstance(expr, VarRefNode):
            return env.get(expr.name)
        elif isinstance(expr, BinaryOpNode):
            left = self.eval_expr(expr.left, env)
            right = self.eval_expr(expr.right, env)
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a // b,
                '==': lambda a, b: 1 if a == b else 0,
                '!=': lambda a, b: 1 if a != b else 0,
                '<': lambda a, b: 1 if a < b else 0,
                '>': lambda a, b: 1 if a > b else 0,
            }
            if expr.op in ops:
                return ops[expr.op](left, right)
        return None