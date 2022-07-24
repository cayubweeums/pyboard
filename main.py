import subprocess 

from datetime import datetime
from sys import stdout
from textual.app import App
from textual.widget import Widget, Reactive
from textual.widgets import Header, Footer, Placeholder
from textual import events
from rich.traceback import install
from rich.logging import RichHandler
from rich.panel import Panel
from rich.console import Console, RenderableType
from rich.align import Align
from rich import box, print
from tools import writer


install()
console = Console()

class Clock(Widget):
    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        time = datetime.now().strftime("%c")
        return Align.center(time, vertical="middle")

class Toggleables(Widget, can_focus=True):

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    style: Reactive[str] = Reactive("")
    height: Reactive[int | None] = Reactive(None)
    vpn_status: Reactive[str] = Reactive("")

    def on_mount(self):
        self.style_border = "bold"
        self.set_interval(1, self.refresh)

    def render(self) -> RenderableType:
        result = subprocess.run(["sudo", "wg", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
        if len(result.stdout) > 0:
                vpn_status = '[bold green] [■] [/bold green] VPN'
        else:
                vpn_status = '[bold red] [ ] [/bold red] VPN'

        return Panel(Align.left(vpn_status, vertical="top"), 
                        border_style='green' if self.mouse_over else 'blue', 
                        box=box.HEAVY if self.has_focus else box.ROUNDED,
                        style=self.style,
                        height=self.height
                        )

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        self.mouse_over = False
     
    async def on_key(self, event: events.Key):
        if self.has_focus:
            self.console.bell()
            if event.key == 'v':
                result = subprocess.run(["sudo", "wg", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if len(result.stdout) > 0:
                    umount = subprocess.Popen(["sudo", "umount", "cayubs-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    umount.wait()
                    writer.log(console, 'info', f'cayubs-server unmounted \n{umount.stdout}')

                    vpn_down = subprocess.run(["sudo", "wg-quick", "down", "peer2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    writer.log(console, 'info', f'VPN toggled off \n{vpn_down.stdout}')

                else:
                    vpn_up = subprocess.run(["sudo", "wg-quick", "up", "peer2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    writer.log(console, 'info', f'VPN toggled on \n{vpn_up.stdout}')
                
                    mount = subprocess.Popen(["sudo", "mount", "-a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    mount.wait()
                    writer.log(console, 'info', f'cayubs-server mounted \n{mount.stdout}')



class Pyboard(App):
        async def on_load(self, event):
                await self.bind("escape", "quit")
                await self.bind("ctrl+b", "view.toggle('sidebar')", "Toggle sidebar")

        async def on_mount(self) -> None: 
                await self.view.dock(Placeholder(), edge="left", size=30, name="sidebar")
                await self.view.dock(Header(), edge="top")
                await self.view.dock(Footer(), edge="bottom")
                await self.view.dock(Clock(), Toggleables(), edge="right")


Pyboard.run(title="Dashboard")
