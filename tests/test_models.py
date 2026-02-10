"""Unit tests for EmailCampaign model"""
import pytest
from app.models import EmailCampaign, ParseError, InvalidCampaignError, EmptyReportError


class TestEmailCampaign:
    """Test EmailCampaign class"""
    
    def test_campaign_initialization(self):
        """Test basic campaign initialization"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test Subject",
            email_title="Test Title",
            unique_id="test123",
            sent_at="2021-01-01 10:00:00",
            delivered=1000,
            opens=300,
            open_rate=0.30,
            clicks=50,
            click_rate=0.05,
            ctor=0.1667,
            unsubscribes=5,
            unsubscribe_rate=0.005
        )
        
        assert campaign.platform == "mailchimp"
        assert campaign.subject == "Test Subject"
        assert campaign.delivered == 1000
        assert campaign.opens == 300
    
    def test_campaign_to_dict(self):
        """Test conversion to dictionary"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test",
            unique_id="123"
        )
        
        result = campaign.to_dict()
        
        assert isinstance(result, dict)
        assert result["platform"] == "mailchimp"
        assert result["subject"] == "Test"
        assert result["unique_id"] == "123"
        assert "delivered" in result
    
    def test_has_meaningful_data_with_all_fields(self):
        """Test has_meaningful_data returns True when all required fields present"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test",
            email_title="Test Title",
            unique_id="123",
            sent_at="2021-01-01",
            delivered=100,
            opens=30,
            open_rate=0.30,
            clicks=10,
            click_rate=0.10
        )
        
        assert campaign.has_meaningful_data() is True
    
    def test_has_meaningful_data_missing_required_fields(self):
        """Test has_meaningful_data returns False when required fields missing"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test",
            email_title="Test Title"
        )
        
        assert campaign.has_meaningful_data() is False
    
    def test_has_meaningful_data_empty_strings(self):
        """Test has_meaningful_data returns False for empty string fields"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="",  # Empty string
            email_title="Test Title",
            unique_id="123",
            sent_at="2021-01-01",
            delivered=100,
            opens=30,
            open_rate=0.30,
            clicks=10,
            click_rate=0.10
        )
        
        assert campaign.has_meaningful_data() is False
    
    def test_has_meaningful_data_zero_delivered(self):
        """Test has_meaningful_data returns False when delivered is 0"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test",
            email_title="Test Title",
            unique_id="123",
            sent_at="2021-01-01",
            delivered=0,  # Zero delivered
            opens=0,
            open_rate=0.0,
            clicks=0,
            click_rate=0.0
        )
        
        assert campaign.has_meaningful_data() is False
    
    def test_has_meaningful_data_partial_fields(self):
        """Test has_meaningful_data with partial required fields"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="Test",
            email_title="Test Title",
            unique_id="123",
            sent_at="2021-01-01",
            delivered=100
        )
        
        assert campaign.has_meaningful_data() is False
    
    def test_campaign_repr(self):
        """Test string representation"""
        campaign = EmailCampaign(
            platform="mailchimp",
            subject="This is a very long subject line that should be truncated"
        )
        
        repr_str = repr(campaign)
        assert "EmailCampaign" in repr_str
        assert "mailchimp" in repr_str


class TestParseErrors:
    """Test custom error classes"""
    
    def test_parse_error_basic(self):
        """Test ParseError initialization"""
        error = ParseError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.filename is None
    
    def test_parse_error_with_filename(self):
        """Test ParseError with filename"""
        error = ParseError("Test error", filename="test.csv")
        assert error.message == "Test error"
        assert error.filename == "test.csv"
    
    def test_invalid_campaign_error(self):
        """Test InvalidCampaignError inheritance"""
        error = InvalidCampaignError("Invalid data")
        assert isinstance(error, ParseError)
        assert str(error) == "Invalid data"
    
    def test_empty_report_error(self):
        """Test EmptyReportError inheritance"""
        error = EmptyReportError("No data")
        assert isinstance(error, ParseError)
        assert str(error) == "No data"
