"""Anonymized test fixtures for email campaign parsers"""

MAILERLITE_CLASSIC_SAMPLE = """Campaign report
"Subject:","Weekly Newsletter - Product Updates"
"Sent","2021-08-07 16:00:00"

"Campaign results"
"Total emails sent:","3902"
"Opened:","1489 (38.91%)"
"Clicked:","33 (0.86%)"

"Bad statistics"
"Unsubscribed:","97 (2.49%)"
"Spam complaints:","0 (0%)"
"Hard bounce:","21 (0.54%)"
"Soft bounce:","54 (1.38%)"

"Reading environment"
"Mobile:","34.92%"
"Webmail:","61.38%"
"Desktop:","3.7%"

"Links activity"
"Links","Unique clicks","Total clicks"
"Unsubscribe link","83","90"
"""

MAILCHIMP_SINGLE_SAMPLE = """Email Campaign Report
"Title:","Summer Sale Campaign"
"Subject Line:","Get 20% Off Today Only!"
"Delivery Date/Time:","Mon, Apr 26, 2021 12:25"

"Overall Stats"
"Total Recipients:","1000"
"Successful Deliveries:","995"
"Bounces:","5 (0.5%)"
"Times Forwarded:","0"
"Forwarded Opens:","0"
"Recipients Who Opened:","350 (35.18%)"
"Total Opens:","500"
"Last Open Date:","4/30/21 6:04"
"Recipients Who Clicked:","100 (10.05%)"
"Total Clicks:","150"
"Last Click Date:","4/30/21 6:01"
"Total Unsubs:","5"
"Total Abuse Complaints:","0"
"Times Liked on Facebook:","0"

"Clicks by URL"
"URL","Total Clicks","Unique Clicks"
"""

MAILCHIMP_AB_SAMPLE = """Campaign Report
"Title:","Spring Promo AB Test"
"Delivery Date/Time:","Sat, May 1, 2021 10:15"

"Combination 1 Stats"
"Subject Line:","Spring Sale - Up to 30% Off"
"From Name:","Company Store"
"From Email:","hello@example.com"
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

"Combination 2 Stats"
"Subject Line:","Limited Time - Spring Savings Event"
"From Name:","Company Store"
"From Email:","hello@example.com"
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
"""

MAILCHIMP_AGGREGATED_SAMPLE = """Title,Subject,List,"Send Date","Send Weekday","Total Recipients","Successful Deliveries","Soft Bounces","Hard Bounces","Total Bounces","Times Forwarded","Forwarded Opens","Unique Opens","Open Rate","Total Opens","Unique Clicks","Click Rate","Total Clicks",Unsubscribes,"Abuse Complaints","Times Liked on Facebook","Folder Id","Unique Id","Total Orders","Total Gross Sales","Total Revenue"
"Campaign A","Welcome Email","Main List","Jun 09, 2018 09:30 pm",Saturday,110,108,1,1,2,0,0,30,27.78%,57,7,6.48%,7,0,0,0,0,17671f6028,0,0,0
"Campaign B","Newsletter #1","Main List","Jun 18, 2018 09:15 am",Monday,137,134,1,2,3,0,0,30,22.39%,52,5,3.73%,6,1,0,0,0,6e3fb30c88,0,0,0
"Campaign C","Product Launch","Main List","Jun 27, 2018 09:15 am",Wednesday,134,133,1,0,1,0,0,35,26.32%,62,4,3.01%,4,0,0,0,0,b5da57cea8,0,0,0
"""

EMPTY_REPORT = ""

INVALID_FORMAT = """Random text that is not a valid report format
Some other data
More random content"""

MAILERLITE_INCOMPLETE = """Campaign report
"Subject:","Test Campaign"

"Campaign results"
"Total emails sent:","100"
"""
