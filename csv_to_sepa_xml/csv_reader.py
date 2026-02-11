"""
CSV file reading with validation.
"""

import csv
import logging
import os
from datetime import datetime
from .validation import validate_payment_row

logger = logging.getLogger(__name__)


def read_csv_file(filepath, error_report_path=None):
    """
    Read a CSV file and return a list of valid payment dictionaries.
    Invalid rows are logged and skipped. Optionally writes an error report.

    Arguments:
        filepath: The path to the CSV file (like "/Users/me/payments.csv")
        error_report_path: Optional path for CSV error report. If None, generates
                          filename based on input CSV (e.g., "payments_errors.csv")

    Returns:
        A list of dictionaries, one for each valid payment

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the CSV is malformed or has no valid rows
    """
    payments = []
    invalid_payments_data = []  # Will store (row, row_number, errors)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Check if required columns exist
            required_columns = {'name', 'iban', 'bic', 'amount', 'reference'}
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no header")
            
            missing_columns = required_columns - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")
            
            # Process each row with validation
            for row_number, row in enumerate(reader, start=2):  # Start at 2 (row 1 is header)
                is_valid, validation_errors = validate_payment_row(row, row_number)
                
                if is_valid:
                    payments.append(row)
                else:
                    invalid_payments_data.append((row, row_number, validation_errors))
                    # Log all errors for this row
                    for error in validation_errors:
                        logger.error(error)
        
        # Summary logging
        total_rows = len(payments) + len(invalid_payments_data)
        logger.info(f"Processed {total_rows} rows: {len(payments)} valid, {len(invalid_payments_data)} invalid")
        
        if len(payments) == 0:
            raise ValueError("No valid payments found in CSV file")
        
        if len(invalid_payments_data) > 0:
            logger.warning(f"Skipped {len(invalid_payments_data)} invalid payment(s)")
            
            # Generate error report
            if error_report_path is None:
                # Auto-generate error report path from input filename with timestamp
                base_name = os.path.splitext(os.path.basename(filepath))[0]
                directory = os.path.dirname(filepath) or '.'
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                error_report_path = os.path.join(directory, f"{base_name}_errors_{timestamp}.csv")
            
            write_error_report(invalid_payments_data, error_report_path, reader.fieldnames)
            logger.info(f"Error report written to: {error_report_path}")
        
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        raise
    
    return payments


def write_error_report(invalid_payments_data, output_path, original_fieldnames):
    """
    Write a CSV error report for invalid payments.
    
    Arguments:
        invalid_payments_data: List of tuples (row_dict, row_number, error_messages)
        output_path: Path where to write the error report CSV
        original_fieldnames: Original CSV column names
    """
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            # Add error columns to the original fieldnames
            fieldnames = ['row_number'] + list(original_fieldnames) + ['error_details']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for row, row_number, errors in invalid_payments_data:
                # Combine all errors into a single string
                error_text = ' | '.join(errors)
                
                # Create output row with all original fields plus error info
                output_row = {'row_number': row_number}
                output_row.update(row)
                output_row['error_details'] = error_text
                
                writer.writerow(output_row)
        
        logger.info(f"Successfully wrote {len(invalid_payments_data)} error(s) to {output_path}")
    except Exception as e:
        logger.error(f"Failed to write error report: {e}")
