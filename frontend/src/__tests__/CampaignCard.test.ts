import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import CampaignCard from '@/components/CampaignCard.vue'

describe('CampaignCard', () => {
  const mockCampaign = {
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
  }

  it('renders campaign title', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('Test Campaign')
  })

  it('renders campaign subject if different from title', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('Test Subject')
  })

  it('displays delivered count', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('1,000')
  })

  it('displays open rate', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('25.0%')
  })

  it('displays click rate', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('5.0%')
  })

  it('displays platform badge', () => {
    const wrapper = mount(CampaignCard, {
      props: { campaign: mockCampaign },
    })
    expect(wrapper.text()).toContain('mailchimp')
  })
})
