def get_average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)
