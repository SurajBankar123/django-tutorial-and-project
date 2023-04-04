import sqlite3
import tkinter as tk
from tkinter import messagebox

class Menu:
    def __init__(self):
        self.dishes = {'Spaghetti': 10.99, 'Pizza': 12.99, 'Burger': 8.99}

class Order:
    def __init__(self, menu):
        self.menu = menu
        self.order = []

    def add_dish(self, dish, quantity):
        if dish not in self.menu.dishes:
            messagebox.showerror('Error', 'Sorry, that dish is not on the menu.')
        else:
            self.order.append((dish, quantity))

    def remove_dish(self, dish):
        for i, item in enumerate(self.order):
            if item[0] == dish:
                del self.order[i]
                break

    def calculate_total(self):
        total = 0
        for dish, quantity in self.order:
            total += self.menu.dishes[dish] * quantity
        return total

    def clear_order(self):
        self.order.clear()

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('orders.db')
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      dish TEXT,
                      quantity INTEGER,
                      total REAL)''')
        self.conn.commit()

    def insert_order(self, order):
        c = self.conn.cursor()
        for dish, quantity in order.order:
            total = order.menu.dishes[dish] * quantity
            c.execute('INSERT INTO orders (dish, quantity, total) VALUES (?, ?, ?)', (dish, quantity, total))
        self.conn.commit()

    def retrieve_orders(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM orders')
        orders = c.fetchall()
        return orders

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.menu = Menu()
        self.order = Order(self.menu)
        self.database = Database()

        self.dish_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.total_var = tk.StringVar()
        self.order_listbox = tk.Listbox(root)
        self.populate_order_listbox()

        dish_label = tk.Label(root, text='Dish:')
        dish_label.grid(row=0, column=0, padx=5, pady=5)
        dish_entry = tk.Entry(root, textvariable=self.dish_var)
        dish_entry.grid(row=0, column=1, padx=5, pady=5)
        quantity_label = tk.Label(root, text='Quantity:')
        quantity_label.grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(root, textvariable=self.quantity_var)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        add_button = tk.Button(root, text='Add', command=self.add_dish)
        add_button.grid(row=2, column=0, padx=5, pady=5)
        remove_button = tk.Button(root, text='Remove', command=self.remove_dish)
        remove_button.grid(row=2, column=1, padx=5, pady=5)
        clear_button = tk.Button(root, text='Clear', command=self.clear_order)
        clear_button.grid(row=2, column=2, padx=5, pady=5)
        total_label = tk.Label(root,        textvariable=self.total_var)
        total_label.grid(row=3, column=0, padx=5, pady=5)

        self.order_listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        save_button = tk.Button(root, text='Save Order', command=self.save_order)
        save_button.grid(row=5, column=0, padx=5, pady=5)
        view_button = tk.Button(root, text='View Orders', command=self.view_orders)
        view_button.grid(row=5, column=1, padx=5, pady=5)
        exit_button = tk.Button(root, text='Exit', command=root.quit)
        exit_button.grid(row=5, column=2, padx=5, pady=5)

    def add_dish(self):
        dish = self.dish_var.get()
        quantity = self.quantity_var.get()
        self.order.add_dish(dish, quantity)
        self.update_total_var()
        self.populate_order_listbox()

    def remove_dish(self):
        dish = self.order_listbox.get(tk.ACTIVE)
        self.order.remove_dish(dish)
        self.update_total_var()
        self.populate_order_listbox()

    def clear_order(self):
        self.order.clear_order()
        self.update_total_var()
        self.populate_order_listbox()

    def update_total_var(self):
        total = self.order.calculate_total()
        self.total_var.set('Total: $%.2f' % total)

    def populate_order_listbox(self):
        self.order_listbox.delete(0, tk.END)
        for dish, quantity in self.order.order:
            self.order_listbox.insert(tk.END, '%s x%d' % (dish, quantity))

    def save_order(self):
        self.database.insert_order(self.order)
        messagebox.showinfo('Success', 'Order saved successfully.')

    def view_orders(self):
        orders = self.database.retrieve_orders()
        order_summary = ''
        for order in orders:
            order_summary += 'Dish: %s, Quantity: %d, Total: $%.2f\n' % (order[1], order[2], order[3])
        if order_summary == '':
            order_summary = 'No orders found.'
        messagebox.showinfo('Orders', order_summary)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Restaurant App')
    app = RestaurantApp(root)
    root.mainloop()
