from lexer.Tokens import *
from parser_and_ast.SyntaxTree import *
from parser_and_ast.ParseResult import ParseResult


#########
# PARSER
#########


class Parser:
    def __init__(self, _tokens):
        self.tokens = _tokens
        self.idx = -1
        self.next_token()

    def parse(self):
        result = self.analyze_expr()
        if not result.error and self.current_tok.type != T_EOF:
            return result.failure("Syntax error")

        return result

    def next_token(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_tok = self.tokens[self.idx]

        return self.current_tok

    def analyze_factor(self):
        result = ParseResult()

        tok = self.current_tok

        # Check if PLUS | MINUS is in the beginning
        if tok.type in (T_PLUS, T_MINUS):
            result.register(self.next_token())

            factor = result.register(self.analyze_factor())
            if result.error: return result

            return result.success(UnaryNode(tok, factor))

        # Check what type of variable is being considered  token
        elif tok.type in (T_INT, T_FLOAT):
            result.register(self.next_token())

            return result.success(NumberNode(tok))

        elif tok.type == T_LPAREN:
            result.register(self.next_token())
            expr = result.register(self.analyze_expr())
            if result.error: return result

            if self.current_tok.type == T_RPAREN:
                result.register(self.next_token())
                return result.success(expr)
            else:
                return result.failure("error")

        return result.failure("error")

    def analyze_term(self):
       return self.analyze_op(self.analyze_factor, (T_MUL, T_DIV))

    def analyze_expr(self):
        return self.analyze_op(self.analyze_term, (T_PLUS, T_MINUS))

    def analyze_op(self, fun, ops): # for expr and term
        result = ParseResult()
        left = result.register(fun())
        if result.error: return result

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            result.register(self.next_token())
            right = result.register(fun())
            if result.error: return result
            left = OperatorNode(left, op_tok, right)

        return result.success(left)
