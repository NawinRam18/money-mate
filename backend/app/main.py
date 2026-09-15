from fastapi import FastAPI

from app.api.ai import router as ai_router
from app.api.security import router as security_router
from app.api.offline import router as offline_router
from app.api.finance import router as finance_router
from app.api.mandates import router as mandates_router
from app.api.health import router as health_router
from app.api.auth import router as auth_router
<<<<<<< HEAD
from app.api.offline import router as offline_router

=======
from app.api.wallet import router as wallet_router
from app.api.payments import router as payments_router
from app.api.transactions import router as transactions_router
from app.api.fraud import router as fraud_router
>>>>>>> 6f84e09 (Complete MONEY-MATE backend)
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

app = FastAPI()

app = FastAPI(title="MONEY-MATE API")


Base.metadata.create_all(bind=engine)


app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)
<<<<<<< HEAD
app.include_router(
    offline_router,
    prefix="/api/v1"
)
=======

app.include_router(
    wallet_router,
    prefix="/api/v1"
)

app.include_router(
    payments_router,
    prefix="/api/v1"
)
app.include_router(
    transactions_router,
    prefix="/api/v1"
) 
app.include_router(fraud_router, prefix="/api/v1")

app.include_router(mandates_router, prefix="/api/v1")

app.include_router(finance_router, prefix="/api/v1")

app.include_router(offline_router, prefix="/api/v1")

app.include_router(security_router, prefix="/api/v1")

app.include_router(ai_router, prefix="/api/v1")
>>>>>>> 6f84e09 (Complete MONEY-MATE backend)
