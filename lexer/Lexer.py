from lexer.Tokens import *
from parser_and_ast.Parser import *
from interpreter.Interpreter import *

#########
# TOKEN
#########

class Token:
    def __init__(self, _type, _value=None, pos_start_ = None, pos_end_ = None):
        self.type = _type
        self.value = _value

    def __repr__(self):
        return f'{self.type} : {self.value}' if self.value else f'{self.type}'

##########
# LEXER
##########

class Lexer:
    def __init__(self, _text):
        self.text = _text
        self.pos = 0
        self.current_char = None
        self.analyze_text()

    def analyze_text(self):
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.pos += 1

    def create_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.analyze_text()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS, pos_start_=self.pos))
                self.analyze_text()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS, pos_start_=self.pos))
                self.analyze_text()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL, pos_start_=self.pos))
                self.analyze_text()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV, pos_start_=self.pos))
                self.analyze_text()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAREN, pos_start_=self.pos))
                self.analyze_text()
            elif self.current_char == ')':
                tokens.append(Token(T_RPAREN, pos_start_=self.pos))
                self.analyze_text()
            else:
                return [], InvalidCharError("'" + self.current_char + "'")

        tokens.append(Token(T_EOF, pos_start_=self.pos))
        return tokens, []

    def make_number(self):
        num = ''
        dot_count = 0
        pos_start = self.pos

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num += '.'
            else:
                num += self.current_char

            self.analyze_text()

        if dot_count == 0:
            return Token(T_INT, int(num), pos_start, self.pos)
        else:
            return Token(T_FLOAT, float(num), pos_start, self.pos)


#######
# RUN
#######

def run(text):
    # Gen Tokens
    lexer = Lexer(text)
    tokens, error = lexer.create_tokens()

    if error: return None, error

    # Gen AST
    parser = Parser(tokens)
    tree = parser.parse()
    if tree.error: return None, tree.error

    interpreter = Interpreter()
    res = interpreter.process_node(tree.node)

    return res.value, res.error