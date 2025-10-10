#!/usr/bin/env python3
"""
Deployment testing script for Vercel.
This script helps you test different Vercel configurations.
"""

import os
import shutil
import sys


def deploy_minimal():
    """Deploy with minimal configuration"""
    print("Setting up minimal deployment...")

    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-minimal.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    # Copy minimal config
    shutil.copy(config_path, vercel_path)

    print("Minimal configuration ready!")
    print("Next steps:")
    print("   1. git add .")
    print("   2. git commit -m 'test: minimal deployment'")
    print("   3. git push")
    print("   4. Test: https://your-app.vercel.app/")


def deploy_simple():
    """Deploy with simple FastAPI configuration"""
    print("Setting up simple FastAPI deployment...")

    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-simple.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    # Copy simple config
    shutil.copy(config_path, vercel_path)

    print("Simple FastAPI configuration ready!")
    print("Next steps:")
    print("   1. git add .")
    print("   2. git commit -m 'test: simple fastapi deployment'")
    print("   3. git push")
    print("   4. Test: https://your-app.vercel.app/")


def deploy_full():
    """Deploy with full application configuration"""
    print("Setting up full application deployment...")

    # Use the original vercel.json (it should already be there)
    print("Full application configuration ready!")
    print("Next steps:")
    print("   1. Set DATABASE_URL environment variable in Vercel")
    print("   2. git add .")
    print("   3. git commit -m 'test: full application deployment'")
    print("   4. git push")
    print("   5. Test: https://your-app.vercel.app/health")


def deploy_test_minimal():
    """Deploy with absolute minimal configuration"""
    print("Setting up absolute minimal deployment...")

    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-test-minimal.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    # Copy test minimal config
    shutil.copy(config_path, vercel_path)

    print("Absolute minimal configuration ready!")
    print("Next steps:")
    print("   1. git add .")
    print("   2. git commit -m 'test: absolute minimal deployment'")
    print("   3. git push")
    print("   4. Test: https://your-app.vercel.app/")


def main():
    """Main deployment script"""
    print("Vercel Deployment Testing Script")
    print("=" * 40)

    if len(sys.argv) < 2:
        print("Usage: python deploy-test.py [test-minimal|minimal|simple|full]")
        print()
        print("Options:")
        print("  test-minimal  - Test with absolute minimal Python function")
        print("  minimal       - Test with minimal Python function")
        print("  simple        - Test with simple FastAPI app")
        print("  full          - Test with full application")
        return

    mode = sys.argv[1].lower()

    if mode == "test-minimal":
        deploy_test_minimal()
    elif mode == "minimal":
        deploy_minimal()
    elif mode == "simple":
        deploy_simple()
    elif mode == "full":
        deploy_full()
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: test-minimal, minimal, simple, full")


if __name__ == "__main__":
    main()
