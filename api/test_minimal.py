"""
Absolute minimal test for Vercel Python function.
This is the simplest possible function to test if Python works.
"""


def handler(request):
    """Minimal handler - just return success"""
    return {
        "statusCode": 200,
        "body": "OK"
    }
