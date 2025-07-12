from textual.app import App
from textual.screen import Screen, ModalScreen
from textual.widgets import Label, Input
from rich.panel import Panel
from textual import on

class SettingTest(App):

    CSS = """\
Label{
border: green;
width: 100%;
height: auto;
}
"""

    string = "H"

    def compose(self):
        yield Input(placeholder="type here")
        yield Rg(markup=True)

    def on_input_submitted(self, text: Input.Submitted):
        self.query_one(Label).update(Panel(text.value))

    
    def on_mount(self):
        self.set_interval(3, self.updating)

    def updating(self):
        self.string += " i"
        self.query_one(Label).update(Panel(f"[green]{self.string}", border_style="red"))


class Rg(Label):

    def __init__(self, renderable = "", *, variant = None, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
        super().__init__(renderable, variant=variant, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)

    def _on_mount(self, event):
        return super()._on_mount(event)


if __name__ == "__main__":
    SettingTest().run()