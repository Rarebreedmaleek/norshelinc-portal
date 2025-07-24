# Norshel Care Web Application

A secure web application for Norshel, an organization that helps adults with physical and developmental disabilities. The application includes a secure login system, dashboard with program schedules, and sign language learning resources.

## Features

- Secure parent login system with JWT authentication
- Interactive dashboard showing weekly schedules and team assignments
- Sign language learning page with video resources
- Responsive design using Tailwind CSS

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd norshel-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key-here
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Default Login Credentials

For testing purposes, use these credentials:
- Email: parent@example.com
- Password: parentpassword

**Note:** In production, make sure to:
- Change the SECRET_KEY in the .env file
- Use a secure database for user management
- Add proper SSL/TLS encryption
- Implement proper user registration system

## Project Structure

```
norshel_app/
│
├── backend/
│ ├── main.py         # FastAPI application
│ ├── models.py       # Data models
│ ├── auth.py         # Authentication logic
│ └── database.py     # Database configuration (to be implemented)
│
├── frontend/
│ ├── base.html       # Base template
│ ├── index.html      # Landing page
│ ├── login.html      # Login form
│ ├── dashboard.html  # Secure dashboard
│ └── video.html      # Sign language video page
│
├── static/
│ └── sign_language.mp4  # Sign language video file
│
├── .env              # Environment variables
└── requirements.txt  # Python dependencies
```

## API Endpoints

- `POST /login` - Authenticate user and get JWT token
- `GET /dashboard` - Get schedule and team data (requires authentication)
- `GET /clients` - Get client list and team assignments (requires authentication)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 