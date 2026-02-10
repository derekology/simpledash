# Testing Guide for Simple Dash

This document provides comprehensive information about testing in the Simple Dash application.

## Overview

Simple Dash uses:
- **Backend**: pytest for Python unit and integration tests
- **Frontend**: Vitest + Vue Test Utils for TypeScript/Vue component tests

## Backend Tests

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Dependencies include:
# - pytest: Testing framework
# - httpx: Required for TestClient
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_parsers.py::TestMailerLiteClassicParser

# Run specific test
pytest tests/test_api.py::TestParseEndpoint::test_parse_valid_csv

# Run with coverage
pytest --cov=app --cov-report=html tests/
```

### Backend Test Structure

#### **tests/test_api.py**
Tests FastAPI endpoints:
- ✅ Health check endpoint
- ✅ File upload validation (CSV only, size limits, file count limits)
- ✅ Parsing endpoint success and error handling
- ✅ Deduplication logic
- ✅ Static file serving

#### **tests/test_parsers.py**
Tests email campaign parsers:
- ✅ MailerLite Classic format parsing
- ✅ MailChimp Aggregated format parsing
- ✅ MailChimp A/B Test format parsing
- ✅ MailChimp individual campaign format parsing
- ✅ Error handling for invalid/malformed CSVs

#### **tests/test_utils.py**
Tests utility functions:
- ✅ Campaign ID generation (consistency, uniqueness)
- ✅ Format detection
- ✅ Error handling

### Writing Backend Tests

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMyFeature:
    def test_basic_case(self):
        """Test description"""
        response = client.get("/endpoint")
        assert response.status_code == 200
        assert response.json()["key"] == "expected_value"
    
    def test_error_case(self):
        """Test error handling"""
        with pytest.raises(Exception):
            # Code that should raise exception
            pass
```

## Frontend Tests

### Setup

```bash
cd frontend

# Install dependencies (includes vitest, @vue/test-utils, happy-dom)
npm install
```

### Running Frontend Tests

```bash
# Run all tests
npm test

# Run in watch mode (re-runs on file changes)
npm test -- --watch

# Run with UI
npm test -- --ui

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- src/__tests__/CampaignCard.test.ts
```

### Frontend Test Structure

#### **src/__tests__/campaign.store.test.ts**
Tests Pinia campaign store:
- ✅ Store initialization
- ✅ Setting campaigns
- ✅ Calculating aggregate statistics
- ✅ State reactivity

#### **src/__tests__/CampaignCard.test.ts**
Tests CampaignCard component:
- ✅ Rendering campaign data
- ✅ Displaying metrics (delivered, open rate, click rate)
- ✅ Platform badge display
- ✅ Subject vs title handling

#### **src/__tests__/MultiSearchDropdown.test.ts**
Tests MultiSearchDropdown component:
- ✅ Rendering options
- ✅ Search filtering
- ✅ Selection state
- ✅ Outliers button functionality
- ✅ Low volume button functionality
- ✅ Event emissions

#### **src/__tests__/utils.test.ts**
Tests utility functions:
- ✅ Number formatting
- ✅ Percentage formatting
- ✅ CTOR calculation
- ✅ Outlier detection (IQR method)
- ✅ Low volume detection (median-based)

### Writing Frontend Tests

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: { myProp: 'value' }
    })
    
    expect(wrapper.text()).toContain('expected text')
    expect(wrapper.find('.my-class').exists()).toBe(true)
  })
  
  it('handles user interaction', async () => {
    const wrapper = mount(MyComponent)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('myEvent')).toBeTruthy()
  })
})
```

## Test Coverage Goals

### Backend
- **Parsers**: 90%+ (critical for data accuracy)
- **API Endpoints**: 85%+ (ensure proper error handling)
- **Utilities**: 90%+ (shared code needs high confidence)

### Frontend
- **Components**: 80%+ (UI consistency)
- **Views**: 70%+ (integration-level tests)
- **Stores**: 85%+ (state management critical)

## Continuous Integration

Tests should be run:
1. Before committing code
2. In CI/CD pipeline
3. Before deploying to production

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app tests/
  
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: cd frontend && npm install
      - run: cd frontend && npm test
```

## Test Data

Sample CSV files for manual testing:
- `campaign_Campaign_COVERUP_29_04_2021_Feb_8_2026.csv` - MailChimp A/B test
- `campaign_Campaign_Personal_Styling_Amy_02__Feb_8_2026.csv` - MailChimp single

## Debugging Tests

### Backend
```bash
# Run with print statements visible
pytest -s

# Run with debugger
pytest --pdb

# Stop on first failure
pytest -x
```

### Frontend
```bash
# Run with console output
npm test -- --reporter=verbose

# Debug specific test
npm test -- --reporter=verbose src/__tests__/MyComponent.test.ts
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Test names should clearly describe what they test
3. **Arrange-Act-Assert**: Structure tests with setup, action, and verification
4. **Mock External Dependencies**: Use mocks for API calls, file I/O, etc.
5. **Test Edge Cases**: Include tests for error conditions, empty data, etc.
6. **Keep Tests Fast**: Fast tests = more frequent execution
7. **Update Tests with Code**: When changing features, update corresponding tests

## Common Issues

### Backend
- **Import errors**: Ensure `PYTHONPATH` includes app directory
- **Database state**: Tests should not depend on external state
- **Async issues**: Use `async def` and `await` properly

### Frontend
- **Component not mounting**: Check if all dependencies are provided
- **Events not emitting**: Use `await` after triggering events
- **CSS selectors failing**: Use test IDs or semantic selectors

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Vitest documentation](https://vitest.dev/)
- [Vue Test Utils documentation](https://test-utils.vuejs.org/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
