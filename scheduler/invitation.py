from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.models.invitation import Invitation
from app.db.base import get_db

invitation_scheduler = BackgroundScheduler()

def invalidate_expired_invitations():
    db = get_db()
    current_time = datetime.now()
    expired_invitations = db.query(Invitation).filter(Invitation.expires_at < current_time).all()
    
    for invitation in expired_invitations:
        db.delete(invitation)
    
    db.commit()

invitation_scheduler.add_job(invalidate_expired_invitations, 'interval', minutes=60)  # Run every hour
invitation_scheduler.start()
