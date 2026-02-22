"""
Unit tests for debate manager module
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from src.agents.debate_manager import DebateManager

class TestDebateManager(unittest.TestCase):
    """Tests for the DebateManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.investor_team = {
            'Investor1': MagicMock(),
            'Investor2': MagicMock()
        }
        self.analyst_team = {
            'Analyst1': MagicMock(),
            'Analyst2': MagicMock()
        }

        # Create a debate manager with mock teams
        self.debate_manager = DebateManager(self.investor_team, self.analyst_team)
    
    def test_initialization(self):
        """Test that debate manager is correctly initialized"""
        self.assertEqual(self.debate_manager.investor_team, self.investor_team)
        self.assertEqual(self.debate_manager.analyst_team, self.analyst_team)
        self.assertIsNotNone(self.debate_manager.llm)
        self.assertIsNotNone(self.debate_manager.synthesis_chain)
    
    def test_get_market_context(self):
        """Test that market context is returned"""
        context = self.debate_manager.get_market_context()
        self.assertIsInstance(context, str)
        self.assertIn("market indicators", context.lower())
    
    def test_get_analyst_reports(self):
        """Test that analyst reports are retrieved"""
        # Setup mock agents to return reports
        for name, agent in self.analyst_team.items():
            agent.invoke.return_value = {'text': f'Report from {name}'}

        # Call the method
        stock_data = {'key': 'value'}
        reports = self.debate_manager.get_analyst_reports('AAPL', stock_data)

        # Check results
        self.assertIsInstance(reports, dict)
        self.assertEqual(len(reports), len(self.analyst_team))

    def test_get_investor_opinions(self):
        """Test that investor opinions are retrieved"""
        # Setup mock agents to return opinions
        for name, agent in self.investor_team.items():
            agent.invoke.return_value = {'text': f'Opinion from {name}'}

        # Call the method
        stock_data = {'key': 'value'}
        analyst_reports = {'Analyst1': 'Report text'}
        opinions = self.debate_manager.get_investor_opinions('AAPL', stock_data, analyst_reports)

        # Check results
        self.assertIsInstance(opinions, dict)
        self.assertEqual(len(opinions), len(self.investor_team))
    
    def test_synthesize_decision(self):
        """Test that decision synthesis works correctly"""
        # Call the method
        investor_opinions = {'Investor1': 'Opinion text'}
        result = self.debate_manager.synthesize_decision('AAPL', investor_opinions)

        # Check results - synthesis returns a dict with decision info
        self.assertIsNotNone(result)
        self.assertIsInstance(result, (dict, str))
    
    def test_run_debate(self):
        """Test that the full debate process runs correctly"""
        # Setup mocks
        self.debate_manager.get_analyst_reports = MagicMock(return_value={'Analyst1': 'Report'})
        self.debate_manager.get_investor_opinions = MagicMock(return_value={'Investor1': 'Opinion'})
        self.debate_manager.synthesize_decision = MagicMock(return_value='Decision')
        
        # Call the method
        tickers = ['AAPL', 'MSFT']
        stock_data = {'AAPL': {}, 'MSFT': {}}
        results = self.debate_manager.run_debate(tickers, stock_data)
        
        # Check results
        self.assertEqual(len(results), len(tickers))
        for ticker in tickers:
            self.assertIn(ticker, results)
            result = results[ticker]
            self.assertIn('analyst_reports', result)
            self.assertIn('investor_opinions', result)
            self.assertIn('decision', result)
        
        # Check method calls
        self.assertEqual(self.debate_manager.get_analyst_reports.call_count, len(tickers))
        self.assertEqual(self.debate_manager.get_investor_opinions.call_count, len(tickers))
        self.assertEqual(self.debate_manager.synthesize_decision.call_count, len(tickers))

if __name__ == '__main__':
    unittest.main()