import csv

unique_students = {}

with open("data/students.csv", "r") as f:
    reader = csv.DictReader(f)
    for line_num, row in enumerate(
        reader, start=2
    ):  # Tracking line numbers for easy fixing
        try:
            name = row["name"].strip().title()
            # This is the line that usually crashes
            grade = int(row["grade"])

            if name not in unique_students or grade > unique_students[name]["grade"]:
                unique_students[name] = {
                    "name": name,
                    "course": row["course"],
                    "grade": grade,
                }

        except ValueError:
            error_msg = (
                f"Line {line_num}: Invalid grade '{row['grade']}' for {row['name']}\n"
            )
            print(f"⚠️ {error_msg.strip()}")  # Still print to screen

            # Open the log file in 'a' (append) mode
            with open("data/error_log.txt", "a") as log:
                log.write(error_msg)
print("\nExported: data/students_ranked.csv")
