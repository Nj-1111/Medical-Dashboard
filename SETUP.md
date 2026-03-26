# Setup and Installation Instructions

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional, for containerized development)
- Git

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

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
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

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

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
