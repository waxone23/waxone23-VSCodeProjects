class Contact:
    def __init__(self, name, phone, email, category="friend"):
        # Lagrer alle attributter i én linje
        self.name, self.phone, self.email, self.category = name, phone, email, category

    def matches(self, query):
        # Bruker any() for å sjekke alle felt samtidig
        fields = [self.name, self.phone, self.email]
        return any(query.lower() in f.lower() for f in fields)

    def __str__(self):
        return f"📛 {self.name} | 📱 {self.phone} | 📧 {self.email} | 🏷️ {self.category}"


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, *args):
        # *args lar oss sende alle 4 verdiene rett inn i Contact
        self.contacts.append(Contact(*args))

    def search(self, q):
        # List comprehension: En en-linjers for-løkke
        return [c for c in self.contacts if c.matches(q)]

    def list_by_category(self, cat):
        return [c for c in self.contacts if c.category.lower() == cat.lower()]

    def delete_contact(self, name):
        # Beholder alle som IKKE matcher navnet
        initial_count = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        return len(self.contacts) < initial_count

    def count(self):
        return len(self.contacts)


def main():
    book = ContactBook()
    menu = ["Add", "Search", "Category", "Delete", "Show All", "Quit"]

    while True:
        print("\n--- Contact Book ---")
        for i, opt in enumerate(menu, 1):
            print(f"{i}. {opt}")

        choice = input("\nChoice: ")

        if choice == "1":
            book.add_contact(
                input("Name: "), input("Phone: "), input("Email: "), input("Category: ")
            )
        elif choice == "2":
            for c in book.search(input("Search: ")):
                print(c)
        elif choice == "3":
            for c in book.list_by_category(input("Category: ")):
                print(c)
        elif choice == "4":
            print("Deleted" if book.delete_contact(input("Name: ")) else "Not found")
        elif choice == "5":
            print(f"Total: {book.count()}")
            for c in book.contacts:
                print(c)
        elif choice == "6":
            break
