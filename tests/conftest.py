"""
Pytest configuration and fixtures for the Extend Voice Assistant tests.
"""
import os
import pytest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def mock_vapi_client():
    """Mock Vapi client for testing."""
    with patch('vapi_python.Vapi') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_extend_client():
    """Mock Extend client for testing."""
    with patch('extend.ExtendClient') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_extend_toolkit():
    """Mock Extend AI Toolkit for testing."""
    with patch('extend_ai_toolkit.openai.toolkit.ExtendOpenAIToolkit') as mock:
        mock_instance = MagicMock()
        mock.default_instance.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_virtual_cards():
    """Sample virtual card data for testing."""
    return [
        {
            "id": "card_1",
            "last_four": "1234",
            "spend_limit": 50000,  # $500.00
            "status": "active",
            "expiry_date": "2025-12"
        },
        {
            "id": "card_2",
            "last_four": "5678",
            "spend_limit": 100000,  # $1,000.00
            "status": "active",
            "expiry_date": "2025-12"
        }
    ]

@pytest.fixture
def sample_transactions():
    """Sample transactions for testing."""
    now = datetime.now()
    return [
        {
            "id": "txn_1",
            "amount": 2500,  # $25.00
            "description": "Coffee Shop",
            "category": "Food",
            "date": now - timedelta(days=1),
            "merchant": "Starbucks"
        },
        {
            "id": "txn_2",
            "amount": 5000,  # $50.00
            "description": "Office Supplies",
            "category": "Office",
            "date": now - timedelta(days=2),
            "merchant": "Staples"
        },
        {
            "id": "txn_3",
            "amount": 15000,  # $150.00
            "description": "Flight Ticket",
            "category": "Travel",
            "date": now - timedelta(days=3),
            "merchant": "United Airlines"
        }
    ]

@pytest.fixture
def sample_expense_categories():
    """Sample expense categories for testing."""
    return [
        {
            "id": "cat_1",
            "name": "Travel",
            "description": "Business travel expenses"
        },
        {
            "id": "cat_2",
            "name": "Food",
            "description": "Meals and entertainment"
        },
        {
            "id": "cat_3",
            "name": "Office",
            "description": "Office supplies and equipment"
        }
    ] 