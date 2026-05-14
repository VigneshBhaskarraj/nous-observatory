"""
Shared config loader for Nous Observatory scripts.
Reads OPENAI_API_KEY from scripts/.env (gitignored).
"""
import os, pathlib

def load_env():
    env_path = pathlib.Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

load_env()

SB_URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
SB_KEY = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"

def get_openai_key():
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise SystemExit(
            "\n✗  OpenAI API key not found.\n"
            "   Add it to scripts/.env:\n"
            "       OPENAI_API_KEY=sk-...\n"
        )
    return key
