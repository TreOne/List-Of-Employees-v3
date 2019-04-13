def smart_ending(number, one, two, five):
    """
    Возвращает существительное сответствующее числительному, например:
        smart_ending(number, 'год', 'года', 'лет')
        1 год, 2 года, 5 лет
    """
    last_digit = number % 10
    last_two_digits = number % 100
    if last_digit == 1 and last_two_digits != 11:
        return one
    elif last_digit in (2, 3, 4) and last_two_digits not in (12, 13, 14):
        return two
    else:
        return five
