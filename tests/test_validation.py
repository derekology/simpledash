"""Integration tests for parser validation behavior"""
import pytest
from app.parsers.mailerlite_classic import MailerLiteClassicParser
from app.parsers.mailchimp import MailChimpParser
from app.parsers.mailchimp_ab import MailChimpABParser
from app.parsers.mailchimp_aggregated import MailChimpAggregatedParser
from app.models import EmptyReportError


class TestParserValidation:
    """Test that all parsers properly validate campaigns"""
    
    def test_mailerlite_validates_meaningful_data(self):
        """Test MailerLite parser validates campaign has meaningful data"""
        parser = MailerLiteClassicParser()
        
        # Incomplete report missing required fields
        incomplete = """Campaign report
"Subject:","Test"

"Campaign results"
"Total emails sent:","100"
"""
        
        with pytest.raises(EmptyReportError):
            parser.parse(incomplete)
    
    def test_mailchimp_validates_meaningful_data(self):
        """Test MailChimp parser validates campaign has meaningful data"""
        parser = MailChimpParser()
        
        # Incomplete report
        incomplete = """Email Campaign Report
"Title:","Test"

"Overall Stats"
"Total Recipients:","100"
"""
        
        with pytest.raises(EmptyReportError):
            parser.parse(incomplete)
    
    def test_mailchimp_aggregated_skips_incomplete_rows(self):
        """Test aggregated parser only returns campaigns with all required fields"""
        parser = MailChimpAggregatedParser()
        
        # Mix of complete and incomplete campaigns  
        mixed_csv = 'Title,Subject,List,"Send Date","Send Weekday","Total Recipients","Successful Deliveries","Soft Bounces","Hard Bounces","Total Bounces","Times Forwarded","Forwarded Opens","Unique Opens","Open Rate","Total Opens","Unique Clicks","Click Rate","Total Clicks",Unsubscribes,"Abuse Complaints"\n' \
            '"Complete 1","Subject 1","List","Jun 09, 2018 09:30 pm",Saturday,110,108,1,1,2,0,0,30,27.78%,57,7,6.48%,7,0,0\n' \
            '"Has Title But Missing Subject","","List","Jun 18, 2018 09:15 am",Monday,137,134,1,2,3,0,0,30,22.39%,52,5,3.73%,6,1,0\n' \
            '"Complete 2","Subject 2","List","Jun 27, 2018 09:15 am",Wednesday,134,133,1,0,1,0,0,35,26.32%,62,4,3.01%,4,0,0\n'
        
        campaigns = parser.parse(mixed_csv)
        
        # Should only get the 2 complete campaigns (row 2 has empty subject)
        assert len(campaigns) == 2, f"Expected 2 campaigns, got {len(campaigns)}: {[c.subject for c in campaigns]}"
        assert campaigns[0].subject == "Subject 1"
        assert campaigns[1].subject == "Subject 2"
    
    def test_mailchimp_ab_validates_combinations(self):
        """Test A/B parser validates each combination"""
        parser = MailChimpABParser()
        
        # A/B test with one valid and one incomplete combination
        mixed_ab = """Campaign Report
"Title:","Test Campaign"
"Delivery Date/Time:","Sat, May 1, 2021 10:15"

"Combination 1 Stats"
"Subject Line:","Valid Subject"
"Total Recipients:","1,751"
"Successful Deliveries:","1,742"
"Bounces:","9 (0.5%)"
"Recipients Who Opened:","141 (8.1%)"
"Recipients Who Clicked:","20 (1.1%)"
"Total Unsubs:","1"
"Total Abuse Complaints:","0"

"Combination 2 Stats"
"Subject Line:","Missing Data"
"Total Recipients:","1,750"
"""
        
        campaigns = parser.parse(mixed_ab)
        
        # Should only get the valid combination
        assert len(campaigns) == 1
        assert campaigns[0].subject == "Valid Subject"
