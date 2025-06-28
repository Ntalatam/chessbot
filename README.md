# AI-Powered Personalized Chess Coach

A full-stack application that provides personalized chess coaching using AI. The application analyzes games, provides tactical puzzles, and offers personalized lessons based on the user's skill level and playing style.

## ✨ Features

- **🎮 Game Analysis**: Upload and analyze chess games with Stockfish
- **🧩 Tactical Puzzles**: Solve puzzles tailored to your skill level
- **🤖 AI Coaching**: Get personalized coaching with GPT-4 integration
- **📊 Progress Tracking**: Monitor your improvement with detailed statistics
- **🎓 Interactive Lessons**: Learn chess concepts with interactive content
- **🔒 User Authentication**: Secure JWT-based authentication
- **🌐 WebSocket Support**: Real-time game analysis and coaching

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: 
  - Stockfish for game analysis
  - OpenAI GPT-4 for natural language processing
- **Authentication**: JWT (JSON Web Tokens)
- **Caching**: Redis
- **WebSockets**: For real-time features

### Frontend
- **Framework**: React 18 with TypeScript
- **State Management**: React Context API
- **UI Components**: Custom components with Tailwind CSS
- **Chess Board**: chess.js + react-chessboard
- **Routing**: React Router v6

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (for production)
- **CI/CD**: GitHub Actions (configurable)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+ (for frontend development)
- OpenAI API key (for AI features)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chess-coach.git
cd chess-coach
```

### 2. Set up environment variables

Copy the example environment file and update the values:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=chess_coach

# Backend
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# External Services
OPENAI_API_KEY=your-openai-api-key

# Frontend (only needed for development)
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start the application with Docker

```bash
docker-compose up -d --build
```

This will start:
- PostgreSQL database
- Redis for caching
- Backend API (FastAPI)
- Frontend (React)
- Nginx (in production mode)

### 4. Initialize the database

```bash
docker-compose exec backend python -m app.db.init_db
```

### 5. Access the application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Adminer** (Database GUI): http://localhost:8080

## 🛠 Development

### Backend Development

1. Set up a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. Install dependencies:
   ```bash
   cd web
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd web
npm test
```

## 📂 Project Structure

```
chess-coach/
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── v1/             # API version 1
│   │   │   │   ├── endpoints/   # Route handlers
│   │   │   │   └── deps.py     # Dependencies
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Application settings
│   │   │   └── security.py    # Authentication utils
│   │   ├── db/                # Database configuration
│   │   │   ├── session.py     # Database session
│   │   │   └── init_db.py     # Database initialization
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic models
│   │   ├── services/          # Business logic
│   │   │   ├── ai.py          # AI/ML services
│   │   │   ├── auth.py        # Authentication
│   │   │   └── chess.py       # Chess-specific logic
│   │   └── main.py            # FastAPI app
│   ├── tests/                 # Backend tests
│   └── requirements.txt       # Python dependencies
│
├── web/                       # React frontend
│   ├── public/                # Static files
│   ├── src/
│   │   ├── assets/          # Images, fonts, etc.
│   │   ├── components/        # Reusable components
│   │   ├── contexts/          # React contexts
│   │   ├── hooks/             # Custom hooks
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── types/             # TypeScript types
│   │   ├── utils/             # Utility functions
│   │   ├── App.tsx            # Main App component
│   │   └── main.tsx           # Entry point
│   └── package.json
│
├── infrastructure/           # Infrastructure as Code
│   ├── nginx/                 # Nginx configs
│   └── docker/                # Dockerfiles
│
├── scripts/                  # Utility scripts
│   ├── init_db.py            # Database initialization
│   └── deploy.sh             # Deployment script
│
├── docker-compose.yml        # Docker Compose config
└── README.md                 # This file
```

## 🔒 Environment Variables

See `.env.example` for all available environment variables.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Stockfish](https://stockfishchess.org/) - Powerful open-source chess engine
- [python-chess](https://python-chess.readthedocs.io/) - Python chess library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Chessground](https://github.com/ornicar/chessground) - Mobile/Web chess UI
- [OpenAI](https://openai.com/) - For the GPT-4 API
