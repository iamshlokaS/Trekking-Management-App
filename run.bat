@echo off
echo Starting Trekking Management Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing dependencies...
pip install -r requirements.txt -q

REM Run the application
echo.
echo ============================================
echo Trekking Management Application
echo ============================================
echo.
echo Starting Flask server...
echo Application URL: http://localhost:5000
echo.
echo Default Admin Login:
echo   Username: admin
echo   Password: admin123
echo.
echo Press CTRL+C to stop the server
echo ============================================
echo.

python app.py
