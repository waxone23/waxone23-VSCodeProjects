from exceptions import PatientError, TemperatureError


class Patient:
    VALID_TEMP_RANGE = (34.0, 43.0)

    def __init__(self, patient_id, name):
        # Match test expectation for ID length
        if len(patient_id) < 3:
            raise PatientError("ID must be at least 3 characters", patient_id)

        self.patient_id = patient_id
        # Triggers the @name.setter
        self.name = name
        self.temperatures = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value.strip()) >= 2:
            self._name = value.strip()
        else:
            raise PatientError("Name is too short or invalid!", self.patient_id)

    @property
    def status(self):
        if not self.temperatures:
            return "No readings"

        avg_temp = self.get_average_temperatures()
        # Tests expect uppercase "FEVER" or "NORMAL"
        condition = "FEVER" if self.has_fever() else "NORMAL"

        # Format avg_temp to 1 decimal place to match "39.0°C"
        return f"{self.name} (ID: {self.patient_id}): {avg_temp:.1f}°C - {condition}"

    def add_temperature(self, temp_celsius):
        if not isinstance(temp_celsius, (int, float)):
            raise TemperatureError("Temperature must be a number", temp_celsius)

        if (
            temp_celsius < self.VALID_TEMP_RANGE[0]
            or temp_celsius > self.VALID_TEMP_RANGE[1]
        ):
            raise TemperatureError("Temperature out of range", temp_celsius)

        self.temperatures.append(temp_celsius)

    def get_average_temperatures(self):
        # The test expects this to CRASH if there are no temperatures
        if len(self.temperatures) == 0:
            raise PatientError(
                "No temperatures was recorded for this patient!", self.patient_id
            )

        average = sum(self.temperatures) / len(self.temperatures)
        return round(float(average), 1)

    def has_fever(self):
        try:
            return self.get_average_temperatures() > 38.0
        except PatientError:
            # If no temperatures exist, they technically don't have a fever
            return False
