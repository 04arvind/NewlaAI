import os 
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv()

CLAUDE_API_KEY= os.getenv("CLAUDE_API_KEY","")
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY","")

WORKSPACE_ROOT = BASE_DIR/"workspace"

DEFAULT_LLM = "claude" # or gemini

CLAUDE_MODEL="claude-3-haiku-20240307"
GEMINI_MODEL="gemini-1.5-flash"

MAX_RETRIES=3
COMMAND_TIMEOUT=30
