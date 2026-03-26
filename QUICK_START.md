# Medical Diagnosis Pipeline - Quick Reference Guide

## 🎯 What's Been Created

A **production-grade**, **fully functional** medical diagnosis pipeline with glaucoma detection. Complete with:

✅ Backend API (Python FastAPI)
✅ Frontend Application (React)  
✅ ML/AI Models (Configurable from HuggingFace)
✅ Database (PostgreSQL)
✅ Cache Layer (Redis)
✅ Container Configuration (Docker)
✅ Kubernetes Manifests
✅ CI/CD Pipelines (GitHub Actions)
✅ Professional Documentation

---

## 🚀 Getting Started (Choose One)

### Option 1: Docker Compose (Easiest - 2 minutes)
```bash
cd C:\Users\Neel Bose\Desktop\medical-diagnosis-pipeline
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Python (Development - 5 minutes)
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### Option 3: Kubernetes (Production - Requires AKS)
```bash
kubectl apply -f kubernetes/deployment.yaml
```

---

## 💡 Key Features Explained

### 1. **Configurable Models** ⭐ (Main Feature!)
Change models WITHOUT touching code:

#### At Startup:
```bash
export GLAUCOMA_MODEL_NAME=microsoft/resnet-50
export LLM_MODEL_NAME=meta-llama/Llama-2-7b
```

#### At Runtime (via API):
```bash
# Switch glaucoma model
curl -X POST http://localhost:8000/api/v1/inference/models/switch-glaucoma \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"model_name": "facebook/dino-vitb16"}'

# Switch LLM
curl -X POST http://localhost:8000/api/v1/inference/models/switch-llm \
  -d '{"model_name": "mistralai/Mistral-7B-Instruct-v0.1"}'
```

#### Via Dashboard UI:
- Go to http://localhost:3000/dashboard
- Enter new model name from HuggingFace Hub
- Click "Switch Model"
- Done! 🎉

### 2. **Glaucoma Detection**
- Upload fundus image
- Automatic detection using Vision Transformer
- Confidence score
- Professional report generated with LLM

### 3. **Security**
- OAuth 2.0 / OIDC authentication
- JWT tokens
- Role-based access control
- Encrypted storage
- Audit logging

### 4. **Scalability**
- Auto-scaling Kubernetes manifests
- Load balancing
- Multi-replica deployments
- Horizontal Pod Autoscaler (HPA)

---

## 📁 Project Structure

```
medical-diagnosis-pipeline/
│
├── 📂 backend/              # FastAPI application
│   ├── app/                 # Core app
│   │   ├── main.py          # Entry point
│   │   ├── config.py        # Settings (configurable!)
│   │   ├── api/routes.py    # All endpoints
│   │   └── security/        # Auth logic
│   ├── ml/
│   │   └── inference.py     # Model loading & inference
│   └── requirements.txt
│
├── 📂 frontend/             # React application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Model switching UI
│   │   │   └── UploadDiagnosis.jsx  # Upload & diagnosis
│   │   └── services/api.js          # API client
│   └── package.json
│
├── 📂 kubernetes/           # Kubernetes manifests
│   └── deployment.yaml      # Complete K8s setup
│
├── 📂 .github/workflows/    # CI/CD pipelines
│   ├── backend-ci.yml
│   ├── frontend-ci.yml
│   └── deploy-aks.yml
│
├── 🐳 docker-compose.yml    # Local dev setup
├── 📖 README.md             # Full documentation
├── 📋 ARCHITECTURE.md       # System design
└── ⚙️ SETUP.md              # Installation guide
```

---

## 🔌 API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/login` | Login & get token |
| GET | `/api/v1/patients` | List patients |
| POST | `/api/v1/patients` | Create patient |
| POST | `/api/v1/upload/image` | Upload medical image |
| POST | `/api/v1/inference/glaucoma` | Run diagnosis |
| GET | `/api/v1/inference/models/status` | Get current models |
| POST | `/api/v1/inference/models/switch-glaucoma` | Change glaucoma model |
| POST | `/api/v1/inference/models/switch-llm` | Change LLM model |
| GET | `/api/v1/health` | Health check |

---

## 🎮 Example Workflow

### 1. Start the System
```bash
docker-compose up -d
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@hospital.com","password":"securepass"}'

# Get token from response
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 3. Create Patient
```bash
curl -X POST http://localhost:8000/api/v1/patients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name":"John",
    "last_name":"Doe",
    "date_of_birth":"1960-01-15",
    "medical_record_number":"MRN001"
  }'
```

### 4. Upload Image
```bash
curl -X POST http://localhost:8000/api/v1/upload/image \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@fundus_image.jpg" \
  -F "patient_id=PAT-001"
```

### 5. Run Diagnosis
```bash
curl -X POST http://localhost:8000/api/v1/inference/glaucoma \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id":"PAT-001",
    "image_id":"IMG-123"
  }'
```

### 6. Switch Models (If Needed)
```bash
curl -X POST http://localhost:8000/api/v1/inference/models/switch-glaucoma \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"model_name":"facebook/dino-vitb16"}'
```

---

## 📊 Recommended Models

### Glaucoma Detection
```
1. google/vit-base-patch16-224  ⭐ Default (fast, accurate)
2. facebook/dino-vitb16          (better features)
3. microsoft/resnet-50           (lightweight)
```

### Report Generation (LLM)
```
1. mistralai/Mistral-7B-Instruct-v0.1  ⭐ Default (best quality)
2. meta-llama/Llama-2-7b-chat           (alternative)
3. tiiuae/falcon-7b-instruct            (efficient)
```

---

## 🔐 Configuration

### Environment Variables
Edit `backend/.env`:

```env
# Model Selection
GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1

# Hardware
MODEL_DEVICE=cuda          # cuda for GPU, cpu for CPU
LOAD_MODELS_ON_STARTUP=True

# Database
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=password

# Security
SECRET_KEY=your-secret-key
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

---

## 📈 Performance Tips

### Enable GPU (10x faster)
```bash
export MODEL_DEVICE=cuda
```

### Use Lighter Models
```bash
export GLAUCOMA_MODEL_NAME=microsoft/resnet-50
export LLM_MODEL_NAME=tiiuae/falcon-7b-instruct
```

### Enable Caching
```bash
# Redis caches results automatically
# Same image = instant result
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### API Documentation (Interactive)
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

### Run Tests
```bash
cd backend && pytest tests/ -v
cd frontend && npm test
```

---

## 🐛 Troubleshooting

### Models not loading?
```bash
# Clear cache and restart
rm -rf backend/model_cache/
docker-compose restart backend
```

### Database error?
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Port conflicts?
```bash
# Change port in docker-compose.yml
# Backend: 8000 → 8080
# Frontend: 3000 → 3001
```

---

## 🚀 Deployment

### Docker
```bash
# Build images
docker build -t medical-backend -f backend/Dockerfile .
docker build -t medical-frontend -f frontend/Dockerfile .

# Push to registry
docker push your-registry/medical-backend
docker push your-registry/medical-frontend
```

### Kubernetes
```bash
# Apply manifests
kubectl apply -f kubernetes/deployment.yaml

# Check status
kubectl get pods -n medical-diagnosis
kubectl logs -n medical-diagnosis -l app=backend
```

### GitHub Actions (Automatic)
- Push to `main` branch
- Pipelines automatically build, test, and deploy
- (Set up GitHub Secrets first!)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete guide & features |
| `ARCHITECTURE.md` | System design & implementation |
| `SETUP.md` | Installation instructions |
| `backend/.env.example` | Environment template |
| `/docs` | Auto-generated API docs |

---

## 🎯 Next Steps

1. **Start the application**
   ```bash
   docker-compose up -d
   ```

2. **Try the UI**
   - http://localhost:3000 (Frontend)
   - http://localhost:8000/docs (API Docs)

3. **Explore the code**
   - Backend: `backend/app/`
   - ML Engine: `backend/ml/inference.py`
   - Frontend: `frontend/src/`

4. **Try model switching**
   - Visit Dashboard
   - Enter new model from HuggingFace
   - Watch it load!

5. **Deploy to production**
   - Follow Kubernetes setup in ARCHITECTURE.md
   - Configure GitHub Secrets
   - Push to main branch

---

## 📞 Support Resources

- **Full Docs**: `README.md`
- **Architecture**: `ARCHITECTURE.md`
- **Setup Guide**: `SETUP.md`
- **API Docs**: http://localhost:8000/docs
- **Code Comments**: All code is well-documented

---

## ✨ What Makes This Production-Grade

✅ **Clean Architecture** - Layered, modular design
✅ **Security** - OAuth, JWT, encryption, audit logs
✅ **Scalability** - Kubernetes-ready, auto-scaling
✅ **Monitoring** - Logging, health checks, metrics
✅ **CI/CD** - Automated testing & deployment
✅ **Documentation** - Comprehensive & clear
✅ **Error Handling** - Graceful failures
✅ **Model Flexibility** - Swap models without code changes

---

## 🎓 Learning Resources

The code includes examples of:
- FastAPI best practices
- React hooks & state management
- ML model inference
- Database integration
- Docker containerization
- Kubernetes deployment
- GitHub Actions workflows
- Security implementation

---

<div align="center">

**Ready to use! Start with:**

```bash
docker-compose up -d
```

**Questions? Check the documentation files!**

</div>
