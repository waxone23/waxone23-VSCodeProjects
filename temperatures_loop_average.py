temperatures = []
while True:
    tmp = float(input(" enter temp : "))
    temperatures.append(tmp)
    print(temperatures)
    print("average temperature is :", sum(temperatures) / len(temperatures))
