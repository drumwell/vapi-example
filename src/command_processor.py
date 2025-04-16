import re
from datetime import datetime, timedelta

class CommandProcessor:
    def __init__(self, extend_integration):
        self.extend_integration = extend_integration
        
    async def process_command(self, command):
        """
        Processes a voice command and returns the appropriate response
        """
        command = command.lower()
        
        # Check for virtual card commands
        if "virtual card" in command or "virtual cards" in command:
            return await self._handle_virtual_card_command(command)
        
        # Check for transaction commands
        elif "transaction" in command or "transactions" in command or "spent" in command or "spending" in command:
            return await self._handle_transaction_command(command)
        
        # Check for expense category commands
        elif "category" in command or "categories" in command or "expense" in command:
            return await self._handle_expense_category_command(command)
        
        # Check for receipt commands
        elif "receipt" in command or "upload" in command:
            return await self._handle_receipt_command(command)
        
        # Default response for unrecognized commands
        else:
            return "I'm not sure how to help with that. You can ask me about your virtual cards, transactions, expense categories, or uploading receipts."
    
    async def _handle_virtual_card_command(self, command):
        """
        Handles commands related to virtual cards
        """
        virtual_cards = await self.extend_integration.get_virtual_cards()
        
        if not virtual_cards:
            return "You don't have any virtual cards."
        
        if "list" in command or "show" in command or "what" in command:
            response = "You have {} virtual cards. ".format(len(virtual_cards))
            
            for card in virtual_cards:
                last_four = card.get("lastFour", "unknown")
                balance = card.get("balance", 0) / 100  # Convert cents to dollars
                response += "Card ending in {} has a balance of ${:.2f}. ".format(last_four, balance)
            
            return response
        
        return "I can help you with your virtual cards. You can ask me to list your virtual cards or show details about a specific card."
    
    async def _handle_transaction_command(self, command):
        """
        Handles commands related to transactions
        """
        # Extract time period from command
        time_period = self._extract_time_period(command)
        
        # Extract category from command
        category = self._extract_category(command)
        
        # Build filters
        filters = {}
        
        if time_period:
            filters["startDate"] = time_period["start_date"]
            filters["endDate"] = time_period["end_date"]
        
        if category:
            filters["category"] = category
        
        # Get transactions
        transactions = await self.extend_integration.get_transactions(filters=filters)
        
        if not transactions:
            return "I couldn't find any transactions matching your criteria."
        
        # Calculate total spending
        total_spending = sum(transaction.get("amount", 0) for transaction in transactions)
        total_spending_dollars = total_spending / 100  # Convert cents to dollars
        
        # Generate response
        if "how much" in command:
            response = "You spent ${:.2f} ".format(total_spending_dollars)
            
            if time_period:
                response += "{} ".format(time_period["description"])
            
            if category:
                response += "on {} ".format(category)
            
            response += "."
            
            return response
        
        elif "list" in command or "show" in command or "what" in command:
            response = "Here are your recent transactions: "
            
            for transaction in transactions[:5]:  # Limit to 5 transactions
                amount = transaction.get("amount", 0) / 100  # Convert cents to dollars
                description = transaction.get("description", "Unknown")
                date = transaction.get("date", "Unknown")
                
                response += "${:.2f} for {} on {}. ".format(amount, description, date)
            
            if len(transactions) > 5:
                response += "And {} more transactions. ".format(len(transactions) - 5)
            
            return response
        
        return "I can help you with your transactions. You can ask me how much you spent or to list your recent transactions."
    
    async def _handle_expense_category_command(self, command):
        """
        Handles commands related to expense categories
        """
        categories = await self.extend_integration.get_expense_categories()
        
        if not categories:
            return "You don't have any expense categories."
        
        if "list" in command or "show" in command or "what" in command:
            response = "You have {} expense categories: ".format(len(categories))
            
            for category in categories:
                name = category.get("name", "Unknown")
                response += "{}, ".format(name)
            
            return response[:-2] + "."  # Remove trailing comma and space
        
        return "I can help you with your expense categories. You can ask me to list your categories."
    
    async def _handle_receipt_command(self, command):
        """
        Handles commands related to receipts
        """
        # This is a placeholder for receipt handling
        # In a real implementation, this would involve file handling and UI interaction
        return "I can help you upload receipts. In a real implementation, this would guide you through taking a photo and attaching it to a transaction."
    
    def _extract_time_period(self, command):
        """
        Extracts time period from command
        """
        today = datetime.now()
        
        if "today" in command:
            return {
                "start_date": today.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d"),
                "description": "today"
            }
        
        elif "yesterday" in command:
            yesterday = today - timedelta(days=1)
            return {
                "start_date": yesterday.strftime("%Y-%m-%d"),
                "end_date": yesterday.strftime("%Y-%m-%d"),
                "description": "yesterday"
            }
        
        elif "this week" in command:
            start_of_week = today - timedelta(days=today.weekday())
            return {
                "start_date": start_of_week.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d"),
                "description": "this week"
            }
        
        elif "this month" in command:
            start_of_month = today.replace(day=1)
            return {
                "start_date": start_of_month.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d"),
                "description": "this month"
            }
        
        elif "last month" in command:
            if today.month == 1:
                start_of_last_month = today.replace(year=today.year-1, month=12, day=1)
            else:
                start_of_last_month = today.replace(month=today.month-1, day=1)
            
            if today.month == 1:
                end_of_last_month = today.replace(year=today.year-1, month=12, day=31)
            else:
                if today.month == 3:
                    end_of_last_month = today.replace(month=today.month-1, day=28)
                elif today.month in [5, 7, 10, 12]:
                    end_of_last_month = today.replace(month=today.month-1, day=30)
                else:
                    end_of_last_month = today.replace(month=today.month-1, day=31)
            
            return {
                "start_date": start_of_last_month.strftime("%Y-%m-%d"),
                "end_date": end_of_last_month.strftime("%Y-%m-%d"),
                "description": "last month"
            }
        
        return None
    
    def _extract_category(self, command):
        """
        Extracts category from command
        """
        # This is a simple implementation
        # In a real implementation, this would use NLP to extract categories
        categories = ["travel", "food", "office", "entertainment", "utilities"]
        
        for category in categories:
            if category in command:
                return category
        
        return None 