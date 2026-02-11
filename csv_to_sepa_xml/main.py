#!/usr/bin/env python3
"""
CSV to SEPA XML Converter - Main Entry Point

Converts CSV payment files into SEPA-compliant XML (pain.001.001.03).
Includes macOS compatibility layer with diagnostics and CLI fallback.

Features:
- GUI mode (default): Interactive Tkinter interface
- CLI mode: Headless operation for automation/fallback
- Diagnostics mode: System compatibility check

Usage:
    python3 main.py                          # GUI mode
    python3 main.py --cli input.csv out.xml  # CLI mode
    python3 main.py --diagnostics            # Check system

The CSV file must have columns: name, iban, amount, reference, bic
"""

import sys
import os
import logging

# Minimum Python version check
MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit(f"ERROR: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required. "
             f"You have {sys.version_info.major}.{sys.version_info.minor}")

# Fix imports when running directly from package directory
if __name__ == "__main__":
    # Add parent directory to path so package can be imported
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)


def main():
    """Main entry point with mode selection."""
    # Import modules
    from csv_to_sepa_xml.cli import parse_arguments, run_cli_mode
    from csv_to_sepa_xml.diagnostics import print_diagnostics, check_tkinter_available
    from csv_to_sepa_xml.config import setup_logging
    
    # Parse arguments early
    args = parse_arguments()
    
    # Setup logging
    setup_logging(quiet=args.quiet)
    logger = logging.getLogger(__name__)
    
    # --- DIAGNOSTICS MODE ---
    if args.diagnostics:
        diag = print_diagnostics()
        sys.exit(0 if diag.get('tk_available') else 1)
    
    # --- CLI MODE ---
    if args.cli:
        input_file, output_file = args.cli
        exit_code = run_cli_mode(
            input_file,
            output_file,
            debtor_name=args.debtor_name,
            debtor_iban=args.debtor_iban,
            debtor_bic=args.debtor_bic,
            quiet=args.quiet
        )
        sys.exit(exit_code)
    
    # --- GUI MODE ---
    # Check if Tkinter is available
    tk_available, tk_error = check_tkinter_available()
    
    if not tk_available:
        print("\n" + "=" * 65)
        print("  ERROR: GUI Mode Unavailable")
        print("=" * 65)
        print(f"\n  Reason: {tk_error}")
        print("\n  Options:")
        print("    1. Use CLI mode:")
        print("       python3 main.py --cli input.csv output.xml")
        print("\n    2. Run diagnostics:")
        print("       python3 main.py --diagnostics")
        print("\n    3. Fix Tkinter (macOS):")
        print("       brew reinstall python-tk@3.11")
        print("\n    4. Or use python.org installer (includes Tcl/Tk)")
        print("\n" + "=" * 65 + "\n")
        logger.error(f"GUI unavailable: {tk_error}")
        sys.exit(1)
    
    # Import GUI module (only when we know Tkinter is available)
    try:
        from csv_to_sepa_xml.gui import start_gui
        logger.info("Tkinter initialized successfully")
    except ImportError as e:
        print(f"\nERROR: Could not import GUI module: {e}")
        logger.error(f"GUI import failed: {e}")
        sys.exit(1)
    
    # Start GUI
    exit_code = start_gui(
        debtor_name=args.debtor_name,
        debtor_iban=args.debtor_iban,
        debtor_bic=args.debtor_bic
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
