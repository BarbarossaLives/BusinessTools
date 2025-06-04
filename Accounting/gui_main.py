import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, DoubleVar
from checkbook import load_transactions, save_transactions, add_transaction, calculate_balance

class CheckbookApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Checkbook Manager")
        self.geometry("1000x800")
        self.page = 0
        self.per_page = 20


        self.transactions = load_transactions()

        # Variables
        self.trans_type = StringVar(value="income")
        self.catagory = StringVar()
        self.description = StringVar()
        self.amount = DoubleVar()

        self.create_widgets()
        self.update_transaction_view()
        self.update_balance()

    def create_widgets(self):
        # --- Top Balance Display ---
        self.balance_label = ttk.Label(self, text="", font=("Arial", 20))
        self.balance_label.pack(pady=10)

        # --- Transaction Entry Form ---
        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Type").grid(row=0, column=0)
        ttk.Combobox(form, textvariable=self.trans_type, values=["income", "expense"]).grid(row=0, column=1)

        ttk.Label(form, text="Category").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.catagory).grid(row=1, column=1)

        ttk.Label(form, text="Description").grid(row=2, column=0)
        ttk.Entry(form, textvariable=self.description).grid(row=2, column=1)

        ttk.Label(form, text="Amount").grid(row=3, column=0)
        ttk.Entry(form, textvariable=self.amount).grid(row=3, column=1)

        ttk.Button(form, text="Add Transaction", command=self.add_new_transaction, bootstyle=SUCCESS).grid(row=4, columnspan=2, pady=5)

        # --- Transaction Table ---
        self.tree = ttk.Treeview(self, columns=("date", "type", "amount", "description", "catagory"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100)
        self.tree.pack(fill=BOTH, expand=True, pady=10)
        
        # --- Edit/Delete Buttons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        # --- Pagination Controls ---
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=5)

        ttk.Button(nav_frame, text="<< Previous", command=self.previous_page, bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        self.page_label = ttk.Label(nav_frame, text="")
        self.page_label.pack(side=LEFT, padx=10)
        ttk.Button(nav_frame, text="Next >>", command=self.next_page, bootstyle=SECONDARY).pack(side=LEFT, padx=5)


        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected, bootstyle=INFO).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected, bootstyle=DANGER).pack(side=LEFT, padx=10)


    def add_new_transaction(self):
        new = add_transaction(
            self.transactions,
            self.trans_type.get(),
            self.catagory.get(),
            self.description.get(),
            self.amount.get()
        )
        self.tree.insert("", END, values=(new["date"], new["type"], new["amount"], new["description"], new["catagory"]))
        self.update_balance()
        self.clear_fields()
        self.page = 0
        self.update_transaction_view()


    def clear_fields(self):
        self.catagory.set("")
        self.description.set("")
        self.amount.set(0.0)

    def update_transaction_view(self):
        self.tree.delete(*self.tree.get_children())

        start = self.page * self.per_page
        end = start + self.per_page
        page_data = self.transactions[start:end]

        for row in page_data:
            self.tree.insert("", END, values=(row["date"], row["type"], row["amount"], row["description"], row["catagory"]))

        self.page_label.config(text=f"Page {self.page + 1} of {max(1, (len(self.transactions) - 1) // self.per_page + 1)}")


    def update_balance(self):
        balance = calculate_balance(self.transactions)
        self.balance_label.config(text=f"Current Balance: ${balance:.2f}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        for item in selected:
            values = self.tree.item(item, "values")
            self.transactions = [t for t in self.transactions if not (
                t["date"] == values[0] and
                t["type"] == values[1] and
                str(t["amount"]) == values[2] and
                t["description"] == values[3] and
                t["catagory"] == values[4]
            )]
            self.tree.delete(item)

        save_transactions(self.transactions)
        self.update_balance()
        self.page = 0
        self.update_transaction_view()


    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = selected[0]
        values = self.tree.item(item, "values")

        # Fill form with selected row's values
        self.trans_type.set(values[1])
        self.catagory.set(values[4])
        self.description.set(values[3])
        self.amount.set(float(values[2]))

        # Remove it so we can re-add the updated version
        self.transactions = [t for t in self.transactions if not (
            t["date"] == values[0] and
            t["type"] == values[1] and
            str(t["amount"]) == values[2] and
            t["description"] == values[3] and
            t["catagory"] == values[4]
        )]
        self.tree.delete(item)
        save_transactions(self.transactions)
        self.update_balance()
    
    def next_page(self):
        if (self.page + 1) * self.per_page < len(self.transactions):
            self.page += 1
            self.update_transaction_view()

    def previous_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_transaction_view()



if __name__ == "__main__":
    app = CheckbookApp()
    app.mainloop()
