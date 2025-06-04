from checkbook import save_transactions
from checkbook import load_transactions
from checkbook import add_transaction
from checkbook import calculate_balance

def show_menu():
    print("\n === Checkbook Menu ===")
    print("1. View Balance")
    print("2. Add Income")
    print("3. Add Expense")
    print("4. View all transactions")
    print("5. Exit")

def view_transactions(transactions):
    if not transactions:
        print("\nNo transactions found.")
        return
    print("\n --- Tranactions ---")
    for entry in transactions:
        print(f"{entry['date']} | {entry['type'].upper():<7} | ${entry['amount']:.2f} | {entry['description']} | {entry['catagory']}")

def main():
    transactions = load_transactions()

    while True:
        show_menu()
        choice = input("\nChoose an option (1-5):").strip()

        if choice == "1":
            balance = calculate_balance(transactions)
            print(f"\nCurrent Balance:{balance:.2f}")
        elif choice == "2":
            description = input("Enter income description: ")
            amount = float(input("Enter amunt: "))
            catagory = input("Enter the catagory")
            add_transaction(transactions, "income", catagory, description, amount)
            print("Expense recorded.")
        
        elif choice == "3":
            description = input("Enter expense description: ")
            amount = float(input("Enter amount: "))
            catagory = input("Enter a catagory: ")
            add_transaction(transactions, "expense", description, catagory, amount)
            print("Expense recorded")

        elif choice == "4":
            view_transactions(transactions)

        elif choice == "5":
            print("Exiting ... Goodbye:")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

