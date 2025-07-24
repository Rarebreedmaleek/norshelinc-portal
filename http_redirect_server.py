#!/usr/bin/env python3
"""
HTTP to HTTPS Redirect Server for Norshel Web Application
Automatically redirects all HTTP traffic to HTTPS for security
"""

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import uvicorn
import sys
import os

app = FastAPI(
    title="HTTP to HTTPS Redirect Server",
    description="Redirects all HTTP requests to HTTPS"
)

@app.middleware("http")
async def redirect_to_https(request: Request, call_next):
    """Redirect all HTTP requests to HTTPS"""
    # Get the host from the request
    host = request.headers.get("host", "localhost")
    
    # Remove port if it exists and add HTTPS port
    if ":" in host:
        host = host.split(":")[0]
    
    # Construct HTTPS URL
    https_url = f"https://{host}:8443{request.url.path}"
    if request.url.query:
        https_url += f"?{request.url.query}"
    
    print(f"🔄 Redirecting: {request.url} → {https_url}")
    
    # Return permanent redirect to HTTPS (301)
    return RedirectResponse(url=https_url, status_code=301)

@app.get("/health")
async def health_check():
    """Health check endpoint (should redirect to HTTPS)"""
    return {"status": "redirect_server_running"}

def start_redirect_server():
    """Start the HTTP to HTTPS redirect server"""
    print("🔄 Starting HTTP to HTTPS Redirect Server...")
    print("📍 HTTP URL: http://localhost:8000")
    print("➡️  All requests will redirect to: https://localhost:8443")
    print("🛑 Press Ctrl+C to stop the redirect server\n")
    
    try:
        uvicorn.run(
            "http_redirect_server:app",
            host="127.0.0.1",
            port=8000,
            reload=False,  # No reload needed for redirect server
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 HTTP redirect server stopped by user")
    except Exception as e:
        print(f"❌ Error starting redirect server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 Norshel HTTP to HTTPS Redirect Server")
    print("=" * 45)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Error: Please run this script from the project root directory")
        print("   (The directory containing the 'backend' folder)")
        sys.exit(1)
    
    # Start the redirect server
    if not start_redirect_server():
        sys.exit(1) 