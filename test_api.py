# import requests

# # Test health
# print("Testing health endpoint...")
# response = requests.get("http://localhost:8000/health")
# print(f"Status: {response.status_code}")
# print(f"Response: {response.json()}")
# print()

# # Test workspace
# print("Testing workspace endpoint...")
# response = requests.get("http://localhost:8000/workspace")
# print(f"Status: {response.status_code}")
# print(f"Response: {response.json()}")
# print()

# # Test file listing
# print("Testing file listing...")
# response = requests.get("http://localhost:8000/workspace/files")
# print(f"Status: {response.status_code}")
# print(f"Response: {response.json()}")