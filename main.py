import random
import time

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]

        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    for symbol, count in symbols.items():  # FIXED variable shadowing
        all_symbols.extend([symbol] * count)

    columns = []

    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]

        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    print("\n--- SPIN RESULT ---")

    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

    print("-------------------\n")


def deposit():
    while True:
        amount = input("What would you like to deposit? $")

        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")


def get_number_of_lines():
    while True:
        lines = input(f"Enter number of lines to bet on (1-{MAX_LINES}): ")

        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")


def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")

        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f"Bet must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")


def spin(balance):
    lines = get_number_of_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Not enough balance. Current balance: ${balance}")
        else:
            break

    print(f"\nYou are betting ${bet} on {lines} lines (Total bet: ${total_bet})")

    time.sleep(1)  # small delay for realism

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    if winnings > 0:
        print(f"You won ${winnings}!")
    else:
        print("You didn't win this round.")

    if winning_lines:
        print("Winning lines:", *winning_lines)
    else:
        print("No winning lines.")

    # Optional jackpot message
    if winnings >= 50:
        print("🎉 JACKPOT! 🎉")

    return winnings - total_bet


def main():
    balance = deposit()

    while True:
        if balance <= 0:
            print("You ran out of money!")
            break

        print(f"\nCurrent balance: ${balance}")
        answer = input("Press Enter to play (q to quit): ")

        if answer.lower() == "q":
            break

        balance += spin(balance)

    print(f"\nYou left with ${balance}")


main()