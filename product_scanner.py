# gui_scanner.py
import os, sys, django
import tkinter as tk
from tkinter import messagebox, ttk

# setup Django ORM environment
sys.dont_write_bytecode = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from db.models import Product


class CashRegisterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash Register Scanner")
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        self.total = 0.0
        self.scanned_items = []

        # title 
        tk.Label(root, text="Cash Register Scanner", font=("Arial", 16, "bold")).pack(pady=10)

        # input area 
        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter UPC Code:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.upc_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.upc_entry.grid(row=0, column=1)
        self.upc_entry.bind("<Return>", self.scan_product)

        tk.Button(input_frame, text="Scan", font=("Arial", 12), command=self.scan_product).grid(row=0, column=2, padx=5)

        # product list
        columns = ("Product", "Price")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        self.tree.heading("Product", text="Product Name")
        self.tree.heading("Price", text="Price ($)")
        self.tree.column("Product", width=250)
        self.tree.column("Price", width=100, anchor="center")
        self.tree.pack(pady=10)

        # total label
        self.total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)

        # buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Clear Cart", font=("Arial", 12), command=self.clear_cart, bg="tomato", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Exit", font=("Arial", 12), command=root.destroy, bg="gray", fg="white").grid(row=0, column=1, padx=5)

    # scan product
    def scan_product(self, event=None):
        upc = self.upc_entry.get().strip()
        if not upc:
            messagebox.showwarning("Input Error", "Please enter a UPC code.")
            return

        try:
            product = Product.objects.get(upc_code=upc)
            self.add_to_cart(product)
        except Product.DoesNotExist:
            messagebox.showerror("Not Found", f"No product found for UPC: {upc}")
        finally:
            self.upc_entry.delete(0, tk.END)

    # add product to cart 
    def add_to_cart(self, product):
        # add to list display
        self.tree.insert("", "end", values=(product.name, f"{product.price:.2f}"))

        # update running total
        self.total += float(product.price)
        self.update_total_label()

    # update total label
    def update_total_label(self):
        self.total_label.config(text=f"Total: ${self.total:.2f}")

    # clear all scanned items
    def clear_cart(self):
        confirm = messagebox.askyesno("Clear Cart", "Are you sure you want to clear all items?")
        if confirm:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.total = 0.0
            self.update_total_label()


if __name__ == "__main__":
    root = tk.Tk()
    app = CashRegisterGUI(root)
    root.mainloop()
