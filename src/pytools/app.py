from textual.app import App, ComposeResult
from textual.theme import Theme

from pytools.config.settings import settings
from pytools.screens.main import MainScreen
from pytools.screens.settings import SettingsScreen


class ToolsApp(App):
    """Main Textual application"""

    TITLE = settings.app_name
    SUB_TITLE = f"Version {settings.version}"
    CSS_PATH = "styles.tcss"

    MODES = {
        "main": MainScreen,
        "settings": SettingsScreen,
    }

    def __init__(self):
        self.dark = settings.ui.theme == "dark"
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        """Compose the application"""
        yield from super().compose()

    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.switch_mode(settings.ui.default_screen)

    def get_css_variables(self) -> dict:
        """Get CSS variables based on current theme"""
        if self.dark:
            return {
                "background": "#1e1e1e",
                "surface": "#2d2d2d",
                "primary": "#4fc3f7",
                "secondary": "#9c27b0",
                "text": "#ffffff",
                "text-secondary": "#b0b0b0",
            }
        else:
            return {
                "background": "#ffffff",
                "surface": "#f5f5f5",
                "primary": "#03a9f4",
                "secondary": "#9c27b0",
                "text": "#000000",
                "text-secondary": "#666666",
            }


if __name__ == "__main__":
    app = ToolsApp()
    app.run()
