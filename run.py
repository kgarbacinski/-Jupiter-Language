from lexer import Lexer

while True:
    text = input("jupiter > ")
    out, error = Lexer.run(text)

    if error: print(str(error))
    else: print(out)