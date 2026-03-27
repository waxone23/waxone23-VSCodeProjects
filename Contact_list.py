class Contact:
    """Represents a single contact."""

    def __init__(self, name: str, phone: str, email: str, category: str = "friend"):
        # Attributes: name, phone, email, category
        self.name = name
        self.phone = phone
        self.email = email
        self.category = category

    def matches(self, query: str) -> bool:
        """Return True if query appears in name, phone, or email (case-insensitive)."""
        query = query.lower()
        # Sjekker alle feltene spesifisert i oppgaven
        if (
            query in self.name.lower()
            or query in self.phone.lower()
            or query in self.email.lower()
        ):
            return True
        return False

    def __str__(self) -> str:
        """Returns a formatted contact card."""
        return f"📛 {self.name}\n    📱(phone) {self.phone}\n    📧(email) {self.email}\n    🏷️(tag)   {self.category}"


class ContactBook:
    """Manages a collection of contacts."""

    def __init__(self):
        # Stores a list of Contact objects
        self.contact_list = []

    def add_contact(self, name: str, phone: str, email: str, category: str = "friend"):
        """Create and store a new Contact."""
        new_person = Contact(name, phone, email, category)
        self.contact_list.append(new_person)

    def search(self, query: str) -> list:
        """Return all contacts matching the query."""
        results = []
        for contact in self.contact_list:
            if contact.matches(query):
                results.append(contact)
        return results

    def list_by_category(self, category: str) -> list:
        """Return all contacts in the given category."""
        results = []
        for contact in self.contact_list:
            if contact.category.lower() == category.lower():
                results.append(contact)
        return results

    def delete_contact(self, name: str) -> bool:
        """Delete contact by exact name. Return True if found and deleted."""
        for contact in self.contact_list:
            if contact.name.lower() == name.lower():
                self.contact_list.remove(contact)
                return True
        return False

    def count(self) -> int:
        """Return total number of contacts."""
        return len(self.contact_list)


def main():
    book = ContactBook()

    while True:
        # CLI menu loop basert på spesifikasjonen
        print("\n--- Contact Book ---")
        print("1. Add contact")
        print("2. Search contacts")
        print("3. List by category")
        print("4. Delete contact")
        print("5. Show all")
        print("6. Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            category = input("Category (friend/family/work): ")
            book.add_contact(name, phone, email, category)
            print("✅ Contact added!")

        elif choice == "2":
            query = input("Enter search term: ")
            results = book.search(query)
            if not results:
                print("No matches found.")
            else:
                for c in results:
                    print(c)

        elif choice == "3":
            cat = input("Enter category: ")
            results = book.list_by_category(cat)
            if not results:
                print(f"No contacts in category '{cat}'.")
            else:
                for c in results:
                    print(c)

        elif choice == "4":
            name = input("Exact name to delete: ")
            if book.delete_contact(name):
                print(f"🗑️ Deleted {name}.")
            else:
                print("❌ Contact not found.")

        elif choice == "5":
            if book.count() == 0:
                print("Contact book is empty.")
            else:
                print(f"Total contacts: {book.count()}")
                for c in book.contact_list:
                    print(c)
                    print("-" * 15)

        elif choice == "6":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
