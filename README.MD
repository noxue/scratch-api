python -m venv .venv
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install bcrypt
pip install "python-jose[cryptography]"
uvicorn app:app --port=9999 --reload