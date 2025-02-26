"""
Stock Data Utility Module

This module provides functions for retrieving and processing stock data.
It fetches financial data using yfinance and prepares it for analysis.
"""

import os
import logging
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

def get_stock_data(ticker: str, period: str = "1y") -> Dict[str, Any]:
    """
    Retrieve comprehensive stock data for a given ticker.
    
    Args:
        ticker: The stock ticker symbol
        period: The time period for historical data (default: 1 year)
        
    Returns:
        A dictionary containing various stock data metrics
    """
    logger.info(f"Fetching data for {ticker}")
    
    try:
        # Get stock info
        stock = yf.Ticker(ticker)
        
        # Basic company info
        info = stock.info
        
        # Historical price data
        hist = stock.history(period=period)
        
        # Calculate some basic metrics
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            year_high = hist['High'].max()
            year_low = hist['Low'].min()
            avg_volume = hist['Volume'].mean()
            price_change = ((current_price / hist['Close'].iloc[0]) - 1) * 100  # percentage
        else:
            current_price = year_high = year_low = avg_volume = price_change = 0
        
        # Get financial statements if available
        try:
            income_stmt = stock.income_stmt
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
        except Exception as e:
            logger.warning(f"Could not fetch financial statements for {ticker}: {e}")
            income_stmt = balance_sheet = cash_flow = pd.DataFrame()
        
        # Format the data
        stock_data = {
            "ticker": ticker,
            "company_name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "current_price": current_price,
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "forward_pe": info.get("forwardPE", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "52w_high": year_high,
            "52w_low": year_low,
            "52w_change": price_change,
            "avg_volume": avg_volume,
            "beta": info.get("beta", 0),
            "eps": info.get("trailingEps", 0),
            "short_ratio": info.get("shortRatio", 0),
            "recommendation": info.get("recommendationKey", ""),
            "target_price": info.get("targetMeanPrice", 0),
            
            # Add key financial metrics from statements
            "revenue_growth": calculate_revenue_growth(income_stmt),
            "profit_margin": calculate_profit_margin(income_stmt),
            "debt_to_equity": calculate_debt_to_equity(balance_sheet),
            "current_ratio": calculate_current_ratio(balance_sheet),
            "return_on_equity": calculate_roe(income_stmt, balance_sheet),
            "free_cash_flow": get_latest_value(cash_flow, "Free Cash Flow"),
            
            # Recent price trend
            "recent_trend": get_recent_trend(hist),
            
            # Company description
            "business_summary": info.get("longBusinessSummary", ""),
        }
        
        return stock_data
        
    except Exception as e:
        logger.error(f"Error retrieving data for {ticker}: {e}")
        return {
            "ticker": ticker,
            "error": str(e)
        }

def calculate_revenue_growth(income_stmt: pd.DataFrame) -> float:
    """Calculate year-over-year revenue growth rate."""
    if income_stmt.empty or 'Total Revenue' not in income_stmt.index:
        return 0.0
    
    revenues = income_stmt.loc['Total Revenue']
    if len(revenues) >= 2:
        current = revenues.iloc[0]
        previous = revenues.iloc[1]
        if previous and previous != 0:
            return ((current / previous) - 1) * 100
    return 0.0

def calculate_profit_margin(income_stmt: pd.DataFrame) -> float:
    """Calculate net profit margin."""
    if income_stmt.empty or 'Net Income' not in income_stmt.index or 'Total Revenue' not in income_stmt.index:
        return 0.0
    
    net_income = income_stmt.loc['Net Income'].iloc[0] if not income_stmt.empty else 0
    total_revenue = income_stmt.loc['Total Revenue'].iloc[0] if not income_stmt.empty else 0
    
    if total_revenue and total_revenue != 0:
        return (net_income / total_revenue) * 100
    return 0.0

def calculate_debt_to_equity(balance_sheet: pd.DataFrame) -> float:
    """Calculate debt-to-equity ratio."""
    if balance_sheet.empty:
        return 0.0
    
    total_debt = get_latest_value(balance_sheet, "Total Debt") or 0
    total_equity = get_latest_value(balance_sheet, "Total Stockholder Equity") or 0
    
    if total_equity and total_equity != 0:
        return total_debt / total_equity
    return 0.0

def calculate_current_ratio(balance_sheet: pd.DataFrame) -> float:
    """Calculate current ratio (current assets / current liabilities)."""
    if balance_sheet.empty:
        return 0.0
    
    current_assets = get_latest_value(balance_sheet, "Total Current Assets") or 0
    current_liabilities = get_latest_value(balance_sheet, "Total Current Liabilities") or 0
    
    if current_liabilities and current_liabilities != 0:
        return current_assets / current_liabilities
    return 0.0

def calculate_roe(income_stmt: pd.DataFrame, balance_sheet: pd.DataFrame) -> float:
    """Calculate Return on Equity (ROE)."""
    if income_stmt.empty or balance_sheet.empty:
        return 0.0
    
    net_income = get_latest_value(income_stmt, "Net Income") or 0
    shareholder_equity = get_latest_value(balance_sheet, "Total Stockholder Equity") or 0
    
    if shareholder_equity and shareholder_equity != 0:
        return (net_income / shareholder_equity) * 100
    return 0.0

def get_latest_value(df: pd.DataFrame, row_name: str) -> Optional[float]:
    """Get the most recent value from a financial statement row."""
    if df.empty or row_name not in df.index:
        return None
    
    return df.loc[row_name].iloc[0]

def get_recent_trend(hist: pd.DataFrame) -> str:
    """Analyze recent price trend (last 30 days)."""
    if hist.empty:
        return "Unknown"
    
    # Get the last 30 days of data
    recent = hist.tail(30)
    
    # Calculate the overall change
    start_price = recent['Close'].iloc[0]
    end_price = recent['Close'].iloc[-1]
    
    percent_change = ((end_price / start_price) - 1) * 100
    
    # Simple trend analysis
    if percent_change > 5:
        return "Strong Uptrend"
    elif percent_change > 2:
        return "Moderate Uptrend"
    elif percent_change > -2:
        return "Sideways"
    elif percent_change > -5:
        return "Moderate Downtrend"
    else:
        return "Strong Downtrend"