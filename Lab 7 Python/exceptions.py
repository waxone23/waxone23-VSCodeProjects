class PatientError(Exception):
    def __init__(self, message, patient_id):
        super().__init__(message)  # Pass message to the base Exception
        self.patient_id = patient_id  # This removes the red line for patient_id
        self.message = message


class TemperatureError(Exception):
    def __init__(self, message, temperature):
        super().__init__(message)
        self.temperature = temperature  # This removes the red line for temperature
        self.message = message
