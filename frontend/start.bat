@echo off
echo Starting GrowthPath Frontend...

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    npm install
)

REM Start the development server
echo Starting development server on http://localhost:3000
echo.
npm run dev
