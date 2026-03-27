import pytest
from exceptions import PatientError, TemperatureError
from patient import Patient


# --- Fixtures ---
@pytest.fixture
def default_patient():
    return Patient("P001", "Ola Nordmann")


# --- Basic Functionality Tests ---


def test_create_valid_patient():
    p = Patient("P001", "Ola Nordmann")
    assert p.patient_id == "P001"
    assert p.name == "Ola Nordmann"
    assert p.temperatures == []


def test_invalid_patient_id_too_short():
    with pytest.raises(PatientError, match="ID must be at least 3 characters"):
        Patient("12", "Ola Nordmann")


def test_add_valid_temperatures(default_patient):
    default_patient.add_temperature(37.5)
    default_patient.add_temperature(38.2)
    assert len(default_patient.temperatures) == 2
    assert 37.5 in default_patient.temperatures


def test_temperature_range_exceptions(default_patient):
    with pytest.raises(TemperatureError, match="Temperature out of range"):
        default_patient.add_temperature(44.0)
    with pytest.raises(TemperatureError, match="Temperature out of range"):
        default_patient.add_temperature(33.0)


def test_average_calculation(default_patient):
    default_patient.add_temperature(37.0)
    default_patient.add_temperature(38.0)
    assert default_patient.get_average_temperatures() == 37.5


def test_fever_logic(default_patient):
    default_patient.add_temperature(39.0)
    assert default_patient.has_fever() is True

    p2 = Patient("P002", "No Fever")
    p2.add_temperature(36.5)
    assert p2.has_fever() is False


def test_status_property_format():
    p = Patient("P001", "Ola")
    p.add_temperature(39.0)
    # Note: Ensure Patient class uses FEVER (caps) and 1 decimal place
    assert p.status == "Ola (ID: P001): 39.0°C - FEVER"


def test_status_no_readings():
    p = Patient("P001", "Ola")
    assert p.status == "No readings"


# --- Exception Attribute Tests ---


class TestExceptionAttributes:
    def test_temperature_error_attributes(self, default_patient):
        """Verify TemperatureError stores temperature value."""
        with pytest.raises(TemperatureError) as exc_info:
            default_patient.add_temperature(50.0)

        exc = exc_info.value
        assert exc.temperature == 50.0

    def test_patient_error_attributes(self):
        """Verify PatientError stores patient_id."""
        with pytest.raises(PatientError) as exc_info:
            Patient("AB", "Test")

        exc = exc_info.value
        assert exc.patient_id == "AB"


# --- Edge Case Tests ---


class TestEdgeCases:
    def test_boundary_temperatures(self, default_patient):
        """Test exact boundary values (34.0 and 43.0)."""
        default_patient.add_temperature(34.0)
        default_patient.add_temperature(43.0)
        assert len(default_patient.temperatures) == 2

        with pytest.raises(TemperatureError):
            default_patient.add_temperature(33.9)
        with pytest.raises(TemperatureError):
            default_patient.add_temperature(43.1)

    def test_empty_temperature_list(self):
        """Test behavior with no readings."""
        patient = Patient("P001", "Ole")
        # Ensure 'match' is a subset of the string used in patient.py
        with pytest.raises(PatientError, match="No temperatures was recorded"):
            patient.get_average_temperatures()

        # This part should not crash because has_fever handles the empty case
        assert patient.has_fever() is False

    def test_whitespace_in_name(self):
        """Test name trimming."""
        patient = Patient("P001", " Ole Nordmann ")
        assert patient.name == "Ole Nordmann"

    # --- Parametrized Tests ---


class TestParametrized:
    @pytest.mark.parametrize(
        "temp,expected",
        [
            (37.0, False),  # Normal
            (38.0, False),  # Exactly 38.0 is not a fever (must be > 38.0)
            (38.1, True),  # Just above 38.0
            (39.5, True),  # Clear fever
        ],
    )
    def test_fever_detection(self, temp, expected):
        """Test fever detection with multiple temperatures."""
        patient = Patient("P001", "Ole")
        patient.add_temperature(temp)
        assert patient.has_fever() == expected

    @pytest.mark.parametrize(
        "invalid_temp",
        [
            30.0,  # Too low
            50.0,  # Too high
            100.0,  # Way too high
            -10.0,  # Negative
        ],
    )
    def test_invalid_temperatures(self, invalid_temp):
        """Test multiple invalid temperature values."""
        patient = Patient("P001", "Ole")
        with pytest.raises(TemperatureError):
            patient.add_temperature(invalid_temp)
