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
        # Using __setattr__ for validation or modifications if needed
        self.__setattr__('title', title)
        self.__setattr__('author', author)
        self.__setattr__('publication_date', publication_date)
        self.__setattr__('genre', genre)
        self.__setattr__('price', price)

    def __setattr__(self, name, value):
        # Additional checks can be added here if needed
        super().__setattr__(name, value)


# Aggregation: EBookCatalog holds a collection of e-books,
# but they exist independently of the catalog and could belong to multiple catalogs.
class EBookCatalog:
    def __init__(self):
        self.__setattr__('ebooks', [])

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

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
        self.__setattr__('cart', Cart(name))  # Cart is tightly linked to Customer

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

    def is_loyalty_member(self):
        return self.loyalty_member


# Aggregation: Cart holds a list of e-book items but does not "own" them, allowing flexibility for each e-book to exist independently.
class Cart:
    def __init__(self, customer_name):
        self.__setattr__('items', [])
        self.__setattr__('customer_name', customer_name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

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


# Aggregation: DiscountCalculator takes a Customer and Cart to calculate discounts, but it does not own them.
class DiscountCalculator:
    def calculate_discount(self, customer, base_total):
        discount = 0
        if customer.is_loyalty_member():
            discount += base_total * 0.10
        if len(customer.cart.get_items()) >= 5:
            discount += base_total * 0.20
        return discount


# Aggregation: VATCalculator calculates VAT for an order's subtotal but does not own the Order.
class VATCalculator:
    VAT_RATE = 0.08

    def calculate_vat(self, amount):
        return amount * VATCalculator.VAT_RATE


# Composition: Each Order is associated with a Customer who places the order.
class Order:
    def __init__(self, customer):
        self.__setattr__('customer', customer)
        self.__setattr__('ebooks', customer.cart.get_items())
        self.__setattr__('order_date', datetime.now())

        base_total = sum(ebook.price for ebook in self.ebooks)
        self.__setattr__('base_total', base_total)

        discount_calculator = DiscountCalculator()
        discount = discount_calculator.calculate_discount(self.customer, self.base_total)
        self.__setattr__('discount', discount)

        subtotal = self.base_total - self.discount
        self.__setattr__('subtotal', subtotal)

        vat_calculator = VATCalculator()
        vat = vat_calculator.calculate_vat(self.subtotal)
        self.__setattr__('vat', vat)

        final_total = round(self.subtotal + self.vat, 2)
        self.__setattr__('final_total', final_total)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)


# Composition: Each Invoice is generated for a specific Order.
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







