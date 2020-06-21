from lexer.Tokens import *
from parser_and_ast.SyntaxTree import *

#########
# PARSER
#########

class Parser:
    def __init__(self, _tokens):
        self.tokens = _tokens
        self.idx = -1
        self.analyze_tokens()

    def parse(self):
        return self.analyze_expr()

    def analyze_tokens(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_tok = self.tokens[self.idx]

        return self.current_tok

    def analyze_factor(self):
        tok = self.current_tok

        if tok.type in (T_INT, T_FLOAT):
            self.analyze_tokens()

            return NumberNode(tok)

    def analyze_term(self):
       return self.analyze_op(self.analyze_factor, (T_MUL, T_DIV))

    def analyze_expr(self):
        return self.analyze_op(self.analyze_term, (T_PLUS, T_MINUS))

    def analyze_op(self, fun, ops): # for expr and term
        left = fun()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.analyze_tokens()
            right = fun()

            left = OperatorNode(left, op_tok, right)

        return left
