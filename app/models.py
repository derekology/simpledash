from typing import Optional
from datetime import datetime


class EmailCampaign:
    """Represents a single email campaign with metrics"""
    
    def __init__(
        self,
        platform: str,
        subject: Optional[str] = None,
        email_title: Optional[str] = None,
        unique_id: Optional[str] = None,
        sent_at: Optional[str] = None,
        delivered: Optional[int] = None,
        opens: Optional[int] = None,
        open_rate: Optional[float] = None,
        clicks: Optional[int] = None,
        click_rate: Optional[float] = None,
        ctor: Optional[float] = None,
        unsubscribes: Optional[int] = None,
        unsubscribe_rate: Optional[float] = None,
        spam_complaints: Optional[int] = None,
        bounces: Optional[int] = None,
        bounce_rate: Optional[float] = None,
        hard_bounces: Optional[int] = None,
        hard_bounce_rate: Optional[float] = None,
        soft_bounces: Optional[int] = None,
        soft_bounce_rate: Optional[float] = None,
    ):
        self.platform = platform
        self.subject = subject
        self.email_title = email_title
        self.unique_id = unique_id
        self.sent_at = sent_at
        self.delivered = delivered
        self.opens = opens
        self.open_rate = open_rate
        self.clicks = clicks
        self.click_rate = click_rate
        self.ctor = ctor
        self.unsubscribes = unsubscribes
        self.unsubscribe_rate = unsubscribe_rate
        self.spam_complaints = spam_complaints
        self.bounces = bounces
        self.bounce_rate = bounce_rate
        self.hard_bounces = hard_bounces
        self.hard_bounce_rate = hard_bounce_rate
        self.soft_bounces = soft_bounces
        self.soft_bounce_rate = soft_bounce_rate
    
    def to_dict(self) -> dict:
        """Convert campaign to dictionary for JSON serialization"""
        return {
            "platform": self.platform,
            "subject": self.subject,
            "email_title": self.email_title,
            "unique_id": self.unique_id,
            "sent_at": self.sent_at,
            "delivered": self.delivered,
            "opens": self.opens,
            "open_rate": self.open_rate,
            "clicks": self.clicks,
            "click_rate": self.click_rate,
            "ctor": self.ctor,
            "unsubscribes": self.unsubscribes,
            "unsubscribe_rate": self.unsubscribe_rate,
            "spam_complaints": self.spam_complaints,
            "bounces": self.bounces,
            "bounce_rate": self.bounce_rate,
            "hard_bounces": self.hard_bounces,
            "hard_bounce_rate": self.hard_bounce_rate,
            "soft_bounces": self.soft_bounces,
            "soft_bounce_rate": self.soft_bounce_rate,
        }
    
    def has_meaningful_data(self) -> bool:
        """Check if campaign has all required fields populated with meaningful values"""
        # Check required fields exist and are not None
        required_fields = [
            self.platform,
            self.subject,
            self.email_title,
            self.unique_id,
            self.sent_at,
            self.delivered,
            self.opens,
            self.open_rate,
            self.clicks,
            self.click_rate,
        ]
        
        if not all(field is not None for field in required_fields):
            return False
        
        # Check string fields are not empty (including whitespace-only strings)
        if not self.subject or (isinstance(self.subject, str) and not self.subject.strip()):
            return False
        if not self.email_title or (isinstance(self.email_title, str) and not self.email_title.strip()):
            return False
        if not self.sent_at or (isinstance(self.sent_at, str) and not str(self.sent_at).strip()):
            return False
        
        # Check numeric fields are meaningful (not just zeros)
        # At least delivered should be > 0 for a real campaign
        if not isinstance(self.delivered, (int, float)) or self.delivered <= 0:
            return False
        
        return True
    
    def __repr__(self):
        return f"EmailCampaign(platform={self.platform}, subject={self.subject[:30] if self.subject else None}...)"


class ParseError(Exception):
    """Base class for parsing errors"""
    
    def __init__(self, message: str, filename: Optional[str] = None):
        self.message = message
        self.filename = filename
        super().__init__(self.message)


class InvalidCampaignError(ParseError):
    """Raised when campaign data is invalid or missing required fields"""
    pass


class EmptyReportError(ParseError):
    """Raised when report contains no data"""
    pass


class UnsupportedFormatError(ParseError):
    """Raised when report format is not recognized"""
    pass


class InvalidFileError(ParseError):
    """Raised when file cannot be processed"""
    pass
