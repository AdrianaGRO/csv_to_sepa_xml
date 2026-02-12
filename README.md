# CSV to SEPA XML Converter

A Python application that converts payment data from CSV files to SEPA Credit Transfer XML format (pain.001.001.03). Features both GUI and CLI modes with built-in validation, macOS compatibility layer, and system diagnostics.

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Performance](https://img.shields.io/badge/performance-10k%20in%200.66s-brightgreen)

## Demo Tutorial

[![Watch the demo tutorial](https://img.youtube.com/vi/5BbBlSZ4T2s/0.jpg)](https://www.youtube.com/watch?v=5BbBlSZ4T2s)

Watch on YouTube: https://www.youtube.com/watch?v=5BbBlSZ4T2s

## Features

- **Dual Mode** — GUI for interactive use, CLI for automation/fallback
- **macOS Compatibility** — Defensive Tkinter handling with graceful fallbacks
- **System Diagnostics** — Built-in troubleshooting for Python/Tcl/Tk issues
- **Input Validation** — IBAN checksum, BIC format, amount verification
- **Security** — Sanitizes fields to prevent formula injection attacks
- **Configurable** — Set your company IBAN/BIC via GUI or command line
- **Audit Trail** — Logs all operations to `sepa_converter.log`
- **SEPA Compliant** — Generates valid pain.001.001.03 format

## Requirements

- Python 3.8+
- Tkinter (needed for GUI mode only; CLI works without it)

## Quick Start

### Method 1: Run as Module (Recommended)

```bash
# GUI mode
python3 -m csv_to_sepa_xml.main

# CLI mode
python3 -m csv_to_sepa_xml.main --cli input.csv output.xml

# Diagnostics
python3 -m csv_to_sepa_xml.main --diagnostics
```

### Method 2: Use Wrapper Script

> **Note:** Example CSV files are located in the `examples/` folder.

```bash
# GUI mode
python3 run_converter.py

# CLI mode (use the examples folder)
python3 run_converter.py --cli examples/sample_payments.csv output.xml
```

### Method 3: Run Directly from Package

```bash
cd csv_to_sepa_xml
python3 main.py --cli ../examples/sample_payments.csv output.xml
```

### CLI Options

```bash
# Basic usage (use the examples folder)
python3 -m csv_to_sepa_xml.main --cli examples/sample_payments.csv output.xml

# With custom debtor info
python3 -m csv_to_sepa_xml.main --cli examples/sample_payments.csv sepa_output.xml \
    --debtor-name "My Company GmbH" \
    --debtor-iban "DE89370400440532013000" \
    --debtor-bic "COBADEFFXXX"

# Quiet mode (for scripts)
python3 -m csv_to_sepa_xml.main --cli examples/sample_payments.csv output.xml --quiet
```

### GUI Mode

Launch the GUI and:
1. Enter your company details (name, IBAN, BIC)
2. Click "Select CSV File" to choose your CSV
3. Click "Generate SEPA XML" to create the output

### Diagnostics Mode

```bash
python3 -m csv_to_sepa_xml.main --diagnostics
```

Shows Python version, Tcl/Tk status, and recommendations. **Run this first if the GUI fails.**

## Project Structure

```
csv_to_sepa_xml/
├── csv_to_sepa_xml/         # Main package
│   ├── main.py              # Entry point & mode routing
│   ├── config.py            # Constants (IBAN lengths, defaults)
│   ├── cli.py               # CLI mode & argument parsing
│   ├── gui.py               # Tkinter GUI
│   ├── validation.py        # IBAN/BIC validators
│   ├── csv_reader.py        # CSV parsing with validation & error reports
│   ├── xml_builder.py       # XML generation
│   └── diagnostics.py       # System diagnostics
├── examples/                # Sample CSV files and test data generator
├── tests/                   # Test files
├── docs/                    # Additional documentation (SEPA guide for users)
├── run_converter.py         # Backward compatibility wrapper
├── README.md                # This file
├── requirements.txt         # Python dependencies (none required)
└── .gitignore               # Git ignore rules
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--cli INPUT OUTPUT` | Run in CLI mode (no GUI) |
| `--diagnostics` | Show system diagnostics and exit |
| `--debtor-name` | Your company name |
| `--debtor-iban` | Your company IBAN |
| `--debtor-bic` | Your company BIC |
| `--force` | Generate XML even with validation errors |
| `--quiet` | Suppress non-error output |

## CSV Format

Your CSV file must include these columns:

| Column | Description | Required | Example |
|--------|-------------|----------|---------|
| name | Beneficiary name | Yes | Maria Schmidt |
| iban | Beneficiary IBAN | Yes | DE89370400440532013000 |
| bic | Bank BIC/SWIFT code | No | COBADEFFXXX |
| amount | Payment amount (EUR) | Yes | 1500.00 |
| reference | Payment reference | No | Invoice 2024-001 |

See `examples/sample_payments.csv` for a working example.

## Validation

The converter validates:

- **IBAN** — Country code, length, and checksum (mod 97)
- **BIC** — Format and length (8 or 11 characters)
- **Amount** — Positive numbers, max 999,999,999.99
- **Name** — Required, max 70 characters

Invalid rows are marked in the GUI preview. Use `--force` in CLI mode to generate XML with valid rows only.

### Error Reports

When invalid payments are detected, the system **automatically generates a CSV error report** containing:

- All invalid payment rows from your input
- Row numbers for easy reference
- Complete original data (name, IBAN, BIC, amount, reference, etc.)
- Detailed error messages explaining what's wrong

**File naming format**: `[input_filename]_errors_YYYYMMDD_HHMMSS.csv`

**Example**: If you process `sample_payments_10k.csv` on Feb 11, 2026 at 14:31:31, the error report will be named:
```
sample_payments_10k_errors_20260211_143131.csv
```

**Error report columns**:
- `row_number` — Original line number from input CSV
- All your original columns (name, iban, bic, amount, reference, address, etc.)
- `error_details` — Specific validation errors (multiple errors separated by ` | `)

**Example error entries**:
```csv
row_number,name,iban,bic,amount,reference,error_details
3,Schmidt Ltd,IT28W8000000292100645211111,UNCRITMM,44531.96,Invoice 2024369,Invalid IBAN check digit (MOD-97 validation failed)
4,Maria Klein,DE89370400440532013000,INTESA,42571.34,Payment 2024040,Invalid BIC: must be 8 or 11 characters (got 6)
```

You can open the error report in Excel or any spreadsheet application to review and fix problematic accounts before re-uploading. The error report is logged and its location is displayed when the conversion completes.

## Security Features

- **Formula Injection Protection** — Fields starting with `=`, `+`, `-`, `@` are prefixed
- **Input Sanitization** — All fields validated before XML generation
- **Row Limits** — Maximum 10,000 payments to prevent memory issues

---

## macOS Troubleshooting Guide

### Why Tkinter Breaks After macOS Updates

Tkinter on macOS depends on a chain of components that can break when the OS updates:

```
Your Script → tkinter → _tkinter.so → libtcl/libtk → macOS Display
```

Common causes of failure:

| macOS Update | What Typically Breaks |
|--------------|----------------------|
| Security patches | Gatekeeper blocks unsigned Python |
| Major releases | Tcl/Tk libraries relocated or removed |
| ARM transition | x86 Python on ARM Mac (Rosetta issues) |
| Homebrew updates | Python rebuilt without Tk support |

### Step 1: Run Diagnostics

Always start here:

```bash
python3 csv_to_sepa_xml.py --diagnostics
```

Example output (healthy system):
```
=================================================================
  SEPA Converter - System Diagnostics
=================================================================

[Python Environment]
  Version:      3.11.7
  Executable:   /opt/homebrew/bin/python3
  Architecture: arm64
  Source:       Homebrew (ARM)

[Operating System]
  Platform:     macOS-14.2-arm64
  macOS:        14.2

[Tkinter/Tcl/Tk]
  Status:       AVAILABLE
  Tcl/Tk:       8.6.13

[Recommendations]
  GUI mode should work correctly.
=================================================================
```

### Step 2: Quick Fixes by Error Type

#### Error: "Tkinter module not found"

```bash
# For Homebrew Python
brew install python-tk@3.11

# Verify
python3 -c "import tkinter; print('OK')"
```

#### Error: "Tcl/Tk initialization failed"

```bash
# Reinstall with Tk support
brew reinstall python-tk@3.11

# Or use python.org installer (includes Tk)
# Download from: https://www.python.org/downloads/macos/
```

#### Error: "App is damaged" or Gatekeeper blocks

```bash
# Remove quarantine
xattr -cr /path/to/csv_to_sepa_xml.py

# Or allow in System Preferences:
# Security & Privacy → General → "Allow Anyway"
```

#### Error: GUI opens then crashes

```bash
# Check if using system Python (bad)
which python3
# If /usr/bin/python3, switch to Homebrew or python.org

# Use CLI as workaround
python3 csv_to_sepa_xml.py --cli input.csv output.xml
```

### Step 3: Nuclear Options

If nothing else works:

#### Option A: Use pyenv with Explicit Tcl/Tk

```bash
# Install Tcl/Tk first
brew install tcl-tk

# Configure environment
export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"

# Install Python with pyenv
pyenv install 3.11.7
pyenv global 3.11.7

# Verify
python3 csv_to_sepa_xml.py --diagnostics
```

#### Option B: Use Official python.org Installer

1. Download from https://www.python.org/downloads/macos/
2. Run the installer (includes Tcl/Tk)
3. Use `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3`

#### Option C: Always Use CLI Mode

Add this alias to your `~/.zshrc`:

```bash
alias sepa-convert='python3 /path/to/csv_to_sepa_xml.py --cli'
```

Then use:
```bash
sepa-convert input.csv output.xml
```

### Pre-Update Checklist

Before upgrading macOS, save this baseline:

```bash
# Save current working state
python3 -c "import tkinter; print(tkinter.Tcl().eval('info patchlevel'))"
which python3
python3 --version
python3 csv_to_sepa_xml.py --diagnostics > pre_update_diagnostics.txt
```

### Post-Update Recovery

After macOS upgrade:

```bash
# 1. Check what broke
python3 csv_to_sepa_xml.py --diagnostics

# 2. If Tk broken, reinstall
brew reinstall python-tk@3.11

# 3. If still broken, use CLI
python3 csv_to_sepa_xml.py --cli input.csv output.xml
```

---

## Logging

All operations are logged to `sepa_converter.log` in the same directory as the script:

- CSV file loads
- Validation errors
- XML generation events
- Errors and exceptions

## Output

The generated XML follows the ISO 20022 pain.001.001.03 standard, compatible with European banks for SEPA Credit Transfers.

### Formatting XML Output

To format the generated XML for better readability:

```bash
xmllint --format sepa_payment_YYYYMMDD_HHMMSS.xml > formatted_sepa_payment.xml
```

## Configuration

Default debtor values are set in the script. For production use:

1. Edit the defaults in the script (`DEFAULT_COMPANY_*` constants)
2. Use the GUI fields to enter your details
3. Pass values via CLI arguments


## Additional Documentation

- `sepa_converter.log` — Runtime logs for troubleshooting

---

Built by Adriana G. | Python Automation Specialist

*Last updated: February 2026 — Added macOS Tahoe compatibility layer*
