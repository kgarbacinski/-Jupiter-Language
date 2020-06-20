import abc

##########
# TOKENS
##########

T_INT = 'INT'
T_FLOAT = 'FLOAT'
T_PLUS = 'PLUS'
T_MINUS = 'MINUS'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'

class Token:
    def __init__(self, _type, _value = None):
        self.type = _type
        self.value= _value

    def __repr__(self):
        return f'{self.type} : {self.value}' if self.value else f'{self.type}'


##########
# CONSTANTS
##########

DIGITS = '0123456789'


##########
# CharError
##########

class Error():
    def __init__(self, _name, _info):
        self.name = _name
        self.info = _info

    def __str__(self):
        return f'{self.name}: {self.info}'

class InvalidCharError(Error):
    def __init__(self, _info):
        super().__init__('Invalid Char', _info)

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
                tokens.append(Token(T_PLUS))
                self.analyze_text()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS))
                self.analyze_text()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL))
                self.analyze_text()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV))
                self.analyze_text()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAREN))
                self.analyze_text()
            elif self.current_char == ')':
                tokens.append(Token(T_RPAREN))
                self.analyze_text()
            else:
                return [], InvalidCharError("'" + self.current_char + "'")

        return tokens, []

    def make_number(self):
        num = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num += '.'
            else:
                num += self.current_char

            self.analyze_text()

        if dot_count == 0:
            return Token(T_INT, int(num))
        else:
            return Token(T_FLOAT, float(num))


#######
# RUN
#######

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.create_tokens()

    return tokens, error