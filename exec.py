import jupiter

while True:
    text = input("jupiter > ")
    tokens, error = jupiter.run(text)

    if error: print(str(error))
    else: print(tokens)