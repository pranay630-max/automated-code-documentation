def calculate(a, b, operation):
    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return None
        return a / b

    return None


def calculate_average(numbers):
    total = 0

    for number in numbers:
        total += number

    if len(numbers) == 0:
        return 0

    return total / len(numbers)