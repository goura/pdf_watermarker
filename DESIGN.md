# PDF Watermarker - Technical Design

## Overview
A simple desktop application that adds text watermarks to PDF files with optional password protection. Built with Python and Tkinter.

## Core Components

### 1. GUI (Tkinter)
- Simple file selection and input fields
- Transparency slider for watermark
- Password protection toggle
- Error handling with message boxes

### 2. PDF Processing
- Uses PyPDF2 for PDF manipulation
- Uses ReportLab for watermark creation
- Handles PDF encryption for password protection

## Key Features
- Text watermarking with adjustable transparency
- Password protection for output PDFs
- Non-ASCII character validation
- Simple and intuitive interface

## Dependencies
- Python 3.13+
- PyPDF2
- ReportLab
- Tkinter (built-in)

## Future Improvements
- Image watermark support
- Batch processing
- Progress indicators
- More watermark customization options 