import re
from typing import List
from app.utils.id_generator import generate_unique_id
from app.models import EmailCampaign, EmptyReportError
from app.parsers.base_parser import BaseParser

def parse_kv(line: str):
    """Parse key-value pair from CSV format like '"Title:","Personal Styling (Amy 02)"'"""
    parts = [p.strip().strip('"') for p in line.split('","') if p.strip()]
    if len(parts) >= 2:
        key = parts[0].strip(':').strip()
        value = parts[1].strip()
        return key, value
    return None, None


def extract_number_and_percent(value: str):
    """Extract number and percentage from strings like '1 (100.0%)'"""
    if not value:
        return None, None
    
    # Extract main number
    num_match = re.search(r'([\d,]+)', value)
    num = int(num_match.group(1).replace(',', '')) if num_match else None
    
    # Extract percentage
    pct_match = re.search(r'\(([\d.]+)%\)', value)
    pct = float(pct_match.group(1)) / 100 if pct_match else None
    
    return num, pct


def sanitize_title(subject: str) -> str:
    """Remove special characters from subject line to create a clean title."""
    if not subject:
        return "Untitled"
    cleaned = re.sub(r'[^\w\s\-.,!?]', '', subject)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if cleaned else "Untitled"


class MailChimpParser(BaseParser):
    """Parser for MailChimp individual single campaign reports"""
    
    def can_parse(self, text: str) -> bool:
        """Check if text is a MailChimp single campaign report"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return any("Email Campaign Report" in line for line in lines[:5]) and \
               any("Overall Stats" in line for line in lines[:20])
    
    def parse(self, text: str) -> List[EmailCampaign]:
        """Parse MailChimp individual single campaign report"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        
        subject = None
        email_title = None
        sent_at = None
        delivered = None
        opens = None
        open_rate = None
        clicks = None
        click_rate = None
        unsubscribes = None
        unsubscribe_rate = None
        spam_complaints = None
        bounces = None
        bounce_rate = None
        ctor = None
        
        campaign_title = None
        
        for line in lines:
            if line.startswith('"Clicks by URL"') or line.startswith('"URL"'):
                break
                
            key, val = parse_kv(line)
            
            if not key:
                continue
            
            if key == "Title":
                campaign_title = val
            elif key == "Subject Line":
                subject = val
            elif key == "Delivery Date/Time":
                sent_at = val
            elif key == "Successful Deliveries":
                delivered = int(val.replace(',', ''))
            elif key == "Recipients Who Opened":
                num, pct = extract_number_and_percent(val)
                opens = num
                open_rate = pct
            elif key == "Recipients Who Clicked":
                num, pct = extract_number_and_percent(val)
                clicks = num
                click_rate = pct
            elif key == "Total Unsubs":
                unsubscribes = int(val.replace(',', '')) if val != "0" else 0
            elif key == "Total Abuse Complaints":
                spam_complaints = int(val.replace(',', '')) if val != "0" else 0
            elif key == "Bounces":
                num, pct = extract_number_and_percent(val)
                bounces = num
                bounce_rate = pct
        
        if opens and clicks and opens > 0:
            ctor = clicks / opens
        
        if delivered and unsubscribes is not None and delivered > 0:
            unsubscribe_rate = unsubscribes / delivered
        
        title = sanitize_title(campaign_title or subject or "")
        email_title = title
        
        unique_id = generate_unique_id(
            title=title,
            subject=subject or "",
            sent_at=sent_at or "",
            platform="mailchimp"
        )
        
        campaign = EmailCampaign(
            platform="mailchimp",
            subject=subject,
            email_title=email_title,
            unique_id=unique_id,
            sent_at=sent_at,
            delivered=delivered,
            opens=opens,
            open_rate=open_rate,
            clicks=clicks,
            click_rate=click_rate,
            ctor=ctor,
            unsubscribes=unsubscribes,
            unsubscribe_rate=unsubscribe_rate,
            spam_complaints=spam_complaints,
            bounces=bounces,
            bounce_rate=bounce_rate,
            hard_bounces=None,
            hard_bounce_rate=None,
            soft_bounces=None,
            soft_bounce_rate=None,
        )
        
        if not campaign.has_meaningful_data():
            raise EmptyReportError("Campaign data incomplete or missing key metrics")
        
        return [campaign]


def parse_mailchimp(text: str):
    """Legacy function for backward compatibility"""
    parser = MailChimpParser()
    campaigns = parser.parse(text)
    return {"campaigns": [c.to_dict() for c in campaigns]}
