"""Unit tests for parser implementations"""
import pytest
from app.parsers.mailerlite_classic import MailerLiteClassicParser
from app.parsers.mailchimp import MailChimpParser
from app.parsers.mailchimp_ab import MailChimpABParser
from app.parsers.mailchimp_aggregated import MailChimpAggregatedParser
from app.models import EmailCampaign, EmptyReportError
from tests.fixtures import (
    MAILERLITE_CLASSIC_SAMPLE,
    MAILCHIMP_SINGLE_SAMPLE,
    MAILCHIMP_AB_SAMPLE,
    MAILCHIMP_AGGREGATED_SAMPLE,
    EMPTY_REPORT,
    INVALID_FORMAT,
    MAILERLITE_INCOMPLETE
)


class TestMailerLiteClassicParser:
    """Test MailerLite Classic parser"""
    
    def test_can_parse_valid_report(self):
        """Test parser recognizes valid MailerLite Classic report"""
        parser = MailerLiteClassicParser()
        assert parser.can_parse(MAILERLITE_CLASSIC_SAMPLE) is True
    
    def test_cannot_parse_invalid_format(self):
        """Test parser rejects invalid format"""
        parser = MailerLiteClassicParser()
        assert parser.can_parse(INVALID_FORMAT) is False
    
    def test_parse_returns_email_campaign(self):
        """Test parser returns EmailCampaign instance"""
        parser = MailerLiteClassicParser()
        campaigns = parser.parse(MAILERLITE_CLASSIC_SAMPLE)
        
        assert len(campaigns) == 1
        assert isinstance(campaigns[0], EmailCampaign)
    
    def test_parse_extracts_correct_data(self):
        """Test parser extracts all data correctly"""
        parser = MailerLiteClassicParser()
        campaigns = parser.parse(MAILERLITE_CLASSIC_SAMPLE)
        campaign = campaigns[0]
        
        assert campaign.platform == "mailerlite_classic"
        assert campaign.subject == "Weekly Newsletter - Product Updates"
        assert campaign.sent_at == "2021-08-07 16:00:00"
        assert campaign.delivered == 3902
        assert campaign.opens == 1489
        assert campaign.open_rate == pytest.approx(0.3891, rel=0.001)
        assert campaign.clicks == 33
        assert campaign.click_rate == pytest.approx(0.0086, rel=0.001)
        assert campaign.unsubscribes == 97
        assert campaign.hard_bounces == 21
        assert campaign.soft_bounces == 54
    
    def test_parse_calculates_ctor(self):
        """Test CTOR calculation"""
        parser = MailerLiteClassicParser()
        campaigns = parser.parse(MAILERLITE_CLASSIC_SAMPLE)
        campaign = campaigns[0]
        
        expected_ctor = 33 / 1489
        assert campaign.ctor == pytest.approx(expected_ctor, rel=0.001)
    
    def test_parse_generates_unique_id(self):
        """Test unique ID generation"""
        parser = MailerLiteClassicParser()
        campaigns = parser.parse(MAILERLITE_CLASSIC_SAMPLE)
        campaign = campaigns[0]
        
        assert campaign.unique_id is not None
        assert len(campaign.unique_id) > 0
    
    def test_parse_empty_report_raises_error(self):
        """Test parser raises error for empty report"""
        parser = MailerLiteClassicParser()
        
        with pytest.raises(EmptyReportError):
            parser.parse(EMPTY_REPORT)
    
    def test_parse_incomplete_report_raises_error(self):
        """Test parser raises error for incomplete report"""
        parser = MailerLiteClassicParser()
        
        with pytest.raises(EmptyReportError):
            parser.parse(MAILERLITE_INCOMPLETE)


class TestMailChimpParser:
    """Test MailChimp single campaign parser"""
    
    def test_can_parse_valid_report(self):
        """Test parser recognizes valid MailChimp report"""
        parser = MailChimpParser()
        assert parser.can_parse(MAILCHIMP_SINGLE_SAMPLE) is True
    
    def test_cannot_parse_invalid_format(self):
        """Test parser rejects invalid format"""
        parser = MailChimpParser()
        assert parser.can_parse(INVALID_FORMAT) is False
    
    def test_parse_returns_email_campaign(self):
        """Test parser returns EmailCampaign instance"""
        parser = MailChimpParser()
        campaigns = parser.parse(MAILCHIMP_SINGLE_SAMPLE)
        
        assert len(campaigns) == 1
        assert isinstance(campaigns[0], EmailCampaign)
    
    def test_parse_extracts_correct_data(self):
        """Test parser extracts all data correctly"""
        parser = MailChimpParser()
        campaigns = parser.parse(MAILCHIMP_SINGLE_SAMPLE)
        campaign = campaigns[0]
        
        assert campaign.platform == "mailchimp"
        assert campaign.subject == "Get 20% Off Today Only!"
        assert campaign.delivered == 995
        assert campaign.opens == 350
        assert campaign.open_rate == pytest.approx(0.3518, rel=0.001)
        assert campaign.clicks == 100
        assert campaign.click_rate == pytest.approx(0.1005, rel=0.001)
        assert campaign.unsubscribes == 5
    
    def test_parse_calculates_ctor(self):
        """Test CTOR calculation"""
        parser = MailChimpParser()
        campaigns = parser.parse(MAILCHIMP_SINGLE_SAMPLE)
        campaign = campaigns[0]
        
        expected_ctor = 100 / 350
        assert campaign.ctor == pytest.approx(expected_ctor, rel=0.001)
    
    def test_parse_calculates_unsubscribe_rate(self):
        """Test unsubscribe rate calculation"""
        parser = MailChimpParser()
        campaigns = parser.parse(MAILCHIMP_SINGLE_SAMPLE)
        campaign = campaigns[0]
        
        expected_rate = 5 / 995
        assert campaign.unsubscribe_rate == pytest.approx(expected_rate, rel=0.001)


class TestMailChimpABParser:
    """Test MailChimp A/B test parser"""
    
    def test_can_parse_valid_report(self):
        """Test parser recognizes valid A/B test report"""
        parser = MailChimpABParser()
        assert parser.can_parse(MAILCHIMP_AB_SAMPLE) is True
    
    def test_cannot_parse_invalid_format(self):
        """Test parser rejects invalid format"""
        parser = MailChimpABParser()
        assert parser.can_parse(INVALID_FORMAT) is False
    
    def test_parse_returns_multiple_campaigns(self):
        """Test parser returns multiple campaigns for A/B test"""
        parser = MailChimpABParser()
        campaigns = parser.parse(MAILCHIMP_AB_SAMPLE)
        
        assert len(campaigns) == 2
        assert all(isinstance(c, EmailCampaign) for c in campaigns)
    
    def test_parse_extracts_both_combinations(self):
        """Test parser extracts both A/B combinations"""
        parser = MailChimpABParser()
        campaigns = parser.parse(MAILCHIMP_AB_SAMPLE)
        
        combo1 = campaigns[0]
        combo2 = campaigns[1]
        
        assert combo1.subject == "Spring Sale - Up to 30% Off"
        assert combo2.subject == "Limited Time - Spring Savings Event"
        
        assert combo1.delivered == 1742
        assert combo2.delivered == 1742
    
    def test_parse_generates_unique_ids_per_combination(self):
        """Test unique IDs are different for each combination"""
        parser = MailChimpABParser()
        campaigns = parser.parse(MAILCHIMP_AB_SAMPLE)
        
        assert campaigns[0].unique_id != campaigns[1].unique_id
    
    def test_parse_sets_correct_platform(self):
        """Test platform is set to mailchimp_ab"""
        parser = MailChimpABParser()
        campaigns = parser.parse(MAILCHIMP_AB_SAMPLE)
        
        assert all(c.platform == "mailchimp_ab" for c in campaigns)
    
    def test_parse_empty_combinations_raises_error(self):
        """Test parser raises error when no combinations found"""
        parser = MailChimpABParser()
        invalid_ab = """Campaign Report
"Title:","Test"
"Delivery Date/Time:","Sat, May 1, 2021 10:15"
"""
        
        with pytest.raises(EmptyReportError):
            parser.parse(invalid_ab)


class TestMailChimpAggregatedParser:
    """Test MailChimp aggregated report parser"""
    
    def test_can_parse_valid_report(self):
        """Test parser recognizes valid aggregated report"""
        parser = MailChimpAggregatedParser()
        assert parser.can_parse(MAILCHIMP_AGGREGATED_SAMPLE) is True
    
    def test_cannot_parse_invalid_format(self):
        """Test parser rejects invalid format"""
        parser = MailChimpAggregatedParser()
        assert parser.can_parse(INVALID_FORMAT) is False
    
    def test_parse_returns_multiple_campaigns(self):
        """Test parser returns multiple campaigns"""
        parser = MailChimpAggregatedParser()
        campaigns = parser.parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert len(campaigns) == 3
        assert all(isinstance(c, EmailCampaign) for c in campaigns)
    
    def test_parse_extracts_all_campaigns(self):
        """Test parser extracts all campaigns from CSV"""
        parser = MailChimpAggregatedParser()
        campaigns = parser.parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert campaigns[0].subject == "Welcome Email"
        assert campaigns[1].subject == "Newsletter #1"
        assert campaigns[2].subject == "Product Launch"
    
    def test_parse_converts_percentages(self):
        """Test parser converts percentage strings to floats"""
        parser = MailChimpAggregatedParser()
        campaigns = parser.parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert campaigns[0].open_rate == pytest.approx(0.2778, rel=0.001)
        assert campaigns[0].click_rate == pytest.approx(0.0648, rel=0.001)
    
    def test_parse_calculates_ctor(self):
        """Test CTOR calculation for aggregated data"""
        parser = MailChimpAggregatedParser()
        campaigns = parser.parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        expected_ctor = 7 / 30
        assert campaigns[0].ctor == pytest.approx(expected_ctor, rel=0.001)
    
    def test_parse_sets_correct_platform(self):
        """Test platform is set to mailchimp_aggregated"""
        parser = MailChimpAggregatedParser()
        campaigns = parser.parse(MAILCHIMP_AGGREGATED_SAMPLE)
        
        assert all(c.platform == "mailchimp_aggregated" for c in campaigns)
    
    def test_parse_empty_csv_raises_error(self):
        """Test parser raises error for empty CSV"""
        parser = MailChimpAggregatedParser()
        empty_csv = "Title,Subject,List"
        
        with pytest.raises(EmptyReportError):
            parser.parse(empty_csv)
    
    def test_parse_skips_invalid_rows(self):
        """Test parser skips rows with invalid/incomplete data"""
        parser = MailChimpAggregatedParser()
        # Only 1 valid campaign - others have issues
        csv_with_invalid = 'Title,Subject,List,"Send Date","Send Weekday","Total Recipients","Successful Deliveries","Soft Bounces","Hard Bounces","Total Bounces","Times Forwarded","Forwarded Opens","Unique Opens","Open Rate","Total Opens","Unique Clicks","Click Rate","Total Clicks",Unsubscribes,"Abuse Complaints"\n' \
            '"Valid Campaign","Test Email","Main List","Jun 09, 2018 09:30 pm",Saturday,110,108,1,1,2,0,0,30,27.78%,57,7,6.48%,7,0,0\n' \
            '"Has Title No Subject","","Main List","Jun 18, 2018 09:15 am",Monday,137,134,1,2,3,0,0,30,22.39%,52,5,3.73%,6,1,0\n' \
            '"Zero Delivered","Subject Here","Main",,,0,0,0,0,0,0,0,0,0%,0,0,0%,0,0,0\n'
        
        campaigns = parser.parse(csv_with_invalid)
        # Only first row is valid - others fail validation
        assert len(campaigns) == 1, f"Expected 1 campaign, got {len(campaigns)}: {[c.subject for c in campaigns]}"
        assert campaigns[0].subject == "Test Email"
