import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
import logging
from typing import Optional, Tuple, BinaryIO
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class WatermarkConfig:
    """Configuration for watermark creation."""
    text: str
    alpha: float
    font_size: int = 40
    max_length: int = 20
    min_font_size: int = 20

class PDFWatermarker:
    """A GUI application for adding watermarks to PDF files."""
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the PDFWatermarker application.
        
        Args:
            root: The root tkinter window
        """
        self.root = root
        self.root.title("PDF Watermarker")
        self.root.geometry("500x500")
        
        # Variables
        self.input_file = tk.StringVar()
        self.watermark_text = tk.StringVar()
        self.password = tk.StringVar()
        self.use_password = tk.BooleanVar(value=False)
        self.alpha_value = tk.DoubleVar(value=0.2)
        
        self.create_widgets()
    
    def contains_non_ascii(self, text: str) -> bool:
        """
        Check if text contains non-ASCII characters.
        
        Args:
            text: The text to check
            
        Returns:
            bool: True if text contains non-ASCII characters, False otherwise
        """
        return not all(ord(char) < 128 for char in text)
    
    def create_widgets(self) -> None:
        """Create and layout the GUI widgets."""
        # Input PDF selection
        tk.Label(self.root, text="Input PDF:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.input_file, width=50).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_file).pack(pady=5)
        
        # Watermark text
        tk.Label(self.root, text="Watermark Text:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.watermark_text, width=50).pack(pady=5)
        
        # Alpha slider
        alpha_frame = tk.Frame(self.root)
        alpha_frame.pack(pady=10)
        tk.Label(alpha_frame, text="Transparency:").pack(side=tk.LEFT)
        self.alpha_label = tk.Label(alpha_frame, text="0.2")
        self.alpha_label.pack(side=tk.RIGHT, padx=5)
        tk.Scale(
            alpha_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.alpha_value,
            command=self.update_alpha_label
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password protection
        tk.Checkbutton(self.root, text="Password Protect", variable=self.use_password).pack(pady=5)
        tk.Label(self.root, text="Password:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show="*", width=50).pack(pady=5)
        
        # Process button
        tk.Button(self.root, text="Generate Watermarked PDF", command=self.process_pdf).pack(pady=20)
    
    def update_alpha_label(self, value: str) -> None:
        """
        Update the alpha value label.
        
        Args:
            value: The new alpha value as a string
        """
        self.alpha_label.config(text=f"{float(value):.1f}")
    
    def browse_file(self) -> None:
        """Open a file dialog to select a PDF file."""
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.input_file.set(filename)
    
    def create_watermark(self, config: WatermarkConfig) -> BinaryIO:
        """
        Create a watermark PDF page.
        
        Args:
            config: Watermark configuration
            
        Returns:
            BinaryIO: A BytesIO object containing the watermark PDF
        """
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        
        # Calculate font size based on text length
        if len(config.text) > config.max_length:
            font_size = config.font_size * (config.max_length / len(config.text))
            font_size = max(font_size, config.min_font_size)
        else:
            font_size = config.font_size
        
        # Set font and properties
        c.setFont("Helvetica", font_size)
        c.setFillColorRGB(0.5, 0.5, 0.5, alpha=config.alpha)
        
        # Rotate text and position in center
        c.rotate(45)
        c.drawString(200, 100, config.text)
        
        c.save()
        packet.seek(0)
        return packet
    
    def validate_inputs(self) -> Tuple[bool, str]:
        """
        Validate user inputs.
        """
        if not self.input_file.get():
            return False, "Please select an input PDF file"
        
        if not self.watermark_text.get():
            return False, "Please enter watermark text"
        
        if self.use_password.get() and not self.password.get():
            return False, "Please enter a password"
        
        if self.contains_non_ascii(self.watermark_text.get()):
            if not messagebox.askyesno(
                "Warning",
                "The watermark text contains non-ASCII characters. "
                "This may result in incorrect display. Continue anyway?"
            ):
                return False, "Operation cancelled by user"
        
        return True, ""
    
    def process_pdf(self) -> None:
        """Process the PDF file and add the watermark."""
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
        
        try:
            # Create watermark configuration
            config = WatermarkConfig(
                text=self.watermark_text.get(),
                alpha=self.alpha_value.get()
            )
            
            # Create watermark
            watermark_packet = self.create_watermark(config)
            
            # Read input PDF
            reader = PdfReader(self.input_file.get())
            writer = PdfWriter()
            
            # Apply watermark to each page
            watermark_page = PdfReader(watermark_packet).pages[0]
            
            for page in reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            # Set password if required
            if self.use_password.get():
                writer.encrypt(self.password.get())
            
            # Save the output file
            output_file = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Watermarked PDF"
            )
            
            if output_file:
                with open(output_file, "wb") as output_stream:
                    writer.write(output_stream)
                messagebox.showinfo("Success", "Watermarked PDF created successfully!")
                logger.info(f"Successfully created watermarked PDF: {output_file}")
        
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logger.error(error_msg, exc_info=True)
            messagebox.showerror("Error", error_msg)

def main() -> None:
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFWatermarker(root)
    root.mainloop()

if __name__ == "__main__":
    main() 