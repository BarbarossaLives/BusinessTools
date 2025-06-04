import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from checkbook import load_transactons, add_transaction, calculate_balance

class CheckbookApp(ttk.Window):
    def __init__(self):
        super().__init__(title = "Checkbook System", themename="superhero", size=(900,800))
        self.transactions = load_transactons()

        self.create_widgets()
        self.update_balance()
        self.update_transactions_list()

    def create_widgets(self):