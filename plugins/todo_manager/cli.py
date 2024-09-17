# python-motion/plugins/todo_manager/cli.py

import os
from pathlib import Path
import click
import logging
from .sync import (
    sync_todos,
    get_all_todos,
    export_todos_to_json,
    export_todos_to_markdown,
    load_todos_json,
    save_todos_json
)

MOTION_API_TOKEN = 'MOTION_API_TOKEN'

@click.group()
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug logging.'
)
@click.pass_context
def cli(ctx, debug):
    """
    todo - A tool to sync TODOs from files with Motion API and export them.
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@cli.command()
@click.option(
    '--dir',
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help='Path to the directory containing files.'
)
@click.option(
    '--file-types',
    default='.tex',
    help='Comma-separated list of file extensions to scan for TODOs (e.g., .tex,.py,.md).'
)
@click.option(
    '--api-key',
    default=lambda: os.getenv(MOTION_API_TOKEN),
    required=False,
    help=f"API key for authentication (or set via {MOTION_API_TOKEN} environment variable)."
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Simulate the sync without making changes to the API.'
)
@click.option(
    '--export-json',
    is_flag=True,
    help='Export TODOs to a JSON file.'
)
@click.option(
    '--json-path',
    default=None,
    show_default=True,
    help='Path to the output JSON file.'
)
@click.option(
    '--export-md',
    is_flag=True,
    help='Export TODOs as a Markdown table.'
)
@click.option(
    '--md-path',
    default=None,
    show_default=True,
    help='Path to the output Markdown file.'
)
def sync(dir, file_types, api_key, dry_run, export_json, json_path, export_md, md_path):
    """
    Sync TODOs from specified files with Motion API.
    """
    logger = logging.getLogger(__name__)

    if not api_key:
        logger.error(f"API key must be provided either via --api-key or the {MOTION_API_TOKEN} environment variable.")
        raise click.ClickException(
            f"API key must be provided either via --api-key or the {MOTION_API_TOKEN} environment variable."
        )

    file_types = [ext.strip() for ext in file_types.split(',')]
    
    # Determine the path to todos.json
    if json_path is None:
        json_path = str((Path(dir) / "todos.json").resolve())

    try:
        logger.info("Starting synchronization of TODOs.")
        todos_to_add, todos_to_update, todos_to_delete = sync_todos(
            directory=dir,
            file_types=file_types,
            api_key=api_key,
            dry_run=dry_run,
            json_path=json_path  # Pass json_path to handle todos.json
        )
        
        # Print summary
        if dry_run:
            click.echo(f"Dry Run: {len(todos_to_add)} new TODOs identified.")
            click.echo(f"Dry Run: {len(todos_to_delete)} completed TODOs identified.")
        else:
            logger.info("Synchronization completed successfully.")
            click.echo(f"Sync complete. {len(todos_to_add)} added, {len(todos_to_delete)} completed.")
        
        # Handle exports based on flags
        if export_json:
            todos_data = load_todos_json(json_path)
            export_todos_to_json(todos_data, output_path=json_path)
            click.echo(f"Exported TODOs to JSON file: {json_path}")
        
        if export_md:
            todos_data = load_todos_json(json_path)
            export_todos_to_markdown(todos_data, output_path=md_path or (Path(dir) / "README.md").resolve())
            click.echo(f"Exported TODOs to Markdown file: {md_path or (Path(dir) / 'README.md').resolve()}")

    except Exception as e:
        logger.exception("An error occurred during synchronization.")
        click.echo(f"An error occurred during synchronization: {e}", err=True)

@cli.command()
@click.option(
    '--dir',
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help='Path to the directory containing files.'
)
@click.option(
    '--file-types',
    default='.tex',
    help='Comma-separated list of file extensions to scan for TODOs (e.g., .tex,.py,.md).'
)
@click.option(
    '--export-json',
    is_flag=True,
    help='Export TODOs to a JSON file.'
)
@click.option(
    '--json-path',
    default=None,
    show_default=True,
    help='Path to the output JSON file.'
)
@click.option(
    '--export-md',
    is_flag=True,
    help='Export TODOs as a Markdown table.'
)
@click.option(
    '--md-path',
    default=None,
    show_default=True,
    help='Path to the output Markdown file.'
)
def export(dir, file_types, export_json, json_path, export_md, md_path):
    """
    Export TODOs from files to a JSON file or Markdown table.
    """
    logger = logging.getLogger(__name__)
    
    # Determine the path to todos.json
    if json_path is None:
        json_path = str((Path(dir) / "todos.json").resolve())
    
    if md_path is None:
        md_path = str((Path(dir) / "README.md").resolve())

    file_types = [ext.strip() for ext in file_types.split(',')]

    try:
        logger.info("Extracting TODOs from files.")
        todos = get_all_todos(directory=dir, file_types=file_types)
        logger.info(f"Extracted {len(todos)} TODO(s) from files.")

        # Load existing todos.json or initialize
        todos_data = load_todos_json(json_path)
        existing_todos = {todo['id']: todo for todo in todos_data.get('todos', [])}
        
        # Determine completed todos by checking todos.json
        current_ids = set(todo['id'] for todo in todos)
        all_ids = set(existing_todos.keys())
        completed_ids = all_ids - current_ids
        
        completed_todos = []
        for cid in completed_ids:
            completed_entry = existing_todos[cid]
            completed_entry['completed_at'] = completed_entry.get('completed_at') or "Unknown"
            completed_todos.append(completed_entry)
        
        # Update todos_data with current todos
        updated_todos = [todo for todo in todos]
        # Append completed todos
        updated_todos.extend(completed_todos)
        
        # Save updated todos.json
        todos_data['todos'] = updated_todos
        save_todos_json(todos_data, json_path)
        logger.info(f"Updated todos.json with current and completed TODOs.")

        if export_json:
            export_todos_to_json(todos_data, output_path=json_path)
        
        if export_md:
            export_todos_to_markdown(todos_data, completed_todos=completed_todos, output_path=md_path)
        
        if not (export_json or export_md):
            logger.warning("No export option specified. Use --export-json and/or --export-md.")
            click.echo("No export option specified. Use --export-json and/or --export-md.", err=True)
    
    except Exception as e:
        logger.exception("An error occurred during export.")
        click.echo(f"An error occurred during export: {e}", err=True)


if __name__ == "__main__":
    cli()
