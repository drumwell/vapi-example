# FinVoice: Tech News Briefing Assistant

A voice-powered financial news assistant that provides concise, 30-second briefings focused on technology and AI market news.

## Features
- Daily tech market briefings
- Focus on AI and technology sector news
- Natural follow-up questions
- Approximately 30-second briefing length

## Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file with your API keys:
   ```
   VAPI_API_KEY=your_vapi_key
   NEWSAPI_KEY=your_newsapi_key
   ```

## Usage
Run the assistant:
```bash
python -m src.main
```

## Example Interactions
- "Give me today's tech news briefing"
- "Tell me more about the AI market news"
- "What's happening with tech stocks today?"

## Project Structure
```
finvoice/
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py      # Handles getting news from APIs
│   ├── news_processor.py    # Processes and summarizes news
│   ├── voice_handler.py     # VAPI integration
│   └── main.py             # Main application entry point
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Contributing
Feel free to submit issues and enhancement requests!