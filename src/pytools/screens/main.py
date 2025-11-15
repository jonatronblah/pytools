from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Static, Input, DataTable
from textual.screen import Screen

from pytools.screens.base import BaseScreen
from pytools.widgets.input import CustomInput
from pytools.services.data import DataService


class MainScreen(BaseScreen):
    """Main application screen"""

    BINDINGS = [
        # ("d", "toggle_dark", "Toggle Dark Mode"),
        ("s", "switch_to_settings", "Settings"),
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh"),
    ]

    def __init__(self):
        super().__init__(name="main")
        self.data_service = DataService()
        self.data_table = DataTable()

    def compose_content(self) -> ComposeResult:
        """Compose the main screen content"""
        with Vertical():
            yield Static("Welcome to My Textual App!", id="welcome")

            with Horizontal():
                yield CustomInput(placeholder="Enter command...", id="command-input")
                yield Button("Execute", variant="primary", id="execute-btn")

            yield self.data_table

    async def on_mount(self) -> None:
        """Initialize the screen when mounted"""
        await super().on_mount()
        await self.update_status("Ready")
        await self.setup_data_table()

    async def setup_data_table(self) -> None:
        """Setup the data table"""
        self.data_table.cursor_type = "row"
        self.data_table.zebra_stripes = True
        self.data_table.add_columns("ID", "Name", "Status", "Updated")
        await self.load_data()

    async def load_data(self) -> None:
        """Load data into the table"""
        try:
            data = await self.data_service.get_data()
            self.data_table.clear()
            for row in data:
                self.data_table.add_row(
                    str(row.get("id", "")),
                    row.get("name", ""),
                    row.get("status", ""),
                    row.get("updated", ""),
                )
            await self.update_status(f"Loaded {len(data)} items")
        except Exception as e:
            self.notify(f"Error loading data: {e}", severity="error")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "execute-btn":
            await self.execute_command()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission"""
        if event.input.id == "command-input":
            await self.execute_command()

    async def execute_command(self) -> None:
        """Execute the command from input"""
        command_input = self.query_one("#command-input", Input)
        command = command_input.value.strip()

        if command:
            try:
                result = await self.data_service.execute_command(command)
                self.notify(f"Command executed: {result}")
                await self.load_data()
            except Exception as e:
                self.notify(f"Command failed: {e}", severity="error")

            command_input.value = ""

    # def action_toggle_dark(self) -> None:
    #     """Toggle dark mode"""
    #     self.app.dark = not self.app.dark

    def action_switch_to_settings(self) -> None:
        """Switch to settings screen"""
        self.app.switch_mode("settings")

    def action_refresh_data(self) -> None:
        """Refresh data"""
        self.run_worker(self.load_data, exclusive=True)
