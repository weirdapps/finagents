"""
Unit tests for analyst agents module
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from src.agents.analyst_agents import (
    ANALYST_TYPES, 
    create_analyst_prompt, 
    create_analyst_agent, 
    create_analyst_team
)

class TestAnalystTypes(unittest.TestCase):
    """Tests for the analyst types configuration"""
    
    def test_analyst_types_structure(self):
        """Test that analyst types have the required fields"""
        required_fields = ['focus', 'methodology']
        
        for analyst, data in ANALYST_TYPES.items():
            for field in required_fields:
                self.assertIn(field, data, f"Analyst {analyst} missing required field {field}")
            
            self.assertIsInstance(data['focus'], str, 
                                f"Focus for {analyst} should be a string")
            self.assertIsInstance(data['methodology'], str, 
                                f"Methodology for {analyst} should be a string")

class TestCreateAnalystPrompt(unittest.TestCase):
    """Tests for the create_analyst_prompt function"""
    
    def test_prompt_creation(self):
        """Test that prompts are correctly created for analysts"""
        for analyst, data in ANALYST_TYPES.items():
            prompt = create_analyst_prompt(analyst, data)
            
            # Check prompt structure
            self.assertIsNotNone(prompt)
            
            # Check if analyst type is in the system message
            system_message = prompt.messages[0][1]
            self.assertIn(analyst, system_message)
            
            # Check if focus and methodology are in the system message
            self.assertIn(data['focus'], system_message)
            self.assertIn(data['methodology'], system_message)

class TestCreateAnalystAgent(unittest.TestCase):
    """Tests for the create_analyst_agent function"""
    
    @patch('src.agents.analyst_agents.ChatAnthropic')
    @patch('src.agents.analyst_agents.os')
    def test_agent_creation(self, mock_os, mock_chat_anthropic):
        """Test that agent is correctly created"""
        # Setup mocks
        mock_os.getenv.return_value = 'test_api_key'
        mock_chat_anthropic.return_value = MagicMock()
        
        # Test for each analyst type
        for analyst, data in ANALYST_TYPES.items():
            agent = create_analyst_agent(analyst, data)
            
            # Check agent was created
            self.assertIsNotNone(agent)
            
            # Check API key was used
            mock_os.getenv.assert_called_with('ANTHROPIC_API_KEY')

class TestCreateAnalystTeam(unittest.TestCase):
    """Tests for the create_analyst_team function"""
    
    @patch('src.agents.analyst_agents.create_analyst_agent')
    def test_team_creation(self, mock_create_agent):
        """Test that team is correctly created with all analyst types"""
        # Setup mock
        mock_create_agent.return_value = MagicMock()
        
        # Create team
        team = create_analyst_team()
        
        # Check all analyst types are in the team
        self.assertEqual(len(team), len(ANALYST_TYPES))
        for analyst in ANALYST_TYPES.keys():
            self.assertIn(analyst, team)
        
        # Check create_agent was called for each analyst type
        self.assertEqual(mock_create_agent.call_count, len(ANALYST_TYPES))

if __name__ == '__main__':
    unittest.main()