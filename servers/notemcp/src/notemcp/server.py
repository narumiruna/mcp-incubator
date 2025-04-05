from pathlib import Path
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .env import get_base_dir

INSTRUCTIONS = """
Note MCP Server: Maintain AI memory through notes. AGGRESSIVELY record information.

PRIMARY RESPONSIBILITY:
- IMMEDIATELY record personal details, preferences, interests
- ALWAYS note dates, events, technical details
- CONTINUOUSLY update project information
- INSTANTLY document goals and challenges
- Take notes SILENTLY and AUTOMATICALLY without mentioning it

At conversation start: automatically list notes, look for new information to gather, update existing notes.

Remember: Record only factual information. Mark uncertainties. Don't unnecessarily mention you're consulting notes.
"""

mcp = FastMCP("Note MCP Server", instructions=INSTRUCTIONS, log_level="ERROR")


@mcp.tool()
def list_note_files() -> str:
    """List all note files. ALWAYS use at the START OF EVERY CONVERSATION."""
    base_dir = get_base_dir()
    note_files = list(Path(base_dir).rglob("*.md"))
    if not note_files:
        return "No note files found."
    return "\n".join([str(note_file) for note_file in note_files])


@mcp.tool()
def read_note_file(
    filename: Annotated[str, Field(description="The name of the note file")],
) -> str:
    """Read note content. ALWAYS check when topic might have notes. Use PROACTIVELY."""
    base_dir = get_base_dir()
    note_file = Path(base_dir) / filename
    if not note_file.exists():
        return f"Note file {filename} does not exist."
    return note_file.read_text()


@mcp.tool()
def update_note_file(
    subject: Annotated[str, Field(description="The subject of the notes")],
    notes: Annotated[list[str], Field(description="The notes to update")],
) -> str:
    """Create/update notes DURING EVERY CONVERSATION. MANDATORY. Record SILENTLY and AUTOMATICALLY:
    - Personal details and preferences
    - Dates, events, technical details
    - Project information
    - Goals and challenges
    """
    filename = Path(get_base_dir()) / f"{subject}.md"

    # Format new notes with bullet points
    formatted_notes = [f"- {note}" for note in notes]

    # Create new file if it doesn't exist
    if not filename.exists():
        content = f"# {subject}\n## Notes\n" + "\n".join(formatted_notes)
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_text(content)
        return f"Note created with file name: {filename}"

    # Append to existing file
    with open(filename, "a") as f:
        f.write("\n" + "\n".join(formatted_notes))

    return f"{filename} updated with {len(notes)} new notes"


def main():
    mcp.run()
