"""
Task executor for Newla AI.
Executes planned tasks using filesystem and shell tools.
"""
from typing import Dict, List, Any
from pathlib import Path
from ..tools.filesystem import FileSystemTool
from ..tools.shell import ShellTool
import time

class TaskExecutor:
    """Executes tasks from execution plan."""
    def __init__(self,workspace_root:Path):
        """
        Initialize task executor.
        Args:
           workspace_root : Root workspace directory
        """
        self.workspace_root = workspace_root
        self.fs_tool = FileSystemTool(workspace_root)
        self.shell_tool = ShellTool(workspace_root)
        self.execution_log = []
    def execute_task(self,task:Dict[str,Any])->Dict[str,Any]:
        """
        Execute a single task.
        Args:
           task: Task dictionary from plan
        Returns:   
           Execution result
        """
        task_type = task.get("type")
        details = task.get("details",{})
        result = {
            "task_id":task.get("task_id"),
            "description":task.get("description"),
            "type":task_type,
            "timestamp":time.time()
        }
        try:
            if task_type == "file_create":
                path = details.get("path")
                content = details.get("content","")
                fs_result = self.fs_tool.write_file(path,content)
            elif task_type == "file_edit":
                path = details.get("path")
                content = details.get("content","")
                fs_result = self.fs_tool.write_file(path,content)
                result.update(fs_result)
            elif task_type == "directory_create":
                path = details.get("path")
                fs_result = self.fs_tool.create_directory(path)
                result.update(fs_result)
            elif task_type == "command":
                command = details.get("command")
                shell_result = self.shell_tool.execute(command)
                result.update(shell_result)
            elif task_type == "install_dependencies":
                package_manager = details.get("package_manager","pip")
                packages = details.get("packages",[])
                shell_result = self.shell_tool.install_dependencies(
                    package_manager,packages
                )
                result.update(shell_result)
            elif task_type == "validation":
                validation_type = details.get("validation_type")
                if validation_type == "file_exists":
                    path = details.get("path")
                    exists = self.fs_tool.file_exists(path)
                    result["status"] = "success" if exists else "error"
                    result["exists"] = exists
                else:
                    result["status"] = "success"
                    result["message"] = "validation placeholder"
            else:
                result["status"] = "error"
                result["error"] = f"Unknown task type : {task_type}"

            self.execution_log.append(result)
            return result
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.execution_log.append(result)
            return result
        
    def execute_plan(self,plan:Dict[str,Any],max_retries:int=3)->Dict[str,Any]:
        """
        Execute entire plan.
        Args:
           plan : Execution plan from planner
           max_retries : Maximum retries per task
        Returns :
           Execution summary
        """
        tasks = plan.get("tasks",[])
        results = []
        failed_tasks = []
        for task in tasks:
            retry_count = 0
            success = False
            while retry_count <max_retries and not success:
                result = self.execute_task(task)
                if result.get("status")=="success":
                    success = True
                    results.append(result)
                else:
                    retry_count +=1
                    if retry_count >= max_retries:
                        failed_tasks.append({
                            "task":task,
                            "last_error":result.get("error")
                        })
                        results.append(result)
        return{
             "plan_analysis": plan.get("analysis"),
            "expected_outcome": plan.get("expected_outcome"),
            "total_tasks": len(tasks),
            "successful_tasks": len(tasks) - len(failed_tasks),
            "failed_tasks": failed_tasks,
            "results": results,
            "execution_log": self.execution_log
        }
    
    def get_workspace_files(self) -> List[str]:
        """Get list of all files in workspace."""
        files = []
        for item in self.workspace_root.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.workspace_root)
                files.append(str(rel_path))
        return files
    
    def read_file_content(self, path: str) -> str:
        """Read content of a file."""
        result = self.fs_tool.read_file(path)
        if result.get("status") == "success":
            return result.get("content", "")
        return ""