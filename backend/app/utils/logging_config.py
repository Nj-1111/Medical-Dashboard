"""
Logging Configuration
"""
import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Audit log
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)
    audit_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "audit.log",
        maxBytes=10485760,  # 10MB
        backupCount=20
    )
    audit_handler.setFormatter(file_format)
    audit_logger.addHandler(audit_handler)
    
    return root_logger
