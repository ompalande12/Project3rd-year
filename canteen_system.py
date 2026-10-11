"""
Canteen Food Ordering System
----------------------------
A beginner-friendly, console-based project using only standard Python.
Concepts used: variables, lists, dictionaries, functions, loops,
conditions, exception handling and file handling.
"""

from datetime import datetime  # standard library: for date and time on the bill

# ---------------------------------------------------------------
# 1. DATA SECTION
# ---------------------------------------------------------------
# Menu dictionary:  item ID -> (item name, price in Rs.)
MENU = {
    1: ("Veg Sandwich", 40),
    2: ("Burger", 60),
    3: ("Pizza", 120),
    4: ("French Fries", 50),
    5: ("Samosa", 15),
    6: ("Tea", 10),
    7: ("Coffee", 20),
    8: ("Cold Drink", 30),

}

GST_PERCENT = 5          # tax added to the bill (set to 0 for no tax)
ORDER_FILE = "orders.txt"  # file where completed orders are saved
LINE_WIDTH = 46          # width of the receipt


# ---------------------------------------------------------------
# 2. FUNCTIONS
# ---------------------------------------------------------------
def display_menu():
    """Show every menu item with its ID, name and price."""
    print("\n" + "=" * LINE_WIDTH)
    print("CANTEEN MENU".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)
    print(f"{'ID':<6}{'Item':<26}{'Price (Rs.)':>12}")
    print("-" * LINE_WIDTH)
    for item_id, (name, price) in MENU.items():
        print(f"{item_id:<6}{name:<26}{price:>12.2f}")
    print("=" * LINE_WIDTH)


def place_order(order):
    """Ask for item IDs and quantities until the user types 0.

    'order' is a dictionary:  item ID -> quantity
    """
    display_menu()
    print("\nEnter the item ID and quantity. Type 0 as the ID to finish.")

    while True:
        # --- Step 1: get and validate the item ID ---
        try:
            item_id = int(input("\nItem ID (0 to finish): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if item_id == 0:
            break
        if item_id not in MENU:
            print(f"Item ID {item_id} is not on the menu. Try again.")
            continue

        # --- Step 2: get and validate the quantity ---
        try:
            quantity = int(input(f"Quantity of {MENU[item_id][0]}: "))
            if quantity <= 0:
                raise ValueError  # treat zero/negative as invalid
        except ValueError:
            print("Invalid quantity! Enter a whole number greater than 0.")
            continue

        # --- Step 3: add to the order (add to old quantity if repeated) ---
        order[item_id] = order.get(item_id, 0) + quantity
        print(f"Added: {quantity} x {MENU[item_id][0]}")


def view_order(order):
    """Show the items currently in the order (without tax)."""
    if not order:
        print("\nYour order is empty. Choose 'Place Order' first.")
        return

    print("\n" + "-" * LINE_WIDTH)
    print("YOUR CURRENT ORDER".center(LINE_WIDTH))
    print("-" * LINE_WIDTH)
    print(f"{'ID':<5}{'Item':<20}{'Qty':>5}{'Price':>8}{'Total':>8}")
    print("-" * LINE_WIDTH)
    for item_id, qty in order.items():
        name, price = MENU[item_id]
        print(f"{item_id:<5}{name:<20}{qty:>5}{price:>8.2f}{price * qty:>8.2f}")
    print("-" * LINE_WIDTH)


def remove_item(order):
    """Remove an item (or reduce its quantity) from the order."""
    if not order:
        print("\nNothing to remove. The order is empty.")
        return

    view_order(order)
    try:
        item_id = int(input("Enter the item ID to remove: "))
        if item_id not in order:
            print("That item is not in your order.")
            return

        qty_remove = int(input("How many to remove? "))
        if qty_remove <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input! Please enter whole numbers only.")
        return

    # If removing everything (or more), delete the item completely
    if qty_remove >= order[item_id]:
        del order[item_id]
        print(f"{MENU[item_id][0]} removed from the order.")
    else:
        order[item_id] -= qty_remove
        print(f"Removed {qty_remove} x {MENU[item_id][0]}.")


def calculate_totals(order):
    """Return (subtotal, total quantity, tax, final amount)."""
    subtotal = 0
    total_qty = 0
    for item_id, qty in order.items():
        subtotal += MENU[item_id][1] * qty
        total_qty += qty
    tax = subtotal * GST_PERCENT / 100
    return subtotal, total_qty, tax, subtotal + tax


def build_receipt(order, customer_name):
    """Create the receipt as a single text string (used to print AND save)."""
    subtotal, total_qty, tax, final_amount = calculate_totals(order)
    now = datetime.now().strftime("%d-%m-%Y  %I:%M %p")

    lines = []
    lines.append("=" * LINE_WIDTH)
    lines.append("CANTEEN FOOD ORDERING SYSTEM".center(LINE_WIDTH))
    lines.append("Customer Receipt".center(LINE_WIDTH))
    lines.append("=" * LINE_WIDTH)
    lines.append(f"Customer : {customer_name}")
    lines.append(f"Date     : {now}")
    lines.append("-" * LINE_WIDTH)
    lines.append(f"{'Item':<20}{'Qty':>5}{'Price':>9}{'Total':>10}")
    lines.append("-" * LINE_WIDTH)
    for item_id, qty in order.items():
        name, price = MENU[item_id]
        lines.append(f"{name:<20}{qty:>5}{price:>9.2f}{price * qty:>10.2f}")
    lines.append("-" * LINE_WIDTH)
    lines.append(f"{'Total Quantity':<30}{total_qty:>16}")
    lines.append(f"{'Subtotal (Rs.)':<30}{subtotal:>16.2f}")
    lines.append(f"{'GST @ ' + str(GST_PERCENT) + '% (Rs.)':<30}{tax:>16.2f}")
    lines.append("=" * LINE_WIDTH)
    lines.append(f"{'FINAL BILL (Rs.)':<30}{final_amount:>16.2f}")
    lines.append("=" * LINE_WIDTH)
    lines.append("Thank you! Please visit again.".center(LINE_WIDTH))
    lines.append("=" * LINE_WIDTH)
    return "\n".join(lines)


def generate_bill(order, customer_name):
    """Print the formatted receipt on the screen."""
    if not order:
        print("\nCannot generate a bill. The order is empty.")
        return
    print("\n" + build_receipt(order, customer_name))


def save_order(order, customer_name):
    """Append the receipt to orders.txt. Returns True if saved."""
    if not order:
        print("\nNothing to save. The order is empty.")
        return False

    try:
        # "a" = append mode, so old orders are never erased
        with open(ORDER_FILE, "a", encoding="utf-8") as file:
            file.write(build_receipt(order, customer_name))
            file.write("\n\n")
        print(f"\nOrder saved successfully to '{ORDER_FILE}'.")
        return True
    except OSError as error:
        print(f"\nSorry, the order could not be saved: {error}")
        return False


def show_main_menu():
    """Print the list of choices for the user."""
    print("\n" + "=" * LINE_WIDTH)
    print("MAIN MENU".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)
    print("1. View Menu")
    print("2. Place Order")
    print("3. View Order")
    print("4. Remove Item")
    print("5. Generate Bill")
    print("6. Save Order")
    print("7. Exit")
    print("-" * LINE_WIDTH)


def main():
    """Program starts here: shows the main menu in a loop."""
    print("=" * LINE_WIDTH)
    print("WELCOME TO THE CANTEEN".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)

    customer_name = input("Enter customer name: ").strip()
    if customer_name == "":
        customer_name = "Guest"

    order = {}          # empty order: item ID -> quantity
    order_saved = True  # becomes False when there are unsaved items

    while True:
        show_main_menu()

        # Validate the main-menu choice
        try:
            choice = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Invalid choice! Please enter a number from 1 to 7.")
            continue

        if choice == 1:
            display_menu()
        elif choice == 2:
            place_order(order)
            order_saved = False
        elif choice == 3:
            view_order(order)
        elif choice == 4:
            remove_item(order)
            order_saved = False
        elif choice == 5:
            generate_bill(order, customer_name)
        elif choice == 6:
            if save_order(order, customer_name):
                order_saved = True
                order.clear()  # ready for the next order
                print("Order cleared. You can start a new order.")
        elif choice == 7:
            if order and not order_saved:
                answer = input("You have an unsaved order. Exit anyway? (y/n): ")
                if answer.strip().lower() != "y":
                    continue
            print("\nThank you for using the Canteen System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 7.")


# Run main() only when this file is run directly
if __name__ == "__main__":
    main()
