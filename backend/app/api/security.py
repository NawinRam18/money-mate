from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.security_event import SecurityEvent


router = APIRouter(
    prefix="/security",
    tags=["Security"]
)


@router.get("/overview")
def security_overview(
    user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "security_status": "GOOD",
            "security_score": 85,
            "fraud_protection": True,
            "offline_integrity": True,
            "jwt_authentication": True,
            "idempotency_protection": True,
            "message": "MONEY-MATE security systems are active."
        },
        "error": None
    }


@router.get("/events")
def security_events(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(SecurityEvent).filter(
        SecurityEvent.user_id == user.id
    ).order_by(
        SecurityEvent.created_at.desc()
    ).all()

    data = []

    for event in events:
        data.append({
            "event_id": str(event.id),
            "event_type": event.event_type,
            "severity": event.severity,
            "description": event.description,
            "created_at": event.created_at.isoformat()
        })

    return {
        "success": True,
        "data": data,
        "error": None
    }


@router.get("/score")
def security_score(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(SecurityEvent).filter(
        SecurityEvent.user_id == user.id
    ).all()

    score = 100

    for event in events:
        if event.severity == "CRITICAL":
            score -= 25
        elif event.severity == "HIGH":
            score -= 15
        elif event.severity == "MEDIUM":
            score -= 10
        elif event.severity == "LOW":
            score -= 5

    score = max(0, score)

    if score >= 80:
        status = "GOOD"
    elif score >= 60:
        status = "MODERATE"
    elif score >= 40:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return {
        "success": True,
        "data": {
            "security_score": score,
            "security_status": status,
            "total_security_events": len(events),
            "message": "MONEY-MATE Security Score is a demo security indicator, not a banking security rating."
        },
        "error": None
    }