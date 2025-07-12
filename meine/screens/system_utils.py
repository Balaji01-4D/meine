import psutil


from textual.screen import ModalScreen
from textual import on
from textual.widgets import Select
from textual.css import _style_properties 
from textual.widget import Widget
from textual.containers import VerticalScroll, Middle, Center

from meine.widgets.system_widget_provider import SystemWidgetProvider

    
system_utils_functions = [
    ("system_info", 1),         # SYSTEM
    ("cpu_usage", 2),           # CPU
    ("memory_info", 3),         # RAM Info
    ("disk_usage", 4),          # DiskSpace
    ("disk_details", 5),        # DiskInfo
    ("running_processes", 6),   # Processes
    ("network_interfaces", 7),  # NetWork
    ("ip_info", 8),             # IP
    ("battery_status", 9),      # Battery
    ("current_user", 10),       # USER
    ("current_time", 11),       # Time
    ("home_directory", 12),     # HomeDir
    ("current_directory", 13),  # GetCurrentDir
    ("environment_vars", 14),   # ENV
    ("file_info", 15),          # Info
    ("terminate_process", 16),  # ProcessKill
    ("reboot_system", 17),      # Reboot
    ("shutdown_system", 18),    # ShutDown
]


class SystemUtilScreen(ModalScreen):

    def compose(self):
        
        select = Select(system_utils_functions)
        with Center():
            yield select 

        with Center():

            yield VerticalScroll(SystemWidgetProvider(id="system-utils-provider"),id="widget-container")


    def update_widget(self, function_id):
        self.query_one(SystemWidgetProvider).set_function(function_id)

    
    @on(Select.Changed)
    def response_to_selection_list_changes(self, event: Select.Changed):
        func_id = event.value
        self.update_widget(func_id)

        
