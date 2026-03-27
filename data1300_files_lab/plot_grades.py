import csv
import matplotlib.pyplot as plt

names = []
grades = []

# 1. Load the ranked data
with open("data/students_ranked.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        names.append(row["name"])
        grades.append(int(row["grade"]))

# 2. Create the bar chart
plt.figure(figsize=(8, 5))
plt.bar(names, grades, color="skyblue")
plt.xlabel("Student Name")
plt.ylabel("Grade")
plt.title("Data1300 Student Performance")
plt.ylim(0, 110)  # Set a little room above 100

# 3. Save the chart as an image
plt.savefig("data/grade_chart.png")
print("Chart saved to data/grade_chart.png")
