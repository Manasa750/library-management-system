# PowerShell script to start PostgreSQL and FastAPI app

# Start PostgreSQL service (correct service name)
Start-Service postgresql-x64-16

# Activate virtual environment
. .venv\Scripts\Activate.ps1

# Start FastAPI app with uvicorn
python -m uvicorn main:app --reload
