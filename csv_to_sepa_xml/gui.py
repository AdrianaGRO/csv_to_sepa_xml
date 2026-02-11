"""
Tkinter GUI for the SEPA converter.
Only imported when Tkinter is available.
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Import tkinter - this module should only be imported when we know tkinter is available
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError as e:
    raise ImportError(f"Tkinter not available: {e}")

from .csv_reader import read_csv_file
from .xml_builder import build_sepa_xml
from .config import DEFAULT_COMPANY_NAME


class SimpleConverterApp:
    """
    Tkinter-based GUI for the SEPA converter.
    """

    def __init__(self, debtor_name=None, debtor_iban=None, debtor_bic=None):
        """
        Set up the window and all its components.
        
        Args:
            debtor_name: Optional override for company name
            debtor_iban: Optional override for company IBAN
            debtor_bic: Optional override for company BIC
        """
        self.window = tk.Tk()
        self.window.title("CSV to SEPA XML Converter")
        self.window.geometry("500x280")
        
        # Store optional overrides
        self.debtor_name = debtor_name
        self.debtor_iban = debtor_iban
        self.debtor_bic = debtor_bic

        # Try to set a minimum size
        try:
            self.window.minsize(450, 250)
        except Exception:
            pass  # Ignore if not supported

        self.selected_file = None
        self.create_widgets()
        logger.info("GUI initialized")

    def create_widgets(self):
        """Create all the buttons, labels, and other components."""
        # Add some padding around everything
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill="both", expand=True)

        # --- TITLE ---
        # Use a safe font that exists on all systems
        try:
            title = ttk.Label(
                frame,
                text="CSV to SEPA XML Converter",
                font=("TkDefaultFont", 16, "bold")
            )
        except Exception:
            # Fallback if custom font fails
            title = ttk.Label(frame, text="CSV to SEPA XML Converter")

        title.pack(pady=(0, 20))

        # --- FILE SELECTION ---
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill="x", pady=10)

        select_button = ttk.Button(
            file_frame,
            text="Select CSV File",
            command=self.select_file
        )
        select_button.pack(side="left")

        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side="left", padx=10)

        # --- GENERATE BUTTON ---
        self.generate_button = ttk.Button(
            frame,
            text="Generate SEPA XML",
            command=self.generate_xml,
            state="disabled"
        )
        self.generate_button.pack(pady=20)

        # --- STATUS MESSAGE ---
        self.status_label = ttk.Label(frame, text="")
        self.status_label.pack(pady=10)

        # --- COMPANY INFO ---
        company_name = self.debtor_name or DEFAULT_COMPANY_NAME
        info_text = f"Sending from: {company_name}"
        info_label = ttk.Label(frame, text=info_text, foreground="gray")
        info_label.pack(side="bottom", pady=10)

        # --- VERSION INFO ---
        version_text = "Run with --diagnostics to check system compatibility"
        version_label = ttk.Label(frame, text=version_text, foreground="gray")
        version_label.pack(side="bottom")

    def select_file(self):
        """Open a file dialog and let the user pick a CSV file."""
        try:
            filepath = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filepath:
                self.selected_file = filepath
                filename = os.path.basename(filepath)
                self.file_label.config(text=filename)
                self.generate_button.config(state="normal")
                self.status_label.config(text="")
                logger.info(f"Selected file: {filepath}")
        except Exception as e:
            logger.exception("File dialog error")
            messagebox.showerror("Error", f"Could not open file dialog:\n{e}")

    def generate_xml(self):
        """Read the CSV and create the XML file."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a CSV file first")
            return

        try:
            # Read CSV
            payments = read_csv_file(self.selected_file)

            if not payments:
                messagebox.showwarning("Warning", "The CSV file is empty")
                return

            # Generate XML
            xml_content = build_sepa_xml(
                payments,
                company_name=self.debtor_name,
                company_iban=self.debtor_iban,
                company_bic=self.debtor_bic
            )

            # Ask where to save
            output_path = filedialog.asksaveasfilename(
                title="Save SEPA XML",
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml")],
                initialfile=f"sepa_payment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
            )

            if output_path:
                # Write file
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(xml_content)

                # Show success
                total = sum(float(p.get('amount', 0)) for p in payments)
                self.status_label.config(
                    text=f"Created! {len(payments)} payments, total: EUR {total:,.2f}"
                )

                messagebox.showinfo(
                    "Success",
                    f"SEPA XML file created!\n\n"
                    f"Payments: {len(payments)}\n"
                    f"Total: EUR {total:,.2f}\n\n"
                    f"Saved to:\n{output_path}"
                )

                logger.info(f"Saved XML to: {output_path}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find the CSV file")
            logger.error("CSV file not found")
        except Exception as error:
            messagebox.showerror("Error", f"Something went wrong:\n{error}")
            logger.exception("XML generation failed")

    def run(self):
        """Start the application."""
        logger.info("Starting GUI mainloop")
        self.window.mainloop()


def start_gui(debtor_name=None, debtor_iban=None, debtor_bic=None):
    """
    Start the GUI application.
    
    Args:
        debtor_name: Optional override for company name
        debtor_iban: Optional override for company IBAN
        debtor_bic: Optional override for company BIC
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        app = SimpleConverterApp(debtor_name, debtor_iban, debtor_bic)
        app.run()
        return 0
    except Exception as e:
        logger.exception("GUI crashed")
        print(f"\nFATAL ERROR: {e}")
        print("Run with --diagnostics for more information")
        print("Or use --cli mode as fallback")
        return 1
