"""
Ultra-minimal Python function for Vercel testing.
This doesn't use FastAPI at all to test if Python itself works.
"""

def handler(request):
    """Simple handler function"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': {
            'message': 'Hello from Vercel!',
            'status': 'success',
            'python_working': True
        }
    }
