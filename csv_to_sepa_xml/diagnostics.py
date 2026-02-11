"""
System diagnostics for troubleshooting Tkinter and environment issues.
"""

import sys
import platform


def get_diagnostics():
    """
    Collect comprehensive system information for troubleshooting.
    Returns a dictionary with all diagnostic data.
    """
    info = {
        'python_version': sys.version.split()[0],
        'python_full': sys.version,
        'python_executable': sys.executable,
        'platform': platform.platform(),
        'system': platform.system(),
        'macos_version': 'N/A',
        'architecture': platform.machine(),
        'is_system_python': sys.executable.startswith('/usr/bin/'),
        'tcl_version': 'Not checked',
        'tk_version': 'Not checked',
        'tk_available': False,
        'tk_error': None,
    }

    # macOS-specific info
    if platform.system() == 'Darwin':
        info['macos_version'] = platform.mac_ver()[0]

        # Check for common installation types
        if '/opt/homebrew/' in sys.executable:
            info['python_source'] = 'Homebrew (ARM)'
        elif '/usr/local/' in sys.executable:
            info['python_source'] = 'Homebrew (Intel) or manual install'
        elif '/Library/Frameworks/Python.framework' in sys.executable:
            info['python_source'] = 'python.org installer'
        elif '/.pyenv/' in sys.executable:
            info['python_source'] = 'pyenv'
        elif sys.executable.startswith('/usr/bin/'):
            info['python_source'] = 'Apple System Python (not recommended)'
        else:
            info['python_source'] = 'Unknown'

    # Check Tcl/Tk availability
    try:
        import tkinter
        info['tkinter_module'] = tkinter.__file__

        # Try to actually initialize Tk
        root = tkinter.Tk()
        root.withdraw()
        info['tcl_version'] = root.tk.call('info', 'patchlevel')
        info['tk_version'] = root.tk.call('info', 'patchlevel')
        info['tk_available'] = True
        root.destroy()

        # Check _tkinter library linkage on macOS
        if platform.system() == 'Darwin':
            try:
                import _tkinter
                info['_tkinter_path'] = _tkinter.__file__
            except Exception as e:
                info['_tkinter_path'] = f'ERROR: {e}'

    except ImportError as e:
        info['tk_error'] = f"Import failed: {e}"
    except Exception as e:
        info['tk_error'] = f"Initialization failed: {e}"

    return info


def print_diagnostics():
    """Print formatted diagnostic information."""
    diag = get_diagnostics()

    print("\n" + "=" * 65)
    print("  SEPA Converter - System Diagnostics")
    print("=" * 65)

    print("\n[Python Environment]")
    print(f"  Version:      {diag['python_version']}")
    print(f"  Executable:   {diag['python_executable']}")
    print(f"  Architecture: {diag['architecture']}")
    if 'python_source' in diag:
        print(f"  Source:       {diag['python_source']}")

    print("\n[Operating System]")
    print(f"  Platform:     {diag['platform']}")
    if diag['macos_version'] != 'N/A':
        print(f"  macOS:        {diag['macos_version']}")

    print("\n[Tkinter/Tcl/Tk]")
    if diag['tk_available']:
        print(f"  Status:       AVAILABLE")
        print(f"  Tcl/Tk:       {diag['tcl_version']}")
        if 'tkinter_module' in diag:
            print(f"  Module:       {diag['tkinter_module']}")
    else:
        print(f"  Status:       NOT AVAILABLE")
        print(f"  Error:        {diag['tk_error']}")

    print("\n[Recommendations]")
    if diag['tk_available']:
        print("  GUI mode should work correctly.")
    else:
        print("  GUI mode will NOT work. Options:")
        print("    1. Use CLI mode: --cli input.csv output.xml")
        print("    2. Reinstall Python with Tk:")
        if platform.system() == 'Darwin':
            print("       brew reinstall python-tk@3.11")
            print("    3. Or use python.org installer (includes Tk)")

    if diag.get('is_system_python'):
        print("\n  WARNING: Using Apple System Python.")
        print("           This may have limited Tkinter support.")
        print("           Consider using Homebrew or python.org Python.")

    print("\n" + "=" * 65 + "\n")

    return diag


def check_tkinter_available():
    """
    Quick check if Tkinter is available and functional.
    Returns (available: bool, error: str or None)
    """
    try:
        import tkinter
        import _tkinter  # The C extension
        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        return True, None
    except ImportError as e:
        return False, f"Module not found: {e}"
    except Exception as e:
        return False, f"Initialization failed: {e}"
