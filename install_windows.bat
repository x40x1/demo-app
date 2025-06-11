@echo off
REM Demo Mode Application - Windows Installation Script
REM This script sets up the Demo Mode Application on Windows PCs

echo ===============================================
echo Demo Mode Application - Windows Installer
echo ===============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges for full functionality.
    echo Some features like keyboard lock will not work without admin rights.
    echo.
    pause
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; print(f'Python {sys.version}')"
echo.

REM Create application directory
set APP_DIR=%PROGRAMFILES%\DemoModeApp
if not exist "%APP_DIR%" (
    echo Creating application directory: %APP_DIR%
    mkdir "%APP_DIR%"
)

REM Copy application files
echo Copying application files...
copy "*.py" "%APP_DIR%\" >nul
copy "*.txt" "%APP_DIR%\" >nul
copy "*.md" "%APP_DIR%\" >nul

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Windows-specific dependencies
echo Installing Windows-specific dependencies...
pip install pywin32
pip install win32com.client

REM Create demo content directories
echo Creating content directories...
if not exist "%APP_DIR%\content" mkdir "%APP_DIR%\content"
if not exist "%APP_DIR%\content\images" mkdir "%APP_DIR%\content\images"
if not exist "%APP_DIR%\content\videos" mkdir "%APP_DIR%\content\videos"
if not exist "%APP_DIR%\content\applications" mkdir "%APP_DIR%\content\applications"

REM Create desktop shortcut
echo Creating desktop shortcut...
python -c "
import os, win32com.client
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
shortcut_path = os.path.join(desktop, 'Demo Mode App.lnk')
shell = win32com.client.Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = r'%APP_DIR%\demo_app.py'
shortcut.WorkingDirectory = r'%APP_DIR%'
shortcut.Arguments = ''
shortcut.save()
print('Desktop shortcut created.')
"

REM Create Start Menu entry
echo Creating Start Menu entry...
set START_MENU=%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs
if not exist "%START_MENU%\Demo Mode App" mkdir "%START_MENU%\Demo Mode App"
copy "%USERPROFILE%\Desktop\Demo Mode App.lnk" "%START_MENU%\Demo Mode App\" >nul

REM Create batch file for easy launching
echo Creating launch script...
echo @echo off > "%APP_DIR%\launch_demo.bat"
echo cd /d "%APP_DIR%" >> "%APP_DIR%\launch_demo.bat"
echo python demo_app.py >> "%APP_DIR%\launch_demo.bat"

REM Set up Windows Firewall exception (optional)
echo Setting up Windows Firewall exception...
netsh advfirewall firewall add rule name="Demo Mode App" dir=in action=allow program="%APP_DIR%\demo_app.py" enable=yes >nul 2>&1

REM Create uninstaller
echo Creating uninstaller...
echo @echo off > "%APP_DIR%\uninstall.bat"
echo echo Uninstalling Demo Mode Application... >> "%APP_DIR%\uninstall.bat"
echo reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "DemoModeApp" /f >nul 2^>^&1 >> "%APP_DIR%\uninstall.bat"
echo del "%USERPROFILE%\Desktop\Demo Mode App.lnk" >nul 2^>^&1 >> "%APP_DIR%\uninstall.bat"
echo rmdir /s /q "%APP_DIR%" >> "%APP_DIR%\uninstall.bat"
echo echo Demo Mode Application uninstalled. >> "%APP_DIR%\uninstall.bat"
echo pause >> "%APP_DIR%\uninstall.bat"

echo.
echo ===============================================
echo Installation completed successfully!
echo ===============================================
echo.
echo Application installed to: %APP_DIR%
echo Desktop shortcut created: Demo Mode App
echo Start Menu entry created: Demo Mode App
echo.
echo Next steps:
echo 1. Launch the application from desktop or Start Menu
echo 2. Set up master password in Settings
echo 3. Add your demo content (images, videos, applications)
echo 4. Configure timing and security settings
echo 5. Test demo mode functionality
echo.
echo For kiosk deployment:
echo - Enable auto-startup in Settings
echo - Configure keyboard lock (requires admin privileges)
echo - Set up content rotation schedule
echo.
echo Documentation: %APP_DIR%\DEPLOYMENT_GUIDE.md
echo Uninstaller: %APP_DIR%\uninstall.bat
echo.
pause