import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class BillingModule:
    def __init__(self, parent, db_connection):
        self.parent = parent
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
        # GST rates
        self.gst_rates = [0, 5, 12, 18, 28]
        
    def create_billing_frame(self, parent):
        """Create the main billing interface"""
        frame = ttk.Frame(parent)
        
        # Left side - Customer and Product selection
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Customer selection
        ttk.Label(left_frame, text="Select Customer:").pack(anchor=tk.W)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(left_frame, textvariable=self.customer_var)
        self.customer_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Product selection
        ttk.Label(left_frame, text="Select Product:").pack(anchor=tk.W)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(left_frame, textvariable=self.product_var)
        self.product_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Quantity
        ttk.Label(left_frame, text="Quantity:").pack(anchor=tk.W)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(left_frame, textvariable=self.quantity_var).pack(fill=tk.X, pady=(0, 10))
        
        # Add to invoice button
        ttk.Button(left_frame, text="Add to Invoice", command=self.add_to_invoice).pack(pady=10)
        
        # Right side - Invoice items
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Invoice items treeview
        columns = ("Product", "Quantity", "Price", "GST Rate", "GST Amount", "Total")
        self.items_tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame for totals and buttons
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Totals
        totals_frame = ttk.Frame(bottom_frame)
        totals_frame.pack(side=tk.LEFT)
        
        ttk.Label(totals_frame, text="Subtotal:").grid(row=0, column=0, sticky=tk.W)
        self.subtotal_var = tk.StringVar(value="0.00")
        ttk.Label(totals_frame, textvariable=self.subtotal_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(totals_frame, text="CGST:").grid(row=1, column=0, sticky=tk.W)
        self.cgst_var = tk.StringVar(value="0.00")
        ttk.Label(totals_frame, textvariable=self.cgst_var).grid(row=1, column=1, padx=5)
        
        ttk.Label(totals_frame, text="SGST:").grid(row=2, column=0, sticky=tk.W)
        self.sgst_var = tk.StringVar(value="0.00")
        ttk.Label(totals_frame, textvariable=self.sgst_var).grid(row=2, column=1, padx=5)
        
        ttk.Label(totals_frame, text="Total:").grid(row=3, column=0, sticky=tk.W)
        self.total_var = tk.StringVar(value="0.00")
        ttk.Label(totals_frame, textvariable=self.total_var).grid(row=3, column=1, padx=5)
        
        # Buttons
        buttons_frame = ttk.Frame(bottom_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        ttk.Button(buttons_frame, text="Generate Invoice", command=self.generate_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_invoice).pack(side=tk.LEFT, padx=5)
        
        self.load_customers()
        self.load_products()
        
        return frame
    
    def load_customers(self):
        """Load customers into combobox"""
        self.cursor.execute("SELECT name FROM customers ORDER BY name")
        customers = [row[0] for row in self.cursor.fetchall()]
        self.customer_combo['values'] = customers
    
    def load_products(self):
        """Load products into combobox"""
        self.cursor.execute("SELECT name FROM products ORDER BY name")
        products = [row[0] for row in self.cursor.fetchall()]
        self.product_combo['values'] = products
    
    def add_to_invoice(self):
        """Add selected product to invoice"""
        try:
            product_name = self.product_var.get()
            quantity = int(self.quantity_var.get())
            
            # Get product details
            self.cursor.execute("""
                SELECT id, price, gst_rate FROM products WHERE name = ?
            """, (product_name,))
            product_id, price, gst_rate = self.cursor.fetchone()
            
            # Calculate amounts
            subtotal = price * quantity
            gst_amount = subtotal * (gst_rate / 100)
            total = subtotal + gst_amount
            
            # Add to treeview
            self.items_tree.insert("", tk.END, values=(
                product_name,
                quantity,
                f"{price:.2f}",
                f"{gst_rate}%",
                f"{gst_amount:.2f}",
                f"{total:.2f}"
            ))
            
            # Update totals
            self.update_totals()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_totals(self):
        """Update invoice totals"""
        subtotal = 0
        cgst = 0
        sgst = 0
        
        for item in self.items_tree.get_children():
            values = self.items_tree.item(item)['values']
            item_total = float(values[5])
            gst_amount = float(values[4])
            
            subtotal += item_total - gst_amount
            cgst += gst_amount / 2
            sgst += gst_amount / 2
        
        total = subtotal + cgst + sgst
        
        self.subtotal_var.set(f"{subtotal:.2f}")
        self.cgst_var.set(f"{cgst:.2f}")
        self.sgst_var.set(f"{sgst:.2f}")
        self.total_var.set(f"{total:.2f}")
    
    def generate_invoice(self):
        """Generate and save invoice"""
        try:
            # Create invoices directory if it doesn't exist
            os.makedirs("invoices", exist_ok=True)
            
            # Generate invoice number
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Get customer details
            customer_name = self.customer_var.get()
            self.cursor.execute("""
                SELECT id, gstin, address FROM customers WHERE name = ?
            """, (customer_name,))
            customer_id, gstin, address = self.cursor.fetchone()
            
            # Create PDF
            pdf_path = os.path.join("invoices", f"{invoice_number}.pdf")
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Add invoice header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "INVOICE")
            
            # Add invoice details
            c.setFont("Helvetica", 12)
            c.drawString(50, 720, f"Invoice Number: {invoice_number}")
            c.drawString(50, 700, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
            
            # Add customer details
            c.drawString(50, 670, f"Customer: {customer_name}")
            c.drawString(50, 650, f"GSTIN: {gstin}")
            c.drawString(50, 630, f"Address: {address}")
            
            # Add items table
            y = 580
            c.drawString(50, y, "Product")
            c.drawString(200, y, "Qty")
            c.drawString(250, y, "Price")
            c.drawString(300, y, "GST")
            c.drawString(350, y, "Total")
            
            y -= 20
            for item in self.items_tree.get_children():
                values = self.items_tree.item(item)['values']
                c.drawString(50, y, values[0])
                c.drawString(200, y, str(values[1]))
                c.drawString(250, y, values[2])
                c.drawString(300, y, values[4])
                c.drawString(350, y, values[5])
                y -= 20
            
            # Add totals
            y -= 20
            c.drawString(250, y, "Subtotal:")
            c.drawString(350, y, self.subtotal_var.get())
            y -= 20
            c.drawString(250, y, "CGST:")
            c.drawString(350, y, self.cgst_var.get())
            y -= 20
            c.drawString(250, y, "SGST:")
            c.drawString(350, y, self.sgst_var.get())
            y -= 20
            c.drawString(250, y, "Total:")
            c.drawString(350, y, self.total_var.get())
            
            c.save()
            
            # Save to database
            self.cursor.execute("""
                INSERT INTO invoices (
                    invoice_number, customer_id, invoice_date,
                    total_amount, cgst_amount, sgst_amount, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice_number, customer_id, datetime.now().date(),
                float(self.total_var.get()),
                float(self.cgst_var.get()),
                float(self.sgst_var.get()),
                "PAID"
            ))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", f"Invoice generated successfully: {pdf_path}")
            self.clear_invoice()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_invoice(self):
        """Clear the current invoice"""
        self.items_tree.delete(*self.items_tree.get_children())
        self.update_totals()
        self.quantity_var.set("1") 