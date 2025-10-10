#!/usr/bin/env python3
"""
DevTrackr Demo Summary
Runs all demo files in sequence for a complete overview
"""

import subprocess
import sys
import os


def run_demo_file(filename):
    """Run a demo file and display its output"""
    print(f"\n{'='*80}")
    print(f"RUNNING: {filename}")
    print(f"{'='*80}")

    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error running {filename}:")
            print(result.stderr)

    except Exception as e:
        print(f"Failed to run {filename}: {e}")


def main():
    print("DEVTRACKR COMPLETE DEMONSTRATION")
    print("=" * 80)
    print("This will run all demo files to show you how DevTrackr works.")
    print("Each demo focuses on a different aspect of the system.")
    print("=" * 80)

    demo_files = [
        "basic_demo.py",
        "api_examples.py",
        "search_capabilities.py",
        "activity_logging.py",
        "startup_guide.py",
    ]

    for demo_file in demo_files:
        run_demo_file(demo_file)
        input("\nPress Enter to continue to the next demo...")

    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print("You've now seen all the key features of DevTrackr:")
    print("- Database models and relationships")
    print("- API endpoints with examples")
    print("- Advanced search and filtering")
    print("- Activity logging and audit trails")
    print("- Setup and deployment guide")
    print("\nTo get started with DevTrackr:")
    print("1. Follow the startup guide above")
    print("2. Access the API docs at http://localhost:8000/docs")
    print("3. Start building your task management system!")
    print("=" * 80)


if __name__ == "__main__":
    main()
