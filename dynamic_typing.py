x = 5
print(f"x = {x}, type = {type(x)}, length = {len(str(x))}")

x = "hello"
print(f"x = {x}, type = {type(x)}, length = {len(x)}")

x = [1, 2, 3]
print(f"x = {x}, type = {type(x)}, length = {len(x)}")

x = 3.14
print(f"x = {x}, type = {type(x)}")

import sys

print("\n=== MEMORY COMPARISON ===")
print(f"int(42): {sys.getsizeof(42)} bytes")
print(f"float(3.14): {sys.getsizeof(3.14)} bytes")
print(f"str('hello'): {sys.getsizeof('hello')} bytes")
