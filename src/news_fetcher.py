import aiohttp
import os
from datetime import datetime, timedelta
import json

class NewsFetcher:
    def __init__(self):
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        if not self.newsapi_key:
            raise ValueError("NEWSAPI_KEY environment variable is not set")
        
    async def fetch_tech_news(self):
        """
        Fetches technology and AI focused news from various sources
        """
        if not self.newsapi_key:
            return {"status": "error", "message": "NewsAPI key is not configured"}
            
        async with aiohttp.ClientSession() as session:
            # NewsAPI query for tech and AI news
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': '(technology OR artificial intelligence OR AI) AND (business OR market OR company)',
                'language': 'en',
                'sortBy': 'relevancy',
                'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'apiKey': self.newsapi_key
            }
            
            try:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"NewsAPI error: {error_text}")
                        return {"status": "error", "message": f"NewsAPI returned status {response.status}"}
                    
                    data = await response.json()
                    
                    # Validate the response structure
                    if 'status' in data and data['status'] != 'ok':
                        return {"status": "error", "message": data.get('message', 'Unknown NewsAPI error')}
                    
                    return data
            except Exception as e:
                print(f"Error fetching news: {str(e)}")
                return {"status": "error", "message": str(e)} 