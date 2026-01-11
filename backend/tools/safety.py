"""
Safety enforcement for Newla AI
Ensures all operations are sandboxed within workspace/.
"""
from pathlib import Path
from typing import List

FORBIDDEN_PATTERNS = [
     "..",
    "~",
    "rm -rf",
    "shutdown",
    "kill -9",
    "reboot",
    "sudo",
    "chmod 777",
    "mkfs",
    "dd if=",
    ":(){ :|:& };:",  # Fork bomb
]
ALLOWED_COMMANDS=[
    "python",
    "node",
    "npm",
    "pip",
    "git",
    "ls",
    "cat",
    "echo",
    "mkdir",
    "touch",
    "cd",
    "pwd",
    "which",
    "uvicorn",
    "flask",
    "serve",
    "http-server",
]
def validate_command(cmd:str)->bool:
    """
    Validate that a command is safe to execute
    Args:
       cmd: Command string to validate
    Returns:
       True if safe, raises RuntimeError if unsafe
    Raises:
       RuntimeError: If command contains forbidden patterns
    """
    cmd_lower = cmd.lower().strip()

    for pattern in FORBIDDEN_PATTERNS:
        if pattern in cmd_lower:
            raise RuntimeError(f"Unsafe command detected: '{pattern}' found in '{cmd}' ")
    
    first_word = cmd.split()[0] if cmd.split() else ""
    is_allowed = any(first_word.startswith(allowed) for allowed in ALLOWED_COMMANDS)

    if not is_allowed:
        raise RuntimeError(f"command '{first_word}' is not in the allowed list")
    return True

def validate_path(path:str,workspace_root:Path)->Path:
    """
    Validate that a path is within the workspace boundary.
    Args:
       path : Path string to validate
       workspace_root : Rooth workspace directory
    Returns:
       Resolved absolute path if valid
    Raises:
       RuntimeError: If path escapes workspace
    """
    target_path = Path(path)
    if target_path.is_absolute():
        raise RuntimeError(f"Absolute path not allowed : {path}")
    
    path_str = str(target_path)
    if ".." in path_str:
        raise RuntimeError(f"Path traversal (..) not allowed: {path}")
    if "~" in path_str:
        raise RuntimeError(f"Home directory (~) not allowed: {path}")
    
    full_path = (workspace_root/target_path).resolve()

    try:
        full_path.relative_to(workspace_root.resolve())
    except ValueError:
        raise RuntimeError(f"Path escapes workspace:{path}")
    return full_path

def validate_file_operation(path:str,operation:str)->bool:
    """
    Validate file operations.
    Args:
       path : File path
       operation : Operation type (read,write,delete)
    Returns:
       True if allowed
    Raises:
       RuntineError: If operation is unsafe
    """

    if operation == "delete":
        critical_files = ["__init__py","config.py","main.py"]
        if any(critical_files in path for critical in critical_files):
            raise RuntimeError(f"Can not delete critical file: {path}")
    return True