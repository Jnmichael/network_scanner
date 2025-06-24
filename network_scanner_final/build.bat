@echo off
echo Building Network Scanner .exe...
pyinstaller --onefile --noconsole --clean network_scanner.py
echo Build complete! Check the "dist" folder.
pause
