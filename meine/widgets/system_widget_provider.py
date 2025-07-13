from collections.abc import Callable
from textual.widgets import Static
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.errors import MissingStyle

from meine.Actions import System
from meine.Actions.app_theme import get_theme_colors


async def default():
    """Default func when no widget is selected"""
    theme = get_theme_colors()
    primary = theme.get("primary", "white")
    accent = theme.get("accent", "yellow")
    foreground = theme.get("foreground", "white")

    message = Text.assemble(
        ("Select a ", foreground),
        ("system widget", accent),
        (" from the menu to display information", foreground),
    )

    return Panel(
        Align.center(message),
        title=Text("System Widget", style=accent),
        border_style=primary,
    )


class SystemWidgetProvider(Static):

    RUNNING_FUNCTION: Callable = None
    system_utils_callable_map = None

    def __init__(
        self,
        function_id=0,
        content="",
        *,
        expand=False,
        shrink=True,
        markup=True,
        name=None,
        id=None,
        classes=None,
        disabled=False,
    ):
        super().__init__(
            content,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    async def _on_mount(self, event):
        """this setups system function and update it to the default"""
        self.sys = System()

        self.system_utils_callable_map = {
            0: default,
            1: self.sys.SYSTEM,
            2: self.sys.CPU,
            3: self.sys.ram_info,
            5: self.sys.DiskInfo,
            8: self.sys.IP,
            9: self.sys.Battery,
            10: self.sys.USER,
            14: self.sys.ENV,
        }

        self.update(await default())

        return super()._on_mount(event)

    def get_function_by_id(self, id: int):
        return self.system_utils_callable_map.get(id, default)

    async def update_widget(self):

        try:
            self.sys.refresh_theme()
            result = await self.RUNNING_FUNCTION()

            if isinstance(result, Panel):
                self.update(Align.center(result))
            else:
                self.update(
                    Panel(
                        Align.center(result),
                        border_style=self.app.current_theme.primary,
                    )
                )

        except MissingStyle:
            self.notify("this theme doesnot support dynamic widgets currently")

    def set_function(self, id):
        """this is used to set function based on the id and starts the timeer"""
        self.RUNNING_FUNCTION = self.get_function_by_id(id)
        self.set_interval(3, self.update_widget)
