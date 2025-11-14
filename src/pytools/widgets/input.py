from textual.widgets import Input
from textual.message import Message
from textual.events import Key


class CustomInput(Input):
    """Custom input widget with enhanced functionality"""

    class Submitted(Input.Submitted):
        """Custom submitted message"""

        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self.history_index = 0

    async def on_key(self, event: Key) -> None:
        """Handle key events"""
        if event.key == "up":
            await self._history_up()
            event.prevent_default()
        elif event.key == "down":
            await self._history_down()
            event.prevent_default()
        elif event.key == "enter":
            self._add_to_history()

    async def _history_up(self) -> None:
        """Navigate to previous command in history"""
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)

    async def _history_down(self) -> None:
        """Navigate to next command in history"""
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.value = self.history[self.history_index]
            self.cursor_position = len(self.value)
        elif self.history_index == len(self.history) - 1:
            self.history_index += 1
            self.value = ""

    def _add_to_history(self) -> None:
        """Add current value to history"""
        if self.value and (not self.history or self.value != self.history[-1]):
            self.history.append(self.value)
            # Keep only last 50 commands
            if len(self.history) > 50:
                self.history.pop(0)
            self.history_index = len(self.history)
