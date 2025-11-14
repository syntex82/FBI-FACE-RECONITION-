@echo off
echo ============================================================
echo    FUTURISTIC BIOMETRIC AUTHENTICATION SYSTEM
echo ============================================================
echo.
echo Select an option:
echo.
echo 1. Test UI Components (Static Demo)
echo 2. Run Simple Demo (Identification Only)
echo 3. Run Full Application (Enrollment + Identification)
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting UI Component Test...
    python test_futuristic_ui.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Simple Demo...
    echo Press SPACE to reset, Q to quit
    python futuristic_demo.py
) else if "%choice%"=="3" (
    echo.
    echo Starting Full Application...
    echo Press I for Identify, E for Enroll, R to Reset, Q to Quit
    python futuristic_app.py
) else if "%choice%"=="4" (
    echo.
    echo Goodbye!
    exit
) else (
    echo.
    echo Invalid choice. Please run again.
)

echo.
pause

