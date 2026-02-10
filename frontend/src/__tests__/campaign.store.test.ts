import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCampaignStore } from '@/stores/campaign'

describe('Campaign Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty campaigns', () => {
    const store = useCampaignStore()
    expect(store.campaigns).toEqual([])
  })

  it('sets campaigns correctly', () => {
    const store = useCampaignStore()
    const testCampaigns = [
      {
        platform: 'mailchimp',
        subject: 'Test Subject',
        email_title: 'Test Campaign',
        unique_id: 'test-123',
        sent_at: '2024-01-15 10:00',
        delivered: 1000,
        opens: 250,
        open_rate: 25.0,
        clicks: 50,
        click_rate: 5.0,
        unsubscribes: 5,
        unsubscribe_rate: 0.5,
        spam_complaints: 2,
        hard_bounces: 5,
        hard_bounce_rate: 0.5,
        soft_bounces: 5,
        soft_bounce_rate: 0.5,
        ctor: 20.0,
      },
    ]

    store.setCampaigns(testCampaigns)
    expect(store.campaigns).toEqual(testCampaigns)
  })

  it('calculates stats correctly', () => {
    const store = useCampaignStore()
    const testCampaigns = [
      {
        platform: 'mailchimp',
        subject: 'Campaign 1',
        email_title: 'Campaign 1',
        unique_id: '1',
        sent_at: '2024-01-15 10:00',
        delivered: 1000,
        opens: 250,
        open_rate: 25.0,
        clicks: 50,
        click_rate: 5.0,
        unsubscribes: 5,
        unsubscribe_rate: 0.5,
        spam_complaints: 2,
        hard_bounces: 5,
        hard_bounce_rate: 0.5,
        soft_bounces: 5,
        soft_bounce_rate: 0.5,
        ctor: 20.0,
      },
      {
        platform: 'mailchimp',
        subject: 'Campaign 2',
        email_title: 'Campaign 2',
        unique_id: '2',
        sent_at: '2024-01-16 10:00',
        delivered: 2000,
        opens: 600,
        open_rate: 30.0,
        clicks: 120,
        click_rate: 6.0,
        unsubscribes: 10,
        unsubscribe_rate: 0.5,
        spam_complaints: 4,
        hard_bounces: 10,
        hard_bounce_rate: 0.5,
        soft_bounces: 10,
        soft_bounce_rate: 0.5,
        ctor: 20.0,
      },
    ]

    store.setCampaigns(testCampaigns)

    const stats = store.averageStats
    expect(stats.avgOpenRate).toBeCloseTo(27.5, 1)
    expect(stats.avgClickRate).toBeCloseTo(5.5, 1)
    expect(stats.totalDelivered).toBe(3000)
    expect(stats.totalOpens).toBe(850)
    expect(stats.totalClicks).toBe(170)
  })
})
