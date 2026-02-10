from abc import ABC, abstractmethod
from typing import List
from app.models import EmailCampaign


class BaseParser(ABC):
    """Abstract base parser for email campaign reports"""
    
    @abstractmethod
    def parse(self, text: str) -> List[EmailCampaign]:
        """Parse report text and return list of EmailCampaign instances"""
        pass
    
    @abstractmethod
    def can_parse(self, text: str) -> bool:
        """Check if this parser can handle the given text"""
        pass
