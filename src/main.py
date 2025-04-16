import os
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
from .voice_handler import VoiceHandler
from .extend_integration import ExtendIntegration
from .command_processor import CommandProcessor
from .response_generator import ResponseGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class ExtendVoice:
    """
    Main class for the Extend Voice Assistant.
    Coordinates the interaction between voice handling, Extend integration,
    command processing, and response generation.
    """
    
    def __init__(self):
        """Initialize all components of the Extend Voice Assistant."""
        self.voice_handler = VoiceHandler()
        self.extend_integration = ExtendIntegration()
        self.command_processor = CommandProcessor(self.extend_integration)
        self.response_generator = ResponseGenerator()
        
    async def start(self) -> None:
        """
        Start the voice assistant and begin processing voice commands.
        
        Raises:
            Exception: If there's an error during initialization or execution.
        """
        try:
            # Generate welcome message
            welcome_message = self.response_generator.generate_welcome_message()
            
            logger.info("Starting voice assistant with welcome message: %s", welcome_message)
            
            # Start a new call with the welcome message
            self.voice_handler.start_call(first_message=welcome_message)
            
            logger.info("Call started successfully! You can now interact with the assistant.")
            
            # Keep the connection alive
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error("Error occurred: %s", str(e), exc_info=True)
            raise
        finally:
            # Ensure we stop the assistant when done
            self.voice_handler.stop_call()
            logger.info("Voice assistant stopped.")

if __name__ == "__main__":
    extend_voice = ExtendVoice()
    asyncio.run(extend_voice.start()) 