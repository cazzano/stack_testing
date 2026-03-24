unzip portfolio.zip
cd portfolio

uv init .
uv add fastapi uvicorn jinja2 python-multipart

uv run uvicorn main:app --reload
