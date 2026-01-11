# Newla AI - Quick Start Guide

Get up and running with Newla AI in under 5 minutes!

## Prerequisites

- Python 3.10+
- API key for Claude or Gemini

### Get API Keys

**Claude (Anthropic):**

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new key

**Gemini (Google):**

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key

## Installation

### 1. Navigate to Project

```bash
cd newla-ai
```

### 2. Set Up Environment

**Option A: Use the startup script (Linux/Mac)**

```bash
./start.sh
```

**Option B: Manual setup**

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Your `.env` should look like:

```
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxx
DEFAULT_LLM=claude
```

### 4. Start the Server

```bash
cd backend
python main.py
```

You should see:

```
🚀 Starting Newla AI
============================================================
Workspace: workspace
LLM Provider: claude
============================================================
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## First Request

### Using cURL

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a simple hello.html file that says Hello World with nice styling"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/run",
    json={
        "prompt": "Create a simple calculator in Python that can add, subtract, multiply, and divide"
    }
)

print(response.json())
```

### Check Results

```bash
# List created files
curl http://localhost:8000/workspace/files

# View a specific file
curl http://localhost:8000/workspace/files/hello.html
```

## Test the System

Run the test script to verify everything works:

```bash
python test_newla.py
```

This will:

- Test file operations
- Test safety validation
- Test shell commands
- Optionally test LLM integration

## Example Projects

See `examples.py` for ready-to-use examples:

1. Simple website
2. Python scripts
3. Flask web app
4. Data analysis
5. React components

## Common Issues

### "API key not found"

- Make sure you created `.env` file
- Check API key is correctly set
- Restart the server after changing `.env`

### "Module not found"

- Activate virtual environment
- Run `pip install -r requirements.txt`

### "Permission denied" for start.sh

- Run `chmod +x start.sh`

### Port 8000 already in use

- Change port in `backend/main.py`
- Or kill the process using port 8000

## Next Steps

1. Read the full README.md
2. Try the examples in examples.py
3. Build your own projects!
4. Check the API documentation at http://localhost:8000/docs

## Getting Help

- Check README.md for detailed documentation
- Review examples.py for common patterns
- Open an issue on GitHub

---

**Happy building with Newla AI**
