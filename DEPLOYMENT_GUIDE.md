# Medical Dashboard - Comprehensive Setup and Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Setup Instructions](#detailed-setup-instructions)
4. [Running with Docker](#running-with-docker)
5. [Running Locally](#running-locally)
6. [Configuration Guide](#configuration-guide)
7. [Database Management](#database-management)
8. [Troubleshooting](#troubleshooting)
9. [Automated Code Quality](#automated-code-quality)

---

## System Requirements

### Hardware Requirements
- Processor: 4+ cores (8+ recommended for ML model inference)
- RAM: 8GB minimum (16GB+ recommended)
- Storage: 50GB free (for Docker images and model caches)
- GPU: NVIDIA GPU with CUDA support (optional, for faster inference)

### Software Requirements

#### For Docker-based Deployment
- Docker Desktop 4.20+
- Docker Compose 2.15+
- Windows 10/11, macOS, or Linux

#### For Local Development
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or Docker for database)
- Git 2.40+

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
cd c:\Users\Neel Bose\Medical-Dashboard
start.bat
```

The application will be available at:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

To stop:
```bash
stop.bat
```

### Option 2: Local Development

```bash
cd c:\Users\Neel Bose\Medical-Dashboard
start-local.bat
```

---

## Detailed Setup Instructions

### Prerequisites Verification

Before proceeding, verify all requirements:

```bash
# Check Docker
docker --version
docker-compose --version

# Check Python
python --version  # Should be 3.11+

# Check Node.js
node --version    # Should be 18+
npm --version

# Check PostgreSQL (optional for local dev)
psql --version    # Should be 15+
```

### Step 1: Clone and Navigate

```bash
cd Desktop\Medical-Dashboard
dir
```

Expected structure:
```
Medical-Dashboard/
  backend/
  frontend/
  kubernetes/
  .github/
  docker-compose.yml
  start.bat
  stop.bat
```

### Step 2: Environment Configuration

The application requires environment variables. These are managed via `.env` file:

```bash
# Backend environment file is at: backend/.env
# Template available at: backend/.env.example
# Copy template to create your configuration:
```

Edit `backend/.env`:
```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_diagnosis

# Vector Store Configuration
VECTOR_DB_HOST=localhost
VECTOR_DB_PORT=6379

# Application Configuration
APP_NAME=Medical Diagnosis Pipeline
APP_VERSION=1.0.0
DEBUG=False
SERVER_PORT=8000

# ML Model Configuration
GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
LOAD_MODELS_ON_STARTUP=True
MODEL_DEVICE=cpu  # Use 'cuda' if GPU is available

# Security Configuration
SECRET_KEY=your_super_secret_key_change_this_in_production
```

---

## Running with Docker

### Standard Docker Compose Startup

```bash
cd Medical-Dashboard

# Start services in background
docker-compose up -d

# Wait for services to initialize (2-3 minutes)
# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Service Endpoints (Docker)

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User Dashboard |
| Backend API | http://localhost:8000 | REST API Server |
| API Documentation | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/api/v1/health | Service Health |
| Database | localhost:5432 | PostgreSQL |
| Cache | localhost:6379 | Redis |

### Database Initialization (Docker)

After first-time startup:

```bash
# Initialize database tables and seed data
docker-compose exec backend python init_db.py

# Verify database
docker-compose exec postgres psql -U postgres -d medical_diagnosis -c "\dt"
```

### Stopping Services

```bash
# Stop containers (preserves data)
docker-compose down

# Stop containers and remove volumes (clears data)
docker-compose down -v
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Real-time log streaming
docker-compose logs -f backend

# Last 100 lines in real-time
docker-compose logs -f --tail=100 backend
```

---

## Running Locally

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
copy .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend Setup (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: http://localhost:3000

### Requirements for Local Development

#### Backend (Python)
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PyTorch 2.1.1
- Transformers 4.35.2
- psycopg2-binary (PostgreSQL driver)

#### Frontend (Node.js)
- React 18
- React Router 6
- TailwindCSS 3
- Axios (HTTP client)

---

## Configuration Guide

### Database Configuration

Update `backend/.env`:

```env
# PostgreSQL Connection
DB_HOST=localhost           # Database host address
DB_PORT=5432               # Standard PostgreSQL port
DB_USER=postgres           # Database username
DB_PASSWORD=password       # Database password
DB_NAME=medical_diagnosis  # Database name
```

### ML Model Configuration

Change AI models without code modification:

```env
# Glaucoma Detection Model
GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
# Alternative options:
# - microsoft/swin-base-patch4-window7-224
# - timm/vit_base_patch16_224

# Report Generation LLM
LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
# Alternative options:
# - meta-llama/Llama-2-7b
# - tiiuae/falcon-7b
```

### GPU/Hardware Configuration

```env
# Use CPU (default)
MODEL_DEVICE=cpu

# Use GPU (NVIDIA CUDA)
MODEL_DEVICE=cuda

# Model cache directory (for downloaded models)
MODEL_CACHE_DIR=./model_cache

# Load models on startup (recommended)
LOAD_MODELS_ON_STARTUP=True
```

### Security Configuration

```env
# Generate a secure secret key
SECRET_KEY=your_super_secret_key_change_this_in_production

# OAuth 2.0 Configuration (optional)
OIDC_DISCOVERY_URL=https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret
OAUTH_REDIRECT_URI=http://localhost:3000/callback
```

---

## Database Management

### PostgreSQL Access

```bash
# Connect to PostgreSQL via Docker
docker-compose exec postgres psql -U postgres -d medical_diagnosis

# Common commands inside psql
\dt                          # List tables
\d users                     # Describe table structure
SELECT * FROM users;         # Query data
\q                           # Exit psql
```

### Database Backup

```bash
# Backup database to file
docker-compose exec postgres pg_dump -U postgres medical_diagnosis > backup.sql

# Restore database from backup
docker-compose exec -T postgres psql -U postgres medical_diagnosis < backup.sql
```

### Database Reset

```bash
# Remove volumes to reset all data
docker-compose down -v

# Rebuild and reinitialize
docker-compose up -d
docker-compose exec backend python init_db.py
```

---

## Troubleshooting

### Docker Issues

#### Error: "Docker is not running"
```bash
# Solution: Start Docker Desktop
# Windows: Click the Docker Desktop icon
# macOS: Open Applications > Docker.app
# Linux: sudo systemctl start docker
```

#### Error: "Port already in use"
```bash
# Find process using port
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

#### Error: "Connection refused" to PostgreSQL
```bash
# Check if PostgreSQL container is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Ensure it's healthy
docker-compose exec postgres pg_isready -U postgres
```

### Database Issues

#### Error: "Database 'medical_diagnosis' does not exist"
```bash
# Initialize database
docker-compose exec backend python init_db.py
```

#### Error: "Connection timeout"
```bash
# Check database credentials in .env
# Verify DATABASE_HOST matches service name in docker-compose.yml
# Wait for database container to fully initialize (30-60 seconds)
```

### Frontend Issues

#### Error: "Cannot GET /dashboard"
```bash
# Ensure backend is running
# Check API_URL in frontend/.env
# Verify REACT_APP_API_URL points to backend address
```

#### Error: "npm: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Verify installation
node --version
npm --version
```

### Python/Backend Issues

#### Error: "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Error: "CUDA out of memory"
```bash
# Set GPU to CPU mode
# Edit .env: MODEL_DEVICE=cpu
# Or reduce batch size in code
```

---

## Automated Code Quality

### GitHub Actions Workflow

The project includes automated code quality checks that run:
- On every push to main/develop
- On daily schedule (2 AM UTC)
- Manually via workflow_dispatch

### What Gets Fixed Automatically

1. **Code Formatting**: Black formatter ensures consistent style
2. **Import Organization**: isort sorts and organizes imports
3. **PEP 8 Compliance**: autopep8 fixes style issues
4. **Code Verification**: flake8 identifies potential issues

### Workflow Output

Automated fixes are committed to a new branch and create a pull request for review:
- Branch name: `automated/fixes-<timestamp>`
- PR title: "Automated Code Quality: Formatting and Linting Fixes"
- Labels: `automated`, `code-quality`, `review-required`

### Manual Trigger

To trigger code quality pipeline manually:

```bash
# Via GitHub CLI
gh workflow run code-quality.yml

# Via GitHub Web:
1. Navigate to Actions tab
2. Select "Automated Code Quality Pipeline"
3. Click "Run workflow"
```

---

## Default Credentials

For initial login:

| Field | Value |
|-------|-------|
| Email | test@hospital.com |
| Password | testpass123 |

Change these credentials immediately in production.

---

## Performance Optimization

### For ML Inference
1. Use GPU acceleration: `MODEL_DEVICE=cuda`
2. Pre-load models on startup: `LOAD_MODELS_ON_STARTUP=True`
3. Adjust batch size based on GPU memory

### For Database
1. Use connection pooling (configured by default)
2. Index frequently queried fields
3. Regular maintenance and vacuuming

### For Backend
1. Enable caching for model predictions
2. Use async functions for I/O operations
3. Monitor API response times

---

## Support and Documentation

- Architecture Details: See [ARCHITECTURE.md](ARCHITECTURE.md)
- Quick Reference: See [QUICK_START.md](QUICK_START.md)
- Initial Setup: See [SETUP.md](SETUP.md)
- API Documentation: Available at http://localhost:8000/docs

---

## Next Steps

1. Verify system requirements
2. Choose deployment method (Docker or Local)
3. Follow appropriate setup instructions
4. Initialize database
5. Access application at provided URLs
6. Log in with default credentials
7. Update security settings for production

---

**Last Updated**: March 26, 2026
**Version**: 1.0.0
