from collections.abc import Callable
from textual.widgets import Static
from rich.panel import Panel

from meine.Actions import System



async def default():
    return ""

sys = System()

system_utils_callable_map = {
    0: default, 
    1: sys.SYSTEM,
    2: sys.CPU,
    3: sys.ram_info,
    4: sys.DiskSpace,
    5: sys.DiskInfo,
    6: sys.Processes,
    7: sys.NetWork,
    8: sys.IP,
    9: sys.Battery,
    10: sys.USER,
    11: sys.Time,
    12: sys.HomeDir,
    13: sys.GetCurrentDir,
    14: sys.ENV,
    15: sys.Info,
    16: sys.ProcessKill,
    17: sys.Reboot,
    18: sys.ShutDown,
}


class SystemWidgetProvider(Static):

    RUNNING_FUNCTION: Callable= None

    def __init__(self, function_id = 0, content = "", *, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
        super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.RUNNING_FUNCTION = self.get_function_by_id(function_id)

    
    def get_function_by_id(self, id: int):
        return system_utils_callable_map[id]
    
    async def update_widget(self):
        self.update(await self.RUNNING_FUNCTION())


    def set_function(self, id):
        self.RUNNING_FUNCTION = self.get_function_by_id(id)
        self.set_interval(3, self.update_widget)

        