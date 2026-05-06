# Rock-Paper-Scissors Game

A full-stack web application for playing Rock-Paper-Scissors against an AI opponent. Built with FastAPI backend and modern HTML/CSS frontend, featuring user authentication, game history tracking, and statistics.

## Features

- 👤 **User Authentication**: Register and login with email
- 🎮 **Interactive Gameplay**: Play Rock-Paper-Scissors against AI
- 📊 **Game Statistics**: Track wins, losses, and ties
- 💾 **Game History**: Persistent game logs stored in database
- 🎨 **Responsive Design**: Clean, modern UI with CSS styling
- 🔒 **Secure Backend**: FastAPI with SQLAlchemy ORM and SQLite database

## Technology Stack

### Backend

- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **SQLite** - Lightweight database for data persistence

### Frontend

- **HTML5** - Structure and markup
- **CSS3** - Styling and layout
- **Jinja2** - Template engine for dynamic HTML rendering

## Project Structure

```
RPS game/
├── main.py                 # Main FastAPI application
├── auth.py                 # Authentication state management
├── database.py             # Database configuration and session management
├── model.py                # SQLAlchemy database models
├── schemas.py              # Pydantic models for request/response validation
├── requirements.txt        # Python dependencies
├── routers/
│   ├── __init__.py
│   └── play.py            # Game logic and API routes
├── templates/             # Jinja2 HTML templates
│   ├── layout.html        # Base template
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── play.html          # Play page
│   └── game.html          # Game board page
├── static/                # Static assets
│   └── css/
│       ├── layout.css     # Base styles
│       ├── auth.css       # Authentication page styles
│       ├── index.css      # Home page styles
│       ├── play.css       # Play page styles
│       └── game.css       # Game board styles
└── env/                   # Python virtual environment
```

## Database Schema

### Users Table

- `id` (Integer, Primary Key)
- `username` (String, Unique, Required)
- `email` (String, Unique, Required)

### History Table

- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key → users.id)
- `player_choice` (String) - "rock", "paper", or "scissors"
- `ai_choice` (String) - AI's choice
- `result` (String) - "win", "lose", or "tie"

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**

   ```bash
   cd "RPS game"
   ```

2. **Create and activate virtual environment**

   ```bash
   # On Windows
   python -m venv env
   env\Scripts\activate

   # On macOS/Linux
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

   Or using Uvicorn directly:

   ```bash
   uvicorn main:app --reload
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

## Usage

### Getting Started

1. **Visit the homepage** - Browse the landing page
2. **Register** - Create a new account with username and email
3. **Login** - Login with your registered email
4. **Play** - Navigate to the game board and play against AI
5. **View Stats** - Check your win/loss/tie statistics

### Game Rules

The classic Rock-Paper-Scissors rules apply:

- **Rock** beats Scissors
- **Scissors** beats Paper
- **Paper** beats Rock
- Same choice = Tie

## API Endpoints

### Authentication Routes

- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - Submit login form
- `GET /register` - Registration page
- `POST /register` - Submit registration form

### Game Routes

- `GET /play/` - Play page
- `GET /play/game` - Game board (requires login)
- `POST /play/api/game/` - Play a game round
  - Request: `{"choice": "rock|paper|scissors"}`
  - Response: `{"player_choice": str, "ai_choice": str, "result": "win|lose|tie"}`
- `GET /play/api/history` - Get game statistics
  - Response: `{"win": int, "lose": int, "tie": int}`

## Development Notes

- The application uses in-memory state for current login session (see `auth.py`)
- SQLite database automatically created on first run (`RPS.db`)
- All game choices are case-insensitive
- Form validation uses Pydantic for request bodies
- Custom exception handlers return JSON responses for API errors

## Future Improvements

- Implement JWT-based authentication for better security
- Add user profile and settings pages
- Create leaderboard based on win rates
- Add difficulty levels for AI opponent
- Implement WebSocket for real-time multiplayer
- Add unit tests and integration tests
- Deploy to cloud platform (Heroku, AWS, etc.)

## License

This project is open source and available for educational purposes.
