import os, json, sys
from datetime import datetime

if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    base_path = sys._MEIPASS
else:
    # Running as a script
    base_path = os.path.dirname(__file__)


DATA_FILE = os.path.join(base_path, "data", "transactions.json")
 
def load_transactions():
    """Load transactions from a JSON file. Return an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return[]
    
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return[]
        
def save_transactions(transactions):
    """Save the transactions list to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

def add_transaction(transactions, trans_type, catagory, description, amount):
    """Add a new transactions and save it."""
    new_entry = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "type": trans_type,
        "catagory": catagory,
        "description": description,
        "amount": amount
    }

    transactions.append(new_entry)
    save_transactions(transactions)
    return new_entry

def calculate_balance(transactions):
    """ Claculate the current balance based on all transactions"""
    balance = 0.0
    for entry in transactions:
        if entry["type"] == "income":
            balance += entry["amount"]
        elif entry["type"] == "expense":
            balance -= entry["amount"]
    return balance