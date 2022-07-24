import subprocess 

from datetime import datetime
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder
from rich.traceback import install
from rich.logging import RichHandler
from rich.console import Console
from rich.align import Align
from rich import print
from tools import writer


install()
console = Console()

class Clock(Widget):
    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        time = datetime.now().strftime("%c")
        return Align.center(time, vertical="middle")

class Toggleables(Widget):
    def on_mount(self):
        self.set_interval(10, self.refresh)

    def render(self):
        vpn_status = ''
        result = subprocess.run(["sudo", "wg", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # writer.log('info', f'{result.stdout} output of wg show')
        if len(result.stdout) > 0:
                vpn_status = '[bold green] [■] [/bold green] VPN'
        else:
                vpn_status = '[bold red] [ ] [/bold red] VPN'

        return Align.left(vpn_status, vertical="top")

class SimpleApp(App):
        console.log('Loading')
        async def on_load(self, event):
                await self.bind("q", "quit")
                await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")

        console.log('Mounting')
        async def on_mount(self) -> None:
                 await self.view.dock(Placeholder(), edge="left", size=30, name="sidebar")
                 await self.view.dock(Header(), edge="top")
                 await self.view.dock(Footer(), edge="bottom")
                 await self.view.dock(Clock(), Toggleables(), edge="right")


SimpleApp.run()
