class Health:
    def __init__(self, name: str, weight_kg: float, height_m: float):
        # Validation Logic
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("Weight and height must be greater than zero.")

        self.name = name
        self.weight_kg = weight_kg
        self.height_m = height_m

    def calculate_bmi(self) -> float:
        """Calculates BMI: weight / height^2, rounded to 2 decimals."""
        return round(self.weight_kg / (self.height_m**2), 2)

    def get_category(self) -> str:
        """Categorizes BMI based on the standard ranges."""
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi <= 24.9:
            return "Normal"
        elif 25 <= bmi <= 29.9:
            return "Overweight"
        else:
            return "Obese"

    def get_health_advice(self) -> str:
        """Returns personalized advice based on BMI category."""
        category = self.get_category()

        advice_map = {
            "Underweight": (
                "It is important to ensure you are consuming enough nutrients and calories. "
                "Consider a balanced diet with energy-dense foods and strength training. "
                "Consulting with a nutritionist may help you reach a healthier weight safely."
            ),
            "Normal": (
                "You are within a healthy BMI range. Maintain this by staying active and "
                "eating a diverse range of whole foods. Keep up the great work with your "
                "current lifestyle habits."
            ),
            "Overweight": (
                "A balanced approach to nutrition and regular cardiovascular exercise is recommended. "
                "Small changes like reducing processed sugars can have a significant impact. "
                "Consistency is key to moving toward a more ideal weight range."
            ),
            "Obese": (
                "Focus on sustainable lifestyle changes and regular physical activity. "
                "It may be beneficial to consult a healthcare professional for a personalized weight management plan. "
                "Prioritize heart-healthy foods and gradual progress over quick fixes."
            ),
        }
        return advice_map.get(category, "No advice available.")

    def get_ideal_weight(self) -> float:
        """Formula: 22 × height^2 — rounded to 1 decimal place."""
        return round(22 * (self.height_m**2), 1)
