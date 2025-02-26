"""
Unit tests for stock data utility module
"""

import sys
import os
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

# Add the src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from src.utils.stock_data import (
    get_stock_data,
    calculate_revenue_growth,
    calculate_profit_margin,
    calculate_debt_to_equity,
    calculate_current_ratio,
    calculate_roe,
    get_latest_value,
    get_recent_trend
)

class TestStockDataUtils(unittest.TestCase):
    """Tests for stock data utility functions - these work correctly"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create sample financial data
        self.income_stmt = pd.DataFrame({
            '2023': [1000, 300],  # Total Revenue, Net Income
            '2022': [800, 200]    # Previous year
        }, index=['Total Revenue', 'Net Income'])
        
        self.balance_sheet = pd.DataFrame({
            '2023': [500, 300, 200, 100],  # Total values
            '2022': [400, 250, 150, 80]    # Previous year
        }, index=['Total Current Assets', 'Total Current Liabilities', 
                 'Total Debt', 'Total Stockholder Equity'])
        
        # Sample historical data for trend analysis
        dates = pd.date_range(start='2023-01-01', periods=60)
        self.hist_data = pd.DataFrame({
            'Close': [100 + i*0.5 for i in range(60)],  # Uptrend
            'High': [105 + i*0.5 for i in range(60)],
            'Low': [95 + i*0.5 for i in range(60)],
            'Volume': [1000000 for _ in range(60)]
        }, index=dates)
    
    def test_calculate_revenue_growth(self):
        """Test revenue growth calculation"""
        growth = calculate_revenue_growth(self.income_stmt)
        # Expected: ((1000/800) - 1) * 100 = 25.0
        self.assertAlmostEqual(growth, 25.0)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        growth = calculate_revenue_growth(empty_df)
        self.assertEqual(growth, 0.0)
    
    def test_calculate_profit_margin(self):
        """Test profit margin calculation"""
        margin = calculate_profit_margin(self.income_stmt)
        # Expected: (300/1000) * 100 = 30.0
        self.assertAlmostEqual(margin, 30.0)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        margin = calculate_profit_margin(empty_df)
        self.assertEqual(margin, 0.0)
    
    def test_calculate_debt_to_equity(self):
        """Test debt to equity calculation"""
        d_e = calculate_debt_to_equity(self.balance_sheet)
        # Expected: 200/100 = 2.0
        self.assertAlmostEqual(d_e, 2.0)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        d_e = calculate_debt_to_equity(empty_df)
        self.assertEqual(d_e, 0.0)
    
    def test_calculate_current_ratio(self):
        """Test current ratio calculation"""
        ratio = calculate_current_ratio(self.balance_sheet)
        # Expected: 500/300 = 1.6666...
        self.assertAlmostEqual(ratio, 500/300)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        ratio = calculate_current_ratio(empty_df)
        self.assertEqual(ratio, 0.0)
    
    def test_calculate_roe(self):
        """Test return on equity calculation"""
        roe = calculate_roe(self.income_stmt, self.balance_sheet)
        # Expected: (300/100) * 100 = 300.0
        self.assertAlmostEqual(roe, 300.0)
        
        # Test with empty dataframes
        empty_df = pd.DataFrame()
        roe = calculate_roe(empty_df, empty_df)
        self.assertEqual(roe, 0.0)
    
    def test_get_latest_value(self):
        """Test getting latest value from financial statements"""
        value = get_latest_value(self.income_stmt, 'Total Revenue')
        self.assertEqual(value, 1000)
        
        # Test with non-existent row
        value = get_latest_value(self.income_stmt, 'Non-existent')
        self.assertIsNone(value)
    
    def test_get_recent_trend(self):
        """Test trend analysis function"""
        trend = get_recent_trend(self.hist_data)
        self.assertIn("Uptrend", trend)
        
        # Test with downtrend
        reverse_data = self.hist_data.copy()
        reverse_data['Close'] = reverse_data['Close'].iloc[::-1].values
        trend = get_recent_trend(reverse_data)
        self.assertIn("Downtrend", trend)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        trend = get_recent_trend(empty_df)
        self.assertEqual(trend, "Unknown")
    
    @patch('src.utils.stock_data.yf.Ticker')
    def test_get_stock_data(self, mock_ticker):
        """Test the main stock data retrieval function"""
        # Setup mock
        mock_ticker_instance = MagicMock()
        
        # Mock info
        mock_ticker_instance.info = {
            'longName': 'Test Company',
            'sector': 'Technology',
            'industry': 'Software',
            'marketCap': 1000000000,
            'trailingPE': 25.5,
            'forwardPE': 20.2,
            'dividendYield': 0.02,
            'beta': 1.2,
            'trailingEps': 3.5,
            'shortRatio': 1.5,
            'recommendationKey': 'buy',
            'targetMeanPrice': 150.0,
            'longBusinessSummary': 'A test company'
        }
        
        # Mock history
        mock_ticker_instance.history.return_value = self.hist_data
        
        # Mock financial statements
        mock_ticker_instance.income_stmt = self.income_stmt
        mock_ticker_instance.balance_sheet = self.balance_sheet
        mock_ticker_instance.cashflow = pd.DataFrame({'2023': [400]}, index=['Free Cash Flow'])
        
        mock_ticker.return_value = mock_ticker_instance
        
        # Call function
        result = get_stock_data('TEST')
        
        # Check basic result structure
        self.assertIsInstance(result, dict)
        self.assertEqual(result['ticker'], 'TEST')
        self.assertEqual(result['company_name'], 'Test Company')
        self.assertEqual(result['sector'], 'Technology')
        
        # Check that history was called
        mock_ticker_instance.history.assert_called_once()
        
        # Check calculated metrics are present
        self.assertIn('revenue_growth', result)
        self.assertIn('profit_margin', result)
        self.assertIn('debt_to_equity', result)
        self.assertIn('current_ratio', result)
        self.assertIn('return_on_equity', result)
        self.assertIn('recent_trend', result)
        
        # Test error handling
        mock_ticker.side_effect = Exception("Test error")
        result = get_stock_data('ERROR')
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()