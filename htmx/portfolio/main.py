from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/sections/{section}", response_class=HTMLResponse)
async def get_section(request: Request, section: str):
    allowed = ["home", "projects", "skills", "about", "contact"]
    if section not in allowed:
        return HTMLResponse("<p>not found</p>", status_code=404)
    return templates.TemplateResponse(
        request, f"partials/{section}.html"
    )


@app.post("/api/message", response_class=HTMLResponse)
async def send_message(message: str = Form(...)):
    if not message.strip():
        return HTMLResponse(
            '<span style="color:var(--accent2)">✗ no message provided</span>'
        )
    return HTMLResponse(f"""
        <span style="color:var(--accent)">✓ message received:</span>
        <span style="color:var(--text)">"{message}"</span><br>
        <span style="color:var(--muted)">  → will reply within 24h</span>
    """)
