import os
from extend import ExtendClient
from extend_ai_toolkit.openai.toolkit import ExtendOpenAIToolkit
from extend_ai_toolkit.shared import Configuration, Scope, Product, Actions

class ExtendIntegration:
    def __init__(self):
        self.api_key = os.getenv('EXTEND_API_KEY')
        self.api_secret = os.getenv('EXTEND_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("EXTEND_API_KEY and EXTEND_API_SECRET environment variables must be set")
        
        # Initialize the Extend client
        self.client = ExtendClient(
            api_key=self.api_key,
            api_secret=self.api_secret
        )
        
        # Initialize the Extend AI Toolkit
        self.toolkit = ExtendOpenAIToolkit.default_instance(
            api_key=self.api_key,
            api_secret=self.api_secret,
            configuration=Configuration(
                scope=[
                    Scope(Product.VIRTUAL_CARDS, actions=Actions(read=True)),
                    Scope(Product.CREDIT_CARDS, actions=Actions(read=True)),
                    Scope(Product.TRANSACTIONS, actions=Actions(read=True, write=True)),
                    Scope(Product.EXPENSE_CATEGORIES, actions=Actions(read=True, write=True)),
                ]
            )
        )
    
    async def get_virtual_cards(self):
        """
        Gets all virtual cards
        """
        response = await self.client.virtual_cards.get_virtual_cards()
        return response.get("virtualCards", [])
    
    async def get_transactions(self, filters=None):
        """
        Gets transactions with optional filters
        """
        response = await self.client.transactions.get_transactions(filters=filters)
        return response.get("report", {}).get("transactions", [])
    
    async def get_transaction_detail(self, transaction_id):
        """
        Gets detailed information about a specific transaction
        """
        response = await self.client.transactions.get_transaction_detail(transaction_id)
        return response
    
    async def get_expense_categories(self):
        """
        Gets all expense categories
        """
        response = await self.client.expense_management.get_expense_categories()
        return response.get("expenseCategories", [])
    
    async def create_receipt_attachment(self, transaction_id, file_path):
        """
        Uploads a receipt and attaches it to a transaction
        """
        with open(file_path, 'rb') as file:
            response = await self.client.expense_management.create_receipt_attachment(
                transaction_id=transaction_id,
                file=file
            )
        return response
    
    async def automatch_receipts(self):
        """
        Initiates an async job to automatch uploaded receipts to transactions
        """
        response = await self.client.expense_management.automatch_receipts()
        return response
    
    def get_tools(self):
        """
        Gets the tools from the Extend AI Toolkit
        """
        return self.toolkit.get_tools() 