"""
Command-line argument parsing and CLI mode execution.
"""

import sys
import os
import argparse
import logging
from .csv_reader import read_csv_file
from .xml_builder import build_sepa_xml

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='CSV to SEPA XML Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Start GUI
  %(prog)s --diagnostics                # Check system compatibility
  %(prog)s --cli input.csv output.xml   # Convert without GUI

For macOS troubleshooting, see MACOS_TKINTER_ANALYSIS.md
        """
    )

    parser.add_argument(
        '--cli',
        nargs=2,
        metavar=('INPUT', 'OUTPUT'),
        help='Run in CLI mode: --cli input.csv output.xml'
    )

    parser.add_argument(
        '--diagnostics',
        action='store_true',
        help='Print system diagnostics and exit'
    )

    parser.add_argument(
        '--debtor-name',
        default=None,
        help='Override company/debtor name'
    )

    parser.add_argument(
        '--debtor-iban',
        default=None,
        help='Override company/debtor IBAN'
    )

    parser.add_argument(
        '--debtor-bic',
        default=None,
        help='Override company/debtor BIC'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Generate XML even if validation warnings exist'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress non-error output'
    )

    return parser.parse_args()


def run_cli_mode(input_file, output_file, debtor_name=None, debtor_iban=None, debtor_bic=None, quiet=False):
    """
    Run the converter in headless CLI mode.

    Arguments:
        input_file: Path to input CSV
        output_file: Path for output XML
        debtor_name: Optional override for company name
        debtor_iban: Optional override for company IBAN
        debtor_bic: Optional override for company BIC
        quiet: If True, suppress console output

    Returns:
        Exit code (0 for success, 1 for error)
    """
    from .config import DEFAULT_COMPANY_NAME
    
    logger.info(f"CLI Mode: Converting {input_file} -> {output_file}")

    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        logger.error(f"Input file not found: {input_file}")
        return 1

    try:
        # Read and validate
        payments = read_csv_file(input_file)

        if not payments:
            print("ERROR: CSV file is empty or has no valid data")
            logger.error("Empty CSV file")
            return 1

        # Generate XML
        xml_content = build_sepa_xml(
            payments,
            company_name=debtor_name,
            company_iban=debtor_iban,
            company_bic=debtor_bic
        )

        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        # Report success
        total = sum(float(p.get('amount', 0)) for p in payments)
        company_name = debtor_name or DEFAULT_COMPANY_NAME

        if not quiet:
            print(f"\nSUCCESS: SEPA XML created")
            print(f"  Input:    {input_file}")
            print(f"  Output:   {output_file}")
            print(f"  Payments: {len(payments)}")
            print(f"  Total:    EUR {total:,.2f}")
            print(f"  Debtor:   {company_name}")

        logger.info(f"Successfully created {output_file}")
        return 0

    except FileNotFoundError as e:
        print(f"ERROR: File not found: {e}")
        logger.exception("File not found")
        return 1
    except ValueError as e:
        print(f"ERROR: Invalid data: {e}")
        logger.exception("Validation error")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        logger.exception("Unexpected error in CLI mode")
        return 1
