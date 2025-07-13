"""
Pytest configuration file for Meine app tests.
"""

import pytest
from pathlib import Path
import sys

# Add the parent directory to sys.path to allow importing the app
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from meine.app import MeineAI


@pytest.fixture
async def meine_app():
    """
    Fixture that provides a properly initialized Meine app.
    
    This can be used in tests that need access to an initialized app
    without having to set it up each time.
    """
    app = MeineAI()
    async with app.run_test() as pilot:
        # Wait for app to initialize
        await pilot.pause(0.5)
        yield app
