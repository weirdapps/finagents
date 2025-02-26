from setuptools import setup, find_packages

setup(
    name="finagents",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-anthropic>=0.1.1",
        "langchain-community>=0.0.15",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "yfinance>=0.2.36",
        "pydantic>=2.5.0",
    ],
)