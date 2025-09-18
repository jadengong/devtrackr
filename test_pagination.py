"""
Simple test script to verify pagination functionality.
Run this to test the new pagination features.
"""
import requests
import json
from datetime import datetime


def test_pagination():
    """Test the pagination functionality."""
    base_url = "http://localhost:8000"
    
    # First, you'll need to authenticate and get a token
    # This is a basic test - you'll need to adjust based on your auth setup
    
    print("Testing DevTrackr Pagination")
    print("=" * 40)
    
    # Test basic pagination
    print("\n1. Testing basic pagination:")
    response = requests.get(f"{base_url}/tasks?limit=5")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Items returned: {len(data.get('items', []))}")
        print(f"Has next: {data.get('has_next', False)}")
        print(f"Next cursor: {data.get('next_cursor', 'None')}")
        print(f"Total count: {data.get('total_count', 'Not requested')}")
        
        # Test next page if available
        if data.get('next_cursor'):
            print("\n2. Testing next page:")
            next_response = requests.get(
                f"{base_url}/tasks?cursor={data['next_cursor']}&limit=5"
            )
            print(f"Next page status: {next_response.status_code}")
            
            if next_response.status_code == 200:
                next_data = next_response.json()
                print(f"Next page items: {len(next_data.get('items', []))}")
                print(f"Next page has next: {next_data.get('has_next', False)}")
    
    # Test with filters
    print("\n3. Testing pagination with filters:")
    filtered_response = requests.get(f"{base_url}/tasks?status=todo&limit=3")
    print(f"Filtered status: {filtered_response.status_code}")
    
    if filtered_response.status_code == 200:
        filtered_data = filtered_response.json()
        print(f"Filtered items: {len(filtered_data.get('items', []))}")
    
    # Test with total count
    print("\n4. Testing with total count:")
    total_response = requests.get(f"{base_url}/tasks?include_total=true&limit=10")
    print(f"Total count status: {total_response.status_code}")
    
    if total_response.status_code == 200:
        total_data = total_response.json()
        print(f"Total count: {total_data.get('total_count', 'Not provided')}")


if __name__ == "__main__":
    print("Note: Make sure your DevTrackr API is running on localhost:8000")
    print("You may need to authenticate first if auth is required")
    test_pagination()
