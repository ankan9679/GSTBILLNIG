import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3
from datetime import datetime
import os
from PIL import Image, ImageTk

class GSTBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Billing & Accounting Software")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.init_database()
        
        # Create main menu
        self.create_menu()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create main tabs
        self.create_dashboard_tab()
        self.create_billing_tab()
        self.create_accounting_tab()
        self.create_inventory_tab()
        self.create_reports_tab()
        
    def init_database(self):
        """Initialize SQLite database and create necessary tables"""
        db_path = os.path.join('data', 'gst_billing.db')
        os.makedirs('data', exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Create necessary tables
        self.create_tables()
        
    def create_tables(self):
        """Create all necessary database tables"""
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gstin TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hsn_code TEXT,
                gst_rate REAL,
                price REAL,
                stock_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Invoices table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE,
                customer_id INTEGER,
                invoice_date DATE,
                total_amount REAL,
                cgst_amount REAL,
                sgst_amount REAL,
                igst_amount REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Invoice items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                gst_rate REAL,
                gst_amount REAL,
                total_amount REAL,
                FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        self.conn.commit()
        
    def create_menu(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Invoice", command=self.new_invoice)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="GSTR-1", command=self.generate_gstr1)
        reports_menu.add_command(label="GSTR-2", command=self.generate_gstr2)
        reports_menu.add_command(label="GSTR-3B", command=self.generate_gstr3b)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_dashboard_tab(self):
        """Create the dashboard tab with summary information"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Add dashboard widgets here
        
    def create_billing_tab(self):
        """Create the billing tab for invoice management"""
        billing_frame = ttk.Frame(self.notebook)
        self.notebook.add(billing_frame, text="Billing")
        
        # Add billing widgets here
        
    def create_accounting_tab(self):
        """Create the accounting tab for financial management"""
        accounting_frame = ttk.Frame(self.notebook)
        self.notebook.add(accounting_frame, text="Accounting")
        
        # Add accounting widgets here
        
    def create_inventory_tab(self):
        """Create the inventory management tab"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")
        
        # Add inventory widgets here
        
    def create_reports_tab(self):
        """Create the reports tab for GST reports"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Add reports widgets here
        
    def new_invoice(self):
        """Create a new invoice"""
        pass
        
    def export_data(self):
        """Export data to Excel/CSV"""
        pass
        
    def generate_gstr1(self):
        """Generate GSTR-1 report"""
        pass
        
    def generate_gstr2(self):
        """Generate GSTR-2 report"""
        pass
        
    def generate_gstr3b(self):
        """Generate GSTR-3B report"""
        pass
        
    def show_about(self):
        """Show about dialog"""
        pass

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Using a modern theme
    app = GSTBillingApp(root)
    root.mainloop() 