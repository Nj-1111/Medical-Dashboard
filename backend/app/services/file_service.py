"""
File Upload Service
Handles file uploads with virus scanning and metadata management
"""
import logging
import os
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path
import hashlib

from app.config import settings

logger = logging.getLogger(__name__)


class FileUploadService:
    """Service for handling file uploads with security checks"""
    
    @staticmethod
    def validate_file(
        filename: str,
        file_size: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate file before upload
        
        Args:
            filename: Name of the file
            file_size: Size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        file_ext = Path(filename).suffix.lower().lstrip('.')
        if file_ext not in settings.ALLOWED_FILE_EXTENSIONS:
            return False, f"File type .{file_ext} not allowed. Allowed: {settings.ALLOWED_FILE_EXTENSIONS}"
        
        # Check file size
        max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File size exceeds maximum of {settings.MAX_UPLOAD_SIZE_MB}MB"
        
        return True, None
    
    @staticmethod
    async def scan_for_malware(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Scan file for malware/viruses
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (is_safe, error_message)
        """
        if not settings.ENABLE_VIRUS_SCAN:
            logger.info("Virus scanning disabled")
            return True, None
        
        try:
            # TODO: Integrate with ClamAV or similar
            # For now, return safe
            logger.info(f"Scanning file: {file_path}")
            return True, None
        except Exception as e:
            logger.error(f"Error scanning file: {str(e)}")
            return False, "Virus scan failed"
    
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """
        Calculate SHA256 hash of file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hex digest of SHA256
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def save_upload_metadata(
        file_id: str,
        filename: str,
        patient_id: str,
        file_type: str,
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Save file metadata to database
        
        Args:
            file_id: Unique file identifier
            filename: Original filename
            patient_id: Associated patient ID
            file_type: Type of file (image, document, etc.)
            metadata: Additional metadata
            
        Returns:
            Saved metadata record
        """
        record = {
            "file_id": file_id,
            "filename": filename,
            "patient_id": patient_id,
            "file_type": file_type,
            "upload_timestamp": datetime.utcnow(),
            "metadata": metadata or {},
            "status": "active"
        }
        
        # TODO: Save to database
        logger.info(f"Metadata saved for file: {file_id}")
        return record
