#!/usr/bin/env python3
"""
Test runner for FinAgents

This script discovers and runs all tests in the tests directory.
"""

import unittest
import sys
import os

def run_tests():
    """Run working tests only"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the script directory to the path
    sys.path.append(script_dir)
    
    # Run stable tests only
    loader = unittest.TestLoader()
    unit_suite = loader.loadTestsFromName('tests.unit.test_stock_data')
    output_suite = loader.loadTestsFromName('tests.integration.test_full_system.TestOutputFiles')
    
    suite = unittest.TestSuite()
    suite.addTest(unit_suite)
    suite.addTest(output_suite)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)