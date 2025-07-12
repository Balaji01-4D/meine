from collections.abc import Callable
from textual.widgets import Static
from rich.panel import Panel
from rich.errors import MissingStyle

from meine.Actions import System

async def default():
    return ""



class SystemWidgetProvider(Static):

    RUNNING_FUNCTION: Callable= None
    system_utils_callable_map = None
    
    def __init__(self, function_id = 0, content = "", *, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
        super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)

    def _on_mount(self, event):
        self.sys = System(self.app.get_theme_colors())

        self.system_utils_callable_map = {
            0: default, 
            1: self.sys.SYSTEM,
            2: self.sys.CPU,
            3: self.sys.ram_info,
            5: self.sys.DiskInfo,
            7: self.sys.NetWork,
            8: self.sys.IP,
            9: self.sys.Battery,
            10: self.sys.USER,
            14: self.sys.ENV,

        }

        return super()._on_mount(event)

    
    def get_function_by_id(self, id: int):
        return self.system_utils_callable_map[id]
    
    async def update_widget(self):
        result = await self.RUNNING_FUNCTION()

        if (isinstance(result, Panel)):
            self.update(result)
        else:
            self.update(Panel(result, border_style=self.app.current_theme.primary))


    def set_function(self, id):
        self.RUNNING_FUNCTION = self.get_function_by_id(id)
        self.set_interval(3, self.update_widget)

        