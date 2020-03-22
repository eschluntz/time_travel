def get_value(number):

    for i in range(number):
        print(i)  # this is a test
    number += 1

    if number > 10:
        number = 5
    elif number < 2:
        number = 6
    return _get(number)


def _get(number):
    return number


print(get_value(5))
