# Tests Directory

This directory contains test files for the SEPA converter.

## Files

- **test_validation_functions.py** - Standalone tests for IBAN/BIC validation functions

## Running Tests

### Manual Testing

```bash
# From project root
python3 tests/test_validation_functions.py
```

### With pytest (if installed)

```bash
# Install pytest first
pip3 install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_validation_functions.py
```

## Test Coverage

Current tests cover:
- IBAN validation (format, length, checksum)
- BIC validation (format, length)
- Amount validation (positive, decimal places)

## Adding New Tests

When adding new test files, follow these conventions:
- Prefix test files with `test_`
- Use descriptive test function names: `test_validate_iban_correct_checksum()`
- Include both positive (valid) and negative (invalid) test cases
- Document expected behavior in docstrings
