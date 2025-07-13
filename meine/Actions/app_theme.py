from textual.theme import Theme
import meine.app as app


def get_theme_colors():
    """this is used every command working for avoid circular imports and dynamic theme syncing"""

    _theme: Theme = app.get_app().get_theme_colors()

    return _theme
