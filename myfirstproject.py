name = input("whats your name: ")
age = input("How old are you?: ")

# Convert age to an integer to do math
year_born = 2026 - int(age)

# Remove the space between year and _born
print("You were born in", year_born)