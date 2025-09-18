"""
Test script for the full-text search functionality.
"""
import requests
import json
from datetime import datetime


def test_search_functionality():
    """Test the search functionality."""
    base_url = "http://localhost:8000"
    
    print("Testing DevTrackr Full-Text Search")
    print("=" * 40)
    
    # Test basic search
    print("\n1. Testing basic search:")
    response = requests.get(f"{base_url}/tasks/search?q=API")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Query: '{data['query']}'")
        print(f"Results found: {data['total_matches']}")
        print(f"Items returned: {len(data['items'])}")
        print(f"Search time: {data['search_time_ms']}ms")
        
        if data.get('suggestions'):
            print(f"Suggestions: {data['suggestions'][:3]}")  # Show first 3
    
    # Test search with filters
    print("\n2. Testing search with filters:")
    filtered_response = requests.get(
        f"{base_url}/tasks/search?q=task&status=todo&limit=5"
    )
    print(f"Filtered search status: {filtered_response.status_code}")
    
    if filtered_response.status_code == 200:
        filtered_data = filtered_response.json()
        print(f"Filtered results: {filtered_data['total_matches']}")
        print(f"Items returned: {len(filtered_data['items'])}")
    
    # Test search suggestions
    print("\n3. Testing search suggestions:")
    suggestions_response = requests.get(
        f"{base_url}/tasks/search?q=doc&include_suggestions=true"
    )
    print(f"Suggestions status: {suggestions_response.status_code}")
    
    if suggestions_response.status_code == 200:
        suggestions_data = suggestions_response.json()
        print(f"Suggestions: {suggestions_data.get('suggestions', [])}")
    
    # Test complex search
    print("\n4. Testing complex search:")
    complex_response = requests.get(
        f"{base_url}/tasks/search?q=API documentation review&priority=high&limit=10"
    )
    print(f"Complex search status: {complex_response.status_code}")
    
    if complex_response.status_code == 200:
        complex_data = complex_response.json()
        print(f"Complex query: '{complex_data['query']}'")
        print(f"Complex results: {complex_data['total_matches']}")
    
    # Test empty search
    print("\n5. Testing empty search:")
    empty_response = requests.get(f"{base_url}/tasks/search?q=")
    print(f"Empty search status: {empty_response.status_code}")
    
    # Test invalid search
    print("\n6. Testing invalid search:")
    invalid_response = requests.get(f"{base_url}/tasks/search?q=!!!")
    print(f"Invalid search status: {invalid_response.status_code}")


def create_sample_tasks():
    """Create some sample tasks for testing search."""
    base_url = "http://localhost:8000"
    
    sample_tasks = [
        {
            "title": "API Documentation Review",
            "description": "Review and update the API documentation for the new endpoints",
            "category": "documentation",
            "priority": "high"
        },
        {
            "title": "Implement Search Functionality",
            "description": "Add full-text search across tasks using PostgreSQL",
            "category": "development",
            "priority": "medium"
        },
        {
            "title": "Database Migration",
            "description": "Create migration for search indexes and full-text search",
            "category": "database",
            "priority": "urgent"
        },
        {
            "title": "Code Review",
            "description": "Review the new search implementation and pagination features",
            "category": "development",
            "priority": "medium"
        },
        {
            "title": "API Testing",
            "description": "Test the search endpoints and validate results",
            "category": "testing",
            "priority": "high"
        }
    ]
    
    print("\nCreating sample tasks for search testing...")
    created_tasks = []
    
    for task_data in sample_tasks:
        response = requests.post(f"{base_url}/tasks", json=task_data)
        if response.status_code == 201:
            created_tasks.append(response.json())
            print(f"Created: {task_data['title']}")
        else:
            print(f"Failed to create: {task_data['title']} - {response.status_code}")
    
    return created_tasks


if __name__ == "__main__":
    print("Note: Make sure your DevTrackr API is running on localhost:8000")
    print("You may need to authenticate first if auth is required")
    
    # Uncomment the next line to create sample tasks first
    # create_sample_tasks()
    
    test_search_functionality()
