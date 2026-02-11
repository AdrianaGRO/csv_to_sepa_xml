"""
Configuration constants and settings for the SEPA converter.
"""

import os
import logging

# ============================================================================
# COMPANY CONFIGURATION - Default values (can be overridden via CLI or GUI)
# ============================================================================

DEFAULT_COMPANY_NAME = "Your Company Name"
DEFAULT_COMPANY_IBAN = "DE89370400440532013000"
DEFAULT_COMPANY_BIC = "COBADEFFXXX"

# ============================================================================
# SEPA COUNTRY CODES - IBAN lengths by country
# ============================================================================

# SEPA country codes mapped to their required IBAN lengths
SEPA_COUNTRY_IBAN_LENGTHS = {
    'AD': 24,  # Andorra
    'AL': 28,  # Albania
    'AT': 20,  # Austria
    'BE': 16,  # Belgium
    'BG': 22,  # Bulgaria
    'CH': 21,  # Switzerland
    'CY': 28,  # Cyprus
    'CZ': 24,  # Czech Republic
    'DE': 22,  # Germany
    'DK': 18,  # Denmark
    'EE': 20,  # Estonia
    'ES': 24,  # Spain
    'FI': 18,  # Finland
    'FR': 27,  # France
    'GB': 22,  # United Kingdom
    'GI': 23,  # Gibraltar
    'GR': 27,  # Greece
    'HR': 21,  # Croatia
    'HU': 28,  # Hungary
    'IE': 22,  # Ireland
    'IS': 26,  # Iceland
    'IT': 27,  # Italy
    'LI': 21,  # Liechtenstein
    'LT': 20,  # Lithuania
    'LU': 20,  # Luxembourg
    'LV': 21,  # Latvia
    'MC': 27,  # Monaco
    'MD': 24,  # Moldova
    'ME': 22,  # Montenegro
    'MK': 19,  # North Macedonia
    'MT': 31,  # Malta
    'NL': 18,  # Netherlands
    'NO': 15,  # Norway
    'PL': 28,  # Poland
    'PT': 25,  # Portugal
    'RO': 24,  # Romania
    'RS': 22,  # Serbia
    'SE': 24,  # Sweden
    'SI': 19,  # Slovenia
    'SK': 24,  # Slovakia
    'SM': 27,  # San Marino
    'VA': 22,  # Vatican City State
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(quiet=False):
    """
    Configure logging for the application.
    
    Args:
        quiet: If True, only log to file (no console output)
    
    Returns:
        The configured logger instance
    """
    # Determine log file location (same directory as script)
    from . import __file__ as pkg_file
    pkg_dir = os.path.dirname(os.path.abspath(pkg_file))
    parent_dir = os.path.dirname(pkg_dir)
    log_file = os.path.join(parent_dir, 'sepa_converter.log')
    
    # Configure logging handlers
    handlers = [logging.FileHandler(log_file)]
    if not quiet:
        handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True  # Force reconfiguration
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger
