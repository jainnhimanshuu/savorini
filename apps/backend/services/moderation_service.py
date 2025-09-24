"""Moderation service for content management."""

import uuid
from typing import List, Optional

from domain.entities import Flag, FlagWithDetails
from domain.enums import FlagStatus
from repositories.interfaces import FlagRepository, UserRepository
from core.exceptions import BusinessRuleError, NotFoundError
from core.logging import get_logger

logger = get_logger(__name__)


class ModerationService:
    """Service for content moderation."""
    
    def __init__(self, flag_repo: FlagRepository, user_repo: UserRepository):
        self.flag_repo = flag_repo
        self.user_repo = user_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def create_flag(
        self,
        target_type: str,
        target_id: uuid.UUID,
        reason: str,
        description: Optional[str],
        user_id: uuid.UUID
    ) -> Flag:
        """Create a new flag/report."""
        # Check if user already flagged this target
        existing_flag = await self.flag_repo.get_by_user_and_target(user_id, target_type, target_id)
        if existing_flag and existing_flag.status == FlagStatus.PENDING:
            raise BusinessRuleError(
                "You have already flagged this content",
                code="DUPLICATE_FLAG"
            )
        
        flag = Flag(
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            description=description,
            user_id=user_id,
            status=FlagStatus.PENDING,
        )
        
        created_flag = await self.flag_repo.create(flag)
        self.logger.info(
            "Flag created",
            flag_id=str(created_flag.id),
            target_type=target_type,
            target_id=str(target_id),
            reason=reason
        )
        
        return created_flag
    
    async def get_flag(self, flag_id: uuid.UUID) -> Flag:
        """Get flag by ID."""
        flag = await self.flag_repo.get_by_id(flag_id)
        if not flag:
            raise NotFoundError(f"Flag with id {flag_id} not found")
        
        return flag
    
    async def list_pending_flags(self, limit: int = 50, offset: int = 0) -> List[FlagWithDetails]:
        """List pending flags for moderation."""
        flags = await self.flag_repo.list_pending(limit, offset)
        
        # Convert to FlagWithDetails
        flag_details = []
        for flag in flags:
            # Get reporter info
            reporter = await self.user_repo.get_by_id(flag.user_id)
            reporter_email = reporter.email if reporter else "Unknown"
            
            # Get target name (would need additional queries in real implementation)
            target_name = f"{flag.target_type} {flag.target_id}"
            
            flag_detail = FlagWithDetails(
                flag=flag,
                target_name=target_name,
                reporter_email=reporter_email,
            )
            flag_details.append(flag_detail)
        
        return flag_details
    
    async def resolve_flag(
        self,
        flag_id: uuid.UUID,
        resolved_by: uuid.UUID,
        resolution_notes: Optional[str] = None
    ) -> Flag:
        """Resolve a flag."""
        flag = await self.get_flag(flag_id)
        
        if flag.status != FlagStatus.PENDING:
            raise BusinessRuleError(
                f"Flag is already {flag.status.value}",
                code="FLAG_ALREADY_RESOLVED"
            )
        
        flag.resolve(resolved_by, resolution_notes)
        updated_flag = await self.flag_repo.update(flag)
        
        self.logger.info(
            "Flag resolved",
            flag_id=str(flag_id),
            resolved_by=str(resolved_by),
            status=FlagStatus.RESOLVED.value
        )
        
        return updated_flag
    
    async def dismiss_flag(
        self,
        flag_id: uuid.UUID,
        resolved_by: uuid.UUID,
        resolution_notes: Optional[str] = None
    ) -> Flag:
        """Dismiss a flag."""
        flag = await self.get_flag(flag_id)
        
        if flag.status != FlagStatus.PENDING:
            raise BusinessRuleError(
                f"Flag is already {flag.status.value}",
                code="FLAG_ALREADY_RESOLVED"
            )
        
        flag.dismiss(resolved_by, resolution_notes)
        updated_flag = await self.flag_repo.update(flag)
        
        self.logger.info(
            "Flag dismissed",
            flag_id=str(flag_id),
            resolved_by=str(resolved_by),
            status=FlagStatus.DISMISSED.value
        )
        
        return updated_flag
    
    async def get_flag_stats(self) -> dict:
        """Get moderation statistics."""
        # This would typically query the database for stats
        # For now, return mock data
        return {
            "pending_flags": 0,
            "resolved_flags": 0,
            "dismissed_flags": 0,
            "total_flags": 0,
        }
