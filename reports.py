import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class GSTReports:
    def __init__(self, parent, db_connection):
        self.parent = parent
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
    def create_reports_frame(self, parent):
        """Create the reports interface"""
        frame = ttk.Frame(parent)
        
        # Date selection
        date_frame = ttk.Frame(frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(date_frame, text="From Date:").pack(side=tk.LEFT, padx=5)
        self.from_date = ttk.Entry(date_frame)
        self.from_date.pack(side=tk.LEFT, padx=5)
        self.from_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        ttk.Label(date_frame, text="To Date:").pack(side=tk.LEFT, padx=5)
        self.to_date = ttk.Entry(date_frame)
        self.to_date.pack(side=tk.LEFT, padx=5)
        self.to_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Report buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Generate GSTR-1", command=self.generate_gstr1).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate GSTR-2", command=self.generate_gstr2).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate GSTR-3B", command=self.generate_gstr3b).pack(side=tk.LEFT, padx=5)
        
        # Report preview
        preview_frame = ttk.Frame(frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for different report views
        self.notebook = ttk.Notebook(preview_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for different report formats
        self.json_frame = ttk.Frame(self.notebook)
        self.excel_frame = ttk.Frame(self.notebook)
        self.csv_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.json_frame, text="JSON")
        self.notebook.add(self.excel_frame, text="Excel")
        self.notebook.add(self.csv_frame, text="CSV")
        
        # Add text widgets for preview
        self.json_text = tk.Text(self.json_frame, wrap=tk.WORD)
        self.json_text.pack(fill=tk.BOTH, expand=True)
        
        self.excel_text = tk.Text(self.excel_frame, wrap=tk.WORD)
        self.excel_text.pack(fill=tk.BOTH, expand=True)
        
        self.csv_text = tk.Text(self.csv_frame, wrap=tk.WORD)
        self.csv_text.pack(fill=tk.BOTH, expand=True)
        
        return frame
    
    def generate_gstr1(self):
        """Generate GSTR-1 report"""
        try:
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d')
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d')
            
            # Query outward supplies
            self.cursor.execute("""
                SELECT 
                    i.invoice_number,
                    i.invoice_date,
                    c.gstin,
                    c.name as customer_name,
                    p.hsn_code,
                    ii.quantity,
                    ii.price,
                    ii.gst_rate,
                    ii.gst_amount,
                    ii.total_amount
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN products p ON ii.product_id = p.id
                WHERE i.invoice_date BETWEEN ? AND ?
                ORDER BY i.invoice_date
            """, (from_date.date(), to_date.date()))
            
            data = self.cursor.fetchall()
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=[
                'Invoice Number', 'Date', 'GSTIN', 'Customer Name',
                'HSN Code', 'Quantity', 'Price', 'GST Rate',
                'GST Amount', 'Total Amount'
            ])
            
            # Generate JSON format
            json_data = df.to_dict(orient='records')
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(tk.END, json.dumps(json_data, indent=2))
            
            # Generate Excel format
            excel_data = df.to_string()
            self.excel_text.delete(1.0, tk.END)
            self.excel_text.insert(tk.END, excel_data)
            
            # Generate CSV format
            csv_data = df.to_csv(index=False)
            self.csv_text.delete(1.0, tk.END)
            self.csv_text.insert(tk.END, csv_data)
            
            # Save reports
            self.save_reports(df, "GSTR1")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_gstr2(self):
        """Generate GSTR-2 report"""
        try:
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d')
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d')
            
            # Query inward supplies (purchases)
            self.cursor.execute("""
                SELECT 
                    p.invoice_number,
                    p.invoice_date,
                    v.gstin,
                    v.name as vendor_name,
                    p.hsn_code,
                    p.quantity,
                    p.price,
                    p.gst_rate,
                    p.gst_amount,
                    p.total_amount
                FROM purchases p
                JOIN vendors v ON p.vendor_id = v.id
                WHERE p.invoice_date BETWEEN ? AND ?
                ORDER BY p.invoice_date
            """, (from_date.date(), to_date.date()))
            
            data = self.cursor.fetchall()
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=[
                'Invoice Number', 'Date', 'GSTIN', 'Vendor Name',
                'HSN Code', 'Quantity', 'Price', 'GST Rate',
                'GST Amount', 'Total Amount'
            ])
            
            # Generate JSON format
            json_data = df.to_dict(orient='records')
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(tk.END, json.dumps(json_data, indent=2))
            
            # Generate Excel format
            excel_data = df.to_string()
            self.excel_text.delete(1.0, tk.END)
            self.excel_text.insert(tk.END, excel_data)
            
            # Generate CSV format
            csv_data = df.to_csv(index=False)
            self.csv_text.delete(1.0, tk.END)
            self.csv_text.insert(tk.END, csv_data)
            
            # Save reports
            self.save_reports(df, "GSTR2")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_gstr3b(self):
        """Generate GSTR-3B report"""
        try:
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d')
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d')
            
            # Query summary data
            self.cursor.execute("""
                SELECT 
                    SUM(total_amount) as total_taxable_value,
                    SUM(cgst_amount) as total_cgst,
                    SUM(sgst_amount) as total_sgst,
                    SUM(igst_amount) as total_igst
                FROM invoices
                WHERE invoice_date BETWEEN ? AND ?
            """, (from_date.date(), to_date.date()))
            
            summary_data = self.cursor.fetchone()
            
            # Create summary DataFrame
            df = pd.DataFrame([{
                'Total Taxable Value': summary_data[0],
                'Total CGST': summary_data[1],
                'Total SGST': summary_data[2],
                'Total IGST': summary_data[3],
                'Total Tax': summary_data[1] + summary_data[2] + summary_data[3]
            }])
            
            # Generate JSON format
            json_data = df.to_dict(orient='records')
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(tk.END, json.dumps(json_data, indent=2))
            
            # Generate Excel format
            excel_data = df.to_string()
            self.excel_text.delete(1.0, tk.END)
            self.excel_text.insert(tk.END, excel_data)
            
            # Generate CSV format
            csv_data = df.to_csv(index=False)
            self.csv_text.delete(1.0, tk.END)
            self.csv_text.insert(tk.END, csv_data)
            
            # Save reports
            self.save_reports(df, "GSTR3B")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def save_reports(self, df, report_type):
        """Save reports in different formats"""
        try:
            # Create reports directory if it doesn't exist
            os.makedirs("reports", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"{report_type}_{timestamp}"
            
            # Save JSON
            json_path = os.path.join("reports", f"{base_filename}.json")
            df.to_json(json_path, orient='records', indent=2)
            
            # Save Excel
            excel_path = os.path.join("reports", f"{base_filename}.xlsx")
            df.to_excel(excel_path, index=False)
            
            # Save CSV
            csv_path = os.path.join("reports", f"{base_filename}.csv")
            df.to_csv(csv_path, index=False)
            
            messagebox.showinfo("Success", f"Reports saved successfully in the 'reports' directory")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving reports: {str(e)}") 