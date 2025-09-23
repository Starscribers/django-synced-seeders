#!/usr/bin/env python3
"""
Test runner script for django-synced-seeds.

This script provides various ways to run the test suite with different
configurations and options.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Main test runner function."""
    # Set up the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Ensure Python path includes the src directory
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Parse command line arguments
    args = sys.argv[1:]

    if not args:
        print("Running full test suite...")
        run_full_tests()
    elif args[0] == "quick":
        print("Running quick tests (unit tests only)...")
        run_quick_tests()
    elif args[0] == "integration":
        print("Running integration tests...")
        run_integration_tests()
    elif args[0] == "coverage":
        print("Running tests with coverage report...")
        run_coverage_tests()
    elif args[0] == "models":
        print("Running model tests...")
        run_model_tests()
    elif args[0] == "commands":
        print("Running command tests...")
        run_command_tests()
    elif args[0] == "seeders":
        print("Running seeder tests...")
        run_seeder_tests()
    elif args[0] == "help":
        show_help()
    else:
        print(f"Running custom pytest with args: {' '.join(args)}")
        run_custom_tests(args)


def run_full_tests():
    """Run the complete test suite."""
    cmd = ["python", "-m", "pytest", "tests/", "-v"]
    return subprocess.run(cmd)


def run_quick_tests():
    """Run quick unit tests only (excluding slow integration tests)."""
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "-v",
        "-m",
        "not slow and not integration",
        "--tb=short",
    ]
    return subprocess.run(cmd)


def run_integration_tests():
    """Run integration tests only."""
    cmd = ["python", "-m", "pytest", "tests/test_integration.py", "-v", "--tb=long"]
    return subprocess.run(cmd)


def run_coverage_tests():
    """Run tests with coverage reporting."""
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=seeders",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=80",
        "-v",
    ]
    return subprocess.run(cmd)


def run_model_tests():
    """Run model-specific tests."""
    cmd = ["python", "-m", "pytest", "tests/test_models.py", "-v"]
    return subprocess.run(cmd)


def run_command_tests():
    """Run management command tests."""
    cmd = ["python", "-m", "pytest", "tests/test_commands.py", "-v"]
    return subprocess.run(cmd)


def run_seeder_tests():
    """Run seeder and utility tests."""
    cmd = ["python", "-m", "pytest", "tests/test_seeders.py", "-v"]
    return subprocess.run(cmd)


def run_custom_tests(args):
    """Run pytest with custom arguments."""
    cmd = ["python", "-m", "pytest"] + args
    return subprocess.run(cmd)


def show_help():
    """Show help information."""
    help_text = """
Django Synced Seeds Test Runner

Usage: python run_tests.py [command]

Commands:
    (no args)    - Run full test suite
    quick        - Run quick tests (exclude slow/integration tests)
    integration  - Run integration tests only
    coverage     - Run tests with coverage reporting
    models       - Run model tests only
    commands     - Run management command tests only
    seeders      - Run seeder and utility tests only
    help         - Show this help message

Examples:
    python run_tests.py
    python run_tests.py quick
    python run_tests.py coverage
    python run_tests.py tests/test_models.py::TestSeedRevisionModel::test_create_seed_revision
    python run_tests.py -k "test_sync" -v
    python run_tests.py --pdb  # Drop into debugger on failure

Pytest Options:
    You can also pass any pytest arguments directly:
    python run_tests.py -v --tb=short
    python run_tests.py -x  # Stop on first failure
    python run_tests.py --lf  # Run last failed tests
    python run_tests.py --pdb  # Drop into pdb on failure
    python run_tests.py -s  # Don't capture output
    
Markers:
    -m "unit"         - Run unit tests only
    -m "integration"  - Run integration tests only
    -m "slow"         - Run slow tests only
    -m "not slow"     - Skip slow tests
    -m "models"       - Run model tests only
    -m "commands"     - Run command tests only
    -m "seeders"      - Run seeder tests only

Coverage:
    After running coverage tests, open htmlcov/index.html to view detailed coverage report.
    
Dependencies:
    Make sure you have installed the test dependencies:
    pip install pytest pytest-django pytest-cov
    """
    print(help_text)


if __name__ == "__main__":
    main()
