from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    app_name: str = "pyTools"
    version: str = "0.1.0"
    debug: bool = False
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".app")

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "Settings":
        """Load configuration from YAML file"""
        if yaml_path.exists():
            with open(yaml_path, "r") as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)
        return cls()

    def save_to_yaml(self, yaml_path: Path) -> None:
        """Save current configuration to YAML file"""
        yaml_path.parent.mkdir(parents=True, exist_ok=True)
        config_dict = self.model_dump()
        with open(yaml_path, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False, indent=2)


settings = Settings()
