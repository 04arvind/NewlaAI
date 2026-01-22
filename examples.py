"""
Example usage scripts for Newla AI
Demonstrates common use cases
"""

import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"


def example_1_simple_website():
    """Example 1: Create a simple HTML website."""
    
    print("Example 1: Simple Website")
    print("-" * 60)
    
    prompt = """
    Create a single-page gym website.
    File: gym.html
    Gym Name: Iron Temple Gym
    Sections: Hero, Membership Plans, Trainers, Contact
    Use modern UI and responsive CSS.
    Include inline CSS and make it visually appealing.
    """
    
    response = requests.post(
        f"{BASE_URL}/run",
        json={"prompt": prompt}
    )
    
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Files created: {result.get('files_created', [])}")
    print("\n")


def example_2_python_script():
    """Example 2: Create a Python script."""
    
    print("Example 2: Python Script")
    print("-" * 60)
    
    prompt = """
    Create a Python script that:
    1. Generates 10 random passwords
    2. Each password is 12 characters long
    3. Uses letters, numbers, and special characters
    4. Saves passwords to passwords.txt
    5. Prints them to console
    
    File: password_generator.py
    Include comments and good code structure.
    """
    
    response = requests.post(
        f"{BASE_URL}/run",
        json={"prompt": prompt}
    )
    
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Files created: {result.get('files_created', [])}")
    print("\n")


def example_3_web_app():
    """Example 3: Create a web application."""
    
    print("Example 3: Flask Web App")
    print("-" * 60)
    
    prompt = """
    Create a Flask web application with:
    
    Files:
    - app.py (main Flask app)
    - templates/index.html (homepage)
    - requirements.txt
    
    Features:
    - Homepage with a form to submit tasks
    - In-memory task list
    - Display all tasks
    - Route to add task
    - Route to list tasks
    - Simple CSS styling
    
    Make it production-ready with proper structure.
    """
    
    response = requests.post(
        f"{BASE_URL}/run",
        json={"prompt": prompt}
    )
    
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Files created: {result.get('files_created', [])}")
    print("\n")


def example_4_data_analysis():
    """Example 4: Create a data analysis script."""
    
    print("Example 4: Data Analysis")
    print("-" * 60)
    
    prompt = """
    Create a Python data analysis script:
    
    File: analyze_sales.py
    
    The script should:
    1. Generate sample sales data (100 rows)
    2. Data includes: date, product, quantity, price
    3. Calculate total sales per product
    4. Find best-selling product
    5. Create a simple bar chart visualization
    6. Save results to sales_report.txt
    
    Use pandas for data manipulation.
    Include all necessary imports.
    """
    
    response = requests.post(
        f"{BASE_URL}/run",
        json={"prompt": prompt}
    )
    
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Files created: {result.get('files_created', [])}")
    print("\n")


def example_5_react_component():
    """Example 5: Create a React component."""
    
    print("Example 5: React Component")
    print("-" * 60)
    
    prompt = """
    Create a React countdown timer component:
    
    File: CountdownTimer.jsx
    
    Features:
    - Input field for seconds
    - Start button
    - Pause button
    - Reset button
    - Display time in MM:SS format
    - Use React hooks (useState, useEffect)
    - Include inline styles
    - Add comments explaining the code
    
    Make it a complete, working component.
    """
    
    response = requests.post(
        f"{BASE_URL}/run",
        json={"prompt": prompt}
    )
    
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Files created: {result.get('files_created', [])}")
    print("\n")


def check_workspace():
    """Check current workspace status."""
    
    print("Current Workspace Status")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/workspace")
    workspace = response.json()
    
    print(f"Workspace: {workspace['workspace_root']}")
    print(f"Total files: {workspace['total_files']}")
    print(f"Total executions: {workspace['total_executions']}")
    
    if workspace['files']:
        print("\nFiles:")
        for file in workspace['files']:
            print(f"  - {file}")
    
    print("\n")


def main():
    """Run example demonstrations."""
    
    print("=" * 60)
    print("Newla AI - Example Usage Demonstrations")
    print("=" * 60)
    print("\nMake sure the Newla AI server is running on port 8000")
    print("Start it with: cd backend && python main.py")
    print("\n")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("Server is not responding!")
            return
        
        print("Server is running\n")
        
        # Check initial workspace
        check_workspace()
        
        # Run examples
        print("Running examples...\n")
        
        # Uncomment the examples you want to run:
        
        # example_1_simple_website()
        # example_2_python_script()
        # example_3_web_app()
        # example_4_data_analysis()
        # example_5_react_component()
        
        print("\nTo run examples, uncomment them in the main() function")
        print("of examples.py and run again.")
        
        # Final workspace check
        print("\n")
        check_workspace()
        
    except requests.exceptions.ConnectionError:
        print("Could not connect to server!")
        print("Make sure Newla AI is running: cd backend && python main.py")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()