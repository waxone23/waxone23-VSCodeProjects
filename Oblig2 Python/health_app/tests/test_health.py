import pytest
from health_app.health import Health


# ✔ Health creation (valid inputs)
def test_health_creation():
    h = Health("Brede", 80, 1.8)
    assert h.name == "Brede"
    assert h.weight_kg == 80
    assert h.height_m == 1.8


# ✔ Input validation (error cases)
def test_health_validation():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Health("", 80, 1.8)
    with pytest.raises(ValueError, match="greater than zero"):
        Health("Brede", 0, 1.8)
    with pytest.raises(ValueError, match="greater than zero"):
        Health("Brede", 80, -1)


# ✔ BMI calculation
def test_bmi_calculation():
    h = Health("Test", 70, 1.75)
    assert h.calculate_bmi() == 22.86


# ✔ BMI categorization (all 4)
@pytest.mark.parametrize(
    "w, h, expected",
    [
        (50, 1.8, "Underweight"),
        (70, 1.8, "Normal"),
        (90, 1.8, "Overweight"),
        (110, 1.8, "Obese"),
    ],
)
def test_bmi_categories(w, h, expected):
    assert Health("Test", w, h).get_category() == expected


# ✔ Health advice (1 per category)
def test_health_advice():
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    for cat in categories:
        # Create a dummy person for each category
        if cat == "Underweight":
            h = Health("T", 40, 1.8)
        if cat == "Normal":
            h = Health("T", 70, 1.8)
        if cat == "Overweight":
            h = Health("T", 90, 1.8)
        if cat == "Obese":
            h = Health("T", 120, 1.8)

        advice = h.get_health_advice()
        assert isinstance(advice, str)
        assert len(advice.split(".")) >= 2  # Check for 2-3 sentences


# ✔ Ideal weight calculation
def test_ideal_weight_calculation():
    h = Health("Test", 80, 1.8)
    # 22 * 1.8^2 = 71.28 -> 71.3
    assert h.get_ideal_weight() == 71.3
