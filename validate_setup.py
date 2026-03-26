#!/usr/bin/env python
"""
Medical Dashboard - Database and Code Quality Verification Script
Performs comprehensive checks and fixes for database and code issues
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class MedicalDashboardValidator:
    """Validates and fixes Medical Dashboard installation"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.issues = []
        self.fixes_applied = []
        
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}\n")
        
    def print_section(self, text):
        """Print formatted section"""
        print(f"\n--- {text} ---")
        
    def log_issue(self, severity, message):
        """Log an issue"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}]"
        
        if severity == "ERROR":
            print(f"{prefix} ERROR: {message}")
        elif severity == "WARNING":
            print(f"{prefix} WARNING: {message}")
        elif severity == "INFO":
            print(f"{prefix} INFO: {message}")
        elif severity == "SUCCESS":
            print(f"{prefix} SUCCESS: {message}")
            
        self.issues.append({"severity": severity, "message": message})
        
    def check_python_environment(self):
        """Check Python version and virtual environment"""
        self.print_section("Python Environment Check")
        
        # Check Python version
        version_info = sys.version_info
        python_version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        if version_info.major == 3 and version_info.minor >= 11:
            self.log_issue("SUCCESS", f"Python {python_version} detected")
            return True
        else:
            self.log_issue("ERROR", f"Python {python_version} detected. Required: 3.11+")
            return False
            
    def check_dependencies(self):
        """Check if required packages are installed"""
        self.print_section("Dependencies Check")
        
        # Check for venv
        if (self.backend_dir / "venv").exists():
            self.log_issue("SUCCESS", "Virtual environment exists")
        else:
            self.log_issue("WARNING", "Virtual environment not found at backend/venv")
            
        # Check for required files
        required_files = [
            ("backend/requirements.txt", "Python dependencies file"),
            ("backend/.env", "Backend environment configuration"),
            ("frontend/package.json", "Frontend dependencies file"),
            ("docker-compose.yml", "Docker Compose configuration"),
        ]
        
        for file_path, description in required_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                self.log_issue("SUCCESS", f"Found: {description}")
            else:
                self.log_issue("WARNING", f"Missing: {description}")
                
    def check_database_config(self):
        """Check database configuration"""
        self.print_section("Database Configuration Check")
        
        env_file = self.backend_dir / ".env"
        
        if not env_file.exists():
            self.log_issue("WARNING", "Environment file not found. Creating from template...")
            env_example = self.backend_dir / ".env.example"
            if env_example.exists():
                with open(env_example, 'r') as f:
                    content = f.read()
                with open(env_file, 'w') as f:
                    f.write(content)
                self.log_issue("SUCCESS", "Environment file created from template")
                self.fixes_applied.append("Created .env from template")
                return True
            else:
                self.log_issue("ERROR", ".env.example not found")
                return False
        else:
            self.log_issue("SUCCESS", "Environment file exists")
            # Parse configuration
            try:
                config = {}
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                config[key.strip()] = value.strip()
                
                required_keys = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
                for key in required_keys:
                    if key in config:
                        self.log_issue("SUCCESS", f"{key} configured")
                    else:
                        self.log_issue("WARNING", f"{key} not configured")
                        
                return True
            except Exception as e:
                self.log_issue("ERROR", f"Failed to parse environment file: {str(e)}")
                return False
                
    def check_code_quality(self):
        """Check for obvious code quality issues"""
        self.print_section("Code Quality Check")
        
        # Check for Python files
        py_files = list(self.backend_dir.rglob("*.py"))
        if py_files:
            self.log_issue("SUCCESS", f"Found {len(py_files)} Python files")
        else:
            self.log_issue("WARNING", "No Python files found in backend")
            
        # Check for syntax errors
        syntax_errors = []
        for py_file in py_files[:10]:  # Check first 10 files
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {str(e)}")
                
        if syntax_errors:
            self.log_issue("ERROR", f"Syntax errors found: {len(syntax_errors)}")
            for error in syntax_errors[:3]:
                print(f"  {error}")
        else:
            self.log_issue("SUCCESS", "No syntax errors detected in checked files")
            
    def verify_docker_setup(self):
        """Verify Docker configuration"""
        self.print_section("Docker Configuration Check")
        
        docker_files = [
            ("backend/Dockerfile", "Backend container"),
            ("frontend/Dockerfile", "Frontend container"),
            ("docker-compose.yml", "Compose orchestration"),
        ]
        
        for file_path, description in docker_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                self.log_issue("SUCCESS", f"Found: {description}")
            else:
                self.log_issue("WARNING", f"Missing: {description}")
                
    def check_ml_models_config(self):
        """Check ML/AI model configuration"""
        self.print_section("ML Models Configuration Check")
        
        env_file = self.backend_dir / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    
                if 'GLAUCOMA_MODEL_NAME' in content:
                    self.log_issue("SUCCESS", "Glaucoma model configuration found")
                else:
                    self.log_issue("WARNING", "Glaucoma model not configured")
                    
                if 'LLM_MODEL_NAME' in content:
                    self.log_issue("SUCCESS", "LLM model configuration found")
                else:
                    self.log_issue("WARNING", "LLM model not configured")
                    
                if 'MODEL_DEVICE' in content:
                    self.log_issue("SUCCESS", "Model device configuration found")
                else:
                    self.log_issue("WARNING", "Model device not configured (default: CPU)")
                    
            except Exception as e:
                self.log_issue("ERROR", f"Failed to check model configuration: {str(e)}")
                
    def generate_report(self):
        """Generate summary report"""
        self.print_header("VALIDATION REPORT SUMMARY")
        
        # Count issues by severity
        errors = len([i for i in self.issues if i['severity'] == 'ERROR'])
        warnings = len([i for i in self.issues if i['severity'] == 'WARNING'])
        successes = len([i for i in self.issues if i['severity'] == 'SUCCESS'])
        
        print(f"\nStatus Summary:")
        print(f"  Successful checks: {successes}")
        print(f"  Warnings: {warnings}")
        print(f"  Errors: {errors}")
        
        if self.fixes_applied:
            print(f"\nFixes Applied:")
            for fix in self.fixes_applied:
                print(f"  - {fix}")
                
        print(f"\nValidation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nNext Steps:")
        print(f"  1. Review all warnings and errors above")
        print(f"  2. Run: docker-compose up -d")
        print(f"  3. OR Run: python backend/init_db.py (for local development)")
        print(f"  4. Access: http://localhost:3000 (or 8000 for API)")
        
        return errors == 0
        
    def run_validation(self):
        """Run all validation checks"""
        self.print_header("MEDICAL DASHBOARD - SYSTEM VALIDATION")
        
        print(f"Installation Path: {self.root_dir}")
        print(f"Validation Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all checks
        self.check_python_environment()
        self.check_dependencies()
        self.check_database_config()
        self.check_code_quality()
        self.verify_docker_setup()
        self.check_ml_models_config()
        
        # Generate report
        success = self.generate_report()
        
        return 0 if success else 1

def main():
    """Main entry point"""
    try:
        validator = MedicalDashboardValidator()
        exit_code = validator.run_validation()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
