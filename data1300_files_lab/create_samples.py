import csv
import json
import os

os.makedirs("data", exist_ok=True)

with open("data/students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "course", "grade"])
    writer.writerow(["Alice", "Python", "85"])
    writer.writerow(["Bob", "Python", "92"])
    writer.writerow(["Charlie", "Data1300", "78"])

print("Created data/students.csv")
