"""
Newla AI - FastAPI entry point
local autonomous agent for software development
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# from agent import plan_and_execute, NewlaOrchestrator
from backend.agent import NewlaOrchestrator, plan_and_execute

from config import WORKSPACE_ROOT, DEFAULT_LLM

app = FastAPI(
    title="Newla AI",
    description="Local autonomous software engineer agent",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = NewlaOrchestrator(
    workspace_root = WORKSPACE_ROOT,
    llm_provider = DEFAULT_LLM
)

class ProjectRequest(BaseModel):
    """Request model for project creation."""
    prompt: str
    llm_provider: Optional[str] = None

class StatusResponse(BaseModel):
    """Response model for status check."""
    status: str
    message: str

@app.get("/",response_model=StatusResponse)
async def root():
    """Root endpoint - health check."""
    return{
        "status":"active",
        "message":"Newla AI is running."
    }
@app.get("/health",response_model=StatusResponse)
async def health_check():
    """Health check endpoint."""
    return{
        "status":"healthy",
        "message":"All systems operational."
    }
@app.post("/run")
async def run_agent(request:ProjectRequest)->Dict[str,Any]:
    """
    Main endpoint to run Newla AI agent.
    
    Args:
        request: Project request with prompt
        
    Returns:
        Execution result
    """
    try:
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400,detail="Prompt cannot be empty.")
        if request.llm_provider:
            temp_orchestrator = NewlaOrchestrator(
                workspace_root = WORKSPACE_ROOT,
                llm_provider = request.llm_provider
            )
            result = temp_orchestrator.run(request.prompt)
        else:
            result = orchestrator.run(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.get("/workspace")
async def get_workspace_info()->Dict[str,Any]:
    """
    Get information about current workspace.
    Returns:
        Workspace information
    """
    try:
        return orchestrator.get_project_summary()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.get("/workspace/files")
async def list_workspace_files()->Dict[str,Any]:
    """
    List all files in workspace.
    Returns:
      File listing
    """
    try:
        files = orchestrator.executor.get_workspace_files()
        return{
            "total":len(files),
            "files":files
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.post("/workspace/files/{file_path:path}")
async def read_workspace_file(file_path:str)->Dict[str,Any]:
    """
    Read content of a specific file.
    
    Args:
        file_path: Path to file relative to workspace
        
    Returns:
        File content
    """
    try:
        content = orchestrator.executor.read_file_content(file_path)
        if content:
            return {
                "path": file_path,
                "content": content
            }
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
@app.get("/history")
async def get_execution_history()->Dict[str,Any]:
    """
    Get execution history.
    Returns:
        Execution history
    """
    try:
        return{
            "total_executions": len(orchestrator.execution_history),
            "history": orchestrator.execution_history
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/reset")
async def reset_workspace()->StatusResponse:
    """
    Reset workspace
    Returns:
        status message
    """
    try:
        return{
            "status":"success",
            "message":"Reset functionality not yet implemented for safety"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("Starting Newla AI")
    print("="*60)
    print(f"Workspace Root: {WORKSPACE_ROOT}")
    print(f"LLM provider: {DEFAULT_LLM}")
    print("="*60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    
    