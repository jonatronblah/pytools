import asyncio
from typing import List, Dict, Any
from pathlib import Path

from pytools.config.settings import settings
from pytools.utils.logger import get_logger


class DataService:
    """Service for handling data operations"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.data_file = settings.data_dir / "data.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists"""
        settings.data_dir.mkdir(parents=True, exist_ok=True)

    async def get_data(self) -> List[Dict[str, Any]]:
        """Get data (simulated)"""
        # Simulate API call or database query
        await asyncio.sleep(0.1)  # Simulate network delay

        # Return sample data
        return [
            {"id": 1, "name": "Item 1", "status": "active", "updated": "2023-01-01"},
            {"id": 2, "name": "Item 2", "status": "pending", "updated": "2023-01-02"},
            {"id": 3, "name": "Item 3", "status": "completed", "updated": "2023-01-03"},
        ]

    async def execute_command(self, command: str) -> str:
        """Execute a command"""
        self.logger.info(f"Executing command: {command}")

        # Simulate command execution
        await asyncio.sleep(0.5)

        if command.lower() == "clear":
            return "Data cleared"
        elif command.lower() == "refresh":
            return "Data refreshed"
        elif command.lower().startswith("add "):
            item_name = command[4:]
            return f"Added item: {item_name}"
        else:
            return f"Unknown command: {command}"
