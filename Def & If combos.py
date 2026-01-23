def validate_age(age_text):
    age = int(age_text)
    if 0 <= age <= 150:
        return age
    return None

def get_life_stage(age):
    if age <13:
        return "child"
    elif age <65:
        return "Adult"
    else:
        return "Senior"
    
    name = input("Name: ")
    age = validate_age(input("age: "))
    if age:
        print(f"{name} is {get_life_stage(age)}")