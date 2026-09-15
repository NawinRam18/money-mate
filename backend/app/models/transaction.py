import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, JSON, Numeric, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    wallet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("wallets.id"),
        nullable=False,
        index=True
    )

    merchant_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("merchants.id"),
        nullable=True,
        index=True
    )

    recipient_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    recipient_identifier: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False,
        index=True
    )

    risk_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )

    risk_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    risk_decision: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    risk_reasons: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    payment_mode: Mapped[str] = mapped_column(
        String(20),
        default="ONLINE",
        nullable=False
    )

    is_offline: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    offline_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )

    idempotency_key: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        index=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )