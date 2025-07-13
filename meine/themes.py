from textual.theme import Theme

BUILTIN_THEMES: dict[str, Theme] = {
    "textual": Theme(
        name="textual",
        primary="#004578",
        secondary="#0178D4",
        warning="#ffa62b",
        error="#ba3c5b",
        success="#4EBF71",
        accent="#ffa62b",
        dark=True,
        foreground="#FFFFFF",
    ),
    "monokai 1": Theme(
        name="monokai 0.1",
        primary="#F92672",  # Pink
        secondary="#66D9EF",  # Light Blue
        warning="#FD971F",  # Orange
        error="#F92672",  # Pink (same as primary for consistency)
        success="#A6E22E",  # Green
        accent="#AE81FF",  # Purple
        background="#272822",  # Dark gray-green
        surface="#3E3D32",  # Slightly lighter gray-green
        panel="#3E3D32",  # Same as surface for consistency
        foreground="#F8F8F2",  # Light gray with a hint of green
        dark=True,
    ),
    "galaxy": Theme(
        name="galaxy",
        primary="#8A2BE2",  # Improved Deep Magenta (Blueviolet)
        secondary="#a684e8",
        warning="#FFD700",  # Gold, more visible than orange
        error="#FF4500",  # OrangeRed, vibrant but less harsh than pure red
        success="#00FA9A",  # Medium Spring Green, kept for vibrancy
        accent="#FF69B4",  # Hot Pink, for a pop of color
        dark=True,
        background="#0F0F1F",  # Very Dark Blue, almost black
        surface="#1E1E3F",  # Dark Blue-Purple
        panel="#2D2B55",  # Slightly Lighter Blue-Purple
        foreground="#E0E0FF",  # Light lavender white
    ),
    "hacker": Theme(
        name="hacker",
        primary="#00FF00",  # Bright Green (Lime)
        secondary="#32CD32",  # Lime Green
        warning="#ADFF2F",  # Green Yellow
        error="#FF4500",  # Orange Red (for contrast)
        success="#00FA9A",  # Medium Spring Green
        accent="#39FF14",  # Neon Green
        dark=True,
        background="#0D0D0D",  # Almost Black
        surface="#1A1A1A",  # Very Dark Gray
        panel="#2A2A2A",  # Dark Gray
        foreground="#33FF33",  # Bright terminal green
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        primary="#FF007F",  # Neon Pink
        secondary="#00E5FF",  # Neon Cyan
        warning="#FFD700",  # Bright Gold
        error="#FF3131",  # Vivid Red
        success="#00FF7F",  # Bright Green
        accent="#8A2BE2",  # Deep Purple
        dark=True,
        background="#080808",  # Almost Black
        surface="#181818",  # Dark Gray
        panel="#282828",  # Lighter Gray
        foreground="#00FFFF",  # Bright cyan
    ),
    "retro_wave": Theme(
        name="retro_wave",
        primary="#FF6EC7",  # Neon Pink
        secondary="#FFD700",  # Golden Yellow
        warning="#FFA500",  # Orange
        error="#E60000",  # Deep Red
        success="#39FF14",  # Electric Green
        accent="#8B00FF",  # Electric Purple
        dark=True,
        background="#2D1E2F",  # Dark Purple
        surface="#3B2E50",  # Muted Dark Blue
        panel="#503571",  # Deep Magenta
        foreground="#F2F2FF",  # Bright white with slight purple tint
    ),
    "dracula-pro": Theme(
        name="dracula-pro",
        primary="#9580FF",  # Enhanced Purple (slightly brighter)
        secondary="#7390AA",  # Enhanced Comment Blue (higher contrast)
        warning="#FFCA80",  # Enhanced Orange (brighter for better visibility)
        error="#FF6E6E",  # Enhanced Red (slightly brighter)
        success="#5AF78E",  # Enhanced Green (slightly brighter)
        accent="#FF92DF",  # Enhanced Pink (slightly brighter)
        dark=True,
        background="#22212C",  # Darker Background (more contrast)
        surface="#2A2B3C",  # Enhanced Current Line
        panel="#34353E",  # Enhanced Selection
        foreground="#F8F8F2",  # Classic Foreground
        variables={
            "button-color-foreground": "#22212C",
            "scrollbar-background": "#282A36",
            "scrollbar-color": "#BD93F9",
            "link-color": "#8BE9FD",  # Cyan for links
        },
    ),
}
