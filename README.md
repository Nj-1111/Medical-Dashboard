# Medical Diagnosis Pipeline - Production-Grade Architecture

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-blue)

**A scalable, secure, and professional medical diagnosis system with glaucoma detection using AI/ML**

[Features](#features) • [Architecture](#architecture) • [Quick Start](#quick-start) • [Configuration](#configuration) • [Deployment](#deployment) • [API Documentation](#api-documentation)

</div>

---

## 📋 Overview

Medical Diagnosis Pipeline is a **production-grade** full-stack application designed for healthcare facilities to detect glaucoma and generate professional medical reports. Built with enterprise-grade security, scalability, and configurability.

### Key Highlights
- ✅ **Production-Ready**: Full security, monitoring, and audit logging
- ✅ **AI/ML Powered**: Glaucoma detection + LLM-generated reports
- ✅ **Configurable Models**: Switch between HuggingFace models without code changes
- ✅ **Containerized**: Docker & Kubernetes ready
- ✅ **Secure**: OAuth/OIDC auth, encrypted storage, audit trails
- ✅ **Scalable**: Auto-scaling, load balancing, microservices ready
- ✅ **Professional**: Clean code, comprehensive logging, error handling

---

## 🏗 Architecture

### System Diagram
```
┌─────────────────┐
│  Doctor Web App │ (React Frontend)
└────────┬────────┘
         │
         │ HTTPS/TLS
         ▼
┌─────────────────────┐
│  API Ingress        │
│  + Auth (OAuth)     │
│  + Rate Limiting    │
│  + WAF              │
└────────┬────────────┘
         │
    ┌────┴────┬───────────┬─────────────┐
    ▼         ▼           ▼             ▼
[Auth] [Patients] [Upload] [Inference]
    │         │           │             │
    └────┬────┴───────────┴─────────────┘
         ▼
┌──────────────────────────┐
│   Data Layer             │
├──────────────────────────┤
│ • PostgreSQL (Patient)   │
│ • Redis (Cache/Vectors)  │
│ • Azure Blob (Images)    │
│ • Azure Key Vault        │
└──────────────────────────┘
```

### Service Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React 18 | Doctor interface for diagnosis uploads |
| **Backend API** | FastAPI | REST API for all operations |
| **ML Inference** | PyTorch + Transformers | Glaucoma detection model |
| **LLM** | HuggingFace | Report generation |
| **Database** | PostgreSQL | Patient & diagnosis records |
| **Cache** | Redis | Vector store & caching |
| **Storage** | Azure Blob | Medical images & PDFs |
| **Auth** | OAuth 2.0/OIDC | Azure AD integration |
| **Orchestration** | Kubernetes/AKS | Production deployment |

---

## � Documentation

| Document | Purpose |
|----------|---------|
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Comprehensive setup and deployment instructions |
| [QUICK_START.md](QUICK_START.md) | Fast startup instructions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and architecture |
| [SETUP.md](SETUP.md) | Detailed installation guide |

---

## �🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL (or use docker-compose)

### Local Development (5 minutes)

#### 1. Clone & Setup
```bash
git clone https://github.com/Nj-1111/Medical-Dashboard.git
cd medical-diagnosis-pipeline

# Copy environment template
cp backend/.env.example backend/.env
```

#### 2. Start with Docker Compose
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- FastAPI backend (http://localhost:8000)
- React frontend (http://localhost:3000)

#### 3. Access Application
```
Frontend:  http://localhost:3000
API Docs:  http://localhost:8000/docs
Health:    http://localhost:8000/api/v1/health
```

### Manual Setup (Advanced)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m app.main
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

---

## ⚙️ Configuration

### Changing ML Models

The beauty of this pipeline is **changing models is trivial**—just update configuration!

#### Option 1: Environment Variables
```bash
# Change glaucoma detection model
export GLAUCOMA_MODEL_NAME=microsoft/resnet-50

# Change LLM for report generation
export LLM_MODEL_NAME=meta-llama/Llama-2-7b-chat-hf

# Device: cuda for GPU, cpu for CPU
export MODEL_DEVICE=cuda
```

#### Option 2: Config File
Edit `backend/.env`:
```env
GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
MODEL_DEVICE=cuda
```

#### Option 3: API Endpoint (Runtime)
```bash
# Switch glaucoma model
curl -X POST http://localhost:8000/api/v1/inference/models/switch-glaucoma \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model_name": "facebook/dino-vitb16"}'

# Switch LLM model
curl -X POST http://localhost:8000/api/v1/inference/models/switch-llm \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"model_name": "meta-llama/Llama-2-13b-chat"}'
```

### Recommended Models

#### For Glaucoma Detection
- `google/vit-base-patch16-224` ⭐ Recommended (fast, accurate)
- `facebook/dino-vitb16` (better feature extraction)
- `microsoft/resnet-50` (lightweight)

#### For Report Generation
- `mistralai/Mistral-7B-Instruct-v0.1` ⭐ Recommended
- `meta-llama/Llama-2-7b-chat` (uncensored alternative)
- `tiiuae/falcon-7b-instruct` (efficient)

---

## 📦 Project Structure

```
medical-diagnosis-pipeline/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration management
│   │   ├── dependencies.py      # DI/auth
│   │   ├── api/
│   │   │   └── routes.py        # All endpoints
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── services/
│   │   │   └── file_service.py  # File upload logic
│   │   ├── security/
│   │   │   └── auth.py          # Auth & JWT
│   │   └── utils/
│   │       └── logging_config.py
│   │
│   ├── ml/
│   │   ├── inference.py         # Model inference engine (configurable!)
│   │   └── __init__.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx    # Model switching UI
│   │   │   └── UploadDiagnosis.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── index.css
│   │
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── kubernetes/
│   └── deployment.yaml          # Complete K8s manifest
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml       # Backend CI/CD
│       ├── frontend-ci.yml      # Frontend CI/CD
│       └── deploy-aks.yml       # AKS deployment
│
├── docker-compose.yml           # Local dev setup
├── README.md                    # This file
└── ARCHITECTURE.md              # Detailed architecture
```

---

## 🔌 API Endpoints

### Authentication
```bash
POST   /api/v1/auth/login          # Login & get token
POST   /api/v1/auth/logout         # Logout
GET    /api/v1/auth/me             # Current user
```

### Patients
```bash
GET    /api/v1/patients            # List patients
POST   /api/v1/patients            # Create patient
GET    /api/v1/patients/{id}       # Get patient
PUT    /api/v1/patients/{id}       # Update patient
```

### Diagnosis
```bash
POST   /api/v1/upload/image        # Upload medical image
POST   /api/v1/inference/glaucoma  # Run glaucoma detection
GET    /api/v1/inference/models/status  # Model status
```

### Model Management
```bash
POST   /api/v1/inference/models/switch-glaucoma  # Change glaucoma model
POST   /api/v1/inference/models/switch-llm       # Change LLM model
```

### Health
```bash
GET    /api/v1/health             # Health check
```

---

## 🔐 Security Features

✅ **Authentication**
- OAuth 2.0 / OIDC (Azure AD)
- JWT tokens with expiration
- Role-based access control (RBAC)

✅ **Data Protection**
- TLS/SSL for transit encryption
- AES-256 at-rest encryption
- Encrypted database columns

✅ **Audit & Compliance**
- Immutable audit logs
- User action tracking
- HIPAA-ready structure

✅ **API Security**
- Rate limiting
- WAF integration (Azure Front Door)
- CORS configuration

✅ **File Security**
- Virus scanning (ClamAV)
- File type validation
- Size restrictions

---

## 📊 Monitoring & Observability

### Logging
- Structured JSON logs
- Separate audit log (`logs/audit.log`)
- Configurable log levels

### Metrics
- Request/response times
- Model inference latency
- Database query performance

### Alerts
- Service health checks
- Error rate thresholds
- Low disk space warnings

---

## 🐳 Docker

### Build Images
```bash
# Backend
docker build -t medical-backend:v1 -f backend/Dockerfile .

# Frontend
docker build -t medical-frontend:v1 -f frontend/Dockerfile .
```

### Run Containers
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

---

## ☸️ Kubernetes Deployment

### Prerequisites
- AKS cluster running
- kubectl configured
- Images pushed to ACR

### Deploy
```bash
# Apply manifests
kubectl apply -f kubernetes/deployment.yaml

# Check status
kubectl get pods -n medical-diagnosis

# View logs
kubectl logs -n medical-diagnosis -l app=backend

# Port forward for local access
kubectl port-forward -n medical-diagnosis svc/backend 8000:8000
```

### Scaling
```bash
# Manual scale
kubectl scale deployment backend -n medical-diagnosis --replicas=5

# Auto-scaling (already configured in manifest)
kubectl get hpa -n medical-diagnosis
```

---

## 🚢 CI/CD Pipeline

GitHub Actions workflows automate:

1. **backend-ci.yml**: Unit tests, linting, security scan
2. **frontend-ci.yml**: Build, test, bundling
3. **deploy-aks.yml**: Build images, push to ACR, deploy to AKS

### Setup (One-time)
```bash
# Add GitHub Secrets:
AZURE_CREDENTIALS          # Azure login credentials
AZURE_RESOURCE_GROUP       # Resource group name
AKS_CLUSTER_NAME          # AKS cluster name
ACR_LOGIN_SERVER          # Container registry URL
ACR_USERNAME              # Registry username
ACR_PASSWORD              # Registry password
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Smoke Tests (Post-deployment)
```bash
kubectl run smoke-test \
  --image=medical-backend:latest \
  --restart=Never \
  -n medical-diagnosis \
  -- pytest tests/smoke_tests.py
```

---

## 📚 API Documentation

### Automatic Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example Requests

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@hospital.com","password":"securepass"}'
```

#### Upload & Diagnose
```bash
# Get token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@hospital.com","password":"securepass"}' | jq -r '.access_token')

# Upload image
curl -X POST http://localhost:8000/api/v1/upload/image \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@patient_image.jpg" \
  -F "patient_id=PAT-001"

# Run diagnosis
curl -X POST http://localhost:8000/api/v1/inference/glaucoma \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id":"PAT-001",
    "image_id":"IMG-123"
  }'
```

---

## 🔧 Troubleshooting

### Models not loading
```bash
# Check model cache directory
ls -la model_cache/

# Clear cache and reload
rm -rf model_cache/
# Restart with LOAD_MODELS_ON_STARTUP=true
```

### Database connection issues
```bash
# Test connection
psql postgres://user:pass@localhost:5432/medical_diagnosis

# Check Docker container
docker-compose logs postgres
```

### API errors
```bash
# View detailed logs
docker-compose logs -f backend

# Check health endpoint
curl http://localhost:8000/api/v1/health
```

---

## 📈 Performance Optimization

### GPU/CUDA
```bash
# Enable GPU acceleration
export MODEL_DEVICE=cuda
export CUDA_VISIBLE_DEVICES=0

# Monitor GPU usage
nvidia-smi
```

### Model Quantization
For better performance on CPU:
```python
# Use smaller models
GLAUCOMA_MODEL_NAME=microsoft/resnet-50
LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1  # Already optimized
```

### Caching
- Redis caches inference results
- Browser caches frontend assets
- Database query caching

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit: `git commit -m "Add feature"`
3. Push: `git push origin feature/your-feature`
4. Open Pull Request

---

## 📄 License

MIT License - See LICENSE file

---

## 📞 Support

- **Documentation**: See ARCHITECTURE.md for detailed system design
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Email**: support@medical-diagnosis.com

---

## 🎯 Roadmap

- [ ] EU GDPR compliance
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Integration with EMR systems

---

## ✨ Quick Wins for Getting Started

1. **Run locally**: `docker-compose up` ✅
2. **Access frontend**: http://localhost:3000 ✅
3. **View API docs**: http://localhost:8000/docs ✅
4. **Try model switching**: Visit Dashboard → Switch Models ✅
5. **Check logs**: `docker-compose logs -f backend` ✅

---

<div align="center">

**Made with ❤️ for Medical Professionals**

[⬆ Back to top](#medical-diagnosis-pipeline---production-grade-architecture)

</div>
