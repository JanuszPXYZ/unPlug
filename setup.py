"""
Build a standalone macOS .app bundle:

    pip install -r requirements-dev.txt
    python setup.py py2app

The result is written to dist/unPlug.app
"""

from setuptools import setup

APP = ["unPlug.py"]
DATA_FILES = []

OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "unPlug",
        "CFBundleDisplayName": "unPlug",
        "CFBundleIdentifier": "com.januszpolowczyk.unplug",
        "CFBundleShortVersionString": "0.2.0",
        "CFBundleVersion": "0.2.0",
        # Status bar only: keeps the app out of the Dock and app switcher.
        "LSUIElement": True,
        "NSHumanReadableCopyright": "Janusz Polowczyk",
    },
    "packages": ["rumps", "psutil"],
}

setup(
    app=APP,
    name="unPlug",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
