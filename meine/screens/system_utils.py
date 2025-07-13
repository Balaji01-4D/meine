

from textual.screen import ModalScreen
from textual import on
from textual.widgets import Select
from textual.containers import VerticalScroll, Center

from meine.widgets.system_widget_provider import SystemWidgetProvider


system_utils_functions = [
    ("System Overview", 1),
    ("CPU Information", 2),
    ("RAM Usage", 3),
    ("Disk Storage", 5),
    ("Network Configuration", 8),
    ("Battery Status", 9),
    ("User Details", 10),
    ("Environment Variables", 14),
]


class SystemUtilScreen(ModalScreen):

    def compose(self):

        select = Select(system_utils_functions)
        with Center():
            yield select

        yield VerticalScroll(
            SystemWidgetProvider(id="system-utils-provider"), id="widget-container"
        )

    def update_widget(self, function_id):
        self.query_one(SystemWidgetProvider).set_function(function_id)

    @on(Select.Changed)
    def response_to_selection_list_changes(self, event: Select.Changed):
        func_id = event.value
        self.update_widget(func_id)
