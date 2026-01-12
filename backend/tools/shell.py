"""
Shell command execution tool for Newla AI.
Executes commands safely within workspace directory.
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional
from .safety import validate_command
import os


class ShellTool:
    """Handles safe shell command execution."""
    
    def __init__(self, workspace_root: Path, timeout: int = 30):
        """
        Initialize shell tool.
        
        Args:
            workspace_root: Root directory for command execution
            timeout: Command timeout in seconds
        """
        self.workspace_root = workspace_root.resolve()
        self.timeout = timeout
    
    def execute(self, command: str, capture_output: bool = True) -> Dict[str, any]:
        """
        Execute a shell command safely.
        
        Args:
            command: Command to execute
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Execution result dictionary
        """
        try:
            # Validate command safety
            validate_command(command)
            
            # Execute in workspace directory
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.workspace_root),
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
                env=os.environ.copy()
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "action": "execute_command",
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else None,
                "stderr": result.stderr if capture_output else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "action": "execute_command",
                "command": command,
                "error": f"Command timed out after {self.timeout} seconds"
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "execute_command",
                "command": command,
                "error": str(e)
            }
    
    def install_dependencies(self, package_manager: str, packages: list) -> Dict[str, any]:
        """
        Install dependencies using pip or npm.
        
        Args:
            package_manager: "pip" or "npm"
            packages: List of package names
            
        Returns:
            Installation result
        """
        if package_manager == "pip":
            cmd = f"pip install {' '.join(packages)}"
        elif package_manager == "npm":
            cmd = f"npm install {' '.join(packages)}"
        else:
            return {
                "status": "error",
                "error": f"Unsupported package manager: {package_manager}"
            }
        
        return self.execute(cmd)
    
    def run_server(self, command: str, background: bool = False) -> Dict[str, any]:
        """
        Start a development server.
        
        Args:
            command: Server start command
            background: Whether to run in background
            
        Returns:
            Execution result
        """
        if background:
            # For background processes, we don't capture output
            return self.execute(f"{command} &", capture_output=False)
        else:
            return self.execute(command)
    
    def git_init(self, repo_name: Optional[str] = None) -> Dict[str, any]:
        """
        Initialize a git repository.
        
        Args:
            repo_name: Optional repository name
            
        Returns:
            Git init result
        """
        result = self.execute("git init")
        
        if result["status"] == "success" and repo_name:
            # Add initial commit
            self.execute("git add .")
            self.execute(f'git commit -m "Initial commit for {repo_name}"')
        
        return result