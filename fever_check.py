temprature = float(input("Enter the temprature in Celsius: "))
if temprature < 36.5:
    print("Hypothermia risk.")
elif temprature <= 38:
    print("Normal temprature.")
else:
    print("Fever detected.")
