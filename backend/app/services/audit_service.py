from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def create_audit_log(db: Session, user_id, action: str, resource_type: str, resource_id: str | None = None, description: str | None = None, details: dict | None = None):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        details=details
    )
    db.add(audit_log)
    return audit_log