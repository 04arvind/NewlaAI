"""Task planner for Newla AI
Generates execution plans from user requests.
"""
import json 
from typing import Dict, List, Any
from pathlib import Path
from ..llm.router import LLMRouter
from .prompts import NEWLA_SYSTEM_PROMPT, PLANNING_PROMPT
class TaskPlanner:
    """Plans tasks based on user requests."""
    def __init__(self,llm_provider:str="claude"):
        """
        Initialize task planner.
        Args:
           llm_provider:LLM provider to use
        """
        self.llm = LLMRouter(default_provider=llm_provider)
    def parse_plan(self,llm_response:str)->Dict[str,Any]:
        """
        Parse LLM response into structured plan
        Args:
           llm_response:Raw LLM response
        Returns:
           Parsed plan dictionary
        """
        try:
            # Try to extract JSON from response
            response = llm_response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            plan = json.loads(response)
            required_keys = ["analysis","tasks","expected_outcome"]
            if not all(key in plan for key in required_keys):
                raise ValueError("Plan missing required keys")
            return plan
        except json.JSONDecodeError as e:
            return{
                "analysis":"Failed to parse structured plan",
                "tasks":[
                    {
                        "task_id":1,
                        "description":"Manual execution required",
                        "type":"manual",
                        "details":{"raw_response":llm_response}
                    }
                ],
                "expected_outcome":"Manual review needed"
            }
    def create_plan(self,user_request:str)->Dict[str,Any]:
        """
        Create execution plan form user request.
        Args:
           user_request:User's project request
        Returns:
           Structured execution plan
        """
        user_prompt = PLANNING_PROMPT.format(user_request=user_request)
        llm_response = self.llm.call(
            system_prompt=NEWLA_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        plan = self.parse_plan(llm_response)
        plan["raw_llm_response"] = llm_response
        return plan
    
    def refine_plan(self,original_plan:Dict[str,Any],feedback:str)->Dict[str,Any]:
        """
        Refine an existing plan based on feedback.
        Args:
           original_plan : Original execution plan
           feedback: Feedback or error information
        Returns:
            Refined execution plan
        """
        user_prompt = f"""
Original plan:
{json.dumps(original_plan, indent=2)}

Feedback/Issues:
{feedback}

Please refine the plan to address these issues.
"""
        
        llm_response = self.llm.call(
            system_prompt=NEWLA_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        return self.parse_plan(llm_response)
    
    def get_next_task(self, plan: Dict[str, Any], completed_tasks: List[int]) -> Dict[str, Any]:
        """
        Get the next task to execute.
        
        Args:
            plan: Execution plan
            completed_tasks: List of completed task IDs
            
        Returns:
            Next task to execute or None if all complete
        """
        for task in plan.get("tasks", []):
            task_id = task.get("task_id")
            if task_id not in completed_tasks:
                return task
        
        return None