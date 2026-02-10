import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MultiSearchDropdown from '@/components/MultiSearchDropdown.vue'

describe('MultiSearchDropdown', () => {
  const mockOptions = [
    { value: 0, label: 'Campaign 1', subtitle: '2024-01-15' },
    { value: 1, label: 'Campaign 2', subtitle: '2024-01-16' },
    { value: 2, label: 'Campaign 3', subtitle: '2024-01-17' },
  ]

  it('renders all options', () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
      },
    })

    expect(wrapper.text()).toContain('Campaign 1')
    expect(wrapper.text()).toContain('Campaign 2')
    expect(wrapper.text()).toContain('Campaign 3')
  })

  it('shows selected options count', () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [0, 1],
      },
    })

    expect(wrapper.text()).toContain('2 selected')
  })

  it('filters options by search query', async () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
      },
    })

    const input = wrapper.find('input[type="text"]')
    await input.setValue('Campaign 1')

    expect(wrapper.text()).toContain('Campaign 1')
    expect(wrapper.text()).not.toContain('Campaign 2')
  })

  it('shows outliers button when provided', () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
        showOutliers: true,
        outliersCount: 2,
        outliersButtonText: 'Select Outliers',
      },
    })

    expect(wrapper.text()).toContain('Select Outliers')
    expect(wrapper.text()).toContain('(2)')
  })

  it('shows low volume button when provided', () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
        showLowVolume: true,
        lowVolumeCount: 1,
        lowVolumeButtonText: 'Select Low Volume',
      },
    })

    expect(wrapper.text()).toContain('Select Low Volume')
    expect(wrapper.text()).toContain('(1)')
  })

  it('emits toggle-outliers event', async () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
        showOutliers: true,
        outliersCount: 2,
        outliersButtonText: 'Select Outliers',
      },
    })

    const outliersButton = wrapper.find('.outliers-button')
    await outliersButton.trigger('click')

    expect(wrapper.emitted('toggleOutliers')).toBeTruthy()
  })

  it('emits toggle-low-volume event', async () => {
    const wrapper = mount(MultiSearchDropdown, {
      props: {
        options: mockOptions,
        modelValue: [],
        showLowVolume: true,
        lowVolumeCount: 1,
        lowVolumeButtonText: 'Select Low Volume',
      },
    })

    const lowVolumeButton = wrapper.find('.low-volume-button')
    await lowVolumeButton.trigger('click')

    expect(wrapper.emitted('toggleLowVolume')).toBeTruthy()
  })
})
