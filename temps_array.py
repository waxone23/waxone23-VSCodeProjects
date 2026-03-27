temps = [36.2, 37.1, 38.5, 39.0]
for t in temps:
    if t < 36.5:
        print(f"{t}°C: Hypothermia risk.")
    elif t <= 38:
        print(f"{t}°C: Normal temperature.")
    else:
        print(f"{t}°C: Fever detected.")
