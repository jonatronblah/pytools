import sys
from pathlib import Path
import click

from pytools.config.settings import settings, Settings
from pytools.app import ToolsApp


@click.group()
@click.version_option(settings.version)
def cli():
    """My Textual App CLI"""
    pass


@cli.command()
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="Configuration file path"
)
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
def run(config, debug):
    """Run the Textual application"""
    if config:
        # Load configuration from file
        config_path = Path(config)
        if config_path.suffix.lower() == ".yaml":
            settings = Settings.from_yaml(config_path)
        else:
            click.echo("Unsupported config file format. Use YAML.")
            sys.exit(1)

    if debug:
        settings.debug = True

    # Ensure data directory exists
    settings.data_dir.mkdir(parents=True, exist_ok=True)

    # Run the application
    app = ToolsApp()
    app.run()


@cli.command()
@click.option(
    "--output", "-o", type=click.Path(), default="config.yaml", help="Output file path"
)
def generate_config(output):
    """Generate default configuration file"""
    output_path = Path(output)
    settings.save_to_yaml(output_path)
    click.echo(f"Configuration saved to {output_path}")


@cli.command()
def show_config():
    """Show current configuration"""
    import json

    config_dict = settings.model_dump()
    click.echo(json.dumps(config_dict, indent=2, default=str))


if __name__ == "__main__":
    cli()
