"""
Validator for Newla AI.
Validates generated projects and detects errors.
"""

from typing import Dict, List, Any
from pathlib import Path
from ..tools.filesystem import FileSystemTool
from ..tools.shell import ShellTool
from ..llm.router import LLMRouter
from .prompts import VALIDATION_PROMPT, ERROR_FIX_PROMPT
import json


class Validator:
    """Validates project correctness."""
    
    def __init__(self, workspace_root: Path, llm_provider: str = "claude"):
        """
        Initialize validator.
        
        Args:
            workspace_root: Workspace directory
            llm_provider: LLM provider for validation
        """
        self.workspace_root = workspace_root
        self.fs_tool = FileSystemTool(workspace_root)
        self.shell_tool = ShellTool(workspace_root)
        self.llm = LLMRouter(default_provider=llm_provider)
    
    def validate_file_structure(self, expected_files: List[str]) -> Dict[str, Any]:
        """
        Validate that expected files exist.
        
        Args:
            expected_files: List of expected file paths
            
        Returns:
            Validation result
        """
        missing_files = []
        existing_files = []
        
        for file_path in expected_files:
            if self.fs_tool.file_exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        return {
            "valid": len(missing_files) == 0,
            "existing_files": existing_files,
            "missing_files": missing_files
        }
    
    def validate_syntax(self, file_path: str, language: str) -> Dict[str, Any]:
        """
        Validate file syntax.
        
        Args:
            file_path: Path to file
            language: Programming language (python, javascript, etc.)
            
        Returns:
            Validation result
        """
        result = {"valid": True, "errors": []}
        
        if language == "python":
            # Check Python syntax
            cmd_result = self.shell_tool.execute(f"python -m py_compile {file_path}")
            if cmd_result.get("returncode") != 0:
                result["valid"] = False
                result["errors"].append(cmd_result.get("stderr", ""))
                
        elif language == "javascript":
            # Check JavaScript syntax (if node is available)
            cmd_result = self.shell_tool.execute(f"node --check {file_path}")
            if cmd_result.get("returncode") != 0:
                result["valid"] = False
                result["errors"].append(cmd_result.get("stderr", ""))
        
        return result
    
    def run_tests(self, test_command: str) -> Dict[str, Any]:
        """
        Run project tests.
        
        Args:
            test_command: Command to run tests
            
        Returns:
            Test results
        """
        result = self.shell_tool.execute(test_command)
        
        return {
            "passed": result.get("returncode") == 0,
            "output": result.get("stdout", ""),
            "errors": result.get("stderr", "")
        }
    
    def validate_with_llm(self, files_content: Dict[str, str]) -> Dict[str, Any]:
        """
        Use LLM to validate code quality.
        
        Args:
            files_content: Dictionary of file paths to content
            
        Returns:
            LLM validation result
        """
        files_str = json.dumps(files_content, indent=2)
        user_prompt = VALIDATION_PROMPT.format(files=files_str)
        
        try:
            llm_response = self.llm.call(
                system_prompt="You are a code reviewer. Validate code and return JSON.",
                user_prompt=user_prompt
            )
            
            # Parse response
            response = llm_response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            
            return json.loads(response)
            
        except Exception as e:
            return {
                "valid": True,
                "issues": [],
                "suggestions": [],
                "error": str(e)
            }
    
    def analyze_error(self, error_details: str, failed_task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze error and suggest fix.
        
        Args:
            error_details: Error message
            failed_task: Task that failed
            
        Returns:
            Fix suggestion
        """
        user_prompt = ERROR_FIX_PROMPT.format(
            error_details=error_details,
            failed_task=json.dumps(failed_task, indent=2)
        )
        
        try:
            llm_response = self.llm.call(
                system_prompt="You are a debugging expert. Analyze errors and provide fixes as JSON.",
                user_prompt=user_prompt
            )
            
            # Parse response
            response = llm_response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            
            return json.loads(response)
            
        except Exception as e:
            return {
                "analysis": "Failed to analyze error",
                "fix_type": "manual",
                "fix_details": {},
                "error": str(e)
            }
    
    def comprehensive_validation(
        self, 
        expected_files: List[str],
        test_command: str = None
    ) -> Dict[str, Any]:
        """
        Run comprehensive validation.
        
        Args:
            expected_files: Expected files in project
            test_command: Optional test command
            
        Returns:
            Complete validation report
        """
        report = {
            "overall_valid": True,
            "checks": {}
        }
        
        # Check file structure
        structure_check = self.validate_file_structure(expected_files)
        report["checks"]["file_structure"] = structure_check
        if not structure_check["valid"]:
            report["overall_valid"] = False
        
        # Run tests if provided
        if test_command:
            test_results = self.run_tests(test_command)
            report["checks"]["tests"] = test_results
            if not test_results["passed"]:
                report["overall_valid"] = False
        
        return report