#!/usr/bin/env python3
import os
import subprocess
import sys

# Change to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

# Run PyInstaller
cmd = [
    sys.executable,
    "-m", "PyInstaller",
    "--clean",
    "--distpath", os.path.join(project_root, "dist"),
    "--workpath", os.path.join(project_root, "build", "pyi-build"),
    os.path.join("build", "jarvis.spec")
]

print("Running from:", project_root)
print("Command:", " ".join(cmd))
sys.exit(subprocess.call(cmd))
