#!/usr/bin/env python3
"""Quick test of validation functions"""

from csv_to_sepa_xml import validate_iban, validate_bic, validate_amount

print('=== IBAN Validation Tests ===')
test_cases = [
    ('DE44500105175407324931', 'Valid German IBAN'),
    ('FR7630006000011234567890189', 'Valid French IBAN'),
    ('IT60X0542811101000000123456', 'Valid Italian IBAN'),
    ('DE89370400440532013001', 'Invalid check digit'),
    ('XX1234567890', 'Invalid country'),
    ('DE123', 'Too short'),
]

for iban, desc in test_cases:
    valid, error = validate_iban(iban)
    status = 'PASS' if valid else 'FAIL'
    print(f'[{status}] {desc}: {iban}')
    if error:
        print(f'      Error: {error}')

print('\n=== BIC Validation Tests ===')
bic_cases = [
    ('COBADEFFXXX', 'Valid 11-char BIC'),
    ('BNPAFRPP', 'Valid 8-char BIC'),
    ('SHORT', 'Too short'),
    ('1234DEFFXXX', 'Invalid format'),
]

for bic, desc in bic_cases:
    valid, error = validate_bic(bic)
    status = 'PASS' if valid else 'FAIL'
    print(f'[{status}] {desc}: {bic}')
    if error:
        print(f'      Error: {error}')

print('\n=== Amount Validation Tests ===')
amount_cases = [
    ('1500.00', 'Valid amount'),
    ('890', 'Valid integer'),
    ('-100', 'Negative'),
    ('0', 'Zero'),
    ('100.123', 'Too many decimals'),
]

for amt, desc in amount_cases:
    valid, error, parsed = validate_amount(amt)
    status = 'PASS' if valid else 'FAIL'
    print(f'[{status}] {desc}: {amt}')
    if error:
        print(f'      Error: {error}')

print('\n=== All validation tests complete! ===')
