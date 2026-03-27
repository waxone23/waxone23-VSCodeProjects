import unittest
from vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    def setUp(self):
        """Creates a standard vehicle instance for use in multiple tests."""
        self.car = Vehicle("V100", "Tesla", "Model 3", 2024, 150.0)

    # --- 1. VALIDATION TESTS ---
    def test_vehicle_creation_valid(self):
        """Test that a vehicle is created correctly with valid data."""
        self.assertEqual(self.car.make, "Tesla")
        self.assertEqual(self.car.year, 2024)

    def test_invalid_year(self):
        """Test that a year outside 1900-2026 raises a ValueError."""
        with self.assertRaises(ValueError):
            Vehicle("V101", "Ford", "T", 1899, 50.0)
        with self.assertRaises(ValueError):
            Vehicle("V102", "Future", "Car", 2027, 50.0)

    def test_invalid_daily_rate(self):
        """Test that a zero or negative daily_rate raises a ValueError."""
        with self.assertRaises(ValueError):
            Vehicle("V103", "Chevy", "Bolt", 2023, 0)
        with self.assertRaises(ValueError):
            Vehicle("V104", "Chevy", "Bolt", 2023, -10.0)

    # --- 2. LOGIC TESTS ---
    def test_rent_calculation(self):
        """Test that rent returns the correct total cost."""
        cost = self.car.rent("Alice", 3)
        self.assertEqual(cost, 450.0)  # 150 * 3
        self.assertEqual(self.car.get_rental_count(), 1)

    # --- 3. DATACLASS FEATURE TESTS ---
    def test_repr_output(self):
        """Verifies __repr__ includes key info but EXCLUDES rental_history."""
        output = repr(self.car)
        # Should contain identifying info
        self.assertIn("Tesla", output)
        self.assertIn("Model 3", output)
        # Should NOT contain the history (because of repr=False)
        self.assertNotIn("rental_history", output)


if __name__ == "__main__":
    unittest.main()
