"""Unit tests for ParserFactory and detector"""
import pytest
from app.utils.detector import ParserFactory, detect_and_parse
from app.parsers.mailerlite_classic import MailerLiteClassicParser
from app.parsers.mailchimp import MailChimpParser
from app.parsers.mailchimp_ab import MailChimpABParser
from app.parsers.mailchimp_aggregated import MailChimpAggregatedParser
from app.models import UnsupportedFormatError, EmailCampaign
from tests.fixtures import (
    MAILERLITE_CLASSIC_SAMPLE,
    MAILCHIMP_SINGLE_SAMPLE,
    MAILCHIMP_AB_SAMPLE,
    MAILCHIMP_AGGREGATED_SAMPLE,
    INVALID_FORMAT
)


class TestParserFactory:
    """Test ParserFactory singleton and functionality"""
    
    def test_singleton_pattern(self):
        """Test ParserFactory is a singleton"""
        factory1 = ParserFactory()
        factory2 = ParserFactory()
        
        assert factory1 is factory2
    
    def test_factory_has_all_parsers(self):
        """Test factory initializes with all parser types"""
        factory = ParserFactory()
        
        assert len(factory.parsers) == 4
        assert any(isinstance(p, MailerLiteClassicParser) for p in factory.parsers)
        assert any(isinstance(p, MailChimpParser) for p in factory.parsers)
        assert any(isinstance(p, MailChimpABParser) for p in factory.parsers)
        assert any(isinstance(p, MailChimpAggregatedParser) for p in factory.parsers)
    
    def test_get_parser_mailerlite(self):
        """Test factory returns correct parser for MailerLite"""
        factory = ParserFactory()
        parser = factory.get_parser(MAILERLITE_CLASSIC_SAMPLE)
        
        assert isinstance(parser, MailerLiteClassicParser)
    
    def test_get_parser_mailchimp_single(self):
        """Test factory returns correct parser for MailChimp single"""
        factory = ParserFactory()
        parser = factory.get_parser(MAILCHIMP_SINGLE_SAMPLE)
        
        assert isinstance(parser, MailChimpParser)
    
    def test_get_parser_mailchimp_ab(self):
        """Test factory returns correct parser for MailChimp A/B"""
        factory = ParserFactory()
        parser = factory.get_parser(MAILCHIMP_AB_SAMPLE)
        
        assert isinstance(parser, MailChimpABParser)
    
    def test_get_parser_mailchimp_aggregated(self):
        """Test factory returns correct parser for MailChimp aggregated"""
        factory = ParserFactory()
        parser = factory.get_parser(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert isinstance(parser, MailChimpAggregatedParser)
    
    def test_get_parser_unsupported_format(self):
        """Test factory raises error for unsupported format"""
        factory = ParserFactory()
        
        with pytest.raises(UnsupportedFormatError) as exc_info:
            factory.get_parser(INVALID_FORMAT)
        
        assert "Unsupported or unrecognized report format" in str(exc_info.value)
    
    def test_parser_order_priority(self):
        """Test parsers are checked in correct priority order"""
        factory = ParserFactory()
        
        # A/B parser should come before single campaign parser
        ab_index = next(i for i, p in enumerate(factory.parsers) if isinstance(p, MailChimpABParser))
        single_index = next(i for i, p in enumerate(factory.parsers) if isinstance(p, MailChimpParser))
        
        assert ab_index < single_index, "A/B parser should be checked before single campaign parser"


class TestDetectAndParse:
    """Test detect_and_parse function"""
    
    def test_detect_and_parse_mailerlite(self):
        """Test detect_and_parse with MailerLite report"""
        campaigns = detect_and_parse(MAILERLITE_CLASSIC_SAMPLE)
        
        assert len(campaigns) == 1
        assert isinstance(campaigns[0], EmailCampaign)
        assert campaigns[0].platform == "mailerlite_classic"
    
    def test_detect_and_parse_mailchimp_single(self):
        """Test detect_and_parse with MailChimp single report"""
        campaigns = detect_and_parse(MAILCHIMP_SINGLE_SAMPLE)
        
        assert len(campaigns) == 1
        assert isinstance(campaigns[0], EmailCampaign)
        assert campaigns[0].platform == "mailchimp"
    
    def test_detect_and_parse_mailchimp_ab(self):
        """Test detect_and_parse with MailChimp A/B report"""
        campaigns = detect_and_parse(MAILCHIMP_AB_SAMPLE)
        
        assert len(campaigns) == 2
        assert all(isinstance(c, EmailCampaign) for c in campaigns)
        assert all(c.platform == "mailchimp_ab" for c in campaigns)
    
    def test_detect_and_parse_mailchimp_aggregated(self):
        """Test detect_and_parse with MailChimp aggregated report"""
        campaigns = detect_and_parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert len(campaigns) == 3
        assert all(isinstance(c, EmailCampaign) for c in campaigns)
        assert all(c.platform == "mailchimp_aggregated" for c in campaigns)
    
    def test_detect_and_parse_unsupported(self):
        """Test detect_and_parse raises error for unsupported format"""
        with pytest.raises(UnsupportedFormatError):
            detect_and_parse(INVALID_FORMAT)
    
    def test_detect_and_parse_returns_list(self):
        """Test detect_and_parse always returns a list"""
        campaigns = detect_and_parse(MAILERLITE_CLASSIC_SAMPLE)
        
        assert isinstance(campaigns, list)
    
    def test_detect_and_parse_campaigns_have_data(self):
        """Test all returned campaigns have meaningful data"""
        campaigns = detect_and_parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert all(c.has_meaningful_data() for c in campaigns)
