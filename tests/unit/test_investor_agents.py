"""
Unit tests for investor agents module
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from src.agents.investor_agents import (
    INVESTOR_PERSONAS, 
    create_investor_prompt, 
    create_investor_agent, 
    create_investor_team
)

class TestInvestorPersonas(unittest.TestCase):
    """Tests for the investor personas configuration"""
    
    def test_investor_personas_structure(self):
        """Test that investor personas have the required fields"""
        required_fields = ['philosophy', 'risk_profile', 'famous_quotes']
        
        for investor, data in INVESTOR_PERSONAS.items():
            for field in required_fields:
                self.assertIn(field, data, f"Investor {investor} missing required field {field}")
            
            self.assertIsInstance(data['famous_quotes'], list, 
                                 f"Famous quotes for {investor} should be a list")
            self.assertGreaterEqual(len(data['famous_quotes']), 1, 
                                   f"Famous quotes for {investor} should have at least one quote")

class TestCreateInvestorPrompt(unittest.TestCase):
    """Tests for the create_investor_prompt function"""
    
    def test_prompt_creation(self):
        """Test that prompts are correctly created for investors"""
        for investor, data in INVESTOR_PERSONAS.items():
            prompt = create_investor_prompt(investor, data)
            
            # Check prompt structure
            self.assertIsNotNone(prompt)
            
            # Check if investor name is in the system message
            system_message = prompt.messages[0][1]
            self.assertIn(investor, system_message)
            
            # Check if philosophy is in the system message
            self.assertIn(data['philosophy'], system_message)

class TestCreateInvestorAgent(unittest.TestCase):
    """Tests for the create_investor_agent function"""
    
    @patch('src.agents.investor_agents.ChatAnthropic')
    @patch('src.agents.investor_agents.os')
    def test_agent_creation(self, mock_os, mock_chat_anthropic):
        """Test that agent is correctly created"""
        # Setup mocks
        mock_os.getenv.return_value = 'test_api_key'
        mock_chat_anthropic.return_value = MagicMock()
        
        # Test for each investor
        for investor, data in INVESTOR_PERSONAS.items():
            agent = create_investor_agent(investor, data)
            
            # Check agent was created
            self.assertIsNotNone(agent)
            
            # Check API key was used
            mock_os.getenv.assert_called_with('ANTHROPIC_API_KEY')

class TestCreateInvestorTeam(unittest.TestCase):
    """Tests for the create_investor_team function"""
    
    @patch('src.agents.investor_agents.create_investor_agent')
    def test_team_creation(self, mock_create_agent):
        """Test that team is correctly created with all investors"""
        # Setup mock
        mock_create_agent.return_value = MagicMock()
        
        # Create team
        team = create_investor_team()
        
        # Check all investors are in the team
        self.assertEqual(len(team), len(INVESTOR_PERSONAS))
        for investor in INVESTOR_PERSONAS.keys():
            self.assertIn(investor, team)
        
        # Check create_agent was called for each investor
        self.assertEqual(mock_create_agent.call_count, len(INVESTOR_PERSONAS))

if __name__ == '__main__':
    unittest.main()