"""
Test script for Newla AI
Run this to verify basic functionality
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from .backend.agent import NewlaOrchestrator
from .backend.config import WORKSPACE_ROOT


def test_basic_functionality():
    """Test basic agent functionality."""
    
    print("=" * 60)
    print("Testing Newla AI - Basic Functionality")
    print("=" * 60)
    
    # Initialize orchestrator
    print("\n1. Initializing orchestrator...")
    orchestrator = NewlaOrchestrator()
    print(" Orchestrator initialized")
    
    # Test workspace creation
    print("\n2. Testing workspace...")
    summary = orchestrator.get_project_summary()
    print(f" Workspace: {summary['workspace_root']}")
    print(f" Total files: {summary['total_files']}")
    
    # Test file operations
    print("\n3. Testing file operations...")
    result = orchestrator.executor.fs_tool.write_file(
        "test.txt",
        "Hello from Newla AI"
    )
    if result["status"] == "success":
        print(" File write successful")
    else:
        print(f" File write failed: {result.get('error')}")
        return False
    
    # Test file read
    read_result = orchestrator.executor.fs_tool.read_file("test.txt")
    if read_result["status"] == "success":
        print(" File read successful")
        print(f"   Content: {read_result['content'][:50]}...")
    else:
        print(f" File read failed: {read_result.get('error')}")
        return False
    
    # Test directory operations
    print("\n4. Testing directory operations...")
    dir_result = orchestrator.executor.fs_tool.create_directory("test_dir")
    if dir_result["status"] == "success":
        print(" Directory creation successful")
    else:
        print(f" Directory creation failed: {dir_result.get('error')}")
        return False
    
    # Test safety validation
    print("\n5. Testing safety validation...")
    from backend.tools.safety import validate_command, validate_path
    
    try:
        validate_command("python script.py")
        print(" Safe command validated")
    except RuntimeError as e:
        print(f" Safe command rejected: {e}")
        return False
    
    try:
        validate_command("rm -rf /")
        print(" Unsafe command not caught!")
        return False
    except RuntimeError:
        print(" Unsafe command blocked")
    
    try:
        validate_path("../etc/passwd", WORKSPACE_ROOT)
        print(" Path traversal not caught!")
        return False
    except RuntimeError:
        print(" Path traversal blocked")
    
    # Test shell commands
    print("\n6. Testing shell commands...")
    shell_result = orchestrator.executor.shell_tool.execute("echo 'Hello Shell'")
    if shell_result["status"] == "success":
        print(" Shell command execution successful")
        print(f" Output: {shell_result['stdout'].strip()}")
    else:
        print(f" Shell command failed: {shell_result.get('error')}")
    
    print("\n" + "=" * 60)
    print(" All basic tests passed!")
    print("=" * 60)
    
    return True


def test_simple_project():
    """Test creating a simple project."""
    
    print("\n" + "=" * 60)
    print(" Testing Simple Project Creation")
    print("=" * 60)
    
    orchestrator = NewlaOrchestrator()
    
    # Create a simple HTML file
    simple_request = """
    Create a simple HTML file named hello.html with:
    - A title "Hello Newla"
    - A heading "Welcome to Newla AI"
    - A paragraph explaining what Newla AI is
    - Basic CSS styling (centered, nice colors)
    """
    
    print("\nRequest:")
    print(simple_request)
    print("\nNote: This test requires API keys to be configured.")
    print("If you haven't set up API keys, this test will be skipped.")
    
    try:
        result = orchestrator.run(simple_request)
        
        print(f"\nStatus: {result['status']}")
        if result['status'] == 'success':
            print(" Project created successfully!")
            print(f"Files created: {result.get('files_created', [])}")
        else:
            print(f"  Project completed with status: {result['status']}")
            
    except Exception as e:
        print(f"\n Could not run LLM test: {e}")
        print("This is expected if API keys are not configured.")
    
    print("=" * 60)

if __name__ == "__main__":
    print("\nStarting Newla AI Tests\n")
    
    # Run basic tests
    if test_basic_functionality():
        # Optionally run project test
        user_input = input("\n\nRun LLM-based project test? (requires API keys) [y/N]: ")
        if user_input.lower() == 'y':
            test_simple_project()
    else:
        print("\nBasic tests failed!")
        sys.exit(1)
    
    print("\nTesting complete!\n")