import csv
import os


def load_temperatures(filename):
    """Load existing temperatures from CSV file."""
    temperatures = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if exists
            for row in reader:
                if row:  # Check if row is not empty
                    temperatures.append(float(row[0]))
    return temperatures


def save_temperature(filename, temperature):
    """Append a temperature to the CSV file."""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Temperature"])  # Write header
        writer.writerow([temperature])


def calculate_average(temperatures):
    """Calculate the average of all temperatures."""
    if not temperatures:
        return 0
    return sum(temperatures) / len(temperatures)


def main():
    filename = "temperature_log.csv"

    # Load existing temperatures
    temperatures = load_temperatures(filename)

    print("Temperature Tracker")
    print("=" * 40)
    print(f"Loaded {len(temperatures)} existing temperature(s)")

    if temperatures:
        print(f"Current average: {calculate_average(temperatures):.2f}°")

    print("\nEnter temperatures (type 'quit' to exit)")
    print("=" * 40)

    while True:
        user_input = input("\nEnter temperature: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nFinal Statistics:")
            print(f"Total temperatures recorded: {len(temperatures)}")
            if temperatures:
                print(f"Average temperature: {calculate_average(temperatures):.2f}°")
            print("Goodbye!")
            break

        try:
            temperature = float(user_input)

            # Add to list
            temperatures.append(temperature)

            # Save to CSV
            save_temperature(filename, temperature)

            # Calculate and display average
            avg = calculate_average(temperatures)
            print(f"Temperature {temperature}° saved!")
            print(f"Total readings: {len(temperatures)}")
            print(f"Current average: {avg:.2f}°")

        except ValueError:
            print("Invalid input! Please enter a valid number or 'quit' to exit.")


if __name__ == "__main__":
    main()
