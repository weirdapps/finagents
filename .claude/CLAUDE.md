# FinAgents - Project Instructions for Claude Code

## Project Overview

Multi-agent system that simulates a debate between famous investor personas (Buffett, Dalio, Wood, Lynch, Burry) analyzing stock investment opportunities using real market data.

**Language:** Python 3.8+
**Frameworks:** LangChain + Anthropic Claude API
**Data Source:** yfinance

## Architecture

```
main.py                          # Entry point (analyzes MSFT by default)
src/
  agents/
    investor_agents.py           # 5 famous investor personas
    analyst_agents.py            # 5 specialized analyst agents
    debate_manager.py            # Orchestrates analysis pipeline
  utils/
    stock_data.py                # yfinance data retrieval
results/                         # Output: {TICKER}_decision.md, {TICKER}_detailed_analysis.md
tests/
  unit/                          # Unit tests
  integration/                   # Integration tests
```

## Commands

| Command | Purpose |
|---------|---------|
| `python main.py` | Run analysis (MSFT default) |
| `python run_tests.py` | Run test suite |
| `source venv/bin/activate` | Activate virtualenv |

## Key Dependencies

- `langchain` + `langchain-anthropic` for agent orchestration
- `yfinance` for market data
- `pandas` for data processing
- `python-dotenv` for env management

## Environment

Requires `.env` with `ANTHROPIC_API_KEY`, `DEFAULT_MODEL`, `STOCK_DATA_SOURCE`.

## Conventions

- Agents run concurrently for performance
- Output saved as Markdown in `results/`
- Educational project - all output must include disclaimers that this is NOT investment advice
