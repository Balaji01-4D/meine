"""
Snapshot tests for the Meine Textual application.
"""

import pytest
from pathlib import Path
import sys

# Add the parent directory to sys.path to allow importing the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from meine.app import MeineAI
from tests.test_helpers import get_run_py_path, get_app_module


def test_home_screen_snapshot(snap_compare):
    """Test snapshot of the home screen."""
    app_path = get_app_module()
    assert snap_compare(app_path, terminal_size=(120, 30))


def test_settings_screen_snapshot(snap_compare):
    """Test snapshot of the settings screen."""
    app_path = get_app_module()
    
    async def run_before(pilot) -> None:
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Direct navigation to settings screen instead of using commands
        app = pilot.app
        from meine.screens.settings import Settings
        await app.push_screen(Settings(id="settings-screen"))
        await pilot.pause(1)  # Wait for screen transition
    
    assert snap_compare(app_path, terminal_size=(120, 30), run_before=run_before)


def test_help_screen_snapshot(snap_compare):
    """Test snapshot of the help screen."""
    app_path = get_app_module()
    
    async def run_before(pilot) -> None:
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Direct navigation to help screen
        app = pilot.app
        from meine.screens.help import HelpScreen
        await app.push_screen(HelpScreen(id="help-screen"))
        await pilot.pause(1)
    
    assert snap_compare(app_path, terminal_size=(120, 30), run_before=run_before)


def test_system_utils_snapshot(snap_compare):
    """Test snapshot of the system utilities screen."""
    app_path = get_app_module()
    
    async def run_before(pilot) -> None:
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Direct navigation to system utils screen
        app = pilot.app
        from meine.screens.system_utils import SystemUtilScreen
        await app.push_screen(SystemUtilScreen(id="system-util-screen"))
        await pilot.pause(1)
    
    assert snap_compare(app_path, terminal_size=(120, 30), run_before=run_before)


def test_directory_tree_snapshot(snap_compare):
    """Test snapshot with directory tree open."""
    app_path = get_app_module()
    
    async def run_before(pilot) -> None:
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Simulate showing directory tree by calling the method directly
        # This is more reliable than using command input in tests
        app = pilot.app
        home_screen = app.screen
        if hasattr(home_screen, "action_tree"):
            await home_screen.action_tree()
        await pilot.pause(1)
    
    assert snap_compare(app_path, terminal_size=(120, 30), run_before=run_before)


def test_command_execution_snapshot(snap_compare):
    """Test snapshot after executing a command."""
    app_path = get_app_module()
    
    async def run_before(pilot) -> None:
        # Wait for the app to fully initialize
        await pilot.pause(0.5)
        
        # Execute a command directly using the appropriate action method
        app = pilot.app
        home_screen = app.screen
        
        # Find the input widget and set its value
        input_widget = home_screen.query_one("#command-input")
        input_widget.value = "echo Hello World"
        
        # Trigger the submit action if available
        if hasattr(home_screen, "on_input_submitted"):
            await home_screen.on_input_submitted(input_widget)
        
        await pilot.pause(1)
    
    assert snap_compare(app_path, terminal_size=(120, 30), run_before=run_before)
