import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="uptime")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=str(ROOT / "templates"))


def normalize(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    if not line.startswith("http://") and not line.startswith("https://"):
        return "https://" + line
    return line


def check(url: str) -> dict:
    try:
        response = httpx.get(url, follow_redirects=True, timeout=8)
        ok = response.status_code < 400
        return {"url": url, "ok": ok, "status": response.status_code, "detail": "up" if ok else "error status"}
    except Exception as exc:
        return {"url": url, "ok": False, "status": "—", "detail": type(exc).__name__}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"draft": "", "rows": None})


@app.post("/check", response_class=HTMLResponse)
def run(request: Request, urls: str = Form(...)):
    rows = [check(url) for url in (normalize(line) for line in urls.splitlines()) if url]
    return templates.TemplateResponse(request, "index.html", {"draft": urls, "rows": rows})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
