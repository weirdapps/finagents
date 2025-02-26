# FinAgents Architecture

## Overview

FinAgents is a multi-agent system that simulates a debate between famous investors analyzing stock investment opportunities. The system uses LangChain and Claude 3.7 to create a team of agents with different personas and investment philosophies, analyzing real market data in parallel.

## System Architecture

### 1. Data Layer

- **Stock Data Utility** (`src/utils/stock_data.py`): 
  - Fetches financial data using yfinance API
  - Processes and formats data for agent consumption
  - Calculates key financial metrics (PE ratio, growth rates, etc.)
  - Extracts technical indicators and recent trends

### 2. Agent Layer

#### Analyst Agents (`src/agents/analyst_agents.py`)

These specialized agents provide focused analysis on specific aspects of a stock:

- **Fundamental Analyst**: Evaluates financial statements, earnings, profit margins, and cash flow
- **Technical Analyst**: Studies price patterns, trading volume, and technical indicators
- **Industry Analyst**: Examines competitive positioning, market share, and industry trends
- **Quantitative Analyst**: Applies statistical analysis and financial models
- **ESG Analyst**: Assesses environmental, social, and governance factors

Each analyst agent is a LangChain chain with:
- Specialized system prompt defining its focus area
- Access to relevant stock data
- Claude 3.7 model with low temperature (0.1) for consistent analysis

#### Investor Agents (`src/agents/investor_agents.py`)

These agents embody the investment philosophies of famous investors:

- **Warren Buffett**: Value investing, focus on fundamentals, competitive advantage
- **Ray Dalio**: Macro perspective, economic cycles, diversification
- **Cathie Wood**: Growth investing in disruptive innovation
- **Peter Lynch**: Growth at a reasonable price, investing in the familiar
- **Michael Burry**: Contrarian approach, focus on market inefficiencies

Each investor agent features:
- Detailed persona prompt with investment philosophy and risk profile
- Famous quotes to maintain authentic voice
- Claude 3.7 model with moderate temperature (0.2) for unique perspectives

### 3. Orchestration Layer

#### Debate Manager (`src/agents/debate_manager.py`)

This central component coordinates the entire process:

- Manages parallel execution of analyst agents
- Collects and formats analyst reports for investor consumption
- Manages parallel execution of investor agents
- Synthesizes the final investment decision
- Tracks performance metrics and execution times

The debate manager uses:
- ThreadPoolExecutor for parallel agent execution
- Timeout handling for API stability
- Comprehensive logging for visibility into the process

### 4. Presentation Layer

#### Main Application (`src/main.py`)

Handles the user interface and process flow:

- Stock ticker input
- Progress reporting to terminal
- Comprehensive output formatting
- Writing results to Markdown files for easy consumption

## Data Flow

1. **Stock Data Acquisition**:
   - User specifies stock ticker(s)
   - System fetches comprehensive data via yfinance
   - Data is processed into a standardized format

2. **Parallel Analyst Reports** (Concurrent execution):
   - Each analyst agent receives relevant stock data
   - Agents independently analyze the stock from their specialized perspective
   - Reports are collected and aggregated

3. **Parallel Investor Opinions** (Concurrent execution):
   - Investors receive stock data and all analyst reports
   - Each investor evaluates the opportunity through their unique investment lens
   - Opinions are collected with their individual buy/hold/sell recommendations

4. **Decision Synthesis**:
   - The debate manager evaluates all investor perspectives
   - Areas of agreement and disagreement are identified
   - A final recommendation is synthesized with confidence level
   - Key risks and considerations are highlighted

5. **Output Generation**:
   - Results are displayed in the terminal
   - Detailed reports are saved as Markdown files

## Technical Implementation

- **Parallel Processing**: Using ThreadPoolExecutor for concurrent API calls
- **Error Handling**: Comprehensive try/except blocks with fallbacks
- **Timeout Management**: API calls have configurable timeouts
- **Performance Tracking**: Time measurement for each phase
- **Stateless Design**: Agents maintain no state between invocations

## Extension Points

The system architecture enables several extension possibilities:

- **Additional Agent Types**: New analyst types or investor personas
- **Alternative Data Sources**: Integration with other financial APIs
- **Web Interface**: Adding a Flask/FastAPI frontend
- **Performance Tracking**: Historical recommendation tracking
- **Portfolio Analysis**: Analyzing multiple stocks and portfolio construction
- **Real-time Updates**: Streaming data integration
- **Tool Integration**: Adding retrieval augmentation for current news