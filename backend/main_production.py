from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from datetime import timedelta, datetime
from pathlib import Path
import os

from .auth import (
    authenticate_parent,
    create_access_token,
    get_current_parent,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from .models import (
    Token,
    ParentDashboard,
    MOCK_CLIENTS,
    MOCK_LUNCH_MENU,
    PARENT_CLIENTS
)
from .chatbot import NorshelChatbot, ChatSession

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG_MODE = ENVIRONMENT == "development"

app = FastAPI(
    title="Norshel Parent Portal",
    debug=DEBUG_MODE,
    description="Secure parent portal for Norshel Inc. day programs"
)

# Initialize chatbot and session storage
chatbot = NorshelChatbot()
chat_sessions = {}

# HTTPS Redirect Middleware (only in development)
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only redirect in development or when explicitly configured
        if ENVIRONMENT == "development" and request.url.scheme == "http":
            # Get the host and construct HTTPS URL
            host = request.headers.get("host", "localhost")
            if ":" in host:
                host = host.split(":")[0]
            
            https_url = f"https://{host}:8443{request.url.path}"
            if request.url.query:
                https_url += f"?{request.url.query}"
            
            return RedirectResponse(url=https_url, status_code=301)
        
        return await call_next(request)

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Add HSTS only in production
        if ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "connect-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp_policy
        
        return response

# Add HTTPS redirect middleware only in development
if ENVIRONMENT == "development":
    app.add_middleware(HTTPSRedirectMiddleware)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)

# Trusted host middleware (for production)
if ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # Configure with your actual domain
    )

# CORS middleware (updated for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENVIRONMENT == "development" else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Static files and templates
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend"))

@app.get("/")
async def root(request: Request):
    """Serve the index page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    """Serve the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    """Serve the dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/programs")
async def programs_page(request: Request):
    """Serve the programs page"""
    return templates.TemplateResponse("programs.html", {"request": request})

@app.get("/individual-programs")
async def individual_programs_page(request: Request):
    """Serve the individual programs page"""
    return templates.TemplateResponse("individual-programs.html", {"request": request})

@app.get("/video")
async def video_page(request: Request):
    """Serve the sign language video page"""
    return templates.TemplateResponse("video.html", {"request": request})

@app.get("/contact")
async def contact_page(request: Request):
    """Serve the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Handle parent login"""
    parent = authenticate_parent(form_data.username, form_data.password)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": parent["email"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/dashboard", response_model=ParentDashboard)
async def get_dashboard(current_parent: dict = Depends(get_current_parent)):
    """Get parent dashboard data"""
    # Get client IDs for the parent
    client_ids = PARENT_CLIENTS.get(current_parent["email"], [])
    
    # Get client information
    parent_clients = [client for client in MOCK_CLIENTS if client.id in client_ids]
    
    if not parent_clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No clients found for this parent"
        )
    
    # Return dashboard data
    return ParentDashboard(
        clients=parent_clients,
        lunch_menu=MOCK_LUNCH_MENU
    )

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """Handle chatbot conversations"""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")
        page_context = data.get("page", "")
        
        if not message:
            return {"error": "Message is required"}, 400
        
        # Get or create chat session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = ChatSession(session_id)
        
        session = chat_sessions[session_id]
        session.add_message(message, is_user=True)
        
        # Determine user context
        user_context = {
            "page": page_context,
            "logged_in": False,
            "session_id": session_id
        }
        
        # Check if user is logged in (basic check)
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from .auth import get_current_parent
                # This is a simplified check - in real implementation you'd verify the token
                user_context["logged_in"] = True
            except:
                pass
        
        # Get chatbot response
        response = chatbot.get_response(message, user_context)
        session.add_message(response, is_user=False)
        
        return {
            "response": response,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "response": "I'm having trouble right now. Please call us at (204) 654-6117 for immediate assistance.",
            "error": str(e)
        }

@app.get("/api/chat/start")
async def start_chat():
    """Get a conversation starter"""
    import uuid
    session_id = str(uuid.uuid4())
    starter_message = chatbot.get_conversation_starter()
    
    # Create new session
    chat_sessions[session_id] = ChatSession(session_id)
    chat_sessions[session_id].add_message(starter_message, is_user=False)
    
    return {
        "message": starter_message,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": ENVIRONMENT
    }

# Production startup (no SSL configuration needed for cloud platforms)
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (set by hosting platform)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Norshel Parent Portal in {ENVIRONMENT} mode")
    print(f"🌐 Server will be available on port {port}")
    
    uvicorn.run(
        "backend.main_production:app", 
        host="0.0.0.0", 
        port=port,
        reload=DEBUG_MODE
    ) 