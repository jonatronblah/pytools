from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Grid
from textual.widgets import Button, Input, Label, Switch, Select
from textual.screen import Screen

from pytools.screens.base import BaseScreen
from pytools.config.settings import settings


class SettingsScreen(BaseScreen):
    """Settings screen for application configuration"""

    BINDINGS = [
        ("b", "go_back", "Back"),
        ("s", "save_settings", "Save"),
    ]

    def compose_content(self) -> ComposeResult:
        """Compose the settings screen content"""
        with Vertical(id="settings-container"):
            yield Label("Application Settings", classes="title")

            with Grid(id="settings-grid"):
                # UI Settings
                yield Label("Theme:", classes="setting-label")
                # yield Select(
                #     [("dark", "Dark"), ("light", "Light")],
                #     value=settings.ui.theme,
                #     id="theme-select",
                # )

                yield Label("Refresh Rate:", classes="setting-label")
                yield Input(
                    str(settings.ui.refresh_rate),
                    id="refresh-rate-input",
                    type="number",
                )

                yield Label("Show Debug:", classes="setting-label")
                yield Switch(settings.ui.show_debug, id="debug-switch")

                # API Settings
                yield Label("API Base URL:", classes="setting-label")
                yield Input(settings.api.base_url, id="api-url-input")

                yield Label("API Timeout:", classes="setting-label")
                yield Input(
                    str(settings.api.timeout), id="api-timeout-input", type="number"
                )

                # Database Settings
                yield Label("Database Host:", classes="setting-label")
                yield Input(settings.database.host, id="db-host-input")

                yield Label("Database Port:", classes="setting-label")
                yield Input(
                    str(settings.database.port), id="db-port-input", type="number"
                )

            with Horizontal(id="settings-buttons"):
                yield Button("Save", variant="success")
                yield Button("Cancel", variant="error")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "save-btn":
            await self.save_settings()
        elif event.button.id == "cancel-btn":
            self.action_go_back()

    async def save_settings(self) -> None:
        """Save the current settings"""
        try:
            # Update settings from UI
            theme_select = self.query_one("#theme-select", Select)
            settings.ui.theme = theme_select.value

            refresh_input = self.query_one("#refresh-rate-input", Input)
            settings.ui.refresh_rate = float(refresh_input.value)

            debug_switch = self.query_one("#debug-switch", Switch)
            settings.ui.show_debug = debug_switch.value

            api_url_input = self.query_one("#api-url-input", Input)
            settings.api.base_url = api_url_input.value

            api_timeout_input = self.query_one("#api-timeout-input", Input)
            settings.api.timeout = int(api_timeout_input.value)

            db_host_input = self.query_one("#db-host-input", Input)
            settings.database.host = db_host_input.value

            db_port_input = self.query_one("#db-port-input", Input)
            settings.database.port = int(db_port_input.value)

            # Save to file
            config_path = settings.data_dir / "config.yaml"
            settings.save_to_yaml(config_path)

            self.notify("Settings saved successfully!")
            self.action_go_back()

        except Exception as e:
            self.notify(f"Error saving settings: {e}", severity="error")

    def action_go_back(self) -> None:
        """Go back to main screen"""
        self.app.switch_mode("main")

    def action_save_settings(self) -> None:
        """Save settings action"""
        self.run_worker(self.save_settings, exclusive=True)
