import csv

students = []

# 1. Read the data and clean it
with open("data/students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean the data as we read it
        clean_name = row["name"].strip().title()
        clean_grade = int(row["grade"])
        students.append(
            {"name": clean_name, "course": row["course"], "grade": clean_grade}
        )

# 2. Sort by grade (highest first)
# The 'key' tells Python to look at the grade, and 'reverse=True' puts 100 at the top.
sorted_students = sorted(students, key=lambda x: x["grade"], reverse=True)

# 3. Print the Leaderboard
print(f"{'Name':<10} | {'Course':<10} | {'Grade'}")
print("-" * 30)
for s in sorted_students:
    print(f"{s['name']:<10} | {s['course']:<10} | {s['grade']}")
