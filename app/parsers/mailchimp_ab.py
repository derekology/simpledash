import re
from typing import List
from datetime import datetime
from app.utils.id_generator import generate_unique_id
from app.models import EmailCampaign, EmptyReportError
from app.parsers.base_parser import BaseParser

def parse_kv(line: str):
    """Parse key-value pair from CSV format like '"Title:","COVERUP-29-04-2021"'"""
    parts = [p.strip().strip('"') for p in line.split('","') if p.strip()]
    if len(parts) >= 2:
        key = parts[0].strip(':').strip()
        value = parts[1].strip()
        return key, value
    return None, None


def extract_number_and_percent(value: str):
    """Extract number and percentage from strings like '141 (8.1%)'"""
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


def parse_combination(lines, start_idx):
    """Parse a single combination's stats from the lines"""
    data = {
        "subject": None,
        "sent_at": None,
        "delivered": None,
        "opens": None,
        "open_rate": None,
        "clicks": None,
        "click_rate": None,
        "unsubscribes": None,
        "unsubscribe_rate": None,
        "spam_complaints": None,
        "bounces": None,
        "bounce_rate": None,
    }
    
    idx = start_idx
    while idx < len(lines):
        line = lines[idx].strip()
        
        # Stop if we hit next combination or clicks section
        if line.startswith('"Combination') or line.startswith('"URL"'):
            break
            
        key, val = parse_kv(line)
        
        if key == "Subject Line":
            data["subject"] = val
        elif key == "Successful Deliveries":
            data["delivered"] = int(val.replace(',', ''))
        elif key == "Recipients Who Opened":
            num, pct = extract_number_and_percent(val)
            data["opens"] = num
            data["open_rate"] = pct
        elif key == "Recipients Who Clicked":
            num, pct = extract_number_and_percent(val)
            data["clicks"] = num
            data["click_rate"] = pct
        elif key == "Total Unsubs":
            data["unsubscribes"] = int(val.replace(',', '')) if val != "0" else 0
        elif key == "Total Abuse Complaints":
            data["spam_complaints"] = int(val.replace(',', '')) if val != "0" else 0
        elif key == "Bounces":
            num, pct = extract_number_and_percent(val)
            data["bounces"] = num
            data["bounce_rate"] = pct
        
        idx += 1
    
    # Calculate CTOR if we have data
    if data["opens"] and data["clicks"] and data["opens"] > 0:
        data["ctor"] = data["clicks"] / data["opens"]
    else:
        data["ctor"] = None
    
    # Calculate unsubscribe rate if we have delivered count
    if data["delivered"] and data["unsubscribes"] is not None and data["delivered"] > 0:
        data["unsubscribe_rate"] = data["unsubscribes"] / data["delivered"]
    else:
        data["unsubscribe_rate"] = None
    
    return data, idx


class MailChimpABParser(BaseParser):
    """Parser for MailChimp A/B test campaign reports"""
    
    def can_parse(self, text: str) -> bool:
        """Check if text is a MailChimp A/B test campaign report"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return any("Campaign Report" in line for line in lines[:5]) and \
               any("Combination" in line and "Stats" in line for line in lines[:20])
    
    def parse(self, text: str) -> List[EmailCampaign]:
        """Parse MailChimp individual campaign report (A/B test or single campaign)"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        
        campaign_title = None
        delivery_date = None
        
        for i, line in enumerate(lines):
            key, val = parse_kv(line)
            if key == "Title":
                campaign_title = val
            elif key == "Delivery Date/Time":
                delivery_date = val
        
        campaigns = []
        i = 0
        combination_num = 1
        
        while i < len(lines):
            line = lines[i]
            
            if line.startswith('"Combination') and 'Stats' in line:
                combo_data, next_idx = parse_combination(lines, i + 1)
                
                email_title = f"{campaign_title} - Combo {combination_num}" if campaign_title else f"{sanitize_title(combo_data['subject'])} {combination_num}"
                
                unique_id = generate_unique_id(
                    title=campaign_title or "",
                    subject=combo_data.get('subject', ''),
                    sent_at=f"{delivery_date}_{combination_num}" if delivery_date else f"combo_{combination_num}",
                    platform="mailchimp"
                )
                
                campaign = EmailCampaign(
                    platform="mailchimp_ab",
                    subject=combo_data.get('subject'),
                    email_title=email_title,
                    unique_id=unique_id,
                    sent_at=delivery_date,
                    delivered=combo_data.get('delivered'),
                    opens=combo_data.get('opens'),
                    open_rate=combo_data.get('open_rate'),
                    clicks=combo_data.get('clicks'),
                    click_rate=combo_data.get('click_rate'),
                    ctor=combo_data.get('ctor'),
                    unsubscribes=combo_data.get('unsubscribes'),
                    unsubscribe_rate=combo_data.get('unsubscribe_rate'),
                    spam_complaints=combo_data.get('spam_complaints'),
                    bounces=combo_data.get('bounces'),
                    bounce_rate=combo_data.get('bounce_rate'),
                    hard_bounces=None,
                    hard_bounce_rate=None,
                    soft_bounces=None,
                    soft_bounce_rate=None,
                )
                
                if campaign.has_meaningful_data():
                    campaigns.append(campaign)
                    
                combination_num += 1
                i = next_idx
            else:
                i += 1
        
        if not campaigns:
            raise EmptyReportError("No combinations found in A/B test report")
        
        return campaigns


def parse_mailchimp_ab(text: str):
    """Legacy function for backward compatibility"""
    parser = MailChimpABParser()
    campaigns = parser.parse(text)
    return {"campaigns": [c.to_dict() for c in campaigns]}
