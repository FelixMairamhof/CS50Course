from cs50 import get_int

while True:
    n = get_int("Number: ")
    if n >= 1 and n <= 8:
        break
for i in range(1, n + 1):
    for j in range(n):
        if j < n - i:
            print(" ", end="")
        else:
            print("#", end="")
    print()
