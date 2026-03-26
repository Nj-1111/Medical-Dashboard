# Setup and Installation Instructions

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional, for containerized development)
- Git
- A CUDA-capable GPU is **optional** — set `MODEL_DEVICE=cpu` in `.env` to run on CPU

## Getting the Code

All commands below assume you are starting from the repo root. If you haven't cloned yet:

```bash
git clone https://github.com/Nj-1111/Medical-Dashboard.git
cd Medical-Dashboard
```

## Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env:
#   - Set MODEL_DEVICE=cpu (unless you have a CUDA GPU)
#   - Azure fields (AZURE_*) are only needed for cloud storage; leave as-is for local dev
#   - Set a random SECRET_KEY for *local, non-Docker* development only
#     (when using Docker or deploying, provide SECRET_KEY via environment variables
#      and ensure backend/.env is not copied into images by keeping it in .dockerignore)

# Then run:
python -m app.main
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## Docker Setup (Recommended)

From the repo root (clone instructions are at the top of this file):

```bash
# Start all services (PostgreSQL, Redis, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Once all containers are running, open:

| Service | URL |
|---------|-----|
| Frontend (React app) | http://localhost:3000 |
| Backend health check | http://localhost:8000/api/v1/health |
| Swagger / API docs | http://localhost:8000/docs |

> **Note:** The backend takes ~30 seconds on first start while it loads the ML model. If the frontend shows a connection error, wait and refresh.

> **GPU support:** By default Docker Compose runs the model on CPU. To use a CUDA GPU, set `MODEL_DEVICE=cuda` in your shell before starting: `MODEL_DEVICE=cuda docker compose up -d`

> **Windows shortcut**: Run `start.bat` from the repo root instead of the commands above.

## API Testing

```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@hospital.com","password":"testpass123"}' | jq -r '.access_token')

# Check API health
curl http://localhost:8000/api/v1/health

# Check model status
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/inference/models/status
```

## Troubleshooting

### Models not loading?
```bash
# Clear model cache
rm -rf backend/model_cache/

# Restart backend
python -m app.main
```

### Database connection error?
```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Verify connection string in .env
```

### Port already in use?
```bash
# Change ports in docker-compose.yml or .env
```
