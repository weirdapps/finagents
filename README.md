# FinAgents (Archived)

> **DEPRECATED**: This prototype has been superseded by the [trading-hub investment committee](https://github.com/weirdapps/trading-marketplace) — a production 7-agent system with adversarial debate, codified conviction scoring (CIO v33.0), and self-improving backtest loop. This repo is archived for reference only.

A multi-agent system that simulates a debate between famous investors analyzing stock investment opportunities.

## Overview

FinAgents creates a virtual investment committee where AI agents with personas of famous investors like Warren Buffett and Cathie Wood debate whether stocks are good investments. The system:

1. Gathers real financial data using yfinance
2. Has specialized analyst agents evaluate different aspects of the stock
3. Has investor agents with unique investment philosophies debate the merits
4. Synthesizes a comprehensive investment recommendation

## Current Status

> **Prototype**: This system currently uses **pre-generated static responses** instead of live LLM calls. The investor and analyst agents return canned text from `local_claude_responses.py` rather than calling the Anthropic API. Financial data retrieval via yfinance is real, but the AI debate is simulated. See [Making It Operational](#making-it-operational) below for instructions on wiring up real LLM calls.

## Key Features

- **Parallel Processing**: Agents run concurrently for faster analysis
- **Diverse Perspectives**: 5 famous investor personas with unique philosophies
- **Specialized Analysis**: 5 types of analyst agents focus on different aspects
- **Real Market Data**: Uses yfinance to pull actual stock information
- **Comprehensive Output**: Generates detailed reports saved as Markdown files

## Investor Personas

- **Warren Buffett**: Value investing, long-term perspective
- **Ray Dalio**: Macro investing, economic cycles
- **Cathie Wood**: Growth and disruptive innovation
- **Peter Lynch**: Growth at a reasonable price
- **Michael Burry**: Contrarian investing, spotting market inefficiencies

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_MODEL=claude-sonnet-4-5-20250929
STOCK_DATA_SOURCE=yfinance
```

## Usage

Run the main script:
```bash
python main.py
```

The system will analyze Microsoft (MSFT) by default, using all agents in parallel, and save detailed reports to the `results` directory.

## Output Files

For each analyzed stock (e.g., MSFT):

- `results/MSFT_decision.md`: Final synthesized investment recommendation
- `results/MSFT_detailed_analysis.md`: Detailed reports from all analysts and investors

## Project Structure

```
finagents/
├── main.py                      # Main script to run the system
├── src/
│   ├── agents/
│   │   ├── investor_agents.py   # Famous investor personas
│   │   ├── analyst_agents.py    # Financial analyst agents
│   │   ├── debate_manager.py    # Orchestrates the analysis process
│   ├── utils/
│   │   ├── stock_data.py        # Functions for retrieving stock data
├── tests/                       # Comprehensive test suite
│   ├── unit/                    # Unit tests for individual components
│   ├── integration/             # Integration tests for the whole system
├── results/                     # Output directory for analysis reports
├── requirements.txt             # Project dependencies
├── .env                         # Environment variables (API keys)
├── run_tests.py                 # Script to run all tests
├── README.md                    # This file
├── ARCHITECTURE.md              # Detailed system architecture
├── QUICKSTART.md                # Quick start guide
├── PERSONAS.md                  # Detailed guide to agent personas
├── EXTENDING.md                 # Guide for extending the system
```

## Requirements

- Python 3.8+
- Anthropic API key (for Claude 3.7)
- Internet connection (for financial data retrieval)

## Running Tests

The project includes a test suite focusing on core data utilities and file operations:

```bash
python run_tests.py
```

This will run the stock data utility tests and output file tests, providing a detailed report.

## Making It Operational

To convert this prototype into a fully operational system with real LLM calls:

### 1. Wire up the Anthropic API

Replace the `LocalInvestor` and `LocalAnalyst` classes with real LangChain LLM calls. In `src/agents/investor_agents.py` and `src/agents/analyst_agents.py`, the `create_investor_agent()` and `create_analyst_agent()` functions currently return `LocalInvestor`/`LocalAnalyst` objects that serve canned responses. Replace them with LangChain's `ChatAnthropic`:

```python
from langchain_anthropic import ChatAnthropic

def create_investor_agent(persona_name: str):
    llm = ChatAnthropic(model=os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5-20250929"))
    prompt = create_investor_prompt(persona_name)  # Already defined in the file
    return prompt | llm
```

### 2. Remove mock infrastructure

- Delete `local_claude_responses.py` (1,556 lines of static responses)
- Remove `from unittest.mock import MagicMock` from `debate_manager.py`
- Replace `self.llm = MagicMock()` and `self.synthesis_chain = MagicMock()` with real LangChain chain instances

### 3. Add live market context

Replace `debate_manager.py`'s `get_market_context()` static placeholder with real data. Options:
- Use `yfinance` to fetch S&P 500, VIX, and Treasury yields (already a dependency)
- Use a financial news API for current market sentiment

### 4. Make the portfolio path configurable

In `main.py`, the portfolio path is hardcoded. Replace with:
```python
portfolio_path = os.getenv(
    "PORTFOLIO_PATH",
    os.path.expanduser("~/SourceCode/etorotrade/yahoofinance/output/portfolio.csv")
)
```

### 5. Install additional dependency

```bash
pip install langchain-anthropic
```

### 6. Sync setup.py with requirements.txt

Update `setup.py` version constraints to match `requirements.txt` (langchain `>=0.2.0`, langchain-community `>=0.2.0`).

## License

MIT

## DISCLAIMER: 

This project is purely educational. The AI-generated personas are fictional and do not represent real statements or endorsements from Warren Buffett, Ray Dalio, Cathie Wood, Peter Lynch, or Michael Burry.
