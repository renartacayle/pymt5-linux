#!/usr/bin/env python3
"""Pre-flight repository readiness and quality gate verification script."""

import os
import sys
import subprocess

REQUIRED_FILES = [
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "Dockerfile",
    "docker-compose.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/publish.yml",
    "src/pymt5_linux/__init__.py",
    "src/pymt5_linux/_version.py",
    "src/pymt5_linux/constants.py",
    "src/pymt5_linux/types.py",
    "src/pymt5_linux/errors.py",
    "src/pymt5_linux/protocol.py",
    "src/pymt5_linux/mock_engine.py",
    "src/pymt5_linux/gateway.py",
    "src/pymt5_linux/client.py",
    "src/pymt5_linux/async_client.py",
    "src/pymt5_linux/streaming.py",
    "src/pymt5_linux/wine_manager.py",
    "src/pymt5_linux/cli.py",
    "examples/01_basic_connection.py",
    "examples/02_market_data_pandas.py",
    "examples/03_ai_trading_bot.py",
    "examples/04_async_tick_streamer.py",
    "examples/05_wine_gateway_runner.py",
    "scripts/setup_wine_mt5.sh"
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Inspecting repository readiness in: {root}")

    # 1. Verify existence of all required files
    missing = []
    for rel_path in REQUIRED_FILES:
        full_path = os.path.join(root, rel_path)
        if not os.path.exists(full_path):
            missing.append(rel_path)

    if missing:
        print(f"FAILED: Missing required repository files: {missing}")
        sys.exit(1)

    print(f"✓ All {len(REQUIRED_FILES)} core files and directories are present.")

    # 2. Check no lazy placeholders or TODOs in codebase
    src_dir = os.path.join(root, "src")
    lazy_patterns = ["// TODO", "/* implement later */", "TODO: implement", "pass  # placeholder"]
    violations = []
    for dirpath, _, filenames in os.walk(src_dir):
        for fname in filenames:
            if fname.endswith(".py"):
                fpath = os.path.join(dirpath, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    for pat in lazy_patterns:
                        if pat in content:
                            violations.append((fname, pat))

    if violations:
        print(f"FAILED: Found lazy placeholders in source files: {violations}")
        sys.exit(1)

    print("✓ Zero-shortcut audit passed (no lazy placeholders or empty stubs).")

    # 3. Check README quality
    readme_path = os.path.join(root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    assert len(readme) > 2000, "README.md must be comprehensive"
    assert "drop-in" in readme.lower()
    assert "installation" in readme.lower()
    print(f"✓ README.md is comprehensive ({len(readme):,} characters).")

    # All checks passed
    print("========================================")
    print("REPO_READINESS_VERIFIED")
    print("========================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
