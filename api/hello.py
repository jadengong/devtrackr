"""
Ultra-minimal Python function for Vercel testing.
This doesn't use FastAPI at all to test if Python itself works.
"""


def handler(request):
    """Simple handler function with error handling"""
    try:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {
                "message": "Hello from Vercel!",
                "status": "success",
                "python_working": True,
                "request_method": getattr(request, "method", "unknown"),
                "request_url": getattr(request, "url", "unknown"),
            },
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {
                "error": "Function crashed",
                "message": str(e),
                "type": type(e).__name__,
            },
        }


# Alternative handler for different Vercel Python versions
def main(request):
    """Alternative entry point"""
    return handler(request)


# Export both handlers
__all__ = ["handler", "main"]
