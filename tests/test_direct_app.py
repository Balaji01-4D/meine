"""
Direct app tests for the Meine Textual application.
These tests directly instantiate the app rather than importing it from run.py.
"""

import pytest
from pathlib import Path
import sys

# Add the parent directory to sys.path to allow importing the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from meine.app import MeineAI
from meine.screens.home import HomeScreen


def test_direct_app_snapshot(snap_compare):
    """Test snapshot of the app by creating the app directly."""
    # Use the path to run.py instead of creating the app directly
    # This avoids the asyncio.run() issue
    run_py_path = str(Path(__file__).parent.parent / "run.py")
    
    async def run_before(pilot):
        """Function to run before taking snapshot"""
        # Wait for the app to fully initialize
        await pilot.pause(1)
        
    # Use the run.py path for snapshot testing
    assert snap_compare(run_py_path, run_before=run_before, terminal_size=(120, 30))


def test_direct_app_settings(snap_compare):
    """Test settings screen by creating the app directly."""
    # Use the path to run.py instead of creating the app directly
    run_py_path = str(Path(__file__).parent.parent / "run.py")
    
    async def run_before(pilot):
        """Function to run before taking snapshot"""
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Navigate to settings screen
        await pilot.click("#command-input")
        await pilot.press("s", "e", "t", "t", "i", "n", "g", "s")
        await pilot.press("enter")
        await pilot.pause(1)
        
    # Use the run.py path for snapshot testing
    assert snap_compare(run_py_path, run_before=run_before, terminal_size=(120, 30))


def test_direct_app_help(snap_compare):
    """Test help screen by creating the app directly."""
    # Use the path to run.py instead of creating the app directly
    run_py_path = str(Path(__file__).parent.parent / "run.py")
    
    async def run_before(pilot):
        """Function to run before taking snapshot"""
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Navigate to help screen
        await pilot.click("#command-input")
        await pilot.press("h", "e", "l", "p")
        await pilot.press("enter")
        await pilot.pause(1)
        
    # Use the run.py path for snapshot testing
    assert snap_compare(run_py_path, run_before=run_before, terminal_size=(120, 30))


def test_direct_app_system(snap_compare):
    """Test system screen by creating the app directly."""
    # Use the path to run.py instead of creating the app directly
    run_py_path = str(Path(__file__).parent.parent / "run.py")
    
    async def run_before(pilot):
        """Function to run before taking snapshot"""
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Navigate to system screen
        await pilot.click("#command-input")
        await pilot.press("s", "y", "s", "t", "e", "m")
        await pilot.press("enter")
        await pilot.pause(1)
        
    # Use the run.py path for snapshot testing
    assert snap_compare(run_py_path, run_before=run_before, terminal_size=(120, 30))
