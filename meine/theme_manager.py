
from functools import lru_cache


DEFAULT_THEME = {
    "primary": "cyan",
    "secondary": "blue", 
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "accent": "magenta",
    "foreground": "white",
    "background": "black",
    "surface": "#222222",
    "panel": "#333333",
    "boost": 0.1,
}


_theme_registry = {}

def register_theme_provider(provider):
    global _theme_registry
    _theme_registry["provider"] = provider

def get_theme_colors():
    global _theme_registry
    if "provider" in _theme_registry and hasattr(_theme_registry["provider"], "get_theme_colors"):
        return _theme_registry["provider"].get_theme_colors()
    return DEFAULT_THEME.copy()

@lru_cache(maxsize=1)
def get_cached_theme_colors():
    return get_theme_colors()
