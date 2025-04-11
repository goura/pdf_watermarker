# PDF Watermarker

A simple GUI application to add text watermarks to PDF files with optional password protection.

## Features

- Add text watermarks to PDF files
- Optional password protection for output PDFs
- Simple and intuitive GUI interface

## Installation

1. Make sure you have Python 3.13 or higher installed
2. Make sure you have Tkinter (like `brew install python-tk@3.13`)
2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install the required dependencies:
   ```bash
   poetry install
   ```

## Usage

1. Run the application:
   ```bash
   poetry run python pdf_watermarker.py
   ```
2. Select an input PDF file
3. Enter the watermark text
4. (Optional) Enable password protection and set a password
5. Click "Generate Watermarked PDF"
6. Choose where to save the output file
