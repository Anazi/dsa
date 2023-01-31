def factorial(n):
    if n == 0:
        # Case for handling 0!
        return 1
    if n == 1:
        return 1
    return n * factorial(n-1)


print(factorial(0))


def exponential(number, power):
    if power == 0:
        return 1
    power -= 1
    return number * exponential(number, power)


print(exponential(2, 3))
