# Examples Directory

This directory contains sample CSV files and utilities for testing the SEPA converter.

## Files

### Sample CSV Files

- **sample_payments.csv** - Small sample with 10 payments for quick testing
- **sample_payments_10k.csv** - Large sample with 10,000 payments for load testing

### Utilities

- **generate_large_sample.py** - Script to generate large test datasets

## Usage

### Testing with Small Sample

```bash
# From project root
python3 -m csv_to_sepa_xml.main --cli examples/sample_payments.csv output.xml
```

### Load Testing with 10K Sample

```bash
# From project root
python3 -m csv_to_sepa_xml.main --cli examples/sample_payments_10k.csv output_10k.xml
```

### Generating Custom Test Data

```bash
# From project root
cd examples
python3 generate_large_sample.py
```

This creates a new `sample_payments_10k.csv` with 10,000 randomly generated valid SEPA payments across 9 European countries (DE, FR, IT, ES, NL, BE, AT, CH, RO).

## CSV Format

All sample files use the standard format:

| Column | Description | Example |
|--------|-------------|---------|
| name | Beneficiary name | Maria Schmidt |
| iban | Beneficiary IBAN | DE89370400440532013000 |
| bic | Bank BIC code | COBADEFFXXX |
| amount | Payment amount (EUR) | 1500.00 |
| reference | Payment reference | Invoice 2024-001 |
| address | Street address (optional) | Main Street 123, 10115 Berlin |
| favorite_store | Favorite store (optional) | Aldi |

**Note**: The last two columns (address, favorite_store) are optional and ignored by the converter. Only the first 5 columns are used for SEPA XML generation.
