num1 = float(input("First number: "))
op = input("Operator (+, -, *, /): ")
num2 = float(input("Second number: "))

if op == "+":
    result = num1 + num1
elif op == "-":
    result = num1 - num2
elif op == "*":
    result = num1 * num2
elif op == "/":
    if num2 == 0:
        print("Error: Cannot divide by zero!")
        result = None
    else:
        result = num1 / num2
else:
    print("Invalid operator!")
result = None

if result is not None:
    print(f"{num1} {op} {num2} = {result}")

if result is not None:
    print(f"Result: {num1} {op} {num2} = {result}")

while True:
    # ... calculator code ...
    again = input("Calculate again? (yes/no): ")
    if again.lower() != "yes":
        break
print("Thanks for using the calculator!")
