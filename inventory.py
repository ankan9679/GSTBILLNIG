import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class InventoryManagement:
    def __init__(self, parent, db_connection):
        self.parent = parent
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
    def create_inventory_frame(self, parent):
        """Create the inventory management interface"""
        frame = ttk.Frame(parent)
        
        # Create notebook for different views
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Stock overview tab
        stock_frame = ttk.Frame(notebook)
        notebook.add(stock_frame, text="Stock Overview")
        
        # Stock movement tab
        movement_frame = ttk.Frame(notebook)
        notebook.add(movement_frame, text="Stock Movement")
        
        # Low stock alerts tab
        alerts_frame = ttk.Frame(notebook)
        notebook.add(alerts_frame, text="Low Stock Alerts")
        
        # Create stock overview
        self.create_stock_overview(stock_frame)
        
        # Create stock movement
        self.create_stock_movement(movement_frame)
        
        # Create low stock alerts
        self.create_low_stock_alerts(alerts_frame)
        
        return frame
    
    def create_stock_overview(self, parent):
        """Create stock overview interface"""
        # Product list with stock levels
        columns = ("Product", "HSN Code", "Current Stock", "Min Stock", "Status")
        self.stock_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=100)
        
        self.stock_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export", command=self.export_stock).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_stock()
    
    def create_stock_movement(self, parent):
        """Create stock movement interface"""
        # Date selection
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(date_frame, text="From Date:").pack(side=tk.LEFT, padx=5)
        self.from_date = ttk.Entry(date_frame)
        self.from_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_frame, text="To Date:").pack(side=tk.LEFT, padx=5)
        self.to_date = ttk.Entry(date_frame)
        self.to_date.pack(side=tk.LEFT, padx=5)
        
        # Movement list
        columns = ("Date", "Product", "Type", "Quantity", "Reference")
        self.movement_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.movement_tree.heading(col, text=col)
            self.movement_tree.column(col, width=100)
        
        self.movement_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_movement).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export", command=self.export_movement).pack(side=tk.LEFT, padx=5)
    
    def create_low_stock_alerts(self, parent):
        """Create low stock alerts interface"""
        # Alerts list
        columns = ("Product", "Current Stock", "Min Stock", "Status")
        self.alerts_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.alerts_tree.heading(col, text=col)
            self.alerts_tree.column(col, width=100)
        
        self.alerts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_alerts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export", command=self.export_alerts).pack(side=tk.LEFT, padx=5)
    
    def refresh_stock(self):
        """Refresh stock overview"""
        try:
            self.stock_tree.delete(*self.stock_tree.get_children())
            
            self.cursor.execute("""
                SELECT 
                    name,
                    hsn_code,
                    stock_quantity,
                    min_stock_level,
                    CASE 
                        WHEN stock_quantity <= min_stock_level THEN 'Low Stock'
                        ELSE 'OK'
                    END as status
                FROM products
                ORDER BY name
            """)
            
            for row in self.cursor.fetchall():
                self.stock_tree.insert("", tk.END, values=row)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_movement(self):
        """Refresh stock movement"""
        try:
            self.movement_tree.delete(*self.movement_tree.get_children())
            
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d').date()
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d').date()
            
            # Query stock movements from invoices and purchases
            self.cursor.execute("""
                SELECT 
                    i.invoice_date as date,
                    p.name as product,
                    'OUT' as type,
                    ii.quantity,
                    i.invoice_number as reference
                FROM invoices i
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN products p ON ii.product_id = p.id
                WHERE i.invoice_date BETWEEN ? AND ?
                
                UNION ALL
                
                SELECT 
                    p.invoice_date as date,
                    p.product_name as product,
                    'IN' as type,
                    p.quantity,
                    p.invoice_number as reference
                FROM purchases p
                WHERE p.invoice_date BETWEEN ? AND ?
                
                ORDER BY date DESC
            """, (from_date, to_date, from_date, to_date))
            
            for row in self.cursor.fetchall():
                self.movement_tree.insert("", tk.END, values=row)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_alerts(self):
        """Refresh low stock alerts"""
        try:
            self.alerts_tree.delete(*self.alerts_tree.get_children())
            
            self.cursor.execute("""
                SELECT 
                    name,
                    stock_quantity,
                    min_stock_level,
                    CASE 
                        WHEN stock_quantity <= min_stock_level THEN 'Low Stock'
                        ELSE 'OK'
                    END as status
                FROM products
                WHERE stock_quantity <= min_stock_level
                ORDER BY name
            """)
            
            for row in self.cursor.fetchall():
                self.alerts_tree.insert("", tk.END, values=row)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_stock(self):
        """Export stock overview to Excel"""
        try:
            # Implementation for exporting stock data
            pass
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_movement(self):
        """Export stock movement to Excel"""
        try:
            # Implementation for exporting movement data
            pass
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_alerts(self):
        """Export low stock alerts to Excel"""
        try:
            # Implementation for exporting alerts data
            pass
        except Exception as e:
            messagebox.showerror("Error", str(e)) 