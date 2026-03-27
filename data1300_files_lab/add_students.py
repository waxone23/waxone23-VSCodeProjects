import csv

print("--- Student Data Entry Tool ---")
print("Type 'quit' as the name to stop.\n")

while True:
    name = input("Student Name: ")
    if name.lower() == "quit":
        break

    course = input("Course Name: ")
    grade = input("Grade: ")

    # Append the new data to our CSV
    with open("data/students.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, course, grade])

    print(f"Added {name} successfully!\n")

print("Data entry closed. Goodbye!")
