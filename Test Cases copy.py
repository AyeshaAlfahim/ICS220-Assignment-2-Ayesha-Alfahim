from enum import Enum
from datetime import datetime

# Enum class for defining different e-book genres
class Genre(Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    TECHNOLOGY = "Technology"

# Base class to represent an E-book in the catalog
class EBook:
    def __init__(self, title, author, publication_date, genre, price):
        self.__setattr__('title', title)
        self.__setattr__('author', author)
        self.__setattr__('publication_date', publication_date)
        self.__setattr__('genre', genre)
        self.__setattr__('price', price)

    def __setattr__(self, name, value):
        if name in ['title', 'author', 'publication_date', 'genre', 'price']:
            self.__dict__[name] = value
        else:
            raise AttributeError(f"Cannot set attribute {name}")

    def get_price(self):
        return self.__dict__['price']

# Aggregation: EBookCatalog holds a collection of e-books,
# but they exist independently of the catalog and could belong to multiple catalogs.
class EBookCatalog:
    def __init__(self):
        self.ebooks = []

    def add_ebook(self, ebook):
        self.ebooks.append(ebook)

    def show_catalog(self):
        print("Welcome to The Great E-Book Store!")
        print("Available E-Books:")
        for ebook in self.ebooks:
            print(f"- {ebook.title} by {ebook.author} ({ebook.genre.value}): {ebook.price} AED")

# Composition: Each Customer "owns" a Cart. If a Customer is removed, their Cart is also removed.
class Customer:
    def __init__(self, name, contact_info, loyalty_member=False):
        self.__setattr__('name', name)
        self.__setattr__('contact_info', contact_info)
        self.__setattr__('loyalty_member', loyalty_member)
        self.__setattr__('cart', Cart(name))  # Cart is tightly linked to Customer and does not exist independently.

    def __setattr__(self, name, value):
        if name in ['name', 'contact_info', 'loyalty_member', 'cart']:
            self.__dict__[name] = value
        else:
            raise AttributeError(f"Cannot set attribute {name}")

    def is_loyalty_member(self):
        return self.__dict__['loyalty_member']

# Aggregation: Cart holds a list of e-book items but does not "own" them, allowing flexibility for each e-book to exist independently.
class Cart:
    def __init__(self, customer_name):
        self.__setattr__('items', [])
        self.__setattr__('customer_name', customer_name)

    def __setattr__(self, name, value):
        if name in ['items', 'customer_name']:
            self.__dict__[name] = value
        else:
            raise AttributeError(f"Cannot set attribute {name}")

    def add_item(self, ebook):
        self.items.append(ebook)
        print(f"{self.customer_name} added '{ebook.title}' to the cart.")

    def remove_item(self, ebook):
        if ebook in self.items:
            self.items.remove(ebook)
            print(f"{self.customer_name} removed '{ebook.title}' from the cart.")
        else:
            print(f"{ebook.title} is not in the cart.")

    def get_items(self):
        return self.items

class DiscountCalculator:
    def calculate_discount(self, customer, base_total):
        discount = 0
        if customer.is_loyalty_member():
            discount += base_total * 0.10
        if len(customer.cart.get_items()) >= 5:
            discount += base_total * 0.20
        return discount

class VATCalculator:
    VAT_RATE = 0.08
    def calculate_vat(self, amount):
        return amount * VATCalculator.VAT_RATE

class Order:
    def __init__(self, customer):
        self.customer = customer
        self.ebooks = customer.cart.get_items()
        self.order_date = datetime.now()
        self.base_total = sum(ebook.get_price() for ebook in self.ebooks)

        self.discount_calculator = DiscountCalculator()
        self.discount = self.discount_calculator.calculate_discount(self.customer, self.base_total)

        self.subtotal = self.base_total - self.discount

        self.vat_calculator = VATCalculator()
        self.vat = self.vat_calculator.calculate_vat(self.subtotal)
        self.final_total = round(self.subtotal + self.vat, 2)

class Invoice:
    def generate(self, order):
        print(f"Invoice for {order.customer.name}")
        print(f"Order Date: {order.order_date}\n")
        print("The Great E-Book Shopping Cart:")
        for ebook in order.ebooks:
            print(f"- {ebook.title} by {ebook.author}: {ebook.price} AED")
        print("\nOrder Confirmation:")
        print(f"Base Total: {order.base_total} AED")
        if order.customer.is_loyalty_member():
            print(f"Loyalty Discount (10%): -{round(order.base_total * 0.10, 2)} AED")
        if len(order.ebooks) >= 5:
            print(f"Bulk Discount (20%): -{round(order.base_total * 0.20, 2)} AED")
        print(f"Total Discount: -{round(order.discount, 2)} AED")
        print(f"Subtotal after Discounts: {round(order.subtotal, 2)} AED")
        print(f"VAT (8%): +{round(order.vat, 2)} AED")
        print(f"Final Total: {order.final_total} AED\n")

# Sample Test Cases

# Create an e-book catalog and add some e-books
catalog = EBookCatalog()
ebook1 = EBook("Python Programming", "Afshan Parkar", "2020", Genre.TECHNOLOGY, 50)
ebook2 = EBook("Cat In The Hat", "Dr. Seuss", "1957", Genre.FICTION, 30)
ebook3 = EBook("The Great Roman Empire", "John Smith", "2007", Genre.HISTORY, 75)
ebook4 = EBook("Pride and Prejudice", "Jane Austen", "1813", Genre.NON_FICTION, 40)
ebook5 = EBook("Cosmos", "Carl Sagan", "1980", Genre.SCIENCE, 60)

catalog.add_ebook(ebook1)
catalog.add_ebook(ebook2)
catalog.add_ebook(ebook3)
catalog.add_ebook(ebook4)
catalog.add_ebook(ebook5)

# Display the shop catalog
catalog.show_catalog()

# Test Case 1: Customer1 - Ayesha (Loyalty member with a bulk order)
customer1 = Customer("Customer1: Ayesha", "ayesha1212@mail.com", loyalty_member=True)
customer1.cart.add_item(ebook1)
customer1.cart.add_item(ebook2)
customer1.cart.add_item(ebook3)
customer1.cart.add_item(ebook4)
customer1.cart.add_item(ebook5)
customer1.cart.remove_item(ebook3)
order1 = Order(customer1)
invoice1 = Invoice()
invoice1.generate(order1)

# Test Case 2: Customer2 - Mohammed (Non-loyalty member with a bulk order)
customer2 = Customer("Customer2: Mohammed", "Mohammed123@mail.com", loyalty_member=False)
customer2.cart.add_item(ebook1)
customer2.cart.add_item(ebook2)
customer2.cart.add_item(ebook3)
customer2.cart.add_item(ebook4)
customer2.cart.add_item(ebook5)
order2 = Order(customer2)
invoice2 = Invoice()
invoice2.generate(order2)

# Test Case 3: Customer3 - Afra (Loyalty member with a smaller order)
customer3 = Customer("Customer3: Afra", "Afra345@mail.com", loyalty_member=True)
customer3.cart.add_item(ebook1)
customer3.cart.add_item(ebook2)
customer3.cart.add_item(ebook3)
order3 = Order(customer3)
invoice3 = Invoice()
invoice3.generate(order3)

# Test Case 4: Customer4 - Amna (Non-loyalty member with a single book)
customer4 = Customer("Customer4: Amna", "amna78@mail.com", loyalty_member=False)
customer4.cart.add_item(ebook1)
order4 = Order(customer4)
invoice4 = Invoice()
invoice4.generate(order4)


