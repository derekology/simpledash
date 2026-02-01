import re

def parse_kv(line: str):
    parts = [p.strip().strip('"') for p in line.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None


def extract_number_and_percent(value: str):
    if not value:
        return None, None
    
    num_match = re.search(r"([\d,]+)", value)
    pct_match = re.search(r"\(([\d.]+)%\)", value)

    num = int(num_match.group(1).replace(",", "")) if num_match else None
    pct = float(pct_match.group(1)) / 100 if pct_match else None

    return num, pct


def parse_mailerlite(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    section = None

    data = {
        "platform": "mailerlite",
        "subject": None,
        "sent_at": None,
        "delivered": None,
        "opens": None,
        "open_rate": None,
        "clicks": None,
        "click_rate": None,
        "unsubscribes": None,
        "spam_complaints": None,
        "hard_bounces": None,
        "soft_bounces": None,
    }

    for line in lines:
        print(line)
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
                data["subject"] = val
            elif key == "Sent":
                data["sent_at"] = val

        elif section == "campaign_results":
            key, val = parse_kv(line)
            if key == "Total emails sent:":
                data["delivered"] = int(val.replace(",", ""))
            elif key == "Opened:":
                num, pct = extract_number_and_percent(val)
                data["opens"] = num
                data["open_rate"] = pct
            elif key == "Clicked:":
                num, pct = extract_number_and_percent(val)
                data["clicks"] = num
                data["click_rate"] = pct

        elif section == "bad_statistics":
            key, val = parse_kv(line)
            num, _ = extract_number_and_percent(val)
            if key == "Unsubscribed:":
                data["unsubscribes"] = num
            elif key == "Spam complaints:":
                data["spam_complaints"] = num
            elif key == "Hard bounce:":
                data["hard_bounces"] = num
            elif key == "Soft bounce:":
                data["soft_bounces"] = num

    if data["opens"] and data["clicks"]:
        data["ctor"] = data["clicks"] / data["opens"]
    else:
        data["ctor"] = None

    return {
        "campaign": data
    }
