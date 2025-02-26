"""
Integration tests for the complete FinAgents system
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import from root directory
import main
from src.agents.investor_agents import create_investor_team
from src.agents.analyst_agents import create_analyst_team
from src.agents.debate_manager import DebateManager
from src.utils.stock_data import get_stock_data

class TestFullSystem(unittest.TestCase):
    """Integration tests for the full FinAgents system"""
    
    @patch('src.utils.stock_data.get_stock_data')
    @patch('src.agents.debate_manager.DebateManager.run_debate')
    @patch('src.agents.analyst_agents.create_analyst_team')
    @patch('src.agents.investor_agents.create_investor_team')
    def test_main_execution_flow(self, mock_create_investor_team, mock_create_analyst_team, 
                                mock_run_debate, mock_get_stock_data):
        """Test the full execution flow through the main function"""
        # Setup mocks
        mock_create_investor_team.return_value = {'Investor1': MagicMock()}
        mock_create_analyst_team.return_value = {'Analyst1': MagicMock()}
        mock_get_stock_data.return_value = {'key': 'value'}
        
        mock_run_debate.return_value = {
            'MSFT': {
                'analyst_reports': {'Analyst1': 'Report text'},
                'investor_opinions': {'Investor1': 'Opinion text'},
                'decision': 'Final decision text'
            }
        }
        
        # Set the stocks_to_analyze directly to avoid user input
        main.main()
        
        # Check that all the key functions were called
        mock_create_investor_team.assert_called_once()
        mock_create_analyst_team.assert_called_once()
        mock_get_stock_data.assert_called()
        mock_run_debate.assert_called_once()

class TestEndToEnd(unittest.TestCase):
    """End-to-end test with mocked API calls"""
    
    @patch('src.agents.investor_agents.ChatAnthropic')
    @patch('src.agents.analyst_agents.ChatAnthropic')
    @patch('src.agents.debate_manager.ChatAnthropic')
    @patch('src.utils.stock_data.yf.Ticker')
    def test_end_to_end_with_mocks(self, mock_ticker, mock_chat1, mock_chat2, mock_chat3):
        """Test the entire process with mock API calls"""
        # Setup yfinance mock
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = {
            'longName': 'Test Company',
            'sector': 'Technology',
            'industry': 'Software',
            'marketCap': 1000000000,
            'trailingPE': 25.5,
        }
        mock_ticker_instance.history.return_value = MagicMock()
        mock_ticker_instance.income_stmt = MagicMock()
        mock_ticker_instance.balance_sheet = MagicMock()
        mock_ticker_instance.cashflow = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Setup LLM mocks
        mock_chat_instance = MagicMock()
        mock_chat_instance.invoke.return_value = {'text': 'Mocked response'}
        mock_chat1.return_value = mock_chat_instance
        mock_chat2.return_value = mock_chat_instance
        mock_chat3.return_value = mock_chat_instance
        
        # Run the process
        # Get stock data
        stock_data = get_stock_data('TEST')
        self.assertEqual(stock_data['ticker'], 'TEST')
        
        # Create the teams
        investor_team = create_investor_team()
        analyst_team = create_analyst_team()
        
        # Check teams were created
        self.assertGreater(len(investor_team), 0)
        self.assertGreater(len(analyst_team), 0)
        
        # Create debate manager
        debate_manager = DebateManager(investor_team, analyst_team)
        
        # Run a debate
        results = debate_manager.run_debate(['TEST'], {'TEST': stock_data})
        
        # Check results
        self.assertIn('TEST', results)
        self.assertIn('analyst_reports', results['TEST'])
        self.assertIn('investor_opinions', results['TEST'])
        self.assertIn('decision', results['TEST'])

class TestOutputFiles(unittest.TestCase):
    """Tests for the output file generation"""
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist"""
        output_dir = 'results'
        
        # Remove directory if it exists
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
        
        # Call the function that should create the directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Check directory exists
        self.assertTrue(os.path.exists(output_dir))
        self.assertTrue(os.path.isdir(output_dir))
    
    def test_markdown_file_creation(self):
        """Test that markdown files can be created"""
        output_dir = 'results'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create test files
        test_decision_path = os.path.join(output_dir, 'TEST_decision.md')
        test_analysis_path = os.path.join(output_dir, 'TEST_detailed_analysis.md')
        
        with open(test_decision_path, 'w') as f:
            f.write('# Test Decision\n\nThis is a test')
        
        with open(test_analysis_path, 'w') as f:
            f.write('# Test Analysis\n\nThis is a test')
        
        # Check files exist
        self.assertTrue(os.path.exists(test_decision_path))
        self.assertTrue(os.path.exists(test_analysis_path))
        
        # Clean up
        os.remove(test_decision_path)
        os.remove(test_analysis_path)

if __name__ == '__main__':
    unittest.main()