# FinAgents

A multi-agent system that simulates a debate between famous investors analyzing stock investment opportunities.

## Overview

FinAgents creates a virtual investment committee where AI agents with personas of famous investors like Warren Buffett and Cathie Wood debate whether stocks are good investments. The system:

1. Gathers real financial data using yfinance
2. Has specialized analyst agents evaluate different aspects of the stock
3. Has investor agents with unique investment philosophies debate the merits
4. Synthesizes a comprehensive investment recommendation

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
DEFAULT_MODEL=claude-3-7-sonnet-20250219
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

## License

MIT

## DISCLAIMER: 

This project is purely educational. The AI-generated personas are fictional and do not represent real statements or endorsements from Warren Buffett, Ray Dalio, Cathie Wood, Peter Lynch, or Michael Burry.
