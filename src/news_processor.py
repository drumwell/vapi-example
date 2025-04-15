class NewsProcessor:
    def __init__(self):
        self.max_briefing_words = 75  # Approximately 30 seconds of speech
        
    def create_briefing(self, news_data):
        """
        Creates a concise briefing from news data
        """
        # Check for error responses
        if isinstance(news_data, dict) and news_data.get('status') == 'error':
            error_message = news_data.get('message', 'Unknown error')
            return f"I'm sorry, I couldn't fetch the latest tech news. Error: {error_message}"
            
        # Check for valid news data
        if not news_data or not isinstance(news_data, dict) or 'articles' not in news_data:
            return "I'm sorry, I couldn't fetch any tech news at the moment."
            
        articles = news_data['articles']
        
        # Check if we have any articles
        if not articles:
            return "I couldn't find any recent tech news articles at the moment."
        
        # Prioritize articles about AI and tech market impact
        priority_articles = [
            article for article in articles
            if any(keyword in article['title'].lower() 
                  for keyword in ['ai', 'artificial intelligence', 'tech', 'technology'])
        ]
        
        # If no priority articles, use all articles
        if not priority_articles:
            priority_articles = articles
        
        # Take top 2-3 stories
        top_stories = priority_articles[:3]
        
        # Create briefing
        briefing = "Here's your tech news briefing for today:\n\n"
        
        for story in top_stories:
            title = story['title'].split(' - ')[0]  # Remove source from title
            briefing += f"• {title}\n"
            
        return briefing 