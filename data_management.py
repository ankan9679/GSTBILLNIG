import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DataManagement:
    def __init__(self, parent, db_connection):
        self.parent = parent
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
    def create_customer_frame(self, parent):
        """Create the customer management interface"""
        frame = ttk.Frame(parent)
        
        # Customer list
        list_frame = ttk.Frame(frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "GSTIN", "Phone", "Email")
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=100)
        
        self.customer_tree.pack(fill=tk.BOTH, expand=True)
        
        # Customer form
        form_frame = ttk.Frame(frame)
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Name
        ttk.Label(form_frame, text="Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var).pack(fill=tk.X, pady=(0, 10))
        
        # GSTIN
        ttk.Label(form_frame, text="GSTIN:").pack(anchor=tk.W)
        self.gstin_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.gstin_var).pack(fill=tk.X, pady=(0, 10))
        
        # Address
        ttk.Label(form_frame, text="Address:").pack(anchor=tk.W)
        self.address_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.address_var).pack(fill=tk.X, pady=(0, 10))
        
        # Phone
        ttk.Label(form_frame, text="Phone:").pack(anchor=tk.W)
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var).pack(fill=tk.X, pady=(0, 10))
        
        # Email
        ttk.Label(form_frame, text="Email:").pack(anchor=tk.W)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var).pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add", command=self.add_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        
        # Bind selection event
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        
        # Load initial data
        self.load_customers()
        
        return frame
    
    def create_product_frame(self, parent):
        """Create the product management interface"""
        frame = ttk.Frame(parent)
        
        # Product list
        list_frame = ttk.Frame(frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "HSN Code", "GST Rate", "Price", "Stock")
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=100)
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Product form
        form_frame = ttk.Frame(frame)
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Name
        ttk.Label(form_frame, text="Name:").pack(anchor=tk.W)
        self.product_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.product_name_var).pack(fill=tk.X, pady=(0, 10))
        
        # HSN Code
        ttk.Label(form_frame, text="HSN Code:").pack(anchor=tk.W)
        self.hsn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hsn_var).pack(fill=tk.X, pady=(0, 10))
        
        # GST Rate
        ttk.Label(form_frame, text="GST Rate (%):").pack(anchor=tk.W)
        self.gst_rate_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=self.gst_rate_var, values=[0, 5, 12, 18, 28]).pack(fill=tk.X, pady=(0, 10))
        
        # Price
        ttk.Label(form_frame, text="Price:").pack(anchor=tk.W)
        self.price_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.price_var).pack(fill=tk.X, pady=(0, 10))
        
        # Stock
        ttk.Label(form_frame, text="Stock Quantity:").pack(anchor=tk.W)
        self.stock_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.stock_var).pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        
        # Bind selection event
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select)
        
        # Load initial data
        self.load_products()
        
        return frame
    
    def load_customers(self):
        """Load customers into treeview"""
        self.customer_tree.delete(*self.customer_tree.get_children())
        self.cursor.execute("SELECT name, gstin, phone, email FROM customers ORDER BY name")
        for row in self.cursor.fetchall():
            self.customer_tree.insert("", tk.END, values=row)
    
    def load_products(self):
        """Load products into treeview"""
        self.product_tree.delete(*self.product_tree.get_children())
        self.cursor.execute("SELECT name, hsn_code, gst_rate, price, stock_quantity FROM products ORDER BY name")
        for row in self.cursor.fetchall():
            self.product_tree.insert("", tk.END, values=row)
    
    def add_customer(self):
        """Add a new customer"""
        try:
            self.cursor.execute("""
                INSERT INTO customers (name, gstin, address, phone, email)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.name_var.get(),
                self.gstin_var.get(),
                self.address_var.get(),
                self.phone_var.get(),
                self.email_var.get()
            ))
            self.conn.commit()
            self.load_customers()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_customer(self):
        """Update selected customer"""
        try:
            selected = self.customer_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a customer to update")
                return
            
            customer_name = self.customer_tree.item(selected[0])['values'][0]
            self.cursor.execute("""
                UPDATE customers
                SET gstin = ?, address = ?, phone = ?, email = ?
                WHERE name = ?
            """, (
                self.gstin_var.get(),
                self.address_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                customer_name
            ))
            self.conn.commit()
            self.load_customers()
            self.clear_customer_form()
            messagebox.showinfo("Success", "Customer updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_customer(self):
        """Delete selected customer"""
        try:
            selected = self.customer_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a customer to delete")
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
                customer_name = self.customer_tree.item(selected[0])['values'][0]
                self.cursor.execute("DELETE FROM customers WHERE name = ?", (customer_name,))
                self.conn.commit()
                self.load_customers()
                self.clear_customer_form()
                messagebox.showinfo("Success", "Customer deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_product(self):
        """Add a new product"""
        try:
            self.cursor.execute("""
                INSERT INTO products (name, hsn_code, gst_rate, price, stock_quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.product_name_var.get(),
                self.hsn_var.get(),
                float(self.gst_rate_var.get()),
                float(self.price_var.get()),
                int(self.stock_var.get())
            ))
            self.conn.commit()
            self.load_products()
            self.clear_product_form()
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_product(self):
        """Update selected product"""
        try:
            selected = self.product_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product to update")
                return
            
            product_name = self.product_tree.item(selected[0])['values'][0]
            self.cursor.execute("""
                UPDATE products
                SET hsn_code = ?, gst_rate = ?, price = ?, stock_quantity = ?
                WHERE name = ?
            """, (
                self.hsn_var.get(),
                float(self.gst_rate_var.get()),
                float(self.price_var.get()),
                int(self.stock_var.get()),
                product_name
            ))
            self.conn.commit()
            self.load_products()
            self.clear_product_form()
            messagebox.showinfo("Success", "Product updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_product(self):
        """Delete selected product"""
        try:
            selected = self.product_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product to delete")
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
                product_name = self.product_tree.item(selected[0])['values'][0]
                self.cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
                self.conn.commit()
                self.load_products()
                self.clear_product_form()
                messagebox.showinfo("Success", "Product deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def on_customer_select(self, event):
        """Handle customer selection"""
        selected = self.customer_tree.selection()
        if selected:
            values = self.customer_tree.item(selected[0])['values']
            self.name_var.set(values[0])
            self.gstin_var.set(values[1])
            self.phone_var.set(values[2])
            self.email_var.set(values[3])
            
            # Get address from database
            self.cursor.execute("SELECT address FROM customers WHERE name = ?", (values[0],))
            address = self.cursor.fetchone()[0]
            self.address_var.set(address)
    
    def on_product_select(self, event):
        """Handle product selection"""
        selected = self.product_tree.selection()
        if selected:
            values = self.product_tree.item(selected[0])['values']
            self.product_name_var.set(values[0])
            self.hsn_var.set(values[1])
            self.gst_rate_var.set(values[2])
            self.price_var.set(values[3])
            self.stock_var.set(values[4])
    
    def clear_customer_form(self):
        """Clear customer form fields"""
        self.name_var.set("")
        self.gstin_var.set("")
        self.address_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
    
    def clear_product_form(self):
        """Clear product form fields"""
        self.product_name_var.set("")
        self.hsn_var.set("")
        self.gst_rate_var.set("")
        self.price_var.set("")
        self.stock_var.set("") 