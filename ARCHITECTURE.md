# System Architecture & Implementation Guide

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Component Details](#component-details)
3. [Data Flow](#data-flow)
4. [Security Architecture](#security-architecture)
5. [Deployment Architecture](#deployment-architecture)
6. [Model Infrastructure](#model-infrastructure)

---

## High-Level Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Tier                              │
|  ┌──────────────────────────────────────────────────────────┐  │
│  │            Doctor Web Application (React)                │  │
│  │  • Patient Management  • Upload Images  • View Reports   │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS/TLS
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Security & Gateway Tier                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Azure Front Door (WAF + Rate Limiting + DDoS Protection)│  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │       API Gateway / Ingress Controller                    │  │
│  │  • Request validation  • Route-based access             │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Application Tier (AKS Cluster)                  │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │   Auth       │  Patient     │   Upload     │  Inference   │  │
│  │  Service     │  Service     │  Service     │  Service     │  │
│  │              │              │              │              │  │
│  │ • OAuth 2.0  │ • CRUD       │ • Virus Scan │ • Glaucoma  │  │
│  │ • JWT        │ • Query      │ • Storage    │ • LLM       │  │
│  │ • OIDC       │ • Access     │ • Metadata   │ • Reports   │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              ML/Inference Engine                         │   │
│  │  • Model Loading  • Inference  • Result Processing      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Tier (Private VNet)                    │
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │   PostgreSQL     │  │   Redis        │  │ Azure Blob   │   │
│  │   Database       │  │  (Vectors)     │  │ Storage      │   │
│  │                  │  │  (Cache)       │  │              │   │
│  │ • Patient Data   │  │ • Embeddings   │  │ • Images     │   │
│  │ • Diagnosis      │  │ • Sessions     │  │ • PDFs       │   │
│  │ • Audit Logs     │  │                │  │              │   │
│  └──────────────────┘  └────────────────┘  └──────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Azure Key Vault (Secrets Management)          │   │
│  │  • Database credentials  • API keys  • Certificates      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
        ▲                                          ▲
        │                                          │
        │ Monitoring                               │ Audit
        │                                          │
┌───────┴──────────────────────────────────────────┴──────────────┐
│                  Observability Tier                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Azure Monitor + Log Analytics + Application Insights     │  │
│  │  • Metrics  • Logs  • Traces  • Alerts                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Central Audit Log (Immutable)                 │  │
│  │  • User actions  • API calls  • Data access             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend (React Application)

**Location**: `frontend/src`

**Responsibilities**:
- User authentication & session management
- Patient and diagnosis management interface
- Medical image upload
- Report viewing & PDF download
- Model configuration (dashboard)

**Key Files**:
- `Dashboard.jsx`: Main dashboard with model switching capability
- `UploadDiagnosis.jsx`: Image upload and diagnosis workflow
- `api.js`: Axios client with token injection & error handling

**Architecture**:
```
React App
├─ Authentication Interceptor
├─ API Client (with Bearer token)
├─ Pages (Components)
│  ├─ Dashboard (model status & switching)
│  ├─ Upload (image upload UI)
│  └─ Reports (diagnosis results)
└─ Tailwind CSS (styling)
```

### 2. Backend API (FastAPI)

**Location**: `backend/app`

**Responsibilities**:
- RESTful API for all operations
- Authentication & authorization
- Business logic orchestration
- Request validation & error handling

**Core Components**:

#### Main Application (`main.py`)
- FastAPI instance
- CORS middleware
- Request logging middleware
- Exception handlers
- Model loading on startup

#### Configuration (`config.py`)
- Environment-based settings
- Model names (configurable!)
- Database URLs
- Security credentials
- All settings come from `.env`

#### Security (`security/auth.py`)
- JWT token generation & verification
- Password hashing (bcrypt)
- OAuth provider integration stubs
- Role-based decorators

#### API Routes (`api/routes.py`)
- Authentication endpoints
- Patient CRUD endpoints
- File upload endpoints
- Inference endpoints
- Model switching endpoints
- Health check

**API Structure**:
```
/api/v1/
├─ /auth
│  ├─ POST /login
│  ├─ POST /logout
│  └─ GET /me
├─ /patients
│  ├─ GET / (list)
│  ├─ POST / (create)
│  ├─ GET /{id}
│  └─ PUT /{id}
├─ /upload
│  └─ POST /image
├─ /inference
│  ├─ POST /glaucoma
│  ├─ GET /models/status
│  ├─ POST /models/switch-glaucoma
│  └─ POST /models/switch-llm
└─ /health
   └─ GET /
```

### 3. ML Inference Engine

**Location**: `backend/ml/inference.py`

**Key Features**:
- **Configurable Models**: Switch via environment variables or API
- **Lazy Loading**: Models loaded on first use
- **GPU Support**: Automatic CUDA detection
- **Caching**: Models cached in memory
- **Error Handling**: Graceful fallbacks

**How It Works**:

1. **Model Loading** (Configurable)
   ```python
   # Via environment
   GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
   LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
   
   # These load from HuggingFace Hub automatically
   ```

2. **Inference Workflow**
   ```
   Image Input
   ├─ Validate & Load
   ├─ Preprocess
   ├─ Run Model Inference
   ├─ Extract Results
   └─ Return Predictions
   
   Results
   ├─ Generate Report with LLM
   ├─ Format Results
   └─ Return to API
   ```

3. **Model Switching** (Runtime)
   ```python
   # Just change the model name!
   InferenceEngine.switch_glaucoma_model("facebook/dino-vitb16")
   InferenceEngine.switch_llm_model("meta-llama/Llama-2-7b")
   ```

---

## Data Flow

### Diagnosis Workflow

```
Doctor uploads image
        │
        ▼
[Frontend Upload]
  • Validate file type/size
  • Show progress
        │
        ▼
[Backend Upload Service]
  • Virus scan
  • Save metadata to DB
  • Store in Azure Blob
        │
        ▼
[Request Inference]
  • Get image from storage
  • Call InferenceEngine
        │
        ▼
[Glaucoma Detection Model]
  • Load image
  • Extract features
  • Classify (positive/negative)
  • Return confidence
        │
        ▼
[LLM Report Generation]
  • Take diagnosis result
  • Generate professional report
  • Include recommendations
        │
        ▼
[Generate PDF]
  • Format report
  • Create downloadable PDF
  • Store in Blob Storage
        │
        ▼
[Return Results]
  • Diagnosis status
  • Confidence score
  • Generated report
  • PDF download link
        │
        ▼
[Frontend Display]
  • Show results
  • Allow PDF download
```

### Authentication Flow

```
[Login Request]
  • Email + Password
        │
        ▼
[Verify Credentials]
  • Check against DB
        │
        ▼
[Create JWT Token]
  • Payload: user_id, role, email
  • Expiration: 30 minutes
  • Signed with SECRET_KEY
        │
        ▼
[Return Token to Client]
        │
        ▼
[Subsequent Requests]
  • Include: Authorization: Bearer <token>
        │
        ▼
[Verify Token]
  • Decode JWT
  • Check expiration
  • Extract claims
        │
        ▼
[Allow/Deny Request]
  • Role check (doctor/admin)
  • Resource access control
```

---

## Security Architecture

### Authentication & Authorization

```
┌──────────────────────────────────────────────────────────┐
│               OAuth 2.0 / OIDC Flow                       │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  User → Doctor Web App → Azure AD                        │
│                          ↓                                │
│                    Authorization Code                     │
│                          ↓                                │
│            Backend exchanges for Access Token             │
│                          ↓                                │
│              ✓ Token stored securely (httpOnly)          │
│                          ↓                                │
│  Doc App uses token for authenticated API calls          │
│                                                            │
└──────────────────────────────────────────────────────────┘

JWT Structure:
{
  "sub": "doctor@hospital.com",
  "role": "doctor",
  "email": "doctor@hospital.com",
  "exp": 1704067200,  // expiration
  "iat": 1704063600   // issued at
}
```

### Network Security

```
┌─────────────────────────────────────┐
│    Internet                         │
│    (Public)                         │
└──────────────┬──────────────────────┘
               │ HTTPS + WAF
               ▼
┌─────────────────────────────────────┐
│  Azure Front Door                   │
│  • DDoS Protection                  │
│  • Rate Limiting (1000 req/min)     │
│  • Geographic Routing               │
└──────────────┬──────────────────────┘
               │ Private Link
               ▼
┌─────────────────────────────────────┐
│  AKS Cluster (Private VNet)         │
│  • Network Policies                 │
│  • Pod Security Policies             │
│  • Service Mesh (optional)          │
└──────────────┬──────────────────────┘
               │ Service-to-service
               ├──────────────────────┐
               ▼                      ▼
          ┌─────────┐            ┌────────┐
          │Database │            │Storage │
          │Private  │            │Private │
          └─────────┘            └────────┘
```

### Data Encryption

```
Encryption at Transit (TLS 1.3)
├─ Edge to Client: HTTPS
├─ Client to Backend: HTTPS
├─ Backend to Database: TLS
└─ Backend to Storage: TLS

Encryption at Rest (AES-256)
├─ Database: Column-level encryption
├─ Blob Storage: Server-side encryption
├─ Secrets: Azure Key Vault
│  • Database credentials
│  • API keys
│  • Certificates
│  • Encryption keys
└─ Audit Logs: Write-once storage

Encryption Example:
┌─────────────────────────────┐
│  Plaintext                  │
│  "Patient Data"             │
└──────────────┬──────────────┘
               │ AES-256 + Key from Key Vault
               ▼
┌─────────────────────────────┐
│  Ciphertext                 │
│  (stored in DB)             │
├─────────────────────────────┤
│  Access requires:           │
│  1. Database access         │
│  2. Key Vault access        │
│  3. RBAC permissions        │
└─────────────────────────────┘
```

---

## Deployment Architecture

### Local Development (Docker Compose)

```
docker-compose.yml
├─ postgres (PostgreSQL 15)
├─ redis (Redis 7)
├─ backend (FastAPI)
├─ frontend (React + Serve)
└─ clamav (Virus scanner)

Network: medical-network (isolated)
Volumes: persist data locally
```

### Production (Kubernetes on AKS)

```
┌─────────────────────────────────────────────────────────┐
│           Azure Kubernetes Service (AKS)                │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Namespace: medical-diagnosis                           │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Frontend Deployment (2+ replicas)              │   │
│  │  ├─ Pod 1: React app (3000)                     │   │
│  │  └─ Pod 2: React app (3000)                     │   │
│  │  └─ Service: LoadBalancer (0.0.0.0:3000)       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Backend Deployment (2-10 replicas)             │   │
│  │  ├─ Pod 1: FastAPI (8000) + Models             │   │
│  │  ├─ Pod 2: FastAPI (8000) + Models             │   │
│  │  └─ HorizontalPodAutoscaler (CPU/Memory)        │   │
│  │  └─ Service: ClusterIP (8000)                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  PostgreSQL StatefulSet (1 replica)             │   │
│  │  ├─ Pod: postgres (5432)                        │   │
│  │  ├─ PersistentVolume: 10GB                      │   │
│  │  └─ Service: Headless (ps)                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Redis Deployment (1 replica)                   │   │
│  │  ├─ Pod: redis (6379)                           │   │
│  │  ├─ PersistentVolume: 5GB                       │   │
│  │  └─ Service: ClusterIP (6379)                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Ingress (TLS termination)                      │   │
│  │  ├─ api.medical-diagnosis.com → backend        │   │
│  │  └─ medical-diagnosis.com → frontend           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Network Policies (pod-to-pod)                  │   │
│  │  • Frontend ↔ Backend allowed                   │   │
│  │  • Backend ↔ Database allowed                   │   │
│  │  • Others blocked by default                    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
         │                      │
         ▼                      ▼
    ┌─────────┐            ┌────────────┐
    │Azure    │            │Azure Blob  │
    │Database │            │Storage     │
    │         │            │            │
    │Private  │            │Private     │
    │Network  │            │Endpoint    │
    └─────────┘            └────────────┘
```

### CI/CD Pipeline (GitHub Actions)

```
Developer Push to Main
       │
       ▼
    ┌────────────────────────────────────┐
    │  GitHub Actions Triggered          │
    └────────────────────────────────────┘
       │
       ├─ Backend CI Jobs         ├─ Frontend CI Jobs
       │  • Unit tests            │  • Build
       │  • Linting              │  • Tests
       │  • Security scan        │  • Linting
       │  • Docker build         │  • Docker build
       │                         │
       ▼                         ▼
    ┌────────────────────────────────────┐
    │  Push images to Azure ACR          │
    │  • medical-backend:{sha}          │
    │  • medical-frontend:{sha}         │
    └────────────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────────┐
    │  Deploy to AKS                     │
    │  • Apply K8s manifests             │
    │  • Update deployments              │
    │  • Rollout status check            │
    │  • Smoke tests                     │
    └────────────────────────────────────┘
       │
       ▼
    ┌────────────────────────────────────┐
    │  ✓ Production Live                 │
    └────────────────────────────────────┘
```

---

## Model Infrastructure

### How Model Configuration Works

#### 1. Configuration Hierarchy (Priority Order)
```
1. API Call (highest priority)
   InferenceEngine.switch_glaucoma_model("new-model")
   
2. Environment Variables
   export GLAUCOMA_MODEL_NAME=facebook/dino-vitb16
   
3. .env File
   GLAUCOMA_MODEL_NAME=microsoft/resnet-50
   
4. Default in config.py (lowest)
   GLAUCOMA_MODEL_NAME=google/vit-base-patch16-224
```

#### 2. Model Loading Process

```python
# When app starts with LOAD_MODELS_ON_STARTUP=true

InferenceEngine.initialize()
├─ Load glaucoma model
│  ├─ Check if already loaded (cached)
│  ├─ Get model name from config
│  ├─ Download from HuggingFace Hub (if needed)
│  ├─ Load to device (GPU/CPU)
│  └─ Cache in memory
├─ Load LLM model
│  └─ Same process
└─ Ready for inference!

# Or lazy-load on first inference
detect_glaucoma(image_path)
├─ Check if model loaded
├─ If not, load it now
└─ Run inference
```

#### 3. Model Storage

```
Local:
model_cache/
├─ models--google--vit-base-patch16-224/
│  ├─ snapshots/
│  │  ├─ config.json
│  │  ├─ model.safetensors
│  │  └─ ...
│  └─ refs/
├─ models--mistralai--Mistral-7B-Instruct-v0.1/
│  └─ ...

Azure:
Container Registry (ACR)
├─ medical-backend:v1
│  └─ model_cache/ (in image)
├─ medical-backend:v2
│  └─ model_cache/ (updated models)
```

#### 4. Model Metrics

```python
# Get current model status
status = InferenceEngine.get_model_status()
{
  "glaucoma_model": "google/vit-base-patch16-224",
  "glaucoma_model_loaded": True,
  "glaucoma_model_version": "1.0.0",
  "llm_model": "mistralai/Mistral-7B-Instruct-v0.1",
  "llm_model_loaded": True,
  "llm_model_version": "1.0.0",
  "device": "cuda",
  "cuda_available": True
}
```

---

## Implementation Details

### File Upload Security

```
Upload Request
├─ Validate token
├─ Validate file type (whitelist only)
├─ Validate file size (max 50MB)
├─ Scan for malware (ClamAV)
├─ Calculate SHA256 checksum
├─ Store in Azure Blob
│  └─ URL: https://storage.azure.com/medical-images/{file_id}
├─ Save metadata in DB
└─ Return file_id for inference
```

### Audit Logging

```python
# Every important action logged
Audit Log Entry:
{
  "timestamp": "2024-01-15T10:30:45Z",
  "user_id": "doctor@hospital.com",
  "action": "uploaded_medical_image",
  "resource": "patient_id=PAT-001",
  "status": "success",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": {
    "file_id": "IMG-123",
    "file_size": 2048000
  }
}

# Stored in:
# 1. logs/audit.log (local)
# 2. Azure Log Analytics (cloud)
# 3. Immutable storage (compliance)
```

---

## Performance Considerations

### Model Inference Latency

```
Glaucoma Detection (~1-5 seconds):
├─ Load image: 0.1s
├─ Preprocess: 0.2s
├─ Inference: 0.5-4s (depends on model/device)
└─ Postprocess: 0.2s

LLM Report Generation (~5-10 seconds):
├─ Prepare prompt: 0.1s
├─ Tokenize: 0.2s
├─ Generate tokens: 4-9s
└─ Format: 0.1s

Total End-to-End: ~10-20 seconds
```

### Optimization Tips

1. **Use GPU** (10x faster)
   ```bash
   export MODEL_DEVICE=cuda
   ```

2. **Quantize Models** (smaller, faster)
   ```python
   GLAUCOMA_MODEL_NAME=microsoft/resnet-50  # Lighter
   LLM_MODEL_NAME=tiiuae/falcon-7b-instruct  # Optimized
   ```

3. **Cache Results**
   - Redis caches inference results
   - Same image = instant result

4. **Batch Inference**
   - Process multiple images simultaneously
   - Better GPU utilization

---

## Monitoring & Alerts

### Key Metrics to Monitor

```
Application
├─ Request latency (p50, p95, p99)
├─ Request rate (req/sec)
├─ Error rate (4xx, 5xx %)
├─ Model inference latency
├─ Cache hit rate

Infrastructure
├─ CPU usage (%)
├─ Memory usage (%)
├─ Disk I/O (IOPS)
├─ Network I/O (MB/s)
├─ Pod restarts
└─ Node health

Compliance
├─ Audit log entries
├─ Failed auth attempts
├─ Data access events
└─ Policy violations
```

### Alert Thresholds

```
SET ALERT IF:
├─ API latency > 5 seconds
├─ Error rate > 1%
├─ CPU usage > 80%
├─ Memory usage > 85%
├─ Disk space < 10%
├─ Pod restarts > 3 in 10 min
└─ Failed auth attempts > 10/min
```

---

## Scaling Strategy

### Horizontal Scaling

```
Low Load (1 user):
└─ 1 Backend Pod, 1 Frontend Pod

Medium Load (10 users):
├─ 2-3 Backend Pods (HPA kicks in)
└─ 2 Frontend Pods

High Load (100 users):
├─ 5-10 Backend Pods
├─ 3-5 Frontend Pods
└─ Multi-zone AKS for resilience
```

### Database Scaling

```
Single Instance (dev)
↓ Failover replica
↓ Read replicas
↓ Sharding (by patient_id)
```

---

This architecture provides a **production-grade**, **secure**, and **scalable** medical diagnosis system. Every component is designed for reliability, observability, and ease of deployment.
