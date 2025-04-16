class ResponseGenerator:
    def __init__(self):
        pass
    
    def generate_welcome_message(self):
        """
        Generates a welcome message for the user
        """
        return "Hello! I'm your Extend voice assistant. I can help you manage your virtual cards, check your transactions, view expense categories, and upload receipts. How can I assist you today?"
    
    def generate_error_message(self, error):
        """
        Generates an error message
        """
        return f"I encountered an error: {str(error)}. Please try again or ask for help."
    
    def generate_help_message(self):
        """
        Generates a help message
        """
        return "I can help you with the following: 1) Check your virtual cards, 2) View your transactions, 3) List your expense categories, 4) Upload receipts. What would you like to do?"
    
    def format_transaction_summary(self, transactions, time_period=None, category=None):
        """
        Formats a summary of transactions
        """
        if not transactions:
            return "I couldn't find any transactions matching your criteria."
        
        total_spending = sum(transaction.get("amount", 0) for transaction in transactions)
        total_spending_dollars = total_spending / 100  # Convert cents to dollars
        
        response = f"You spent ${total_spending_dollars:.2f} "
        
        if time_period:
            response += f"{time_period} "
        
        if category:
            response += f"on {category} "
        
        response += "."
        
        return response
    
    def format_transaction_list(self, transactions, limit=5):
        """
        Formats a list of transactions
        """
        if not transactions:
            return "I couldn't find any transactions matching your criteria."
        
        response = "Here are your recent transactions: "
        
        for transaction in transactions[:limit]:
            amount = transaction.get("amount", 0) / 100  # Convert cents to dollars
            description = transaction.get("description", "Unknown")
            date = transaction.get("date", "Unknown")
            
            response += f"${amount:.2f} for {description} on {date}. "
        
        if len(transactions) > limit:
            response += f"And {len(transactions) - limit} more transactions. "
        
        return response
    
    def format_virtual_card_list(self, virtual_cards):
        """
        Formats a list of virtual cards
        """
        if not virtual_cards:
            return "You don't have any virtual cards."
        
        response = f"You have {len(virtual_cards)} virtual cards. "
        
        for card in virtual_cards:
            last_four = card.get("lastFour", "unknown")
            balance = card.get("balance", 0) / 100  # Convert cents to dollars
            response += f"Card ending in {last_four} has a balance of ${balance:.2f}. "
        
        return response
    
    def format_expense_category_list(self, categories):
        """
        Formats a list of expense categories
        """
        if not categories:
            return "You don't have any expense categories."
        
        response = f"You have {len(categories)} expense categories: "
        
        for category in categories:
            name = category.get("name", "Unknown")
            response += f"{name}, "
        
        return response[:-2] + "."  # Remove trailing comma and space 