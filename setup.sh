#!/bin/bash

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Reminders for user
echo "Setup complete!"
echo ""
echo "Remember to add your Anthropic API key to the .env file:"
echo "ANTHROPIC_API_KEY=your_api_key_here"
echo ""
echo "To run the application:"
echo "source venv/bin/activate  # If not already activated"
echo "python src/main.py"