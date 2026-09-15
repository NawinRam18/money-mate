from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.health import router as health_router
from app.api.auth import router as auth_router

from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.wallet import Wallet
from app.models.merchant import Merchant
from app.models.transaction import Transaction
from app.models.mandate import Mandate
from app.models.security_event import SecurityEvent
from app.models.offline_transaction import OfflineTransaction
from app.models.audit_log import AuditLog


Base.metadata.create_all(bind=engine)


bearer_scheme = HTTPBearer()


app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)