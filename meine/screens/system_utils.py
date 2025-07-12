import psutil


from textual.screen import ModalScreen
from textual import on
from textual.widgets import Select
from textual.css import _style_properties 
from textual.widget import Widget
from textual.containers import VerticalScroll, Middle, Center

from meine.widgets.system_widget_provider import SystemWidgetProvider

    
system_utils_functions = [
    ("system_info", 1),         
    ("cpu_usage", 2),           
    ("memory_info", 3),         
    ("disk_details", 5),        
    ("network_interfaces", 7),  
    ("ip_info", 8),             
    ("battery_status", 9),      
    ("current_user", 10),       
    ("environment_vars", 14),   

]


class SystemUtilScreen(ModalScreen):

    def compose(self):
        
        select = Select(system_utils_functions)
        with Center():
            yield select 

        yield VerticalScroll(SystemWidgetProvider(id="system-utils-provider"),id="widget-container")


    def update_widget(self, function_id):
        self.query_one(SystemWidgetProvider).set_function(function_id)

    
    @on(Select.Changed)
    def response_to_selection_list_changes(self, event: Select.Changed):
        func_id = event.value
        self.update_widget(func_id)

        
