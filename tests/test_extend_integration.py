"""
Unit tests for the ExtendIntegration class.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from src.extend_integration import ExtendIntegration

def test_extend_integration_initialization():
    """Test that ExtendIntegration initializes correctly with API keys."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        assert integration.api_key == 'test_api_key'
        assert integration.api_secret == 'test_api_secret'
        assert integration.client is not None
        assert integration.toolkit is not None

def test_extend_integration_initialization_missing_api_key():
    """Test that ExtendIntegration raises an error when API key is missing."""
    with patch.dict(os.environ, {'EXTEND_API_SECRET': 'test_api_secret'}, clear=True):
        with pytest.raises(ValueError, match="EXTEND_API_KEY and EXTEND_API_SECRET environment variables must be set"):
            ExtendIntegration()

def test_extend_integration_initialization_missing_api_secret():
    """Test that ExtendIntegration raises an error when API secret is missing."""
    with patch.dict(os.environ, {'EXTEND_API_KEY': 'test_api_key'}, clear=True):
        with pytest.raises(ValueError, match="EXTEND_API_KEY and EXTEND_API_SECRET environment variables must be set"):
            ExtendIntegration()

@pytest.mark.asyncio
async def test_get_virtual_cards(mock_extend_client, sample_virtual_cards):
    """Test getting virtual cards."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.virtual_cards.get_virtual_cards.return_value = {
            "virtualCards": sample_virtual_cards
        }
        
        # Call the method
        result = await integration.get_virtual_cards()
        
        # Verify the result
        assert result == sample_virtual_cards
        mock_extend_client.virtual_cards.get_virtual_cards.assert_called_once()

@pytest.mark.asyncio
async def test_get_transactions(mock_extend_client, sample_transactions):
    """Test getting transactions."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.transactions.get_transactions.return_value = {
            "report": {
                "transactions": sample_transactions
            }
        }
        
        # Call the method
        result = await integration.get_transactions()
        
        # Verify the result
        assert result == sample_transactions
        mock_extend_client.transactions.get_transactions.assert_called_once_with(filters=None)

@pytest.mark.asyncio
async def test_get_transactions_with_filters(mock_extend_client, sample_transactions):
    """Test getting transactions with filters."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.transactions.get_transactions.return_value = {
            "report": {
                "transactions": sample_transactions
            }
        }
        
        # Define filters
        filters = {
            "startDate": "2023-04-01",
            "endDate": "2023-04-30",
            "category": "travel"
        }
        
        # Call the method
        result = await integration.get_transactions(filters=filters)
        
        # Verify the result
        assert result == sample_transactions
        mock_extend_client.transactions.get_transactions.assert_called_once_with(filters=filters)

@pytest.mark.asyncio
async def test_get_transaction_detail(mock_extend_client):
    """Test getting transaction detail."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        transaction_detail = {
            "id": "tx_123456",
            "amount": 2500,
            "description": "Coffee Shop",
            "date": "2023-04-15",
            "category": "food",
            "merchant": "Starbucks",
            "location": "San Francisco, CA"
        }
        mock_extend_client.transactions.get_transaction_detail.return_value = transaction_detail
        
        # Call the method
        result = await integration.get_transaction_detail("tx_123456")
        
        # Verify the result
        assert result == transaction_detail
        mock_extend_client.transactions.get_transaction_detail.assert_called_once_with(transaction_id="tx_123456")

@pytest.mark.asyncio
async def test_get_expense_categories(mock_extend_client, sample_expense_categories):
    """Test getting expense categories."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.expense_management.get_expense_categories.return_value = {
            "expenseCategories": sample_expense_categories
        }
        
        # Call the method
        result = await integration.get_expense_categories()
        
        # Verify the result
        assert result == sample_expense_categories
        mock_extend_client.expense_management.get_expense_categories.assert_called_once()

@pytest.mark.asyncio
async def test_create_receipt_attachment(mock_extend_client):
    """Test creating a receipt attachment."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.expense_management.create_receipt_attachment.return_value = {
            "id": "receipt_123456",
            "transactionId": "tx_123456",
            "status": "attached"
        }
        
        # Mock file opening
        with patch('builtins.open', MagicMock()):
            # Call the method
            result = await integration.create_receipt_attachment("tx_123456", "path/to/receipt.pdf")
            
            # Verify the result
            assert result == {
                "id": "receipt_123456",
                "transactionId": "tx_123456",
                "status": "attached"
            }
            mock_extend_client.expense_management.create_receipt_attachment.assert_called_once()

@pytest.mark.asyncio
async def test_automatch_receipts(mock_extend_client):
    """Test automatching receipts."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.client = mock_extend_client
        
        # Configure mock to return sample data
        mock_extend_client.expense_management.automatch_receipts.return_value = {
            "jobId": "job_123456",
            "status": "processing"
        }
        
        # Call the method
        result = await integration.automatch_receipts()
        
        # Verify the result
        assert result == {
            "jobId": "job_123456",
            "status": "processing"
        }
        mock_extend_client.expense_management.automatch_receipts.assert_called_once()

def test_get_tools(mock_extend_toolkit):
    """Test getting tools from the Extend AI Toolkit."""
    with patch.dict(os.environ, {
        'EXTEND_API_KEY': 'test_api_key',
        'EXTEND_API_SECRET': 'test_api_secret'
    }):
        integration = ExtendIntegration()
        integration.toolkit = mock_extend_toolkit
        
        # Configure mock to return sample data
        mock_extend_toolkit.get_tools.return_value = ["tool1", "tool2", "tool3"]
        
        # Call the method
        result = integration.get_tools()
        
        # Verify the result
        assert result == ["tool1", "tool2", "tool3"]
        mock_extend_toolkit.get_tools.assert_called_once() 