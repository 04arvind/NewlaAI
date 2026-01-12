"""
Filesystem operations tool for Newla AI.
All operations are restricted to workspace/ directory.
"""

from pathlib import Path
from typing import Optional, List, Dict
import os
import shutil
from .safety import validate_path, validate_file_operation


class FileSystemTool:
    """Handles all filesystem operations within workspace."""
    
    def __init__(self, workspace_root: Path):
        """
        Initialize filesystem tool.
        
        Args:
            workspace_root: Root directory for all operations
        """
        self.workspace_root = workspace_root.resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)
    
    def write_file(self, path: str, content: str) -> Dict[str, str]:
        """
        Create or overwrite a file with content.
        
        Args:
            path: Relative path within workspace
            content: File content
            
        Returns:
            Status dictionary
        """
        try:
            full_path = validate_path(path, self.workspace_root)
            validate_file_operation(path, "write")
            
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            full_path.write_text(content, encoding="utf-8")
            
            return {
                "status": "success",
                "action": "write_file",
                "path": str(full_path.relative_to(self.workspace_root)),
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "write_file",
                "path": path,
                "error": str(e)
            }
    
    def read_file(self, path: str) -> Dict[str, str]:
        """
        Read file content.
        
        Args:
            path: Relative path within workspace
            
        Returns:
            File content or error
        """
        try:
            full_path = validate_path(path, self.workspace_root)
            validate_file_operation(path, "read")
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            content = full_path.read_text(encoding="utf-8")
            
            return {
                "status": "success",
                "action": "read_file",
                "path": str(full_path.relative_to(self.workspace_root)),
                "content": content
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "read_file",
                "path": path,
                "error": str(e)
            }
    
    def create_directory(self, path: str) -> Dict[str, str]:
        """
        Create a directory.
        
        Args:
            path: Relative path within workspace
            
        Returns:
            Status dictionary
        """
        try:
            full_path = validate_path(path, self.workspace_root)
            full_path.mkdir(parents=True, exist_ok=True)
            
            return {
                "status": "success",
                "action": "create_directory",
                "path": str(full_path.relative_to(self.workspace_root))
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "create_directory",
                "path": path,
                "error": str(e)
            }
    
    def list_directory(self, path: str = ".") -> Dict[str, any]:
        """
        List directory contents.
        
        Args:
            path: Relative path within workspace
            
        Returns:
            Directory listing
        """
        try:
            full_path = validate_path(path, self.workspace_root)
            
            if not full_path.exists():
                raise FileNotFoundError(f"Directory not found: {path}")
            
            if not full_path.is_dir():
                raise NotADirectoryError(f"Not a directory: {path}")
            
            items = []
            for item in full_path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
            
            return {
                "status": "success",
                "action": "list_directory",
                "path": str(full_path.relative_to(self.workspace_root)),
                "items": items
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "list_directory",
                "path": path,
                "error": str(e)
            }
    
    def delete_file(self, path: str) -> Dict[str, str]:
        """
        Delete a file (use with caution).
        
        Args:
            path: Relative path within workspace
            
        Returns:
            Status dictionary
        """
        try:
            full_path = validate_path(path, self.workspace_root)
            validate_file_operation(path, "delete")
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            if full_path.is_file():
                full_path.unlink()
            elif full_path.is_dir():
                shutil.rmtree(full_path)
            
            return {
                "status": "success",
                "action": "delete_file",
                "path": str(full_path.relative_to(self.workspace_root))
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "delete_file",
                "path": path,
                "error": str(e)
            }
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        try:
            full_path = validate_path(path, self.workspace_root)
            return full_path.exists()
        except:
            return False