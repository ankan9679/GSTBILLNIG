import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    # Clean previous build
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Create necessary directories
    os.makedirs('dist/data', exist_ok=True)
    os.makedirs('dist/invoices', exist_ok=True)
    os.makedirs('dist/reports', exist_ok=True)
    
    # PyInstaller configuration
    PyInstaller.__main__.run([
        'main.py',
        '--name=GSTBillingApp',
        '--onefile',
        '--windowed',
        '--icon=icon.ico',  # Add your icon file if available
        '--add-data=README.md;.',
        '--hidden-import=ttkthemes',
        '--hidden-import=reportlab',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=PIL',
        '--hidden-import=sqlite3',
    ])
    
    print("Build completed successfully!")
    print("Executable created in the 'dist' directory.")

if __name__ == "__main__":
    build_executable() 