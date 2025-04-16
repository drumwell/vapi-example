# Extend Voice Assistant

A voice-enabled assistant for managing Extend virtual cards, transactions, expense categories, and receipts.

## Features

- Voice-activated virtual card management
- Transaction queries with natural language
- Expense category listing
- Receipt upload and management
- Natural language responses

## Prerequisites

- Python 3.8+
- Vapi API key
- Extend API key and secret

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd extend-voice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
VAPI_API_KEY=your_vapi_api_key
EXTEND_API_KEY=your_extend_api_key
EXTEND_API_SECRET=your_extend_api_secret
```

## Usage

Run the voice assistant:
```bash
python -m src.main
```

### Voice Commands

The assistant understands various voice commands:

- Virtual Cards:
  - "Show my virtual cards"
  - "What's the balance on my card ending in 1234?"

- Transactions:
  - "Show my recent transactions"
  - "How much did I spend last week?"
  - "Show my transactions for travel this month"

- Expense Categories:
  - "List my expense categories"
  - "What categories do I have?"

- Receipts:
  - "Upload a receipt"
  - "Match my receipts"

## Project Structure

- `src/`
  - `main.py`: Main entry point
  - `voice_handler.py`: Vapi integration
  - `extend_integration.py`: Extend API integration
  - `command_processor.py`: Voice command processing
  - `response_generator.py`: Natural language response generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.