# DevTrackr Pagination Guide

## Overview

DevTrackr now supports cursor-based pagination for the `/tasks` endpoint. This provides efficient, consistent pagination that works well with large datasets.

## How It Works

Cursor-based pagination uses a "cursor" (encoded token) to mark where the previous page ended, rather than using offset-based pagination. This approach:

- **Prevents duplicate/missing items** when data is added/removed
- **Scales efficiently** with large datasets
- **Maintains consistent ordering** across pages

## API Usage

### Basic Pagination

```bash
# Get first page (20 items by default)
GET /tasks

# Get first page with custom limit
GET /tasks?limit=10

# Get next page using cursor
GET /tasks?cursor=eyJpZCI6MTIzLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0xNVQxMjowMDowMCJ9&limit=10
```

### Response Format

```json
{
  "items": [
    {
      "id": 123,
      "title": "Task Title",
      "description": "Task description",
      "status": "todo",
      "priority": "medium",
      "category": "work",
      "owner_id": 1,
      "is_archived": false,
      "created_at": "2024-01-15T12:00:00Z",
      "updated_at": "2024-01-15T12:00:00Z"
    }
  ],
  "next_cursor": "eyJpZCI6MTIzLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0xNVQxMjowMDowMCJ9",
  "has_next": true,
  "total_count": null
}
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cursor` | string | null | Cursor for pagination (from previous response) |
| `limit` | integer | 20 | Number of items per page (1-100) |
| `include_total` | boolean | false | Include total count (expensive for large datasets) |

### Filtering with Pagination

All existing filters work with pagination:

```bash
# Filter by status with pagination
GET /tasks?status=todo&limit=10

# Filter by category with pagination
GET /tasks?category=work&cursor=...&limit=5

# Multiple filters
GET /tasks?status=in_progress&category=urgent&limit=15
```

## Implementation Details

### Cursor Format

Cursors are base64-encoded JSON objects containing:
- `id`: Task ID (tiebreaker for same timestamp)
- `created_at`: ISO timestamp of task creation

### Ordering

Tasks are ordered by:
1. `created_at` (descending) - most recent first
2. `id` (descending) - tiebreaker for same timestamp

### Performance

- **Fast**: Uses indexed columns (`created_at`, `id`)
- **Consistent**: No duplicate/missing items during pagination
- **Scalable**: Performance doesn't degrade with dataset size

## Client Implementation

### Python Example

```python
import requests

def get_all_tasks(base_url, headers, limit=20):
    """Fetch all tasks using pagination."""
    all_tasks = []
    cursor = None
    
    while True:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
            
        response = requests.get(f"{base_url}/tasks", params=params, headers=headers)
        data = response.json()
        
        all_tasks.extend(data["items"])
        
        if not data["has_next"]:
            break
            
        cursor = data["next_cursor"]
    
    return all_tasks
```

### JavaScript Example

```javascript
async function getAllTasks(baseUrl, headers, limit = 20) {
    const allTasks = [];
    let cursor = null;
    
    while (true) {
        const params = new URLSearchParams({ limit: limit.toString() });
        if (cursor) {
            params.append('cursor', cursor);
        }
        
        const response = await fetch(`${baseUrl}/tasks?${params}`, { headers });
        const data = await response.json();
        
        allTasks.push(...data.items);
        
        if (!data.has_next) {
            break;
        }
        
        cursor = data.next_cursor;
    }
    
    return allTasks;
}
```

## Migration from Offset Pagination

If you were previously using offset-based pagination, here's how to migrate:

### Before (Offset-based)
```bash
GET /tasks?page=2&per_page=20
```

### After (Cursor-based)
```bash
GET /tasks?cursor=<cursor_from_previous_page>&limit=20
```

### Benefits of Migration

1. **No duplicate items** when new tasks are created during pagination
2. **Better performance** on large datasets
3. **Consistent results** even with concurrent modifications
4. **Simpler client code** - just follow the cursor

## Testing

Run the test script to verify pagination works:

```bash
python test_pagination.py
```

Make sure your API is running on `localhost:8000` before running the test.
