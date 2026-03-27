# ============================================
# OOP IN PYTHON — CLEAN UNIVERSITY VERSION
# ============================================

# %% 1. Basic Class and Object


class Robot:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"My name is {self.name}.")


bot_1 = Robot("wall-e")
bot_2 = Robot("terminator")

bot_1.greet()
bot_2.greet()

bot_1.name = "fofinho"
bot_1.greet()


# %% 2. Methods vs Functions


class MyClass:
    def say_something(self):
        print("I am a method, I have a self.")


instance_1 = MyClass()
instance_1.say_something()


def function():
    print("I am a function, and have no self.")


function()

# Binding a function to an instance
instance_1.say_other_thing = function
instance_1.say_other_thing()


# %% 3. Private Attributes (Name Mangling)


class SecretRobot:
    def __init__(self, name):
        self.__name = name

    def greet(self):
        print(f"My name is {self.__name}.")

    def get_name(self):
        return self.__name


secret_bot = SecretRobot("wall-e")
secret_bot.greet()

# This creates a NEW attribute, not overriding the private one
secret_bot.__name = "fifo"

secret_bot.greet()  # Still prints wall-e

# Accessing the mangled name directly (not recommended in practice)
print(secret_bot._SecretRobot__name)


# %% 4. Validation in __init__

from datetime import datetime


class User:
    def __init__(self, username, age):
        if age < 0:
            raise ValueError("Age cannot be negative.")

        self.username = username
        self.age = age
        self.dob = self.calculate_dob()

    def calculate_dob(self):
        return datetime.now().year - self.age


user = User("alice", 25)
print(user.username, user.age, user.dob)


# %% 5. Decorators


def shout(func):
    def wrapper():
        result = func()
        return result.upper()

    return wrapper


@shout
def greet():
    return "hello"


print(greet())  # HELLO


# %% 6. Read-Only Property


class ReadOnlyAccount:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance


account = ReadOnlyAccount(1000)
print(account.balance)


# %% 7. Read-Write Property


class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = value


account = BankAccount(1000)
print(account.balance)

account.balance = 500
print(account.balance)


# %% 8. Inheritance: Pure, Override, Extend


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def info(self):
        return f"{self.name}, salary: {self.salary}"


class Designer(Employee):
    pass  # Pure inheritance


class Manager(Employee):
    def info(self):  # Override
        return f"Manager {self.name}, salary: confidential"


class Developer(Employee):
    def develop(self):  # Extend
        return "Writing code..."


designer = Designer("Bob", 60000)
manager = Manager("Alice", 80000)
developer = Developer("Charlie", 90000)

print(designer.info())
print(manager.info())
print(developer.info())
print(developer.develop())

print(isinstance(manager, Employee))
print(issubclass(Manager, Employee))


# %% 9. Inheritance with super()


class Predator:
    def __init__(self):
        self.hungry = True

    def hunt(self):
        if self.hungry:
            print("Search, chase, delicious!")
            self.hungry = False
        else:
            print("No thanks.")


class Wolf(Predator):
    def __init__(self):
        super().__init__()
        self.bark_sound = "woof"

    def bark(self):
        print(self.bark_sound)


fenrir = Wolf()
fenrir.bark()
fenrir.hunt()
fenrir.hunt()


# %% 10. Polymorphism


class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


class Cow(Animal):
    def speak(self) -> str:
        return "Moo!"


def make_speak(animal: Animal) -> None:
    print(animal.speak())


make_speak(Dog())
make_speak(Cat())
make_speak(Cow())
