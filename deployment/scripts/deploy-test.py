#!/usr/bin/env python3
"""
Quick script to test different Vercel deployment configs.
Handy when you're debugging deployment issues.
"""

import os
import shutil
import sys


def deploy_minimal():
    """Basic setup for minimal Vercel deployment"""
    print("Setting up minimal deployment...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-minimal.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    shutil.copy(config_path, vercel_path)

    print("Done! Now just:")
    print("   1. git add .")
    print("   2. git commit -m 'test: minimal deployment'")
    print("   3. git push")
    print("   4. Check: https://your-app.vercel.app/")


def deploy_simple():
    """Simple FastAPI setup for Vercel"""
    print("Setting up simple FastAPI deployment...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-simple.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    shutil.copy(config_path, vercel_path)

    print("Ready to go!")
    print("Next:")
    print("   1. git add .")
    print("   2. git commit -m 'test: simple fastapi deployment'")
    print("   3. git push")
    print("   4. Check: https://your-app.vercel.app/")


def deploy_full():
    """Full app deployment with all features"""
    print("Setting up full application deployment...")

    # Using the existing vercel.json config
    print("All set!")
    print("Don't forget:")
    print("   1. Set DATABASE_URL in Vercel dashboard")
    print("   2. git add .")
    print("   3. git commit -m 'test: full application deployment'")
    print("   4. git push")
    print("   5. Test: https://your-app.vercel.app/health")


def deploy_test_minimal():
    """Bare minimum config for testing"""
    print("Setting up absolute minimal deployment...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    config_path = os.path.join(script_dir, "..", "configs", "vercel-test-minimal.json")
    vercel_path = os.path.join(project_root, "vercel.json")

    shutil.copy(config_path, vercel_path)

    print("Minimal config ready!")
    print("Then:")
    print("   1. git add .")
    print("   2. git commit -m 'test: absolute minimal deployment'")
    print("   3. git push")
    print("   4. Test: https://your-app.vercel.app/")


def main():
    """Main script entry point"""
    print("Vercel Deployment Testing Script")
    print("=" * 40)

    if len(sys.argv) < 2:
        print("Usage: python deploy-test.py [test-minimal|minimal|simple|full]")
        print()
        print("Options:")
        print("  test-minimal  - Bare minimum Python function")
        print("  minimal       - Basic Python function")
        print("  simple        - Simple FastAPI app")
        print("  full          - Complete application")
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
