from vapi_python import Vapi
from datetime import datetime
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from .news_fetcher import NewsFetcher
from .news_processor import NewsProcessor
from .voice_handler import VoiceHandler

class FinVoice:
    def __init__(self):
        self.voice_handler = VoiceHandler()
        self.news_fetcher = NewsFetcher()
        self.news_processor = NewsProcessor()
        
    async def get_daily_briefing(self):
        # Fetch tech and AI focused news
        raw_news = await self.news_fetcher.fetch_tech_news()
        
        # Process and summarize news
        summary = self.news_processor.create_briefing(raw_news)
        
        return summary

    async def start(self):
        try:
            # Get the Vapi client
            print("Initializing Vapi client...")
            client = self.voice_handler.get_client()
            
            try:
                # Get initial briefing
                briefing = await self.get_daily_briefing()
            except Exception as e:
                print(f"Error fetching news: {str(e)}")
                briefing = "I apologize, but I'm having trouble fetching the latest news. Would you like me to tell you about technology and AI in general?"
            
            print("Starting voice assistant with briefing:", briefing)
            
            # Start a new call with the briefing as the first message
            client.start(
                assistant={
                    'name': "Tech News Briefer",
                    'model': "gpt-4",
                    'voice': "shimmer-openai",
                    'firstMessage': briefing,
                    'recordingEnabled': True,
                    'interruptionsEnabled': True
                }
            )
            
            print("Call started successfully! You can now interact with the assistant.")
            
            # Keep the connection alive
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise
        finally:
            # Ensure we stop the assistant when done
            self.voice_handler.stop_assistant()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    finvoice = FinVoice()
    asyncio.run(finvoice.start()) 