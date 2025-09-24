import os
import shutil
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from queries.file_queries import FileQueries
from queries.opportunity_queries import OpportunityQueries
from utils.response_helpers import validation_error, not_found_error
from utils.validation import validate_email

class FileService:
    """Service for file-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = FileQueries(db)
        self.opportunity_queries = OpportunityQueries(db)
        self.upload_dir = Path("uploads")
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.png', '.jpg', '.jpeg'}
        self.max_files_per_tenant = 100

    async def upload_proposal_file(
        self,
        file: UploadFile,
        proposal_id: int,
        tenant_id: int
    ) -> Dict[str, Any]:
        """Upload and save proposal file with validation."""
        # Business validation
        self._validate_file(file)
        self._check_tenant_limits(tenant_id)
        self._validate_proposal_exists(proposal_id, tenant_id)

        # Generate secure filename
        secure_filename = self._generate_secure_filename(file.filename)

        # Create tenant directory
        tenant_dir = self.upload_dir / str(tenant_id)
        tenant_dir.mkdir(parents=True, exist_ok=True)

        file_path = tenant_dir / secure_filename

        try:
            # Save file to disk
            await self._save_file_to_disk(file, file_path)

            # Get file size
            file_size = file_path.stat().st_size

            # Create database record
            file_data = {
                "tenant_id": tenant_id,
                "proposal_id": proposal_id,
                "filename": secure_filename,
                "size": file_size,
                "url": f"/api/files/{secure_filename}"
            }

            proposal_file = self.queries.create_proposal_file(file_data)

            return {
                "id": proposal_file.id,
                "filename": proposal_file.filename,
                "original_filename": file.filename,
                "size": proposal_file.size,
                "url": proposal_file.url,
                "proposal_id": proposal_file.proposal_id,
                "created_at": proposal_file.created_at.isoformat()
            }

        except Exception as e:
            # Clean up file if database operation fails
            if file_path.exists():
                file_path.unlink()
            raise Exception(f"File upload failed: {str(e)}")

    def delete_proposal_file(self, filename: str, tenant_id: int) -> Dict[str, str]:
        """Delete proposal file from both disk and database."""
        # Get file record
        proposal_file = self.queries.get_proposal_file_by_filename(filename, tenant_id)
        if not proposal_file:
            raise not_found_error("File")

        # Delete from disk
        file_path = self.upload_dir / str(tenant_id) / filename
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                raise Exception(f"Failed to delete file from disk: {str(e)}")

        # Delete from database
        self.queries.delete_proposal_file(proposal_file)

        return {"message": "File deleted successfully"}

    def get_file_statistics(self, tenant_id: int) -> Dict[str, Any]:
        """Get file statistics for a tenant."""
        total_files = self.queries.count_files_by_tenant(tenant_id)
        total_storage = self.queries.get_total_storage_used(tenant_id)

        return {
            "total_files": total_files,
            "total_storage_bytes": total_storage,
            "total_storage_mb": round(total_storage / (1024 * 1024), 2),
            "storage_limit_mb": round(self.max_file_size / (1024 * 1024), 2),
            "files_limit": self.max_files_per_tenant,
            "storage_usage_percent": round((total_storage / (self.max_file_size * self.max_files_per_tenant)) * 100, 2)
        }

    def cleanup_orphaned_files(self, tenant_id: int) -> Dict[str, Any]:
        """Clean up files on disk that don't have database records."""
        tenant_dir = self.upload_dir / str(tenant_id)
        if not tenant_dir.exists():
            return {"cleaned_files": 0, "message": "No tenant directory found"}

        # Get all files from database
        db_files = {f.filename for f in self.queries.get_proposal_files_by_tenant(tenant_id, limit=1000)}

        # Get all files from disk
        disk_files = {f.name for f in tenant_dir.iterdir() if f.is_file()}

        # Find orphaned files
        orphaned_files = disk_files - db_files

        cleaned_count = 0
        for filename in orphaned_files:
            file_path = tenant_dir / filename
            try:
                file_path.unlink()
                cleaned_count += 1
            except Exception:
                continue  # Skip files that can't be deleted

        return {
            "cleaned_files": cleaned_count,
            "message": f"Cleaned up {cleaned_count} orphaned files"
        }

    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file according to business rules."""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            allowed = ', '.join(self.allowed_extensions)
            raise validation_error(f"File type not allowed. Allowed types: {allowed}")

        # Check file size (if available)
        if hasattr(file, 'size') and file.size:
            if file.size > self.max_file_size:
                max_mb = self.max_file_size / (1024 * 1024)
                raise validation_error(f"File size exceeds {max_mb}MB limit")

        # Check filename
        if not file.filename or len(file.filename.strip()) == 0:
            raise validation_error("Filename is required")

        if len(file.filename) > 255:
            raise validation_error("Filename too long (max 255 characters)")

        # Check for dangerous characters
        dangerous_chars = {'<', '>', ':', '"', '|', '?', '*', '\\', '/'}
        if any(char in file.filename for char in dangerous_chars):
            raise validation_error("Filename contains invalid characters")

    def _check_tenant_limits(self, tenant_id: int) -> None:
        """Check if tenant has reached file limits."""
        file_count = self.queries.count_files_by_tenant(tenant_id)
        if file_count >= self.max_files_per_tenant:
            raise validation_error(f"File limit reached ({self.max_files_per_tenant} files maximum)")

        total_storage = self.queries.get_total_storage_used(tenant_id)
        max_total_storage = self.max_file_size * self.max_files_per_tenant
        if total_storage >= max_total_storage:
            max_gb = max_total_storage / (1024 * 1024 * 1024)
            raise validation_error(f"Storage limit reached ({max_gb:.1f}GB maximum)")

    def _validate_proposal_exists(self, proposal_id: int, tenant_id: int) -> None:
        """Validate that the proposal exists."""
        proposal = self.opportunity_queries.get_opportunity_by_id(proposal_id, tenant_id)
        if not proposal:
            raise not_found_error("Proposal", proposal_id)

    def _generate_secure_filename(self, original_filename: str) -> str:
        """Generate a secure filename to prevent conflicts and security issues."""
        file_ext = Path(original_filename).suffix.lower()
        unique_id = str(uuid.uuid4())

        # Clean original name (remove extension and dangerous chars)
        clean_name = Path(original_filename).stem
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c in '-_')[:50]

        return f"{clean_name}_{unique_id}{file_ext}"

    async def _save_file_to_disk(self, file: UploadFile, file_path: Path) -> None:
        """Save uploaded file to disk."""
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise Exception(f"Failed to save file to disk: {str(e)}")
        finally:
            file.file.close()