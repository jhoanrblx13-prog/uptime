# uptime

Paste URLs, one per line. The page requests each one and shows the status code, or the error if the request failed.

## Run

```bash
cd uptime
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open http://127.0.0.1:8000
