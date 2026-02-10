# Simple Dash Tests

This directory contains unit tests for the Simple Dash application.

## Backend Tests

### Running Backend Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Test Structure

- **test_api.py** - Tests for FastAPI endpoints
  - Health check endpoint
  - Parse endpoint (file upload, validation, deduplication)
  - Static file serving
  
- **test_parsers.py** - Tests for email report parsers
  - MailerLite Classic parser
  - MailChimp Aggregated parser
  - MailChimp A/B Test parser
  - MailChimp individual campaign parser
  
- **test_utils.py** - Tests for utility functions
  - Campaign ID generator
  - Format detector

## Frontend Tests

Frontend tests use Vitest. See `frontend/` directory for test files.

### Running Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## Test Coverage

### Backend Coverage Goals
- Parsers: 90%+ coverage
- API endpoints: 85%+ coverage
- Utilities: 90%+ coverage

### Frontend Coverage Goals
- Components: 80%+ coverage
- Views: 70%+ coverage
- Stores: 85%+ coverage

## Writing New Tests

### Backend Test Template

```python
import pytest
from app.your_module import your_function

class TestYourFeature:
    def test_basic_functionality(self):
        result = your_function(input_data)
        assert result == expected_output
    
    def test_edge_case(self):
        with pytest.raises(ValueError):
            your_function(invalid_input)
```

### Frontend Test Template

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import YourComponent from '@/components/YourComponent.vue'

describe('YourComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(YourComponent, { props: { msg: 'Hello' } })
    expect(wrapper.text()).toContain('Hello')
  })
})
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Before deployment

## Test Data

Sample CSV files for testing are located in the project root:
- `campaign_Campaign_COVERUP_29_04_2021_Feb_8_2026.csv` - MailChimp A/B test
- `campaign_Campaign_Personal_Styling_Amy_02__Feb_8_2026.csv` - MailChimp single campaign
