// Generate realistic demo campaign data
export interface DemoCampaignData {
  platform: string
  subject: string
  email_title: string
  unique_id?: string
  sent_at: string
  delivered: number
  opens: number
  open_rate: number
  clicks: number
  click_rate: number
  ctor: number
  unsubscribes: number
  unsubscribe_rate: number
  spam_complaints: number
  hard_bounces: number
  hard_bounce_rate: number
  soft_bounces: number
  soft_bounce_rate: number
}

const generateCampaign = (index: number, baseDate: Date): DemoCampaignData => {
  // Create delivery outliers for specific campaigns
  let delivered: number
  if (index === 2) {
    // Outlier: Very low deliveries (test send)
    delivered = Math.floor(500 + Math.random() * 200)
  } else if (index === 7) {
    // Outlier: Very high deliveries (major campaign)
    delivered = Math.floor(45000 + Math.random() * 5000)
  } else if (index === 9) {
    // Outlier: Another low deliveries
    delivered = Math.floor(800 + Math.random() * 300)
  } else {
    // Normal deliveries around 15k
    delivered = Math.floor(14000 + Math.random() * 2000)
  }
  
  const open_rate = 0.15 + Math.random() * 0.20
  const opens = Math.floor(delivered * open_rate)
  const click_rate = 0.01 + Math.random() * 0.07
  const clicks = Math.floor(delivered * click_rate)
  const ctor = opens > 0 ? clicks / opens : 0
  const unsubscribe_rate = 0.001 + Math.random() * 0.004
  const unsubscribes = Math.floor(delivered * unsubscribe_rate)
  const hard_bounce_rate = 0.002 + Math.random() * 0.008
  const hard_bounces = Math.floor(delivered * hard_bounce_rate)
  const soft_bounce_rate = 0.005 + Math.random() * 0.015
  const soft_bounces = Math.floor(delivered * soft_bounce_rate)
  const spam_complaints = Math.floor(Math.random() * 5)
  
  // Generate dates with varied weekdays
  // Define specific days of week for each campaign to ensure variety
  const weekdayOffsets = [
    1,  // Monday (index 0)
    3,  // Wednesday (index 1)
    0,  // Sunday (index 2) - test send on weekend
    2,  // Tuesday (index 3)
    4,  // Thursday (index 4)
    5,  // Friday (index 5)
    1,  // Monday (index 6)
    3,  // Wednesday (index 7) - major campaign
    6,  // Saturday (index 8)
    2   // Tuesday (index 9)
  ]
  
  const campaignDate = new Date(baseDate)
  // Go back weeks, then adjust to specific weekday
  campaignDate.setDate(campaignDate.getDate() - (index * 7))
  const currentDay = campaignDate.getDay()
  const targetDay = weekdayOffsets[index % weekdayOffsets.length] ?? 1
  const dayDiff = targetDay - currentDay
  campaignDate.setDate(campaignDate.getDate() + dayDiff)
  
  // Vary the time of day (morning: 8-11am, afternoon: 2-5pm)
  const isMorning = index % 2 === 0
  if (isMorning) {
    campaignDate.setHours(8 + Math.floor(Math.random() * 3), Math.floor(Math.random() * 60))
  } else {
    campaignDate.setHours(14 + Math.floor(Math.random() * 3), Math.floor(Math.random() * 60))
  }
  
  const demoSubjects = [
    '🚀 New Product Launch - Limited Time Offer!',
    '📢 Important Update: Changes to Our Service',
    '💝 Thank You - Exclusive Gift Inside',
    '🎉 Flash Sale: 50% Off Everything!',
    '📚 Your Monthly Newsletter is Here',
    '⭐ Customer Appreciation Week Starts Now',
    '🔥 Hot Deals You Cannot Miss This Week',
    '✨ Introducing Our Latest Features',
    '💰 Save Big: End of Season Clearance',
    '🎁 Special Offer Just for You'
  ]
  
  const demoTitles = [
    'Product Launch Demo',
    'Service Update Demo',
    'Customer Thank You Demo',
    'Flash Sale Demo',
    'Newsletter Demo',
    'Customer Appreciation Demo',
    'Weekly Deals Demo',
    'Feature Announcement Demo',
    'Clearance Sale Demo',
    'Member Offer Demo'
  ]
  
  return {
    platform: 'demo',
    subject: demoSubjects[index % demoSubjects.length] || 'Demo Campaign',
    email_title: (demoTitles[index % demoTitles.length] || 'Demo') + ' (Demo)',
    unique_id: `demo_${index}_${Date.now()}`,
    sent_at: campaignDate.toISOString(),
    delivered,
    opens,
    open_rate,
    clicks,
    click_rate,
    ctor,
    unsubscribes,
    unsubscribe_rate,
    spam_complaints,
    hard_bounces,
    hard_bounce_rate,
    soft_bounces,
    soft_bounce_rate
  }
}

export const generateDemoData = (count: number = 10): DemoCampaignData[] => {
  const baseDate = new Date()
  const campaigns: DemoCampaignData[] = []
  for (let i = 0; i < count; i++) {
    campaigns.push(generateCampaign(i, baseDate))
  }
  return campaigns.sort((a, b) => new Date(a.sent_at).getTime() - new Date(b.sent_at).getTime())
}
