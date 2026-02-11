#!/usr/bin/env python3
"""
Backward compatibility wrapper for csv_to_sepa_xml.

This script provides the same command-line interface as the original
monolithic csv_to_sepa_xml.py, but delegates to the refactored package.

Usage: Same as before!
    python3 run_converter.py --cli input.csv output.xml
    python3 run_converter.py --diagnostics
    python3 run_converter.py  # GUI mode
"""

if __name__ == "__main__":
    from csv_to_sepa_xml.main import main
    main()
