import csv

total = 0
count = 0

with open("data/students.csv", "r") as f:
    # Everything using the file must be indented here
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        try:
            total += int(row[2])
            count += 1
        except ValueError:
            print(f"Skipping bad data: {row[2]}")

# Now you can un-indent to do the final math
if count > 0:
    print(f"Average Grade: {total / count}")
