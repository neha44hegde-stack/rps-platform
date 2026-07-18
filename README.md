
# RPS Platform — AI-Powered Multiplayer Rock Paper Scissors

A full-stack Flask web application that goes far beyond a basic Rock Paper Scissors game. It features an AI opponent that learns and predicts your play patterns, real-time multiplayer via WebSockets, webcam-based hand gesture recognition, a documented REST API, and a full CI/CD pipeline.

## Features

- **Authentication** — Secure register/login/logout with hashed passwords (Flask-Login + Werkzeug)
- **AI Opponent** — Analyzes your move history using sequence pattern detection and frequency analysis to predict and counter your next move
- **Game History & Leaderboard** — Every game is logged; leaderboard ranks players by wins, win %, and best streak
- **Analytics Dashboard** — Win/loss breakdown, move distribution, and win-rate trend charts (Chart.js)
- **REST API with Swagger Docs** — Full JSON API for gameplay, history, and leaderboard, documented at `/api/docs` (Flask-RESTX)
- **Real-Time Multiplayer** — Player-vs-player matchmaking and live gameplay using WebSockets (Flask-SocketIO)
- **Webcam Gesture Recognition** — Play using real hand gestures detected via your webcam (MediaPipe Hand Landmarker), no controller or clicks needed
- **Automated Testing** — pytest suite covering authentication, game logic, and AI behavior
- **CI/CD Pipeline** — GitHub Actions automatically runs the full test suite and verifies the Docker build on every push
- **Containerized** — Dockerfile + docker-compose for consistent deployment

## Tech Stack

**Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-RESTX, Flask-SocketIO
**Database:** SQLite (dev), swappable to PostgreSQL via `DATABASE_URL` env var
**AI:** Custom sequence-pattern and frequency-based prediction (pure Python, no external ML dependency)
**Computer Vision:** MediaPipe Hand Landmarker (runs client-side in-browser)
**Frontend:** Jinja2 templates, Bootstrap 5, Chart.js, vanilla JavaScript
**Real-time:** Socket.IO
**Testing:** pytest, pytest-flask
**DevOps:** Docker, docker-compose, GitHub Actions, Gunicorn + eventlet (production server)

## Project Structure

\`\`\`
rps-platform/
├── app/
│   ├── auth/          # Authentication blueprint (register, login, logout, profile)
│   ├── game/          # Core game logic, AI, dashboard, webcam routes
│   ├── api/           # REST API (Flask-RESTX) with Swagger docs
│   ├── multiplayer/   # Real-time multiplayer (SocketIO events + routes)
│   ├── models/        # SQLAlchemy models (User, Game, Score)
│   └── templates/      # Jinja2 templates
├── tests/             # pytest test suite
├── migrations/        # Flask-Migrate database migrations
├── .github/workflows/ # GitHub Actions CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── config.py           # Environment-based configuration (dev/prod/testing)
└── run.py              # Application entry point
\`\`\`

## Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

1. Clone the repository
   \`\`\`bash
   git clone https://github.com/neha44hegde-stack/rps-platform.git
   cd rps-platform
   \`\`\`

2. Create and activate a virtual environment
   \`\`\`bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   \`\`\`

3. Install dependencies
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Set up the database
   \`\`\`bash
   set FLASK_APP=run.py        # Windows
   export FLASK_APP=run.py     # Mac/Linux
   flask db upgrade
   \`\`\`

5. Run the app
   \`\`\`bash
   python run.py
   \`\`\`

6. Open \`http://127.0.0.1:5000` in your browser

### Running with Docker

\`\`\`bash
docker-compose up --build
\`\`\`

### Running Tests

\`\`\`bash
pytest
\`\`\`

## API Documentation

Once running, interactive Swagger docs are available at:
\`\`\`
http://127.0.0.1:5000/api/docs
\`\`\`

Key endpoints:
- \`POST /api/game/play\` — Submit a move, get AI's response and result
- \`GET /api/game/history\` — Retrieve your game history
- \`GET /api/leaderboard\` — Retrieve the global leaderboard

## How the AI Opponent Works

The AI doesn't choose randomly — it analyzes your recent move history using two strategies:

1. **Sequence Detection (primary):** Looks at your last 2 moves and searches your history for prior instances of that same sequence, then predicts whatever you played most often immediately after.
2. **Frequency Analysis (fallback):** If no matching sequence is found, falls back to your single most-played move overall.

The AI then throws whichever choice beats its prediction. This means predictable or repetitive play styles get punished — the AI genuinely gets harder to beat the more patterned your choices are.

## How Webcam Gesture Recognition Works

Hand tracking runs entirely client-side using Google's MediaPipe Hand Landmarker (WebAssembly, no server round-trip for video). The app:
1. Detects 21 hand landmark points per frame
2. Measures which fingers are extended vs. curled based on landmark distances
3. Classifies the shape as rock, paper, or scissors
4. Requires the gesture to be held steady for ~1 second before locking it in and submitting to the game engine

## CI/CD Pipeline

Every push triggers a GitHub Actions workflow that:
1. Installs dependencies and runs the full pytest suite
2. Builds the Docker image to verify it's deployable

Both must pass before a change is considered stable.

## License

This project is for portfolio/educational purposes.
