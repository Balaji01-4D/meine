"""
Helper functions for testing the Meine Textual application.
"""

import asyncio
from pathlib import Path
from meine.app import MeineAI


async def setup_app():
    """
    Create and initialize a Meine app for testing.
    
    Returns:
        A tuple (app, screen) where app is the MeineAI instance and
        screen is the home screen that was pushed during initialization.
    """
    app = MeineAI()
    
    # Use a mock run_test to initialize the app without running tests
    async with app.run_test() as pilot:
        # Wait for app to initialize
        await pilot.pause(0.5)
        # Return the app and its screen
        return app, app.screen


def get_run_py_path():
    """
    Get the absolute path to run.py in the project root.
    
    Returns:
        The absolute path to run.py as a string.
    """
    return str(Path(__file__).parent.parent / "run.py")


def get_app_module():
    """
    Get the module path to the app, which can be used for snapshot testing.
    
    Returns:
        A string in the format 'module_path:app_name' that can be used with snap_compare
    """
    # The format should be 'package.module:app_variable_name'
    return "run.py:app"
