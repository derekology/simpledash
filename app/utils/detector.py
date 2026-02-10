from typing import List
from app.parsers.mailerlite_classic import MailerLiteClassicParser
from app.parsers.mailchimp_ab import MailChimpABParser
from app.parsers.mailchimp import MailChimpParser
from app.parsers.mailchimp_aggregated import MailChimpAggregatedParser
from app.models import EmailCampaign, UnsupportedFormatError


class ParserFactory:
    """Singleton factory for selecting appropriate parser based on report format"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParserFactory, cls).__new__(cls)
            cls._instance.parsers = [
                MailChimpABParser(),
                MailChimpParser(),
                MailChimpAggregatedParser(),
                MailerLiteClassicParser(),
            ]
        return cls._instance
    
    def get_parser(self, text: str):
        """Detect and return appropriate parser for the given text"""
        for parser in self.parsers:
            if parser.can_parse(text):
                return parser
        raise UnsupportedFormatError("Unsupported or unrecognized report format")


def detect_and_parse(text: str) -> List[EmailCampaign]:
    """Detect the platform and parse accordingly, returning EmailCampaign instances"""
    factory = ParserFactory()
    parser = factory.get_parser(text)
    return parser.parse(text)
