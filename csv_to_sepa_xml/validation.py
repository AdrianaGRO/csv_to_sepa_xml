"""
Validation functions for IBAN, BIC, and payment amounts.
"""

import logging
from .config import SEPA_COUNTRY_IBAN_LENGTHS

logger = logging.getLogger(__name__)


def validate_iban(iban, name=""):
    """
    Validate IBAN format, country code, length, and check digit.
    
    Args:
        iban: The IBAN string to validate
        name: Optional name for better error messages
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if empty
    if not iban or not iban.strip():
        return False, "IBAN is empty"
    
    # Remove any whitespace (though we expect none)
    iban = iban.strip().replace(' ', '')
    
    # Check if contains only uppercase letters and digits
    if not iban.isalnum() or not iban.isupper():
        return False, "IBAN must contain only uppercase letters and digits (no spaces or special characters)"
    
    # Check minimum length (shortest IBAN is NO with 15 chars)
    if len(iban) < 15:
        return False, f"IBAN too short (got {len(iban)} chars, minimum is 15)"
    
    # Extract country code (first 2 characters)
    country_code = iban[:2]
    
    # Check if country code is valid
    if country_code not in SEPA_COUNTRY_IBAN_LENGTHS:
        return False, f"Invalid or unsupported SEPA country code: {country_code}"
    
    # Check exact length for the country
    expected_length = SEPA_COUNTRY_IBAN_LENGTHS[country_code]
    actual_length = len(iban)
    if actual_length != expected_length:
        return False, f"Wrong length for {country_code} (expected {expected_length} chars, got {actual_length})"
    
    # ISO 7064 MOD-97-10 check digit validation
    # Move first 4 characters to the end
    rearranged = iban[4:] + iban[:4]
    
    # Replace letters with numbers (A=10, B=11, ..., Z=35)
    numeric_string = ""
    for char in rearranged:
        if char.isdigit():
            numeric_string += char
        else:
            # A=10, B=11, ..., Z=35
            numeric_string += str(ord(char) - ord('A') + 10)
    
    # Convert to integer and check modulo 97
    try:
        numeric_value = int(numeric_string)
        if numeric_value % 97 != 1:
            return False, "Invalid IBAN check digit (MOD-97 validation failed)"
    except ValueError:
        return False, "IBAN contains invalid characters for check digit calculation"
    
    return True, None


def validate_bic(bic, iban="", name=""):
    """
    Validate BIC/SWIFT code format.
    
    Args:
        bic: The BIC string to validate
        iban: Optional IBAN for country code cross-check
        name: Optional name for better error messages
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if empty
    if not bic or not bic.strip():
        return False, "BIC is empty"
    
    bic = bic.strip().upper()
    
    # BIC must be exactly 8 or 11 characters
    if len(bic) not in [8, 11]:
        return False, f"BIC must be exactly 8 or 11 characters (got {len(bic)})"
    
    # Check if alphanumeric
    if not bic.isalnum():
        return False, "BIC must contain only letters and digits"
    
    # Positions 1-4: Bank code (must be letters)
    if not bic[:4].isalpha():
        return False, "BIC positions 1-4 (bank code) must be letters"
    
    # Positions 5-6: Country code (must be letters)
    if not bic[4:6].isalpha():
        return False, "BIC positions 5-6 (country code) must be letters"
    
    # Positions 7-8: Location code (alphanumeric)
    if not bic[6:8].isalnum():
        return False, "BIC positions 7-8 (location code) must be alphanumeric"
    
    # If 11 characters, positions 9-11: Branch code (alphanumeric)
    if len(bic) == 11 and not bic[8:11].isalnum():
        return False, "BIC positions 9-11 (branch code) must be alphanumeric"
    
    # Cross-check country code with IBAN if provided
    if iban and len(iban) >= 2:
        iban_country = iban[:2].upper()
        bic_country = bic[4:6].upper()
        if iban_country != bic_country:
            logger.warning(f"BIC country code ({bic_country}) does not match IBAN country code ({iban_country}) for {name}")
            # Note: This is a warning, not an error, as some cross-border scenarios might be valid
    
    return True, None


def validate_amount(amount_str, name=""):
    """
    Validate payment amount.
    
    Args:
        amount_str: The amount as a string
        name: Optional name for better error messages
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None, parsed_amount: float or None)
    """
    # Check if empty
    if not amount_str or not str(amount_str).strip():
        return False, "Amount is empty", None
    
    try:
        amount = float(str(amount_str).strip())
    except ValueError:
        return False, f"Amount is not a valid number: {amount_str}", None
    
    # Check if positive
    if amount <= 0:
        return False, f"Amount must be greater than 0 (got {amount})", None
    
    # Check decimal places (max 2)
    amount_str_clean = str(amount_str).strip()
    if '.' in amount_str_clean:
        decimal_part = amount_str_clean.split('.')[1]
        if len(decimal_part) > 2:
            return False, f"Amount cannot have more than 2 decimal places (got {len(decimal_part)})", None
    
    return True, None, amount


def validate_payment_row(row, row_number):
    """
    Validate a single payment row from CSV.
    
    Args:
        row: Dictionary containing payment data
        row_number: Row number for error reporting
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
    """
    errors = []
    name = row.get('name', '').strip()
    
    # Validate name
    if not name:
        errors.append(f"Row {row_number}: Name is empty")
        name = f"Row {row_number}"  # Use row number if name is missing
    
    # Validate IBAN
    iban = row.get('iban', '').strip()
    iban_valid, iban_error = validate_iban(iban, name)
    if not iban_valid:
        errors.append(f"Invalid IBAN for '{name}': {iban} - {iban_error}")
    
    # Validate BIC
    bic = row.get('bic', '').strip()
    bic_valid, bic_error = validate_bic(bic, iban, name)
    if not bic_valid:
        errors.append(f"Invalid BIC for '{name}': {bic} - {bic_error}")
    
    # Validate amount
    amount_str = row.get('amount', '')
    amount_valid, amount_error, parsed_amount = validate_amount(amount_str, name)
    if not amount_valid:
        errors.append(f"Invalid amount for '{name}': {amount_str} - {amount_error}")
    
    # Check reference (optional but log if missing)
    reference = row.get('reference', '').strip()
    if not reference:
        logger.warning(f"Row {row_number} ('{name}'): Reference is empty")
    
    return len(errors) == 0, errors
