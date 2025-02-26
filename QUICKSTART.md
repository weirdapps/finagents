# FinAgents Quick Start Guide

This guide will help you get started with FinAgents quickly.

## Prerequisites

- Python 3.8+ installed
- An Anthropic API key for Claude 3.7
- Internet connection for financial data retrieval

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd finagents
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**
   
   Edit the `.env` file and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   DEFAULT_MODEL=claude-3-7-sonnet-20250219
   STOCK_DATA_SOURCE=yfinance
   ```

## Running the Application

```bash
python src/main.py
```

By default, the system will analyze Microsoft (MSFT) stock. You'll see real-time progress as each agent completes its analysis in parallel.

## Understanding the Results

The system generates two types of files in the `analysis_results` directory:

1. **Decision Summary**: `MSFT_decision.md`
   - Final investment recommendation (Buy/Hold/Sell)
   - Confidence level
   - Summary of each investor's opinion
   - Areas of agreement and disagreement
   - Key decision factors
   - Risk considerations

2. **Detailed Analysis**: `MSFT_detailed_analysis.md`
   - Complete analyst reports from all 5 specialist perspectives
   - Full investor opinions from all 5 famous investor personas

## Customizing the System

### Analyzing Different Stocks

Edit the `main.py` file to change the default stock:

```python
# Change this line in src/main.py
stocks_to_analyze = ["AAPL"]  # or any ticker symbol
```

### Adding New Investor Personas

Edit the `INVESTOR_PERSONAS` dictionary in `src/agents/investor_agents.py`:

```python
"New Investor Name": {
    "philosophy": "Description of investment philosophy",
    "risk_profile": "Risk tolerance description",
    "famous_quotes": [
        "Notable quote 1",
        "Notable quote 2",
    ]
}
```

### Adding New Analyst Types

Edit the `ANALYST_TYPES` dictionary in `src/agents/analyst_agents.py`:

```python
"New Analyst Type": {
    "focus": "Areas of focus for this analyst",
    "methodology": "Analysis approach description"
}
```

## Performance Considerations

- Each analyst and investor requires an API call to Claude 3.7
- For a single stock analysis, expect approximately:
  - 5 analyst API calls
  - 5 investor API calls
  - 1 synthesis API call
  - Total runtime: ~1 minute with parallel processing

## Example Output

The system produces a comprehensive investment analysis like this:

```
# Investment Synthesis: Microsoft Corporation (MSFT)

## 1. Summary of Investor Opinions

**Warren Buffett (HOLD)**: Admires Microsoft's wide economic moat, exceptional profit margins...
**Cathie Wood (HOLD)**: Recognizes Microsoft's AI initiatives and Azure growth...
...

## 5. Final Recommendation: HOLD

## 6. Confidence Level: MEDIUM

## 7. Key Risks and Considerations
- Valuation Risk: At a P/E of 32, Microsoft has limited room for execution missteps...
...
```

## Troubleshooting

- **API Key Issues**: Ensure your Anthropic API key is correctly set in the `.env` file
- **Data Retrieval Errors**: Check your internet connection; yfinance requires internet access
- **Timeouts**: If you encounter timeouts, increase the timeout value in agent configuration files