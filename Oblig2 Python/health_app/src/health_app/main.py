import sys
from health_app.health import Health
from health_app.data import save_all_records, load_records, get_statistics


def get_valid_input(prompt, type_func):
    """Helper to loop until valid input is provided."""
    while True:
        try:
            user_input = input(prompt).strip()
            # Check for empty input before converting
            if not user_input:
                print("Invalid input, please try again")
                continue
            return type_func(user_input)
        except ValueError:
            print("Invalid input, please try again")


def add_record():
    """Option 1: Collects user data and saves immediately."""
    name = input("Enter name: ").strip()
    while not name:
        print("Invalid input, please try again")
        name = input("Enter name: ").strip()

    weight = get_valid_input("Enter weight (kg): ", float)
    height = get_valid_input("Enter height (m): ", float)

    try:
        # Create object and validate via Health class __init__ logic
        record = Health(name, weight, height)

        # Immediate persistence: Load, Append, Save
        current_records = load_records()
        current_records.append(record)
        save_all_records(current_records)

        # Confirmation message formatting
        bmi = record.calculate_bmi()
        cat = record.get_category()
        ideal = record.get_ideal_weight()
        advice = record.get_health_advice()

        print(
            f"\nAdded {name}: BMI {bmi:.2f} ({cat}) | Ideal: {ideal}kg | Advice: {advice}\n"
        )

    except ValueError as e:
        print(f"Error: {e}. Please try again.")


def view_all():
    """Option 2: Display summary of all records."""
    records = load_records()
    if not records:
        print("\nNo records found.\n")
        return

    print("\n--- Health Records ---")
    for r in records:
        bmi = r.calculate_bmi()
        cat = r.get_category()
        ideal = r.get_ideal_weight()
        diff = round(r.weight_kg - ideal, 1)

        # Formatting the difference for readability
        diff_str = f"+{diff}kg" if diff > 0 else f"{diff}kg"

        print(f"{r.name}: BMI {bmi} ({cat}) | Ideal Diff: {diff_str}")
    print("----------------------\n")


def view_stats():
    """Option 3: Display statistics from data module."""
    stats = get_statistics()
    if stats["total_records"] == 0:
        print("\nNo statistics available yet.\n")
        return

    print("\n--- Statistics ---")
    print(f"Total Records: {stats['total_records']}")
    print(f"Average BMI:   {stats['avg_bmi']}")
    print(f"Common Category: {stats['most_common_category']}")
    print("Distribution:")
    for cat, count in stats["category_distribution"].items():
        print(f"  - {cat}: {count}")
    print("------------------\n")


def main():
    """Main menu loop."""
    while True:
        print("1. Add Health Record")
        print("2. View All Records")
        print("3. View Statistics")
        print("4. Save & Quit")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            add_record()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_stats()
        elif choice == "4":
            print("Saving data and exiting...")
            # Note: Records are already saved immediately,
            # but this fulfills the 'Save & Quit' requirement.
            sys.exit()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
