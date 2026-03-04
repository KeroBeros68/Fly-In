"""
Detect and display Python virtual environment status.

This module demonstrates understanding of Python virtual environments by:
- Detecting whether code runs in a venv or global Python
- Displaying environment-specific information
- Providing setup instructions for virtual environments
"""

import tomllib
import re
import site
import sys
import os
import time
from importlib import import_module, metadata


def _virtual_process(virtual_env: str | None) -> None:
    """
    Display virtual environment information and success message.

    When running inside a virtual environment, this function shows:
    - Current Python executable path
    - Virtual environment name and path
    - Location of site-packages directory
    - Security confirmation of isolated environment

    Args:
        virtual_env: Path to the active virtual environment from VIRTUAL_ENV
    """
    print("\nVENV STATUS: Active\n")
    print("Python executable:", sys.executable)
    venv_name: str = (
        os.path.basename(virtual_env) if virtual_env else "unknown"
    )
    print(f"Environment name : {venv_name}")
    print(f"Environment path : {virtual_env}\n")
    print(
        "Isolated environment detected.\n"
        "Packages will not affect the global system.\n"
    )

    print("Site-packages path:")
    if virtual_env:
        site_packages_path: str = os.path.join(
            virtual_env, "lib", "python3.13", "site-packages"
        )
        print(site_packages_path)
    else:
        for s in site.getsitepackages():
            print(s)


def _reality_process(virtual_env: str | None) -> None:
    """
    Display global environment warning and setup instructions.

    When running in the global Python environment (no venv detected),
    this function warns the user about the security risks and provides
    clear instructions for creating and activating a virtual environment.

    Args:
        virtual_env: Value of VIRTUAL_ENV (should be None in global env)
    """
    print("\nVENV STATUS: No virtual environment detected\n")
    print("Python executable:", sys.executable)
    print(f"VIRTUAL_ENV: {virtual_env}")
    print(
        "WARNING: Running in the global Python environment.\n"
        "Installing packages here may affect your entire system.\n"
    )
    print(
        "To set up a virtual environment, run:\n"
        "  uv venv\n"
        "  source .venv/bin/activate  # Unix\n"
        "  .venv\\Scripts\\activate    # Windows\n"
    )
    print("Then restart the program.")


def _check_dependencies(module_list: list[str]) -> bool:
    """
    Verify that all required packages are installed.

    Iterates through module_list, attempting to import each package
    and retrieve its version from package metadata.

    Args:
        module_list: List of package names from pyproject.toml dependencies

    Returns:
        bool: True if all dependencies loaded, False if any are missing
    """
    print("Checking dependencies...\n")
    print("Required packages:")
    all_loaded: bool = True
    lines_written: int = (3)

    for raw_name in module_list:
        package_name: str = re.split(r"[><=!;\s\[]", raw_name)[0].strip()
        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for frame in spinner:
            sys.stdout.write(f"\r    {frame} Loading {package_name}...")
            sys.stdout.flush()
            time.sleep(0.05)

        try:
            import_module(package_name)
            meta = metadata.metadata(package_name)
            print(f"\r    [OK] {meta['Name']} {meta['Version']} — loaded")
            lines_written += 1
        except ModuleNotFoundError:
            all_loaded = False
            print(
                f"\r    [MISSING] '{package_name}' could not be imported. "
                "Run 'uv sync' to install missing dependencies."
            )
            lines_written += 1

    return all_loaded, lines_written


def check_process() -> None:
    """
    Main process to check environment and dependencies.

    Verifies that the script runs in a virtual environment and
    validates that all required dependencies are installed.
    Exits with code 1 if environment or dependencies are invalid.
    """
    virtual_env: str | None = os.environ.get("VIRTUAL_ENV")
    try:
        if sys.prefix == sys.base_prefix and not virtual_env:
            _reality_process(virtual_env)
            input("\n\nPress Enter to exit...")
            sys.exit(1)
        else:
            _virtual_process(virtual_env)
            try:
                with open("pyproject.toml", "rb") as f:
                    data = tomllib.load(f)
                dependencies = data["project"].get("dependencies", [])
                check, line = _check_dependencies(dependencies)
                if not check:
                    sys.exit(1)
                else:
                    sys.stdout.write(f"\033[{line + 13}A\033[J")
                    sys.stdout.flush()
            except FileNotFoundError:
                pass
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
