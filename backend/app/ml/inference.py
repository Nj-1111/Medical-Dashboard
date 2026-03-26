"""
ML Inference Engine
Configurable model loading and inference
"""
import logging
import os
from typing import Optional, Tuple, Dict, Any
import numpy as np
from pathlib import Path

import torch
from PIL import Image
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)

from app.config import settings

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Centralized inference engine for all ML models
    Supports dynamic model loading and switching
    """
    
    # Class-level cache for loaded models
    _glaucoma_model = None
    _glaucoma_processor = None
    _llm_model = None
    _llm_tokenizer = None
    _llm_pipeline = None
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize and load all configured models"""
        logger.info("Initializing ML models...")
        
        try:
            cls.load_glaucoma_model()
            logger.info(f"✓ Glaucoma model loaded: {settings.GLAUCOMA_MODEL_NAME}")
        except Exception as e:
            logger.error(f"✗ Failed to load glaucoma model: {str(e)}")
            raise
        
        try:
            cls.load_llm_model()
            logger.info(f"✓ LLM model loaded: {settings.LLM_MODEL_NAME}")
        except Exception as e:
            logger.error(f"✗ Failed to load LLM model: {str(e)}")
            raise
    
    @classmethod
    def load_glaucoma_model(cls) -> None:
        """
        Load glaucoma detection model
        Configurable via GLAUCOMA_MODEL_NAME
        """
        if cls._glaucoma_model is not None:
            logger.info("Glaucoma model already loaded")
            return
        
        try:
            device = "cuda" if settings.MODEL_DEVICE == "cuda" and torch.cuda.is_available() else "cpu"
            
            logger.info(
                f"Loading glaucoma model: {settings.GLAUCOMA_MODEL_NAME} "
                f"on device: {device}"
            )
            
            # Load processor
            cls._glaucoma_processor = AutoImageProcessor.from_pretrained(
                settings.GLAUCOMA_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR,
            )
            
            # Load model
            cls._glaucoma_model = AutoModelForImageClassification.from_pretrained(
                settings.GLAUCOMA_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR,
            )
            
            cls._glaucoma_model.to(device)
            cls._glaucoma_model.eval()
            
            logger.info("Glaucoma model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading glaucoma model: {str(e)}")
            raise
    
    @classmethod
    def load_llm_model(cls) -> None:
        """
        Load LLM model for report generation
        Configurable via LLM_MODEL_NAME
        """
        if cls._llm_model is not None:
            logger.info("LLM model already loaded")
            return
        
        try:
            device = "cuda" if settings.MODEL_DEVICE == "cuda" and torch.cuda.is_available() else "cpu"
            
            logger.info(
                f"Loading LLM model: {settings.LLM_MODEL_NAME} "
                f"on device: {device}"
            )
            
            # Load tokenizer
            cls._llm_tokenizer = AutoTokenizer.from_pretrained(
                settings.LLM_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR,
            )
            
            # Load model
            cls._llm_model = AutoModelForCausalLM.from_pretrained(
                settings.LLM_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR,
                device_map="auto" if device == "cuda" else "cpu"
            )
            
            cls._llm_model.eval()
            
            # Create pipeline for easier use
            cls._llm_pipeline = pipeline(
                "text-generation",
                model=cls._llm_model,
                tokenizer=cls._llm_tokenizer,
                device=(0 if device == "cuda" else -1)
            )
            
            logger.info("LLM model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading LLM model: {str(e)}")
            raise
    
    @classmethod
    def detect_glaucoma(
        cls,
        image_path: str,
        confidence_threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Perform glaucoma detection inference
        
        Args:
            image_path: Path to the medical image
            confidence_threshold: Confidence threshold for positive classification
            
        Returns:
            Dictionary with classification results
        """
        if cls._glaucoma_model is None:
            cls.load_glaucoma_model()
        
        try:
            device = next(cls._glaucoma_model.parameters()).device
            
            # Load and preprocess image
            image = Image.open(image_path).convert("RGB")
            inputs = cls._glaucoma_processor(
                image,
                return_tensors="pt"
            ).to(device)
            
            # Perform inference
            with torch.no_grad():
                outputs = cls._glaucoma_model(**inputs)
            
            # Get predictions
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class_idx = logits.argmax(-1).item()
            predicted_prob = probabilities[0, predicted_class_idx].item()
            
            # Determine glaucoma status
            class_names = cls._glaucoma_model.config.id2label
            predicted_label = class_names.get(predicted_class_idx, "unknown")
            
            # For binary classification
            is_positive = predicted_prob >= confidence_threshold
            
            return {
                "prediction": predicted_label,
                "confidence": float(predicted_prob),
                "is_positive": is_positive,
                "all_scores": {
                    class_names.get(i, str(i)): float(probabilities[0, i].item())
                    for i in range(len(class_names))
                },
                "model_name": settings.GLAUCOMA_MODEL_NAME,
                "model_version": settings.GLAUCOMA_MODEL_VERSION
            }
            
        except Exception as e:
            logger.error(f"Error during glaucoma detection: {str(e)}")
            raise
    
    @classmethod
    def generate_report(
        cls,
        diagnosis_result: str,
        patient_info: Dict[str, Any],
        additional_context: Optional[str] = None
    ) -> str:
        """
        Generate detailed diagnosis report using LLM
        
        Args:
            diagnosis_result: Result from glaucoma detection
            patient_info: Patient demographic information
            additional_context: Additional clinical context
            
        Returns:
            Generated report text
        """
        if cls._llm_pipeline is None:
            cls.load_llm_model()
        
        try:
            # Construct prompt for report generation
            prompt = f"""Generate a professional medical diagnosis report for glaucoma screening.

Patient: {patient_info.get('name', 'Anonymous')}
Age: {patient_info.get('age', 'Not specified')}

Diagnosis Result: {diagnosis_result}
Confidence: {patient_info.get('confidence', 'N/A')}

{f'Additional Clinical Notes: {additional_context}' if additional_context else ''}

Please generate a professional report including:
1. Clinical findings
2. Diagnosis
3. Recommendations
4. Follow-up requirements

Report:"""
            
            # Generate text
            output = cls._llm_pipeline(
                prompt,
                max_length=500,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            
            report = output[0]['generated_text']
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            # Return a template report on error
            return f"""Medical Diagnosis Report
Patient: {patient_info.get('name', 'Anonymous')}
Diagnosis: {diagnosis_result}
Recommendation: Follow-up required. Consult with ophthalmologist for confirmation."""
    
    @classmethod
    def switch_glaucoma_model(cls, model_name: str) -> bool:
        """
        Switch to a different glaucoma model
        
        Args:
            model_name: HuggingFace model identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Switching glaucoma model to: {model_name}")
            settings.GLAUCOMA_MODEL_NAME = model_name
            cls._glaucoma_model = None
            cls._glaucoma_processor = None
            cls.load_glaucoma_model()
            return True
        except Exception as e:
            logger.error(f"Failed to switch glaucoma model: {str(e)}")
            return False
    
    @classmethod
    def switch_llm_model(cls, model_name: str) -> bool:
        """
        Switch to a different LLM model
        
        Args:
            model_name: HuggingFace model identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Switching LLM model to: {model_name}")
            settings.LLM_MODEL_NAME = model_name
            cls._llm_model = None
            cls._llm_tokenizer = None
            cls._llm_pipeline = None
            cls.load_llm_model()
            return True
        except Exception as e:
            logger.error(f"Failed to switch LLM model: {str(e)}")
            return False
    
    @classmethod
    def get_model_status(cls) -> Dict[str, Any]:
        """Get current model status"""
        return {
            "glaucoma_model": settings.GLAUCOMA_MODEL_NAME,
            "glaucoma_model_loaded": cls._glaucoma_model is not None,
            "glaucoma_model_version": settings.GLAUCOMA_MODEL_VERSION,
            "llm_model": settings.LLM_MODEL_NAME,
            "llm_model_loaded": cls._llm_model is not None,
            "llm_model_version": settings.LLM_MODEL_VERSION,
            "device": settings.MODEL_DEVICE,
            "cuda_available": torch.cuda.is_available()
        }
