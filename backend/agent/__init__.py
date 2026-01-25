"""
Main orchestrator for Newla AI.
Coordinates planning, execution, and validation.
"""
from typing import Dict, Any, Optional
from pathlib import Path
from .planner import TaskPlanner
from .executor import TaskExecutor
from .validator import Validator
from ..config import WORKSPACE_ROOT, MAX_RETRIES, DEFAULT_LLM

class NewlaOrchestrator:
    """Main orchestrator for Newla AI agent."""
    def __init__(
            self,
            workspace_root:Path = WORKSPACE_ROOT,
            llm_provider:str = DEFAULT_LLM
    ):
        """
        Initialize Newla orchestrator.
        
        Args:
            workspace_root: Root workspace directory
            llm_provider: LLM provider to use
        """
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True,exist_ok=True)
        self.planner = TaskPlanner(llm_provider=llm_provider)
        self.executor = TaskExecutor(self.workspace_root)
        self.validator = Validator(self.workspace_root,llm_provider=llm_provider)
        self.execution_history = []
    
    def run(self,user_prompt:str)->Dict[str,Any]:
        """
        Main execution flow.
        
        Args:
            user_prompt: User's project request
            
        Returns:
            Execution result
        """
        result = {
            "user_prompt":user_prompt,
            "status":"started",
            "steps":[]
        }
        try:
            result["steps"].append({"step":"planning","status":"started"})
            plan = self.planner.create_plan(user_prompt)
            result["plan"] = plan
            result["steps"][-1]["status"]="completed"

            result["steps"].append({"step":"execution","status":"started"})
            execution_result = self.executor.execute_plan(plan,max_retries=MAX_RETRIES)
            result["execution"] = execution_result
            if execution_result.get("failed_tasks"):
                result["steps"][-1]["status"] = "completed_with_errors"
                
                # Step 3: Error fixing (if needed)
                result["steps"].append({"step": "error_fixing", "status": "started"})
                fixed = self.fix_errors(execution_result["failed_tasks"], plan)
                result["error_fixes"] = fixed
                result["steps"][-1]["status"] = "completed"
            else:
                result["steps"][-1]["status"] = "completed"
            
            # Step 4: Validation
            result["steps"].append({"step": "validation", "status": "started"})
            files_created = self.executor.get_workspace_files()
            validation = self.validator.validate_file_structure(files_created)
            result["validation"] = validation
            result["steps"][-1]["status"] = "completed"
            
            # Final status
            if execution_result.get("failed_tasks"):
                result["status"] = "completed_with_errors"
            else:
                result["status"] = "success"
            
            # Add file listing
            result["files_created"] = files_created
            
            # Store in history
            self.execution_history.append(result)
            
            return result
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    def fix_errors(
        self, 
        failed_tasks: list, 
        original_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Attempt to fix failed tasks.
        
        Args:
            failed_tasks: List of failed tasks
            original_plan: Original execution plan
            
        Returns:
            Fix results
        """
        fixes = []
        
        for failed in failed_tasks:
            task = failed["task"]
            error = failed["last_error"]
            
            # Get fix suggestion from validator
            fix_suggestion = self.validator.analyze_error(error, task)
            
            # Try to apply fix
            fix_type = fix_suggestion.get("fix_type")
            fix_details = fix_suggestion.get("fix_details", {})
            
            if fix_type == "file_edit":
                # Re-execute with fixed content
                fixed_task = {
                    "task_id": task.get("task_id"),
                    "description": f"Fix: {task.get('description')}",
                    "type": "file_edit",
                    "details": fix_details
                }
                result = self.executor.execute_task(fixed_task)
                fixes.append({
                    "original_task": task,
                    "fix_applied": fixed_task,
                    "result": result
                })
            
            elif fix_type == "command":
                # Re-execute with fixed command
                fixed_task = {
                    "task_id": task.get("task_id"),
                    "description": f"Fix: {task.get('description')}",
                    "type": "command",
                    "details": fix_details
                }
                result = self.executor.execute_task(fixed_task)
                fixes.append({
                    "original_task": task,
                    "fix_applied": fixed_task,
                    "result": result
                })
            else:
                fixes.append({
                    "original_task": task,
                    "fix_applied": None,
                    "result": {"status": "manual_intervention_required"}
                })
        
        return {
            "total_fixes_attempted": len(fixes),
            "fixes": fixes
        }
    
    def get_project_summary(self) -> Dict[str, Any]:
        """
        Get summary of current workspace.
        
        Returns:
            Project summary
        """
        files = self.executor.get_workspace_files()
        
        return {
            "workspace_root": str(self.workspace_root),
            "total_files": len(files),
            "files": files,
            "total_executions": len(self.execution_history)
        }


def plan_and_execute(user_prompt: str) -> Dict[str, Any]:
    """
    Convenience function to run Newla AI.
    
    Args:
        user_prompt: User's project request
        
    Returns:
        Execution result
    """
    orchestrator = NewlaOrchestrator()
    return orchestrator.run(user_prompt)
