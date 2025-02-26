# Extending FinAgents

This guide provides instructions for extending and enhancing the FinAgents system.

## Adding New Investor Personas

1. **Edit the `INVESTOR_PERSONAS` dictionary** in `src/agents/investor_agents.py`:

```python
"New Investor Name": {
    "philosophy": "Detailed description of investment philosophy",
    "risk_profile": "Risk tolerance and approach description",
    "famous_quotes": [
        "Notable quote 1",
        "Notable quote 2",
        "Notable quote 3",
    ]
}
```

2. The system will automatically create an agent for the new investor using the provided information.

## Adding New Analyst Types

1. **Edit the `ANALYST_TYPES` dictionary** in `src/agents/analyst_agents.py`:

```python
"New Analyst Type": {
    "focus": "Detailed description of areas of focus",
    "methodology": "Description of analysis methodology"
}
```

2. The system will automatically create an agent for the new analyst using the provided information.

## Enhancing Prompts

Both investor and analyst agents use prompt templates that can be enhanced:

1. **Analyst Prompts**: Modify the `create_analyst_prompt` function in `src/agents/analyst_agents.py`
2. **Investor Prompts**: Modify the `create_investor_prompt` function in `src/agents/investor_agents.py`

## Adding Multiple Stock Analysis

To analyze multiple stocks at once:

1. **Edit the `main.py` file** to support multiple tickers:

```python
# Change this line in src/main.py
stocks_to_analyze = ["AAPL", "MSFT", "GOOGL"]
```

2. The system will process each stock sequentially, producing separate analysis files for each.

## Adding a Web Interface

You can create a simple web interface using Flask:

1. **Install Flask**:
```bash
pip install flask
```

2. **Create a web app** (e.g., `app.py`):
```python
from flask import Flask, render_template, request
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import analyze_stock

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        result = analyze_stock(ticker)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
```

3. **Modify `main.py`** to expose an `analyze_stock` function
4. **Create HTML templates** in a `templates` folder

## Adding News Data Integration

Enhance the analysis with current news:

1. **Install a news API client**:
```bash
pip install newsapi-python
```

2. **Create a news utility** (e.g., `src/utils/news_data.py`):
```python
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def get_company_news(ticker, company_name, days=7):
    """Get recent news about a company."""
    query = f"{ticker} OR {company_name}"
    news = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='relevancy',
        page_size=5
    )
    
    return news['articles']
```

3. **Integrate the news data** into the analysis process

## Performance Tracking

Add a feature to track the performance of recommendations:

1. **Create a tracking database** (e.g., using SQLite)
2. **Store recommendations** with timestamp and price
3. **Implement a performance check** to compare current prices with recommendations
4. **Generate performance reports**

## Implementing Tool Use for Agents

Enhance agents with the ability to use external tools:

1. **Define tools** for agent use (e.g., calculators, data lookups)
2. **Convert agents to AgentExecutor** instances with the tools
3. **Implement agent logic** for deciding when to use tools

Example tool definition:
```python
from langchain.tools import Tool

calculator_tool = Tool(
    name="Calculator",
    func=lambda x: eval(x),
    description="Useful for performing calculations"
)

# Then add the tools to the agent
agent = create_agent_with_tools(tools=[calculator_tool])
```

## Advanced Features

- **Sentiment Analysis**: Incorporate social media sentiment
- **Alternative Data**: Add alternative data sources (e.g., satellite imagery, app downloads)
- **Backtesting**: Implement historical testing of the system's recommendations
- **Scenario Analysis**: Add scenario-based stress testing
- **Portfolio Construction**: Extend to build optimal portfolios from multiple stock analyses