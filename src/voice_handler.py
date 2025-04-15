from vapi_python import Vapi
import os

class VoiceHandler:
    def __init__(self):
        self.api_key = os.getenv('VAPI_API_KEY')
        if not self.api_key:
            raise ValueError("VAPI_API_KEY environment variable is not set")

        self.client = Vapi(api_key=self.api_key)
        
    def get_client(self):
        """
        Returns the Vapi client instance
        """
        return self.client
        
    def stop_assistant(self):
        """
        Stops the current assistant session
        """
        self.client.stop()
        
    async def create_conversation(self, call_id):
        """
        Creates a new conversation with the assistant
        """
        return call_id 