name = input("What's your name): ")
age_text = input("what is your age?: ")

age = int(age_text)

birth_year = 2026 - age
print(f"{name}, you where born around {birth_year}")

import sys

print(f"Memory: int size = {sys.getsizeof(age)} bytes")

try:
    age = int(input("Your age: "))
    print(f"Birth year: {2026 - age}")
except ValueError:
    print("Please enter a valid number!")
