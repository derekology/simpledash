import re
from typing import List
from app.utils.id_generator import generate_unique_id
from app.models import EmailCampaign, EmptyReportError
from app.parsers.base_parser import BaseParser

def parse_kv(line: str):
    parts = [p.strip().strip('"') for p in line.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None


def extract_number_and_percent(value: str):
    """Extract numeric value and percentage from a string like "1,234 (56.7%)"""
    if not value:
        return None, None
    
    num_match = re.search(r"([\d,]+)", value)
    pct_match = re.search(r"\(([\d.]+)%\)", value)

    num = int(num_match.group(1).replace(",", "")) if num_match else None
    pct = float(pct_match.group(1)) / 100 if pct_match else None

    return num, pct


def sanitize_title(subject: str) -> str:
    """Remove special characters from subject line to create a clean title."""
    if not subject:
        return "Untitled"
    cleaned = re.sub(r'[^\w\s\-.,!?]', '', subject)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if cleaned else "Untitled"


class MailerLiteClassicParser(BaseParser):
    """Parser for MailerLite Classic campaign reports"""
    
    def can_parse(self, text: str) -> bool:
        """Check if text is a MailerLite Classic report"""
        return 'Campaign report' in text and 'Campaign results' in text
    
    def parse(self, text: str) -> List[EmailCampaign]:
        """Parse MailerLite Classic campaign report"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        if not lines:
            raise EmptyReportError("Empty report")

        section = None

        subject = None
        sent_at = None
        delivered = None
        opens = None
        open_rate = None
        clicks = None
        click_rate = None
        unsubscribes = None
        unsubscribe_rate = None
        spam_complaints = None
        hard_bounces = None
        hard_bounce_rate = None
        soft_bounces = None
        soft_bounce_rate = None

        for line in lines:
            if line == 'Campaign report':
                section = "campaign_report"
                continue
            elif line == '"Campaign results"':
                section = "campaign_results"
                continue
            elif line == '"Bad statistics"':
                section = "bad_statistics"
                continue
            elif line == '"Links activity"':
                section = "links_activity"
                continue

            if section == "campaign_report":
                key, val = parse_kv(line)
                if key == "Subject:":
                    subject = val
                elif key == "Sent":
                    sent_at = val

            elif section == "campaign_results":
                key, val = parse_kv(line)
                if key == "Total emails sent:":
                    delivered = int(val.replace(",", ""))
                elif key == "Opened:":
                    num, pct = extract_number_and_percent(val)
                    opens = num
                    open_rate = pct
                elif key == "Clicked:":
                    num, pct = extract_number_and_percent(val)
                    clicks = num
                    click_rate = pct

            elif section == "bad_statistics":
                key, val = parse_kv(line)
                num, pct = extract_number_and_percent(val)
                if key == "Unsubscribed:":
                    unsubscribes = num
                    unsubscribe_rate = pct
                elif key == "Spam complaints:":
                    spam_complaints = num
                elif key == "Hard bounce:":
                    hard_bounces = num
                    hard_bounce_rate = pct
                elif key == "Soft bounce:":
                    soft_bounces = num
                    soft_bounce_rate = pct

        if opens and clicks:
            ctor = clicks / opens
        else:
            ctor = None

        title = sanitize_title(subject or "")
        
        unique_id = generate_unique_id(
            title=title,
            subject=subject or "",
            sent_at=sent_at or "",
            platform="mailerlite"
        )
        
        campaign = EmailCampaign(
            platform="mailerlite_classic",
            subject=subject,
            email_title=title,
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
            bounces=None,
            bounce_rate=None,
            hard_bounces=hard_bounces,
            hard_bounce_rate=hard_bounce_rate,
            soft_bounces=soft_bounces,
            soft_bounce_rate=soft_bounce_rate,
        )
        
        if not campaign.has_meaningful_data():
            raise EmptyReportError("Campaign data incomplete or missing key metrics")

        return [campaign]


def parse_mailerlite_classic(text: str):
    """Legacy function for backward compatibility"""
    parser = MailerLiteClassicParser()
    campaigns = parser.parse(text)
    return {"campaigns": [c.to_dict() for c in campaigns]}
