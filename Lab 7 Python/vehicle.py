from dataclasses import dataclass, field


@dataclass
class Vehicle:
    vehicle_id: str
    make: str
    model: str
    year: int
    daily_rate: float

    rental_history: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        """Validates data immediately after the object is initialized."""
        if not (1900 <= self.year <= 2026):
            raise ValueError(f"Year must be between 1900 and 2026. Got: {self.year}")

        if self.daily_rate <= 0:
            raise ValueError(f"Daily rate must be positive. Got: {self.daily_rate}")

    def rent(self, customer_name: str, days: int) -> float:
        """Processes a rental and updates history."""
        if days <= 0:
            raise ValueError("Rental duration must be at least 1 day.")

        cost = self.daily_rate * days

        # Storing as a small dictionary for easy tracking
        record = {"customer": customer_name, "days": days, "total_cost": cost}
        self.rental_history.append(record)

        return cost

    def get_rental_count(self) -> int:
        """Returns the total number of times this vehicle has been rented."""
        return len(self.rental_history)
