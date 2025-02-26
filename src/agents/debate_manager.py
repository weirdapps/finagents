"""
Debate Manager Module

This module orchestrates the debate between investor agents about stock investment opportunities.
It coordinates the analysis from analyst agents and facilitates the discussion between investors.
"""

import os
import logging
from typing import Dict, List, Any
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)

class DebateManager:
    """
    Manages the debate between investor agents about stock investment opportunities.
    
    Responsibilities:
    1. Coordinate the analysis from analyst agents
    2. Facilitate the discussion between investors
    3. Synthesize the final investment decision
    """
    
    def __init__(self, investor_team: Dict[str, Any], analyst_team: Dict[str, Any]):
        """Initialize the debate manager with investor and analyst teams."""
        self.investor_team = investor_team
        self.analyst_team = analyst_team
        
        # Initialize the debate moderator LLM with timeout
        model_name = os.getenv("DEFAULT_MODEL", "claude-3-7-sonnet-20250219")
        self.llm = ChatAnthropic(
            model=model_name,
            temperature=0.2,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=300.0  # 5 minute timeout
        )
        
        # Create the synthesis prompt
        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a debate moderator and investment decision synthesizer.
            
Your task is to synthesize the diverse opinions of various investors who have analyzed a stock.
Summarize each investor's perspective, highlighting areas of agreement and disagreement.
Identify the key factors that influenced their decisions.
Provide a final investment recommendation based on the majority view and the strength of the arguments.
Be impartial and focus on the quality of reasoning rather than simply counting votes.

Provide your synthesis in the following format:
1. Summary of Investor Opinions
2. Areas of Agreement
3. Areas of Disagreement
4. Key Decision Factors
5. Final Recommendation: [BUY/HOLD/SELL]
6. Confidence Level: [HIGH/MEDIUM/LOW]
7. Key Risks and Considerations
"""),
            ("human", """
Stock Ticker: {ticker}
Market Context: {market_context}

Investor Opinions:
{investor_opinions}

Please synthesize these perspectives and provide a final investment recommendation.
""")
        ])
        
        self.synthesis_chain = LLMChain(llm=self.llm, prompt=self.synthesis_prompt)
    
    def get_market_context(self) -> str:
        """Get the current market context (overall market conditions, economic indicators, etc.)."""
        # In a real implementation, this would pull data from financial APIs or news sources
        # For now, we'll use a simplified placeholder
        return """
Current market indicators:
- S&P 500: Up 0.8% for the week
- Volatility Index (VIX): 18.5 (moderate volatility)
- 10-Year Treasury Yield: 4.3%
- Federal Reserve Stance: Maintaining current interest rates with a neutral outlook
- Economic Growth: Moderate GDP growth of 2.3% annually
- Inflation: 3.2% annually, slightly above target
- Unemployment Rate: 3.9%, relatively low
- Consumer Sentiment: Slightly positive
"""
    
    def get_analyst_reports(self, ticker: str, stock_data: Dict[str, Any]) -> Dict[str, str]:
        """Get reports from all analysts for a specific stock in parallel."""
        from concurrent.futures import ThreadPoolExecutor
        import concurrent.futures
        import time
        
        analyst_reports = {}
        logger.info(f"Starting parallel analysis for {ticker} with {len(self.analyst_team)} analysts")
        print(f"\nGathering analyst reports for {ticker}...")
        
        def get_analyst_report(analyst_data):
            name, agent = analyst_data
            start_time = time.time()
            logger.info(f"Thread started for {name}'s report on {ticker}")
            print(f"  • Working on {name}'s analysis...")
            
            try:
                # Invoke the analyst agent
                report = agent.invoke({
                    "ticker": ticker,
                    "stock_data": str(stock_data)
                })
                elapsed = time.time() - start_time
                logger.info(f"Received {name}'s report in {elapsed:.2f} seconds")
                print(f"  ✓ Completed {name}'s analysis ({elapsed:.2f}s)")
                return name, report["text"]
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"Error getting report from {name} after {elapsed:.2f}s: {e}")
                print(f"  ✗ Failed to get {name}'s analysis: {str(e)}")
                return name, f"Unable to generate report due to: {str(e)}"
        
        # Use ThreadPoolExecutor to run API calls in parallel
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(self.analyst_team)) as executor:
            future_to_analyst = {
                executor.submit(get_analyst_report, (name, agent)): name 
                for name, agent in self.analyst_team.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_analyst):
                try:
                    name, report = future.result()
                    analyst_reports[name] = report
                except Exception as e:
                    logger.error(f"Thread error: {e}")
        
        total_time = time.time() - start_time
        logger.info(f"Completed all analyst reports for {ticker} in {total_time:.2f} seconds")
        print(f"All analyst reports completed in {total_time:.2f} seconds\n")
        
        return analyst_reports
    
    def get_investor_opinions(self, ticker: str, stock_data: Dict[str, Any], analyst_reports: Dict[str, str]) -> Dict[str, str]:
        """Get opinions from all investors for a specific stock in parallel."""
        from concurrent.futures import ThreadPoolExecutor
        import concurrent.futures
        import time
        
        investor_opinions = {}
        market_context = self.get_market_context()
        
        # Format analyst reports as a string
        analyst_reports_str = "\n\n".join([f"{name}:\n{report}" for name, report in analyst_reports.items()])
        
        logger.info(f"Starting parallel investor opinions for {ticker} with {len(self.investor_team)} investors")
        print(f"\nGathering investor opinions for {ticker}...")
        
        def get_investor_opinion(investor_data):
            name, agent = investor_data
            start_time = time.time()
            logger.info(f"Thread started for {name}'s opinion on {ticker}")
            print(f"  • Working on {name}'s investment analysis...")
            
            try:
                # Invoke the investor agent
                opinion = agent.invoke({
                    "ticker": ticker,
                    "stock_info": str(stock_data),
                    "market_context": market_context,
                    "analyst_reports": analyst_reports_str
                })
                elapsed = time.time() - start_time
                logger.info(f"Received {name}'s opinion in {elapsed:.2f} seconds")
                print(f"  ✓ Completed {name}'s investment analysis ({elapsed:.2f}s)")
                return name, opinion["text"]
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"Error getting opinion from {name} after {elapsed:.2f}s: {e}")
                print(f"  ✗ Failed to get {name}'s opinion: {str(e)}")
                return name, f"Unable to generate opinion due to: {str(e)}"
        
        # Use ThreadPoolExecutor to run API calls in parallel
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(self.investor_team)) as executor:
            future_to_investor = {
                executor.submit(get_investor_opinion, (name, agent)): name 
                for name, agent in self.investor_team.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_investor):
                try:
                    name, opinion = future.result()
                    investor_opinions[name] = opinion
                except Exception as e:
                    logger.error(f"Thread error: {e}")
        
        total_time = time.time() - start_time
        logger.info(f"Completed all investor opinions for {ticker} in {total_time:.2f} seconds")
        print(f"All investor opinions completed in {total_time:.2f} seconds\n")
        
        return investor_opinions
    
    def synthesize_decision(self, ticker: str, investor_opinions: Dict[str, str]) -> Dict[str, Any]:
        """Synthesize the final investment decision based on investor opinions."""
        import time
        
        # Format investor opinions as a string
        investor_opinions_str = "\n\n".join([f"{name}:\n{opinion}" for name, opinion in investor_opinions.items()])
        
        print(f"\nSynthesizing final investment decision for {ticker}...")
        start_time = time.time()
        logger.info(f"Starting synthesis for {ticker}")
        
        try:
            # Invoke the synthesis chain
            synthesis = self.synthesis_chain.invoke({
                "ticker": ticker,
                "market_context": self.get_market_context(),
                "investor_opinions": investor_opinions_str
            })
            
            elapsed = time.time() - start_time
            logger.info(f"Completed synthesis for {ticker} in {elapsed:.2f} seconds")
            print(f"Decision synthesis completed in {elapsed:.2f} seconds\n")
            
            return synthesis["text"]
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Error during synthesis for {ticker} after {elapsed:.2f}s: {e}")
            print(f"Failed to complete decision synthesis: {str(e)}")
            return f"Unable to synthesize decision due to: {str(e)}"
    
    def run_debate(self, tickers: List[str], stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full debate process for a list of stocks."""
        results = {}
        
        for ticker in tickers:
            logger.info(f"Starting debate for {ticker}")
            
            # Get analyst reports
            analyst_reports = self.get_analyst_reports(ticker, stock_data.get(ticker, {}))
            
            # Get investor opinions
            investor_opinions = self.get_investor_opinions(ticker, stock_data.get(ticker, {}), analyst_reports)
            
            # Synthesize final decision
            decision = self.synthesize_decision(ticker, investor_opinions)
            
            results[ticker] = {
                "analyst_reports": analyst_reports,
                "investor_opinions": investor_opinions,
                "decision": decision
            }
            
            logger.info(f"Completed debate for {ticker}")
        
        return results