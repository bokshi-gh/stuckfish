#!/usr/bin/env python
"""
Stuckfish - A UCI-compliant chess engine
Author: Rajesh Thapa (bokshi)
"""

import sys
import os

# PyInstaller support for both --onefile and --onedir builds
if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller --onefile: files extracted to temp directory
        application_path = sys._MEIPASS
    else:
        # PyInstaller --onedir: executable directory
        application_path = os.path.dirname(sys.executable)
else:
    # Running as standard Python script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Add the project root to sys.path so 'from engine.uci import UCI' resolves correctly
if application_path not in sys.path:
    sys.path.insert(0, application_path)

from engine.uci import UCI

def main():
    """Main entry point"""
    uci = UCI()
    uci.run()

if __name__ == "__main__":
    main()
