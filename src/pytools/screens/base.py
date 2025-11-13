from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.containers import Container

from pytools.config.settings import settings
from pytools.widgets.status import StatusBar


class BaseScreen(Screen):
    """Base screen class with common functionality"""

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.app_settings = settings

    def compose(self) -> ComposeResult:
        """Compose base screen elements"""
        yield Header()
        yield from self.compose_content()
        yield Footer()
        yield StatusBar()

    def compose_content(self) -> ComposeResult:
        """Override this method to add screen-specific content"""
        yield Container()

    async def on_mount(self) -> None:
        """Called when the screen is mounted"""
        await self.update_status(f"Loaded {self.__class__.__name__}")

    async def update_status(self, message: str) -> None:
        """Update the status bar"""
        status_bar = self.query_one(StatusBar, None)
        if status_bar:
            status_bar.update_status(message)

    def action_toggle_debug(self) -> None:
        """Toggle debug mode"""
        self.app_settings.debug = not self.app_settings.debug
        self.notify(f"Debug mode: {'ON' if self.app_settings.debug else 'OFF'}")
