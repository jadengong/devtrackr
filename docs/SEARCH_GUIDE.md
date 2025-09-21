# DevTrackr Full-Text Search Guide

## Overview

DevTrackr now includes powerful full-text search capabilities that allow you to quickly find tasks across titles and descriptions using PostgreSQL's advanced text search features.

## Features

- **Full-text search** across task titles and descriptions
- **Relevance ranking** - most relevant results first
- **Advanced filtering** - combine search with status, category, priority, and date filters
- **Search suggestions** - get suggestions based on existing content
- **Performance optimized** - uses PostgreSQL GIN indexes for fast searches
- **Query normalization** - handles special characters and whitespace

## API Usage

### Basic Search

```bash
# Search for tasks containing "API"
GET /tasks/search?q=API

# Search with limit
GET /tasks/search?q=documentation&limit=10

# Search with suggestions
GET /tasks/search?q=doc&include_suggestions=true
```

### Advanced Filtering

```bash
# Search with status filter
GET /tasks/search?q=review&status=todo

# Search with category filter
GET /tasks/search?q=API&category=development

# Search with priority filter
GET /tasks/search?q=urgent&priority=high

# Search with date filters
GET /tasks/search?q=task&created_after=2024-01-01&created_before=2024-12-31

# Multiple filters
GET /tasks/search?q=documentation&status=in_progress&priority=medium&category=docs
```

### Response Format

```json
{
  "items": [
    {
      "id": 123,
      "title": "API Documentation Review",
      "description": "Review and update the API documentation",
      "status": "todo",
      "priority": "high",
      "category": "documentation",
      "owner_id": 1,
      "is_archived": false,
      "created_at": "2024-01-15T12:00:00Z",
      "updated_at": "2024-01-15T12:00:00Z"
    }
  ],
  "query": "API documentation",
  "total_matches": 5,
  "search_time_ms": 12.5,
  "suggestions": [
    "API Documentation Review",
    "API Testing Guide",
    "Documentation Standards"
  ]
}
```

## Search Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query (1-200 characters) |
| `limit` | integer | 20 | Number of results to return (1-100) |
| `status` | string | null | Filter by task status (todo, in_progress, done) |
| `category` | string | null | Filter by task category |
| `priority` | string | null | Filter by priority (low, medium, high, urgent) |
| `created_after` | datetime | null | Filter tasks created after this date |
| `created_before` | datetime | null | Filter tasks created before this date |
| `due_after` | datetime | null | Filter tasks due after this date |
| `due_before` | datetime | null | Filter tasks due before this date |
| `archived` | boolean | null | Filter by archived status |
| `include_suggestions` | boolean | true | Include search suggestions in response |

## Search Features

### Relevance Ranking

Results are ranked by relevance using PostgreSQL's `ts_rank` function:
- Exact matches in titles rank higher
- Matches in descriptions rank lower
- Multiple word matches rank higher
- Results are ordered by relevance, then by creation date

### Query Normalization

The search automatically:
- Removes extra whitespace
- Handles special characters
- Normalizes the query for better matching
- Strips invalid characters that might interfere with search

### Search Suggestions

When `include_suggestions=true`, the API returns:
- Task titles that start with your query
- Task descriptions that start with your query
- Up to 5 relevant suggestions
- Suggestions help users discover content

## Examples

### Simple Search

```bash
# Find all tasks about "API"
GET /tasks/search?q=API

# Find tasks about "testing"
GET /tasks/search?q=testing
```

### Filtered Search

```bash
# Find high-priority tasks about "bug"
GET /tasks/search?q=bug&priority=high

# Find todo tasks about "review"
GET /tasks/search?q=review&status=todo

# Find development tasks created this year
GET /tasks/search?q=feature&category=development&created_after=2024-01-01
```

### Complex Queries

```bash
# Find urgent documentation tasks
GET /tasks/search?q=documentation&priority=urgent&status=in_progress

# Find tasks due this week
GET /tasks/search?q=deadline&due_after=2024-01-15&due_before=2024-01-21
```

## Performance

### Indexes

The search uses optimized PostgreSQL indexes:
- **GIN index** on full-text search vectors
- **Trigram index** for case-insensitive search
- **Composite indexes** for filtered searches

### Optimization Tips

1. **Use filters** to narrow down results
2. **Limit results** with the `limit` parameter
3. **Combine search with pagination** for large result sets
4. **Use specific queries** rather than very general ones

## Client Implementation

### Python Example

```python
import requests

def search_tasks(base_url, headers, query, filters=None, limit=20):
    """Search tasks with optional filters."""
    params = {"q": query, "limit": limit}
    
    if filters:
        params.update(filters)
    
    response = requests.get(f"{base_url}/tasks/search", params=params, headers=headers)
    return response.json()

# Usage
results = search_tasks(
    "http://localhost:8000",
    {"Authorization": "Bearer your-token"},
    "API documentation",
    {"status": "todo", "priority": "high"}
)
```

### JavaScript Example

```javascript
async function searchTasks(baseUrl, headers, query, filters = {}, limit = 20) {
    const params = new URLSearchParams({
        q: query,
        limit: limit.toString()
    });
    
    Object.entries(filters).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
            params.append(key, value);
        }
    });
    
    const response = await fetch(`${baseUrl}/tasks/search?${params}`, { headers });
    return await response.json();
}

// Usage
const results = await searchTasks(
    "http://localhost:8000",
    {"Authorization": "Bearer your-token"},
    "API documentation",
    {status: "todo", priority: "high"}
);
```

## Database Setup

### Migration

Run the migration to add search indexes:

```bash
# Apply the migration
python -m alembic upgrade head

# Or create the indexes manually
psql -d devtrackr -c "
CREATE INDEX idx_tasks_fulltext_search 
ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));

CREATE INDEX idx_tasks_title_description_gin 
ON tasks USING gin((title || ' ' || COALESCE(description, '')) gin_trgm_ops);
"
```

### Requirements

- PostgreSQL 9.6+ with full-text search support
- `pg_trgm` extension for trigram search (optional but recommended)

## Testing

Run the test script to verify search functionality:

```bash
python test_search.py
```

The test script will:
- Test basic search functionality
- Test filtered searches
- Test search suggestions
- Test complex queries
- Validate error handling

## Error Handling

The search endpoint handles various error cases:

- **Empty queries**: Returns 400 error
- **Invalid characters**: Automatically normalized
- **Database errors**: Returns 500 error with user-friendly message
- **Large result sets**: Automatically limited to prevent performance issues

## Best Practices

1. **Use specific queries** for better results
2. **Combine with filters** to narrow down results
3. **Implement client-side caching** for frequently searched terms
4. **Use pagination** for large result sets
5. **Monitor search performance** and optimize queries as needed

## Future Enhancements

Potential future improvements:
- **Fuzzy search** for typos and variations
- **Search analytics** to track popular queries
- **Saved searches** for frequently used queries
- **Search history** for user convenience
- **Advanced operators** (AND, OR, NOT) in queries
