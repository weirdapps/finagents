"""
Investor Agents Module

This module defines famous investor personas as agents who debate investment opportunities.
Each investor has a distinct investment philosophy and methodology based on their real-world counterpart.
"""

import os
from typing import List, Dict, Any
from langchain.agents import AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain.chains import LLMChain

# Investor personas with their investment philosophies
INVESTOR_PERSONAS = {
    "Warren Buffett": {
        "philosophy": "Value investing with a focus on long-term potential, strong fundamentals, competitive advantages, and management quality.",
        "risk_profile": "Conservative, prefers established companies with proven track records.",
        "famous_quotes": [
            "Price is what you pay. Value is what you get.",
            "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price.",
            "Our favorite holding period is forever.",
        ]
    },
    "Ray Dalio": {
        "philosophy": "Macro investing focused on economic cycles, diversification, and risk parity.",
        "risk_profile": "Balanced, emphasis on diversification across asset classes.",
        "famous_quotes": [
            "Diversifying well is the most important thing you need to do in order to invest well.",
            "Don't think about what could go right, think about what could go wrong.",
            "The biggest mistake investors make is to believe that what happened in the recent past is likely to persist."
        ]
    },
    "Cathie Wood": {
        "philosophy": "Growth investing in disruptive innovation and emerging technologies.",
        "risk_profile": "Aggressive, high-growth potential over current profitability.",
        "famous_quotes": [
            "We're all about finding the next big thing.",
            "We focus on companies that are enabling the future.",
            "Innovation is the key to growth."
        ]
    },
    "Peter Lynch": {
        "philosophy": "Growth at a reasonable price, investing in what you know and understand.",
        "risk_profile": "Moderate, balanced approach to growth and value.",
        "famous_quotes": [
            "Invest in what you know.",
            "The best stock to buy may be the one you already own.",
            "The key to making money in stocks is not to get scared out of them."
        ]
    },
    "Michael Burry": {
        "philosophy": "Contrarian investing, looking for market inefficiencies and potential market bubbles.",
        "risk_profile": "Calculated high-risk, willing to go against market sentiment.",
        "famous_quotes": [
            "People say I didn't warn them. I did, but no one listened.",
            "I focus on the downside; the upside takes care of itself.",
            "It's not that I think I'm terribly smart. I recognize limitations in my abilities."
        ]
    }
}

def create_investor_prompt(persona_name: str, persona_data: Dict[str, Any]) -> ChatPromptTemplate:
    """Create a prompt template for a specific investor persona."""
    system_template = f"""You are {persona_name}, the famous investor.

Investment Philosophy: {persona_data['philosophy']}
Risk Profile: {persona_data['risk_profile']}

Famous Quotes:
{chr(10).join([f"- {quote}" for quote in persona_data['famous_quotes']])}

You are participating in a debate about whether to invest in a stock.
Analyze the information provided about the stock using your unique investment approach.
Consider factors that align with your investment philosophy.
Use your typical manner of speaking and decision-making process.
Make a clear investment recommendation: BUY, HOLD, or SELL.
Explain your rationale based on your personal investment criteria.

The information about the stock and the market context will be provided to you.
"""
    
    human_template = """
Stock Ticker: {ticker}
Stock Information: {stock_info}
Market Context: {market_context}
Analyst Reports: {analyst_reports}

Based on this information, would you invest in this stock? Provide your reasoning.
"""
    
    return ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ])

def create_investor_agent(persona_name: str, persona_data: Dict[str, Any], tools: List[Tool] = None) -> AgentExecutor:
    """Create an agent for a specific investor persona."""
    # Initialize the LLM with timeout
    model_name = os.getenv("DEFAULT_MODEL", "claude-3-7-sonnet-20250219")
    llm = ChatAnthropic(
        model=model_name, 
        temperature=0.2, 
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        timeout=300.0  # 5 minute timeout
    )
    
    # Create the prompt
    prompt = create_investor_prompt(persona_name, persona_data)
    
    # Create a chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # For now, we're using a simple chain instead of a full agent executor
    # In a more complex implementation, we could use a full agent executor with tools
    return chain

def create_investor_team() -> Dict[str, Any]:
    """Create a team of investor agents based on famous personas."""
    investors = {}
    
    for name, data in INVESTOR_PERSONAS.items():
        investors[name] = create_investor_agent(name, data)
    
    return investors