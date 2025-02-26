"""
Analyst Agents Module

This module defines financial analyst agents that gather and analyze information
about stocks to provide reports for the investor agents to debate.
"""

import os
from typing import Dict, List, Any
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Analyst types with their focus areas
ANALYST_TYPES = {
    "Fundamental Analyst": {
        "focus": "Financial statements, earnings, revenue growth, profit margins, debt levels, and cash flow.",
        "methodology": "Analyzes financial health and intrinsic value through balance sheets, income statements, and cash flow statements."
    },
    "Technical Analyst": {
        "focus": "Price patterns, trading volume, moving averages, and technical indicators.",
        "methodology": "Studies price charts and market statistics to identify trends and potential reversal points."
    },
    "Industry Analyst": {
        "focus": "Industry trends, competitive positioning, market share, and regulatory environment.",
        "methodology": "Evaluates how a company performs relative to its industry peers and assesses industry growth prospects."
    },
    "Quantitative Analyst": {
        "focus": "Statistical patterns, financial models, and mathematical algorithms.",
        "methodology": "Uses data-driven models and statistical analysis to evaluate investment opportunities."
    },
    "ESG Analyst": {
        "focus": "Environmental impact, social responsibility, and corporate governance.",
        "methodology": "Assesses non-financial performance indicators related to sustainability and ethical practices."
    }
}

def create_analyst_prompt(analyst_type: str, analyst_data: Dict[str, str]) -> ChatPromptTemplate:
    """Create a prompt template for a specific analyst type."""
    system_template = f"""You are a {analyst_type}.

Focus Areas: {analyst_data['focus']}
Methodology: {analyst_data['methodology']}

Your task is to analyze a stock from your specialized perspective.
Provide detailed analysis based on the data provided.
Focus only on your area of expertise and provide actionable insights.
Do not make definitive buy/sell recommendations - leave that to the investors.
Instead, highlight the key factors from your perspective that would influence an investment decision.

The stock data will be provided to you.
"""
    
    human_template = """
Stock Ticker: {ticker}
Stock Data: {stock_data}

Please provide your specialized analysis for this stock.
"""
    
    return ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ])

def create_analyst_agent(analyst_type: str, analyst_data: Dict[str, str]) -> LLMChain:
    """Create an agent for a specific analyst type."""
    # Initialize the LLM with timeout
    model_name = os.getenv("DEFAULT_MODEL", "claude-3-7-sonnet-20250219")
    llm = ChatAnthropic(
        model=model_name,
        temperature=0.1,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        timeout=300.0  # 5 minute timeout
    )
    
    # Create the prompt
    prompt = create_analyst_prompt(analyst_type, analyst_data)
    
    # Create a chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain

def create_analyst_team() -> Dict[str, LLMChain]:
    """Create a team of analyst agents."""
    analysts = {}
    
    for name, data in ANALYST_TYPES.items():
        analysts[name] = create_analyst_agent(name, data)
    
    return analysts