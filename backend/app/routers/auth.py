from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token
from app.services.auth_service import register_user, authenticate_user
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new system user (Admin, Tester, Developer)."""
    return register_user(db, user_in)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user with JSON payload and return JWT token."""
    return authenticate_user(db, credentials)

@router.post("/token", response_model=Token, include_in_schema=False)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 Form compatibility endpoint for FastAPI Docs / Swagger UI."""
    credentials = UserLogin(username=form_data.username, password=form_data.password)
    return authenticate_user(db, credentials)

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieve profile of currently authenticated user."""
    return current_user
