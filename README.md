# GST Billing & Accounting Software

A comprehensive desktop application for managing GST billing, accounting, and inventory management. Built with Python and Tkinter, this application provides a complete solution for businesses to manage their GST compliance requirements.

## Features

### 1. Core Functionality
- **Billing System**
  - Customer database management
  - Product & service management with HSN/SAC codes
  - GST slab configuration (5%, 12%, 18%, 28%)
  - Generate GST-compliant invoices with IGST, CGST, SGST breakdown
  - Print and export invoices as PDF

- **Accounting**
  - Record payments, expenses, purchase bills
  - Ledger for sales, purchases, expenses, taxes
  - Track receivables & payables
  - Daily, monthly, and yearly summaries

- **Inventory Management**
  - Track stock in/out
  - Low stock alerts
  - Stock movement history

### 2. GST Reporting
- Auto-generate GST reports:
  - GSTR-1 (Outward Supplies)
  - GSTR-2A/GSTR-2 (Purchases)
  - GSTR-3B (Summary Return)
- Export reports in JSON, Excel, and CSV formats
- Compatible with GST portal upload

### 3. Data Management
- Local SQLite database
- Secure data storage
- Backup and export functionality

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gst-billing-app.git
   cd gst-billing-app
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Initial Setup:
   - Add your business details
   - Configure GST rates
   - Add customers and products

3. Daily Operations:
   - Create invoices
   - Record payments
   - Manage inventory
   - Generate reports

## Directory Structure

```
gst-billing-app/
├── data/              # SQLite database and data files
├── invoices/          # Generated invoice PDFs
├── reports/           # Generated GST reports
├── main.py           # Main application file
├── billing.py        # Billing module
├── data_management.py # Data management module
├── inventory.py      # Inventory management module
├── reports.py        # GST reports module
└── requirements.txt  # Python dependencies
```

## Database Schema

### Customers Table
- id (PRIMARY KEY)
- name
- gstin
- address
- phone
- email
- created_at

### Products Table
- id (PRIMARY KEY)
- name
- hsn_code
- gst_rate
- price
- stock_quantity
- min_stock_level
- created_at

### Invoices Table
- id (PRIMARY KEY)
- invoice_number
- customer_id (FOREIGN KEY)
- invoice_date
- total_amount
- cgst_amount
- sgst_amount
- igst_amount
- status
- created_at

### Invoice Items Table
- id (PRIMARY KEY)
- invoice_id (FOREIGN KEY)
- product_id (FOREIGN KEY)
- quantity
- price
- gst_rate
- gst_amount
- total_amount

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Built with Python and Tkinter
- Uses SQLite for data storage
- ReportLab for PDF generation
- Pandas for data manipulation and export 