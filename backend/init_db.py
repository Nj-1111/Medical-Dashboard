"""
Database Initialization Script
Initializes PostgreSQL database, creates tables, and seeds initial data
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def init_database():
    """Initialize database with all required tables"""
    try:
        from app.config import settings
        from app.database import Base, engine
        from app.models import (
            User, MedicalRecord, DiagnosisReport, 
            AuditLog, ModelConfig
        )
        
        logger.info("🔄 Initializing database...")
        logger.info(f"   Database: {settings.DB_NAME}")
        logger.info(f"   Host: {settings.DB_HOST}:{settings.DB_PORT}")
        
        # Create all tables
        logger.info("📊 Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
        
        # Seed initial data
        seed_data()
        
        logger.info("✅ Database initialization complete!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        return False


def seed_data():
    """Seed initial data into database"""
    try:
        from app.database import SessionLocal
        from app.models import User, ModelConfig
        from app.security import get_password_hash
        
        session = SessionLocal()
        
        # Check if admin user exists
        admin = session.query(User).filter(User.email == "test@hospital.com").first()
        if not admin:
            logger.info("👤 Creating admin user...")
            admin_user = User(
                email="test@hospital.com",
                full_name="Test Admin",
                hashed_password=get_password_hash("testpass123"),
                is_active=True,
                is_admin=True
            )
            session.add(admin_user)
            logger.info("   ✓ Admin user created: test@hospital.com")
        else:
            logger.info("   ℹ Admin user already exists")
        
        # Check if model config exists
        models = session.query(ModelConfig).count()
        if models == 0:
            logger.info("⚙️  Setting up model configurations...")
            from datetime import datetime
            
            glaucoma_config = ModelConfig(
                model_name="google/vit-base-patch16-224",
                model_type="glaucoma_detection",
                is_active=True,
                created_at=datetime.utcnow()
            )
            session.add(glaucoma_config)
            
            llm_config = ModelConfig(
                model_name="mistralai/Mistral-7B-Instruct-v0.1",
                model_type="report_generation",
                is_active=True,
                created_at=datetime.utcnow()
            )
            session.add(llm_config)
            logger.info("   ✓ Model configurations created")
        else:
            logger.info("   ℹ Model configurations already exist")
        
        session.commit()
        session.close()
        logger.info("✅ Database seeding complete")
        
    except Exception as e:
        logger.error(f"❌ Database seeding failed: {str(e)}")
        raise


def check_database_connection():
    """Check if database is accessible"""
    try:
        from app.database import engine
        
        logger.info("🔍 Checking database connection...")
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("═" * 60)
    logger.info("Medical Dashboard - Database Initialization")
    logger.info("═" * 60)
    
    # Check connection first
    if not check_database_connection():
        sys.exit(1)
    
    # Initialize database
    if not init_database():
        sys.exit(1)
    
    logger.info("═" * 60)
