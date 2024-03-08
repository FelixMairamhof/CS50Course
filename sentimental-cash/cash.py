from cs50 import get_float


def main():
    cents = get_cents()

    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    pennies = calculate_pennies(cents)

    coins = quarters + dimes + nickels + pennies

    print(int(coins))


def get_cents():
    while True:
        dollars = get_float("Change owed: ")
        if dollars > 0:
            return round(dollars * 100)


def calculate_quarters(cents):
    quarters = cents // 25
    return quarters


def calculate_dimes(cents):
    dimes = cents // 10
    return dimes


def calculate_nickels(cents):
    nickels = cents // 5
    return nickels


def calculate_pennies(cents):
    return cents


if __name__ == "__main__":
    main()
