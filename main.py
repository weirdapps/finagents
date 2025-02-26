#!/usr/bin/env python3
"""
Main entry point for FinAgents - A multi-agent financial debate system.
This script orchestrates the setup of investor personas, analyst agents, 
and manages the debate about stock investment opportunities.
"""

import os
import logging
import sys
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.investor_agents import create_investor_team
from src.agents.analyst_agents import create_analyst_team
from src.agents.debate_manager import DebateManager
from src.utils.stock_data import get_stock_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Main function to run the financial agents debate system."""
    logger.info("Starting FinAgents System")
    
    # Get stocks to analyze - use MSFT for simplicity
    stocks_to_analyze = ["MSFT"]
    print(f"Analyzing stock: {stocks_to_analyze[0]}")
    
    logger.info(f"Stocks to analyze: {stocks_to_analyze}")
    
    # Create investor team
    investor_team = create_investor_team()
    logger.info(f"Created investor team with {len(investor_team)} investors")
    
    # Create analyst team
    analyst_team = create_analyst_team()
    logger.info(f"Created analyst team with {len(analyst_team)} analysts")
    
    # Get stock data
    stock_data = {}
    for ticker in stocks_to_analyze:
        stock_data[ticker] = get_stock_data(ticker)
    logger.info(f"Retrieved data for {len(stock_data)} stocks")
    
    # Create debate manager
    debate_manager = DebateManager(investor_team, analyst_team)
    
    # Run the debate
    results = debate_manager.run_debate(stocks_to_analyze, stock_data)
    
    # Print results in a more user-friendly format and save to files
    for ticker, result in results.items():
        print("\n" + "="*80)
        print(f"INVESTMENT ANALYSIS FOR {ticker}")
        print("="*80)
        
        print("\nFINAL DECISION:")
        print("-"*50)
        print(result["decision"])
        
        # Save the analysis to files
        output_dir = "results"
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save the final decision
        with open(f"{output_dir}/{ticker}_decision.md", "w") as f:
            f.write(f"# Investment Analysis for {ticker}\n\n")
            f.write(result["decision"])
            
        # Save detailed reports
        with open(f"{output_dir}/{ticker}_detailed_analysis.md", "w") as f:
            f.write(f"# Detailed Analysis for {ticker}\n\n")
            
            f.write("## Analyst Reports\n\n")
            for analyst, report in result["analyst_reports"].items():
                f.write(f"### {analyst}\n\n")
                f.write(report)
                f.write("\n\n---\n\n")
            
            f.write("## Investor Opinions\n\n")
            for investor, opinion in result["investor_opinions"].items():
                f.write(f"### {investor}\n\n")
                f.write(opinion)
                f.write("\n\n---\n\n")
                
        print(f"\nAnalysis saved to:")
        print(f"  - {output_dir}/{ticker}_decision.md (Final Decision)")
        print(f"  - {output_dir}/{ticker}_detailed_analysis.md (Detailed Reports)")
        
        logger.info(f"Completed analysis for {ticker} and saved to files")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nThank you for using FinAgents!")