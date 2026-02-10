"""Unit tests for email campaign parsers."""
import pytest
from app.parsers.mailerlite_classic import parse_mailerlite_classic
from app.parsers.mailchimp_aggregated import parse_mailchimp_aggregated
from app.parsers.mailchimp_ab import parse_mailchimp_ab
from app.parsers.mailchimp import parse_mailchimp


class TestMailerLiteClassicParser:
    def test_parse_valid_report(self):
        csv_content = """Campaign report
"Subject:","Test Subject"
"Sent","2021-09-28 13:00:00"

"Campaign results"
"Total emails sent:","4116"
"Opened:","1085 (26.66%)"
"Clicked:","32 (0.79%)"

"Bad statistics"
"Unsubscribed:","47 (1.14%)"
"Spam complaints:","0 (0%)"
"Hard bounce:","5 (0.12%)"
"Soft bounce:","41 (1%)"

"Reading environment"
"Mobile:","40.63%"
"Webmail:","53.68%"
"Desktop:","5.69%"

"Top email clients"
"Email client","Subscribers"
"Gmail","33.39%"
"WebKit","27.34%"
"unknown","15.96%"
"","10.46%"
"Blink","4.13%"

"Links activity"
"Links","Unique clicks","Total clicks"
"Unsubscribe link","36","41"
"https://casemogulphonerepairs.com/collections/artist-collaboration-series-taytayski?ml_subscriber=&ml_subscriber_hash=","15","19"
"https://casemogulphonerepairs.com/account/register?ml_subscriber=&ml_subscriber_hash=","6","8"
"Link to the web version of this email (plain text version)","5","5"
"https://casemogulphonerepairs.com/pages/repairs?ml_subscriber=&ml_subscriber_hash=","4","4"
"https://casemogulphonerepairs.com/pages/shop?ml_subscriber=&ml_subscriber_hash=","3","3"
"https://casemogulphonerepairs.com/?ml_subscriber=&ml_subscriber_hash=","2","3"
"https://www.instagram.com/casemogul/?ml_subscriber=&ml_subscriber_hash=","2","3"
"https://casemogulphonerepairs.com/apps/store-locator?ml_subscriber=&ml_subscriber_hash=","2","2"
"Unsubscribe link (plain text version)","1","1"
"Link to the web version of this email","1","1"
"https://www.facebook.com/casemogul?ml_subscriber=&ml_subscriber_hash=","1","2"
"""
        
        result = parse_mailerlite_classic(csv_content)
        
        assert "campaigns" in result
        assert len(result["campaigns"]) == 1
        campaign = result["campaigns"][0]
        assert campaign["platform"] == "mailerlite_classic"
        assert campaign["subject"] == "Test Subject"
        assert campaign["email_title"] == "Test Subject"
        assert campaign["delivered"] == 4116
        assert campaign["opens"] == 1085
        assert campaign["open_rate"] == 0.2666
        assert campaign["clicks"] == 32
        assert campaign["click_rate"] == 0.0079
        assert campaign["unsubscribes"] == 47
        assert campaign["unique_id"] is not None

    def test_parse_empty_csv(self):
        result = parse_mailerlite_classic("")
        assert len(result["campaigns"]) == 0


class TestMailChimpAggregatedParser:
    def test_parse_valid_aggregated_report(self):
        csv_content = """Title,Subject,List,"Send Date","Send Weekday","Total Recipients","Successful Deliveries","Soft Bounces","Hard Bounces","Total Bounces","Times Forwarded","Forwarded Opens","Unique Opens","Open Rate","Total Opens","Unique Clicks","Click Rate","Total Clicks",Unsubscribes,"Abuse Complaints","Times Liked on Facebook","Folder Id","Unique Id","Total Orders","Total Gross Sales","Total Revenue","Analytics ROI","Campaign Cost","Revenue Created",Visits,"New Visits",Pages/Visit,"Bounce Rate","Time on Site","Goal Conversion Rate","Per Visit Goal Value",Transactions,"Ecommerce Conversion Rate","Per Visit Value","Average Value"
"[06-10-18] Most Popular Styles","Get Our Most Popular Styles Before They're Gone!","[06-09-18] Subscribed Contacts","Jun 09, 2018 09:30 pm",Saturday,110,108,1,1,2,0,0,30,27.78%,57,7,6.48%,7,0,0,0,0,17671f6028,0,0,0,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a"""
        
        result = parse_mailchimp_aggregated(csv_content)
        
        assert "campaigns" in result
        assert len(result["campaigns"]) == 1
        campaign = result["campaigns"][0]
        assert campaign["platform"] == "mailchimp_aggregated"
        assert campaign["email_title"] == "[06-10-18] Most Popular Styles"
        assert campaign["delivered"] == 108
        assert campaign["opens"] == 30
        assert campaign["clicks"] == 7
        assert campaign["unique_id"] is not None

    def test_parse_multiple_campaigns(self):
        csv_content = """Title,Subject,List,"Send Date","Send Weekday","Total Recipients","Successful Deliveries","Soft Bounces","Hard Bounces","Total Bounces","Times Forwarded","Forwarded Opens","Unique Opens","Open Rate","Total Opens","Unique Clicks","Click Rate","Total Clicks",Unsubscribes,"Abuse Complaints","Times Liked on Facebook","Folder Id","Unique Id","Total Orders","Total Gross Sales","Total Revenue","Analytics ROI","Campaign Cost","Revenue Created",Visits,"New Visits",Pages/Visit,"Bounce Rate","Time on Site","Goal Conversion Rate","Per Visit Goal Value",Transactions,"Ecommerce Conversion Rate","Per Visit Value","Average Value"
"[06-10-18] Most Popular Styles","Get Our Most Popular Styles Before They're Gone!","[06-09-18] Subscribed Contacts","Jun 09, 2018 09:30 pm",Saturday,110,108,1,1,2,0,0,30,27.78%,57,7,6.48%,7,0,0,0,0,17671f6028,0,0,0,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a
"[06-10-18] Most Popular Styles (copy 01)","Meet us at the beach! ☀","[06-17-18] Subscribers","Jun 18, 2018 09:15 am",Monday,137,134,1,2,3,0,0,30,22.39%,52,5,3.73%,6,1,0,0,0,6e3fb30c88,0,0,0,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a,n/a"""
        
        result = parse_mailchimp_aggregated(csv_content)
        
        assert "campaigns" in result
        assert len(result["campaigns"]) == 2


class TestMailChimpABParser:
    def test_parse_ab_test_report(self):
        csv_content = """Campaign Report
"Title:","COVERUP-29-04-2021"
"Delivery Date/Time:","Sat, May 1, 2021 10:15"

"Combination 1 Stats"
"Subject Line:","ALERT: luxury beach cover ups are now on sale"
"From Name:","☀️Sun Vixen Swimwear"
"From Email:","sunvixen@sunvixen.com"
"Total Recipients:","1,751"
"Successful Deliveries:","1,742"
"Bounces:","9 (0.5%)"
"Times Forwarded:","0"
"Forwarded Opens:","0"
"Recipients Who Opened:","141 (8.1%)"
"Total Opens:","201"
"Last Open Date:","1/7/26 17:40"
"Recipients Who Clicked:","20 (1.1%)"
"Total Clicks:","157"
"Last Click Date:","9/8/23 16:20"
"Total Unsubs:","1"
"Total Abuse Complaints:","0"
"Total Sales:","CA$0.00"

"Combination 2 Stats"
"Subject Line:","Now on sale— luxury beach cover ups"
"From Name:","☀️Sun Vixen Swimwear"
"From Email:","sunvixen@sunvixen.com"
"Total Recipients:","1,750"
"Successful Deliveries:","1,742"
"Bounces:","8 (0.5%)"
"Times Forwarded:","0"
"Forwarded Opens:","0"
"Recipients Who Opened:","125 (7.2%)"
"Total Opens:","185"
"Last Open Date:","11/8/23 13:15"
"Recipients Who Clicked:","27 (1.5%)"
"Total Clicks:","624"
"Last Click Date:","9/9/23 7:41"
"Total Unsubs:","1"
"Total Abuse Complaints:","0"
"Total Sales:","CA$0.00"

"Combination 1 Clicks by URL"
"URL","Total Clicks","Unique Clicks"
"https://www.facebook.com/Sun-Vixen-401166783591673/?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","126","1"
"https://www.sunvixen.com/bikini-cover-ups?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","20","13"
"https://www.sunvixen.com/bikinis?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","6","4"
"https://www.sunvixen.com/swimwear?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","2","2"
"https://www.sunvixen.com/one-piece-swimsuits?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/sale?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","1","1"
"https://sunvixen.us17.list-manage.com/unsubscribe?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&c=2ea0097713&utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/mens-swimwear?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/fashion-stylist?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://www.instagram.com/sunvixenswimwear/?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/blog?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://www.youtube.com/channel/UCtcGA5Igln__oCe6xwkzftQ?utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/vcard?u=80abc91a0e5e88d0467415681&id=3d52975149&utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/profile?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&utm_source=Sun+Vixen+Main&utm_campaign=3c2cf0ef38-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-3c2cf0ef38-[LIST_EMAIL_ID]&mc_cid=3c2cf0ef38&mc_eid=UNIQID","0","0"

"Combination 2 Clicks by URL"
"URL","Total Clicks","Unique Clicks"
"https://www.instagram.com/sunvixenswimwear/?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","361","2"
"https://www.facebook.com/Sun-Vixen-401166783591673/?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","219","2"
"https://www.sunvixen.com/bikini-cover-ups?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","23","22"
"https://www.sunvixen.com/bikinis?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","7","4"
"https://www.sunvixen.com/?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","3","3"
"https://www.sunvixen.com/one-piece-swimsuits?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","3","2"
"https://www.sunvixen.com/swimwear?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","2","2"
"https://sunvixen.us17.list-manage.com/unsubscribe?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&c=2ea0097713&utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","2","2"
"https://www.sunvixen.com/mens-swimwear?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/fashion-stylist?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/sale?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","1","1"
"https://www.youtube.com/channel/UCtcGA5Igln__oCe6xwkzftQ?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/blog?utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/vcard?u=80abc91a0e5e88d0467415681&id=3d52975149&utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/profile?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&utm_source=Sun+Vixen+Main&utm_campaign=d4516d7a73-BESTSELLERS-10-04-2021_COPY_01&utm_medium=email&utm_term=0_3d52975149-d4516d7a73-[LIST_EMAIL_ID]&mc_cid=d4516d7a73&mc_eid=UNIQID","0","0"
"""
        
        result = parse_mailchimp_ab(csv_content)
        
        assert "campaigns" in result
        assert len(result["campaigns"]) == 2
        assert result["campaigns"][0]["subject"] == "ALERT: luxury beach cover ups are now on sale"
        assert result["campaigns"][1]["subject"] == "Now on sale— luxury beach cover ups"
        assert result["campaigns"][0]["platform"] == "mailchimp_ab"


class TestMailChimpParser:
    def test_parse_single_campaign_report(self):
        csv_content = """Email Campaign Report
"Title:","Personal Styling (Amy 02)"
"Subject Line:","Personal Styling Sun Vixen Swimwear ☀"
"Delivery Date/Time:","Mon, Apr 26, 2021 12:25"

"Overall Stats"
"Total Recipients:","1"
"Successful Deliveries:","1"
"Bounces:","0 (0.0%)"
"Times Forwarded:","0"
"Forwarded Opens:","0"
"Recipients Who Opened:","1 (100.0%)"
"Total Opens:","13"
"Last Open Date:","4/30/21 6:04"
"Recipients Who Clicked:","1 (100.0%)"
"Total Clicks:","1"
"Last Click Date:","4/30/21 6:01"
"Total Unsubs:","0"
"Total Abuse Complaints:","0"
"Times Liked on Facebook:","0"

"Clicks by URL"
"URL","Total Clicks","Unique Clicks"
"https://www.sunvixen.com/product-page/lace-banded-bikini-bottom?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","1","1"
"https://www.sunvixen.com/?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/onda-de-mar-lotto-longline-underwire-padded-top-removable-straps-hand-embroider?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/profile?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/vcard?u=80abc91a0e5e88d0467415681&id=3d52975149&utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.youtube.com/channel/UCtcGA5Igln__oCe6xwkzftQ?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/blog?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.instagram.com/sunvixenswimwear/?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.facebook.com/Sun-Vixen-401166783591673/?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/yellow-bikini-bottoms?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/yellow-bikini-top?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/swimsuits-for-small-bust?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/lotto-banded-bikini-bottoms?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/bandeau-bikini?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/high-waisted-swimsuit?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/swimwear?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/lace-halter-top?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/black-bikini-bottoms-low-rise-sauvage-swimwear?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/bikini-top-banded-black-sauvage-swimwear?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/white-bikini-bottoms?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/product-page/white-lace-bikini-top?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/sale?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/fashion-stylist?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/mens-swimwear?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/one-piece-swimsuits?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://www.sunvixen.com/bikinis?utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
"https://sunvixen.us17.list-manage.com/unsubscribe?u=80abc91a0e5e88d0467415681&id=3d52975149&e=[UNIQID]&c=2ea0097713&utm_source=Sun+Vixen+VIP&utm_campaign=ba5052d3e9-EMAIL_CAMPAIGN_2020_11_11_09_31_COPY_02&utm_medium=email&utm_term=0_584417e59d-ba5052d3e9-[LIST_EMAIL_ID]&mc_cid=ba5052d3e9&mc_eid=UNIQID","0","0"
,"""
        
        # Note: This parser needs campaign metadata in the CSV header or filename
        # For now, testing basic structure
        result = parse_mailchimp(csv_content)
        
        assert "campaigns" in result
        assert len(result["campaigns"]) == 1
        campaign = result["campaigns"][0]
        assert campaign["platform"] == "mailchimp"
        assert campaign["delivered"] == 1
        assert campaign["opens"] == 1
        assert campaign["clicks"] == 1
