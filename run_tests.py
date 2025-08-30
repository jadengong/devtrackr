#!/usr/bin/env python3
"""
Test runner script for DevTrackr project.
Provides easy access to different testing and coverage options.
"""

import sys
import subprocess
import argparse


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print("=" * 60)

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="DevTrackr Test Runner")
    parser.add_argument(
        "--coverage",
        choices=["none", "term", "html", "xml", "all"],
        default="term",
        help="Coverage report type (default: term)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--fast", action="store_true", help="Run tests without coverage for speed"
    )

    args = parser.parse_args()

    if args.fast:
        cmd = "python -m pytest -v"
        success = run_command(cmd, "Fast test run (no coverage)")
    else:
        if args.coverage == "none":
            cmd = "python -m pytest -v"
        elif args.coverage == "term":
            cmd = "python -m pytest --cov=. --cov-report=term-missing -v"
        elif args.coverage == "html":
            cmd = "python -m pytest --cov=. --cov-report=html --cov-report=term-missing -v"
        elif args.coverage == "xml":
            cmd = (
                "python -m pytest --cov=. --cov-report=xml --cov-report=term-missing -v"
            )
        elif args.coverage == "all":
            cmd = "python -m pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing -v"

        success = run_command(cmd, f"Test run with {args.coverage} coverage")

    if success:
        print("\n✅ Tests completed successfully!")
        if not args.fast and args.coverage != "none":
            print("\n📊 Coverage reports generated:")
            if args.coverage in ["html", "all"]:
                print("   • HTML: htmlcov/index.html")
            if args.coverage in ["xml", "all"]:
                print("   • XML: coverage.xml")
            print("   • Terminal: See output above")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
