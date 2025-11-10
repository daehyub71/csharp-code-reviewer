#!/usr/bin/env python3
"""
Ollama Portable Bundler

Creates a portable Ollama package for offline VDI deployment.

Usage:
    python scripts/bundle_ollama.py [--output-dir DIR]

This script helps prepare:
1. Ollama Windows executable
2. Phi-3-mini model file
3. Portable package structure
"""

import os
import sys
import shutil
import argparse
import urllib.request
from pathlib import Path
from typing import Optional


class OllamaBundleError(Exception):
    """Bundling failed"""
    pass


class OllamaBundler:
    """Creates portable Ollama package"""

    # Ollama download URL (Windows)
    OLLAMA_WINDOWS_URL = "https://ollama.com/download/OllamaSetup.exe"

    # Expected model file name
    MODEL_FILE_NAME = "phi3-mini-4k-instruct-q4.gguf"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.ollama_portable_dir = output_dir / "ollama_portable"
        self.models_dir = self.ollama_portable_dir / "models"

    def create_structure(self):
        """Create portable directory structure"""
        print("=" * 80)
        print("Creating portable directory structure")
        print("=" * 80)

        # Create directories
        dirs_to_create = [
            self.ollama_portable_dir,
            self.models_dir,
            self.output_dir / "config",
            self.output_dir / "logs",
            self.output_dir / "reports" / "markdown",
            self.output_dir / "reports" / "html",
        ]

        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {dir_path.relative_to(self.output_dir)}")

        print()

    def download_ollama(self):
        """Download Ollama Windows installer"""
        print("=" * 80)
        print("Ollama Windows Binary Setup")
        print("=" * 80)

        print()
        print("⚠️  Manual Download Required")
        print()
        print("Due to licensing and distribution restrictions, you must manually")
        print("obtain the Ollama Windows binary.")
        print()
        print("📋 Steps:")
        print()
        print("1. Download Ollama Windows installer:")
        print(f"   {self.OLLAMA_WINDOWS_URL}")
        print()
        print("2. Install Ollama on your system")
        print()
        print("3. Locate the installed ollama.exe:")
        print("   Typical locations:")
        print("   - C:\\Users\\<YourName>\\AppData\\Local\\Programs\\Ollama\\ollama.exe")
        print("   - C:\\Program Files\\Ollama\\ollama.exe")
        print()
        print(f"4. Copy ollama.exe to: {self.ollama_portable_dir}")
        print()

        # Check if ollama.exe already exists
        ollama_exe = self.ollama_portable_dir / "ollama.exe"
        if ollama_exe.exists():
            size_mb = ollama_exe.stat().st_size / (1024 * 1024)
            print(f"✓ ollama.exe found: {ollama_exe}")
            print(f"  Size: {size_mb:.1f} MB")
            return True
        else:
            print(f"⚠️  ollama.exe not found at: {ollama_exe}")
            print("   Please copy it manually and run this script again")
            return False

    def bundle_model(self):
        """Bundle Phi-3-mini model"""
        print("=" * 80)
        print("Phi-3-mini Model Setup")
        print("=" * 80)

        print()
        print("⚠️  Manual Model Preparation Required")
        print()
        print("The Phi-3-mini model must be obtained from Ollama.")
        print()
        print("📋 Steps:")
        print()
        print("1. Ensure Ollama is running:")
        print("   ollama serve")
        print()
        print("2. Pull the Phi-3-mini model:")
        print("   ollama pull phi3:mini")
        print()
        print("3. Locate the model file:")
        print("   - Windows: C:\\Users\\<YourName>\\.ollama\\models\\blobs\\")
        print("   - macOS: ~/.ollama/models/blobs/")
        print("   - Linux: ~/.ollama/models/blobs/")
        print()
        print("   Look for a file ~2.3GB in size (sha256-* format)")
        print()
        print(f"4. Copy the model file to: {self.models_dir}")
        print(f"   Rename it to: {self.MODEL_FILE_NAME}")
        print()

        # Check if model exists
        model_file = self.models_dir / self.MODEL_FILE_NAME
        if model_file.exists():
            size_gb = model_file.stat().st_size / (1024 * 1024 * 1024)
            print(f"✓ Model file found: {model_file}")
            print(f"  Size: {size_gb:.2f} GB")
            return True
        else:
            print(f"⚠️  Model file not found at: {model_file}")
            print("   Please copy it manually and run this script again")
            print()
            print("💡 Tip: After copying, you may need to create a Modelfile")
            print("   to reference this GGUF file. See docs/PORTABLE_GUIDE.md")
            return False

    def create_readme(self):
        """Create user-facing README.txt"""
        print("=" * 80)
        print("Creating README.txt")
        print("=" * 80)

        readme_content = """
================================================================================
C# Code Reviewer - Portable Edition
================================================================================

This is a portable, offline-capable version of C# Code Reviewer that includes:
- CodeReviewer.exe (AI-powered C# code analysis tool)
- Ollama portable (local LLM server)
- Phi-3-mini model (2.3GB)

Total package size: ~2.5 GB (compressed: ~1.5 GB)

================================================================================
Quick Start
================================================================================

1. EXTRACT this ZIP to any folder (no admin rights required)

2. DOUBLE-CLICK CodeReviewer.exe
   - Ollama will start automatically in the background
   - Wait 5-10 seconds for initialization

3. USE the application:
   - Paste C# code → Click "Analyze"
   - Or upload .cs files
   - Or select entire folders

4. CLOSE normally - Ollama will stop automatically

================================================================================
Requirements
================================================================================

- Windows 10/11 (64-bit)
- 8GB+ RAM (16GB recommended)
- 3GB free disk space
- No internet connection required
- No admin rights required

================================================================================
Troubleshooting
================================================================================

Q: "Ollama connection failed"
A: Wait 10-20 seconds and retry. First startup takes longer.

Q: Application is slow
A: Phi-3-mini runs on CPU. Expect 5-10 seconds per analysis.

Q: Port 11434 already in use
A: Another Ollama instance is running. Close it or change port in config/settings.json

Q: Console window appears
A: This is normal on first launch. It will auto-hide.

================================================================================
File Structure
================================================================================

CodeReviewer_Portable/
├── CodeReviewer.exe         Main application
├── ollama_portable/
│   ├── ollama.exe           Ollama server
│   └── models/              Model files
├── config/
│   └── settings.json        User preferences
├── logs/                    Application logs
├── reports/                 Generated reports
│   ├── markdown/
│   └── html/
└── README.txt               This file

================================================================================
Support
================================================================================

For issues or questions, please refer to:
- docs/PORTABLE_GUIDE.md (technical details)
- docs/BUILD_GUIDE.md (for developers)
- GitHub: https://github.com/your-repo/csharp-code-reviewer

================================================================================
License
================================================================================

This application uses:
- PySide6 (LGPL) - https://www.qt.io/licensing/
- Ollama (MIT) - https://github.com/ollama/ollama
- Phi-3-mini (MIT) - https://huggingface.co/microsoft/Phi-3-mini-4k-instruct

See individual licenses in the licenses/ folder.

================================================================================
Version: 1.0.0
Generated: 2025-01-19
================================================================================
""".strip()

        readme_path = self.output_dir / "README.txt"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"✓ Created: {readme_path}")
        print()

    def create_config(self):
        """Create default settings.json"""
        print("=" * 80)
        print("Creating default settings.json")
        print("=" * 80)

        config_content = """{
  "ollama": {
    "host": "http://localhost:11434",
    "model": "phi3:mini",
    "timeout": 30,
    "temperature": 0.7,
    "portable_path": "./ollama_portable/ollama.exe"
  },
  "ui": {
    "theme": "dark",
    "font_family": "Consolas",
    "font_size": 12,
    "sync_scroll": true
  },
  "analysis": {
    "check_null_reference": true,
    "check_exception": true,
    "check_resource": true,
    "check_performance": true,
    "check_security": true,
    "check_naming": true,
    "check_documentation": true,
    "check_hardcoding": true,
    "generate_diagram": true
  },
  "files": {
    "max_file_size_mb": 1,
    "max_file_count": 50
  }
}"""

        config_path = self.output_dir / "config" / "settings.json"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        print(f"✓ Created: {config_path}")
        print()

    def verify_bundle(self) -> bool:
        """Verify portable bundle is complete"""
        print("=" * 80)
        print("Verifying Portable Bundle")
        print("=" * 80)

        checks = [
            ("CodeReviewer.exe", self.output_dir / "CodeReviewer.exe"),
            ("ollama.exe", self.ollama_portable_dir / "ollama.exe"),
            ("Model file", self.models_dir / self.MODEL_FILE_NAME),
            ("README.txt", self.output_dir / "README.txt"),
            ("settings.json", self.output_dir / "config" / "settings.json"),
        ]

        all_ok = True
        for name, path in checks:
            if path.exists():
                if path.is_file():
                    size_mb = path.stat().st_size / (1024 * 1024)
                    print(f"✓ {name}: {path.name} ({size_mb:.1f} MB)")
                else:
                    print(f"✓ {name}: {path}")
            else:
                print(f"✗ {name}: NOT FOUND")
                all_ok = False

        print()

        if all_ok:
            print("✅ All files present!")
        else:
            print("⚠️  Some files are missing. Complete the manual steps above.")

        return all_ok

    def calculate_total_size(self):
        """Calculate total package size"""
        print("=" * 80)
        print("Package Size Summary")
        print("=" * 80)

        def get_dir_size(path: Path) -> int:
            total = 0
            if not path.exists():
                return 0
            if path.is_file():
                return path.stat().st_size
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
            return total

        sizes = {
            "CodeReviewer.exe": get_dir_size(self.output_dir / "CodeReviewer.exe"),
            "ollama_portable/": get_dir_size(self.ollama_portable_dir),
            "config/": get_dir_size(self.output_dir / "config"),
            "Other files": 0,
        }

        total_size = sum(sizes.values())

        for name, size in sizes.items():
            size_mb = size / (1024 * 1024)
            print(f"  {name:<20} {size_mb:>8.1f} MB")

        print(f"  {'─' * 20} {'─' * 10}")
        total_mb = total_size / (1024 * 1024)
        total_gb = total_size / (1024 * 1024 * 1024)
        print(f"  {'TOTAL':<20} {total_mb:>8.1f} MB ({total_gb:.2f} GB)")

        print()
        print(f"Estimated compressed size (ZIP): ~{total_gb * 0.6:.2f} GB")
        print()

    def run(self):
        """Execute bundling process"""
        try:
            print()
            print("╔" + "=" * 78 + "╗")
            print("║" + " " * 20 + "Ollama Portable Bundler" + " " * 35 + "║")
            print("╚" + "=" * 78 + "╝")
            print()

            # Create directory structure
            self.create_structure()

            # Create config files
            self.create_config()
            self.create_readme()

            # Download/prepare Ollama
            ollama_ok = self.download_ollama()

            # Bundle model
            model_ok = self.bundle_model()

            # Verify bundle
            print()
            complete = self.verify_bundle()

            # Calculate size
            if complete:
                self.calculate_total_size()

            # Final instructions
            print("=" * 80)
            print("Next Steps")
            print("=" * 80)
            print()

            if complete:
                print("✅ Portable bundle is ready!")
                print()
                print("1. Copy CodeReviewer.exe to the output directory")
                print("2. Test the portable package:")
                print(f"   cd {self.output_dir}")
                print("   ./CodeReviewer.exe")
                print()
                print("3. Create distributable ZIP:")
                print(f"   zip -r CodeReviewer_Portable.zip {self.output_dir.name}")
                print()
            else:
                print("⚠️  Portable bundle is incomplete")
                print()
                print("Complete these steps:")
                if not ollama_ok:
                    print("  1. Copy ollama.exe to ollama_portable/")
                if not model_ok:
                    print("  2. Copy Phi-3-mini model to ollama_portable/models/")
                print("  3. Build and copy CodeReviewer.exe to the output directory")
                print()
                print("Then run this script again to verify.")
                print()

            return 0 if complete else 1

        except Exception as e:
            print()
            print("=" * 80)
            print("❌ Bundling failed")
            print("=" * 80)
            print(f"Error: {e}")
            print()
            return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create portable Ollama package for C# Code Reviewer"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("CodeReviewer_Portable"),
        help="Output directory for portable package (default: CodeReviewer_Portable)"
    )

    args = parser.parse_args()

    bundler = OllamaBundler(output_dir=args.output_dir)
    sys.exit(bundler.run())


if __name__ == "__main__":
    main()
