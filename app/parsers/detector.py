from app.parsers.mailerlite import parse_mailerlite

def detect_and_parse(text: str):
    if 'Campaign report' in text and 'Campaign results' in text:
        return parse_mailerlite(text)

    raise ValueError("Unsupported or unrecognized report format")
