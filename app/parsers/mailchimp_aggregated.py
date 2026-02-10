import csv
from io import StringIO
from typing import List
from datetime import datetime
from app.utils.id_generator import generate_unique_id, normalize_datetime
from app.models import EmailCampaign, EmptyReportError
from app.parsers.base_parser import BaseParser


class MailChimpAggregatedParser(BaseParser):
    """Parser for aggregated MailChimp CSV campaign reports"""
    
    def can_parse(self, text: str) -> bool:
        """Check if text is a MailChimp aggregated report"""
        return 'Unique Id' in text and 'Send Date' in text and 'Open Rate' in text
    
    def parse(self, text: str) -> List[EmailCampaign]:
        """Parse aggregated MailChimp CSV campaign report"""
        reader = csv.DictReader(StringIO(text))
        campaigns = []
        
        for row in reader:
            try:
                sent_at_raw = row.get('Send Date', '')
                sent_at = normalize_datetime(sent_at_raw)
                
                delivered = int(row.get('Successful Deliveries', 0))
                
                open_rate_str = row.get('Open Rate', '0%').strip('%')
                open_rate = float(open_rate_str) / 100 if open_rate_str else 0
                
                opens = int(row.get('Unique Opens', 0))
                
                click_rate_str = row.get('Click Rate', '0%').strip('%')
                click_rate = float(click_rate_str) / 100 if click_rate_str else 0
                
                clicks = int(row.get('Unique Clicks', 0))
                
                hard_bounces = int(row.get('Hard Bounces', 0))
                soft_bounces = int(row.get('Soft Bounces', 0))
                
                unsubscribes = int(row.get('Unsubscribes', 0))
                
                spam_complaints = int(row.get('Abuse Complaints', 0))
                
                hard_bounce_rate = hard_bounces / delivered if delivered > 0 else 0
                soft_bounce_rate = soft_bounces / delivered if delivered > 0 else 0
                unsubscribe_rate = unsubscribes / delivered if delivered > 0 else 0
                
                ctor = clicks / opens if opens > 0 else 0
                
                subject = row.get('Subject', '')
                email_title = row.get('Title', '')
                
                unique_id = generate_unique_id(
                    title=email_title,
                    subject=subject,
                    sent_at=sent_at,
                    platform="mailchimp"
                )
                
                campaign = EmailCampaign(
                    platform="mailchimp_aggregated",
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
                    hard_bounces=hard_bounces,
                    hard_bounce_rate=hard_bounce_rate,
                    soft_bounces=soft_bounces,
                    soft_bounce_rate=soft_bounce_rate,
                    bounces=None,
                    bounce_rate=None,
                )
                
                if campaign.has_meaningful_data():
                    campaigns.append(campaign)
                
            except (ValueError, KeyError) as e:
                continue
        
        if not campaigns:
            raise EmptyReportError("No valid campaigns found in aggregated report")
        
        return campaigns


def parse_mailchimp_aggregated(text: str):
    """Legacy function for backward compatibility"""
    parser = MailChimpAggregatedParser()
    campaigns = parser.parse(text)
    return {"campaigns": [c.to_dict() for c in campaigns]}
