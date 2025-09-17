"""
Basic notification service for MVP
In production, this would integrate with SMS services like Twilio
"""
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

# Setup logging for notifications
logging.basicConfig(level=logging.INFO)
notification_logger = logging.getLogger("notifications")

class NotificationService:
    def __init__(self):
        self.enabled = True
        
    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Mock SMS sending for MVP
        In production, integrate with Twilio or similar service
        """
        if not self.enabled:
            return False
            
        try:
            # For MVP, just log the SMS
            notification_logger.info(f"📱 SMS to {phone_number}: {message}")
            print(f"📱 SMS NOTIFICATION")
            print(f"   To: {phone_number}")
            print(f"   Message: {message}")
            print(f"   Time: {datetime.now()}")
            print("-" * 50)
            return True
        except Exception as e:
            notification_logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            return False
    
    def notify_issue_created(self, user_phone: str, issue_title: str, issue_id: int):
        """Notify user that their issue has been created"""
        message = f"Your issue '{issue_title[:50]}...' has been submitted successfully. Issue ID: #{issue_id}. You will receive updates on progress."
        return self.send_sms(user_phone, message)
    
    def notify_issue_assigned(self, user_phone: str, issue_title: str, department_name: str, worker_name: str):
        """Notify user that their issue has been assigned"""
        message = f"Your issue '{issue_title[:30]}...' has been assigned to {worker_name} from {department_name}. Work will begin soon."
        return self.send_sms(user_phone, message)
    
    def notify_issue_status_update(self, user_phone: str, issue_title: str, new_status: str):
        """Notify user of issue status change"""
        status_messages = {
            "assigned": "has been assigned to a worker",
            "in_progress": "work has started",
            "resolved": "has been resolved",
            "rejected": "has been reviewed and rejected"
        }
        
        status_text = status_messages.get(new_status, f"status has been updated to {new_status}")
        message = f"Update: Your issue '{issue_title[:40]}...' {status_text}. Thank you for using Nagar Mitra."
        return self.send_sms(user_phone, message)
    
    def notify_worker_assignment(self, worker_phone: str, issue_title: str, issue_id: int, user_address: str):
        """Notify worker about new assignment"""
        message = f"New assignment: Issue #{issue_id} - '{issue_title[:40]}...' at {user_address[:50]}. Please review and begin work."
        return self.send_sms(worker_phone, message)
    
    def notify_admin_new_issue(self, admin_phone: str, issue_title: str, issue_id: int, needs_review: bool):
        """Notify admin about new issue requiring attention"""
        if needs_review:
            message = f"New issue #{issue_id} needs manual review: '{issue_title[:40]}...'. Please assign to appropriate department."
        else:
            message = f"New issue #{issue_id} auto-assigned: '{issue_title[:40]}...'"
        
        return self.send_sms(admin_phone, message)

# Global notification service instance
notification_service = NotificationService()

def get_notification_service() -> NotificationService:
    """Get notification service instance"""
    return notification_service

def send_issue_notifications(db: Session, issue, event_type: str):
    """
    Send appropriate notifications based on issue events
    """
    try:
        if event_type == "created":
            # Notify user
            notification_service.notify_issue_created(
                issue.user.mobile_number,
                issue.title,
                issue.id
            )
            
            # Notify admin if needs review
            if issue.needs_manual_review:
                # In a real app, you'd have admin phone numbers in config
                admin_phone = "+919999999999"  # From sample data
                notification_service.notify_admin_new_issue(
                    admin_phone,
                    issue.title,
                    issue.id,
                    True
                )
        
        elif event_type == "assigned" and issue.worker:
            # Notify user
            notification_service.notify_issue_assigned(
                issue.user.mobile_number,
                issue.title,
                issue.department.name,
                issue.worker.name
            )
            
            # Notify worker
            notification_service.notify_worker_assignment(
                issue.worker.mobile_number,
                issue.title,
                issue.id,
                issue.user.address or "Address not provided"
            )
        
        elif event_type == "status_updated":
            # Notify user of status change
            notification_service.notify_issue_status_update(
                issue.user.mobile_number,
                issue.title,
                issue.status
            )
            
    except Exception as e:
        notification_logger.error(f"Error sending notifications for issue {issue.id}: {str(e)}")

def setup_production_sms():
    """
    Setup production SMS service (Twilio, etc.)
    This would be called in production with proper configuration
    """
    # Example for Twilio integration:
    # from twilio.rest import Client
    # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    # client = Client(account_sid, auth_token)
    pass