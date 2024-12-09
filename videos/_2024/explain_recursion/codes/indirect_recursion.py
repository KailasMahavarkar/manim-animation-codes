def functionA(x):
    if x > 0:
        print("A", x)
        functionB(x - 1)


def functionB(x):
    if x > 0:
        print("B", x)
        functionA(x - 1)


