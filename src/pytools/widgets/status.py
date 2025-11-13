from textual.widgets import Static
from textual.containers import Horizontal
from datetime import datetime


class StatusBar(Horizontal):
    """Status bar widget"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_text = Static("Ready", id="status-text")
        self.time_display = Static("", id="time-display")

    def compose(self):
        yield self.status_text
        yield self.time_display

    def on_mount(self) -> None:
        """Update time display"""
        self.set_interval(1, self._update_time)
        self._update_time()

    def _update_time(self) -> None:
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_display.update(f"[{current_time}]")

    def update_status(self, message: str) -> None:
        """Update the status message"""
        self.status_text.update(message)
