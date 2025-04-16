"""
Unit tests for the VoiceHandler class.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from src.voice_handler import VoiceHandler

def test_voice_handler_initialization():
    """Test that VoiceHandler initializes correctly with API key."""
    with patch.dict(os.environ, {'VAPI_API_KEY': 'test_api_key'}):
        handler = VoiceHandler()
        assert handler.api_key == 'test_api_key'
        assert handler.client is not None

def test_voice_handler_initialization_missing_api_key():
    """Test that VoiceHandler raises an error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="VAPI_API_KEY environment variable is not set"):
            VoiceHandler()

def test_get_client():
    """Test that get_client returns the client instance."""
    with patch.dict(os.environ, {'VAPI_API_KEY': 'test_api_key'}):
        handler = VoiceHandler()
        client = handler.get_client()
        assert client == handler.client

def test_start_call_with_default_message(mock_vapi_client):
    """Test starting a call with the default welcome message."""
    with patch.dict(os.environ, {'VAPI_API_KEY': 'test_api_key'}):
        handler = VoiceHandler()
        handler.client = mock_vapi_client
        
        handler.start_call()
        
        # Verify that start was called with the correct assistant config
        mock_vapi_client.start.assert_called_once()
        call_args = mock_vapi_client.start.call_args[1]
        assert 'assistant' in call_args
        assert call_args['assistant']['firstMessage'] == "Hello! I'm your Extend voice assistant. How can I help you today?"
        assert call_args['assistant']['model'] == 'gpt-4'
        assert call_args['assistant']['voice'] == 'shimmer-openai'
        assert call_args['assistant']['recordingEnabled'] is True
        assert call_args['assistant']['interruptionsEnabled'] is True

def test_start_call_with_custom_message(mock_vapi_client):
    """Test starting a call with a custom welcome message."""
    with patch.dict(os.environ, {'VAPI_API_KEY': 'test_api_key'}):
        handler = VoiceHandler()
        handler.client = mock_vapi_client
        
        custom_message = "Welcome to the Extend voice assistant!"
        handler.start_call(first_message=custom_message)
        
        # Verify that start was called with the custom message
        mock_vapi_client.start.assert_called_once()
        call_args = mock_vapi_client.start.call_args[1]
        assert call_args['assistant']['firstMessage'] == custom_message

def test_stop_call(mock_vapi_client):
    """Test stopping a call."""
    with patch.dict(os.environ, {'VAPI_API_KEY': 'test_api_key'}):
        handler = VoiceHandler()
        handler.client = mock_vapi_client
        
        handler.stop_call()
        
        # Verify that stop was called
        mock_vapi_client.stop.assert_called_once() 