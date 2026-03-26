"""
Data Models
Pydantic models for request/response serialization
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator


# ============ Authentication Models ============
class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str = Field(..., min_length=1)


def _validate_password_complexity(v: str) -> str:
    """Shared password complexity checker used by registration/change-password schemas."""
    errors = []
    if len(v) < 8:
        errors.append("at least 8 characters")
    if not any(c.isupper() for c in v):
        errors.append("one uppercase letter")
    if not any(c.islower() for c in v):
        errors.append("one lowercase letter")
    if not any(c.isdigit() for c in v):
        errors.append("one digit")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
        errors.append("one special character")
    if errors:
        raise ValueError(f"Password must contain {', '.join(errors)}.")
    return v


class UserCreate(BaseModel):
    """New user registration request – enforces password complexity."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1)
    role: str = Field(default="user")

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        return _validate_password_complexity(v)


class ChangePasswordRequest(BaseModel):
    """Change-password request – enforces password complexity."""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def new_password_complexity(cls, v: str) -> str:
        return _validate_password_complexity(v)


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response"""
    id: str
    email: EmailStr
    name: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Patient Models ============
class PatientCreate(BaseModel):
    """Create patient request"""
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    medical_record_number: str = Field(...)


class PatientUpdate(BaseModel):
    """Update patient request"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class PatientResponse(BaseModel):
    """Patient response"""
    id: str
    first_name: str
    last_name: str
    date_of_birth: str
    email: Optional[str]
    phone: Optional[str]
    medical_record_number: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Diagnosis Models ============
class DiagnosisRequest(BaseModel):
    """Diagnosis inference request"""
    patient_id: str
    image_id: str
    image_url: Optional[str] = None
    additional_metadata: Optional[dict] = None


class DiagnosisResult(BaseModel):
    """Diagnosis result"""
    diagnosis_id: str
    patient_id: str
    diagnosis_type: str  # "glaucoma", "other", etc.
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    result: str  # "positive", "negative", "inconclusive"
    findings: str
    recommendations: str
    generated_at: datetime
    model_version: str
    model_name: str


class DiagnosisResponseWithPDF(DiagnosisResult):
    """Diagnosis response with PDF"""
    pdf_url: str
    download_link: str


# ============ Upload Models ============
class UploadResponse(BaseModel):
    """File upload response"""
    file_id: str
    filename: str
    size_bytes: int
    upload_timestamp: datetime
    storage_path: str
    virus_scan_status: str  # "clean", "infected", "pending"


class UploadMetadata(BaseModel):
    """Upload metadata"""
    patient_id: str
    file_type: str
    modality: str  # "fundus", "oct", "general", etc.
    metadata: Optional[dict] = None


# ============ Health Check Models ============
class HealthStatus(BaseModel):
    """Health check status"""
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    version: str
    services: dict


# ============ Error Models ============
class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: str
    timestamp: datetime
