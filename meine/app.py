from textual.app import App

from meine.screens.help import HelpScreen
from meine.screens.settings import NameGetterScreen, Settings
from meine.screens.system_utils import SystemUtilScreen
from meine.themes import BUILTIN_THEMES
from meine.utils.file_manager import (
    save_history,
    save_settings,
    load_history,
    load_settings,
    initialize_user_data_files,
)

initialize_user_data_files()


HOME_SCREEN_ID = "home-screen"
HELP_SCREEN_ID = "help-screen"
SETTINGS_SCREEN_ID = "settings-screen"
SYSTEM_UTILS_SCREEN_ID = "system-util-screen"
CUSTOM_PATH_COMMAND = "Add custom path expansion"
CUSTOM_PATH_HELP = "Add a custom path expansion"


class MeineAI(App[None]):

    def __init__(
        self, driver_class=None, css_path=None, watch_css=False, ansi_color=False
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.more_themes = BUILTIN_THEMES

    async def on_mount(self):
        self.SETTINGS = load_settings()
        self.HISTORY = load_history()

        from meine.screens.home import HomeScreen

        await self.push_screen(HomeScreen(id=HOME_SCREEN_ID))

        for theme in BUILTIN_THEMES.values():
            self.register_theme(theme)
        self.theme = self.SETTINGS["app_theme"]

    def _on_exit_app(self):
        """ctrl + q handles quiting and also saving the configuration changes"""
        save_history(self.HISTORY)
        save_settings(self.SETTINGS)
        return super()._on_exit_app()

    def key_ctrl_k(self):
        """CTRL + K to open the help screen"""
        if self.screen.id == HELP_SCREEN_ID:
            self.pop_screen()
        elif self.screen.id == SETTINGS_SCREEN_ID:
            self.switch_screen(HelpScreen(id=HELP_SCREEN_ID))
        else:
            self.push_screen(HelpScreen(id=HELP_SCREEN_ID))

    def key_ctrl_s(self):
        """ctrl + s to open the setting screen"""

        if self.screen.id == SETTINGS_SCREEN_ID:
            self.pop_screen()
        elif self.screen.id == HELP_SCREEN_ID:
            self.switch_screen(Settings(id=SETTINGS_SCREEN_ID))
        else:
            self.push_screen(Settings(id=SETTINGS_SCREEN_ID))

    def key_ctrl_m(self):
        """ctrl+m to open the system utility screen"""
        if self.screen.id == SYSTEM_UTILS_SCREEN_ID:
            self.pop_screen()
        else:
            self.push_screen(SystemUtilScreen(id=SYSTEM_UTILS_SCREEN_ID))

    def key_escape(self):
        """ESC key for closing the screen"""
        if self.screen.id != HOME_SCREEN_ID:
            self.pop_screen()
        else:
            self.notify("You are in the home screen")

    def push_NameGetter_screen(self, title, callback):
        self.push_screen(NameGetterScreen(title, callback))

    def get_theme_colors(self):
        """this provides theme to actions package
        and this handle textual-ansi due to the MissingStyle exception in rich"""

        _theme = self.current_theme

        if _theme.name != "textual-ansi":

            return {
                "primary": _theme.primary,
                "secondary": _theme.secondary,
                "warning": _theme.warning,
                "error": _theme.error,
                "success": _theme.success,
                "accent": _theme.accent,
                "foreground": _theme.foreground,
                "background": _theme.background,
                "surface": _theme.surface,
                "panel": _theme.panel,
                "boost": _theme.boost,
            }

        return {
            "primary": "#BD93F9",
            "secondary": "#6272A4",
            "warning": "#FFB86C",
            "error": "#FF5555",
            "success": "#50FA7B",
            "accent": "#FF79C6",
            "background": "#282A36",
            "surface": "#2B2E3B",
            "panel": "#313442",
            "foreground": "#F8F8F2",
        }


_app_instance = None


def get_app():
    """singleton function"""
    global _app_instance
    if _app_instance is None:
        _app_instance = MeineAI()
    return _app_instance


def run():
    app = get_app()
    app.run()


if __name__ == "__main__":
    run()
