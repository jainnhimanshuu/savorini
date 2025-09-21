"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr

from core.security import (
    TokenData,
    TokenResponse,
    create_token_pair,
    get_current_user,
    get_password_hash,
    verify_password,
)
from domain.entities import User, UserProfile
from domain.enums import UserRole

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Registration request schema."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """Login user."""
    # TODO: Implement user lookup from repository
    # For now, return mock response
    
    # Mock user validation
    if request.email == "vendor@example.com" and request.password == "password":
        return create_token_pair(user_id="vendor-123", role="vendor")
    elif request.email == "admin@example.com" and request.password == "password":
        return create_token_pair(user_id="admin-123", role="admin")
    elif request.email == "user@example.com" and request.password == "password":
        return create_token_pair(user_id="user-123", role="user")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest) -> TokenResponse:
    """Register new user."""
    # TODO: Implement user creation in repository
    # For now, return mock response
    
    hashed_password = get_password_hash(request.password)
    
    # Mock user creation
    user_id = "new-user-123"
    
    return create_token_pair(user_id=user_id, role=request.role.value)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest) -> TokenResponse:
    """Refresh access token."""
    # TODO: Implement token refresh logic
    # Verify refresh token and create new access token
    
    # Mock refresh
    return create_token_pair(user_id="user-123", role="user")


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: TokenData = Depends(get_current_user),
) -> UserProfile:
    """Get current user profile."""
    # TODO: Implement user profile lookup
    # For now, return mock profile
    
    from datetime import datetime
    import uuid
    
    return UserProfile(
        id=uuid.UUID(current_user.user_id) if len(current_user.user_id) > 10 else uuid.uuid4(),
        email="user@example.com",
        role=UserRole(current_user.role),
        first_name="John",
        last_name="Doe",
        phone=None,
        age_verified=True,
        is_active=True,
        full_name="John Doe",
        created_at=datetime.utcnow(),
        last_login_at=datetime.utcnow(),
    )


@router.post("/logout")
async def logout(
    current_user: TokenData = Depends(get_current_user),
) -> dict:
    """Logout user."""
    # TODO: Implement token blacklisting
    return {"message": "Successfully logged out"}
