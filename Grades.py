score = int(input("Skriv inn poengsum (0-100): "))

if score > 100 or score < 0:
    print("Feil: Poengsum må være mellom 0 og 100.")

elif score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
    
print(f"Karakteren din er: {grade}")