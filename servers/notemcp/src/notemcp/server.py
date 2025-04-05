import difflib
from pathlib import Path
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .env import get_base_dir

INSTRUCTIONS = """
This is the Note MCP Server providing tools for AI assistants to manage user-related notes. As an AI assistant, you can use these tools to:

1. list_note_files: Check what note files already exist in the user's storage directory. Use this to remind yourself of previously saved information.
2. read_note_file: Access the content of specific user notes by filename. This helps you recall previous user information and continue conversations with context.
3. update_note_file: Create new notes or update existing ones when you encounter information worth recording. You can organize notes with subjects, relevant keywords, and detailed content.

You should PROACTIVELY take notes during conversations when you learn important information about the user, such as:
- User preferences, habits, and interests
- Important dates or events mentioned by the user
- Technical details about user projects or environments
- User's goals, challenges, or recurring questions
- Any information that would be valuable for future interactions

Don't wait for explicit instructions to take notes. When you identify valuable information, use the update_note_file tool to record it. Review existing notes at the beginning of conversations to provide continuity.

IMPORTANT: Avoid hallucinations and inaccurate information in your responses and notes:
- Only record information explicitly stated by the user or clearly evident from context
- If you're uncertain about a detail, ask for clarification rather than making assumptions
- Clearly distinguish between facts from notes and your suggestions or inferences
- When providing information from notes, cite the specific note file as your source
- If asked about something not in your notes, acknowledge the information gap instead of fabricating an answer
- Do not blend actual user information with imagined details

These tools are designed to help you, as an AI assistant, maintain persistent memory about user information and provide better continuity in your interactions by referencing and updating notes as needed.
"""  # noqa: E501
# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("Note MCP Server", instructions=INSTRUCTIONS, log_level="ERROR")


@mcp.tool()
def list_note_files() -> str:
    """List all note files in the base directory."""
    base_dir = get_base_dir()
    note_files = list(Path(base_dir).rglob("*.md"))
    if not note_files:
        return "No note files found."
    return "\n".join([str(note_file) for note_file in note_files])


@mcp.tool()
def read_note_file(
    filename: Annotated[str, Field(description="The name of the note file")],
) -> str:
    """Read a note file and return its content."""
    base_dir = get_base_dir()
    note_file = Path(base_dir) / filename
    if not note_file.exists():
        return f"Note file {filename} does not exist."
    return note_file.read_text()


@mcp.tool()
def update_note_file(
    subject: Annotated[str, Field(description="The subject of the notes")],
    keywords: Annotated[list[str], Field(description="The keywords to update")],
    notes: Annotated[list[str], Field(description="The notes to update")],
) -> str:
    """This tool updates notes in a markdown file."""
    filename = Path(f"{subject}.md")

    content = "\n".join(
        [
            f"# {subject}",
            f"keywords: {', '.join(keywords)}",
        ]
        + [f"- {note}" for note in notes],
    )
    if not filename.exists():
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_text(content)
        return f"Note created with file name: {filename}"

    diff = difflib.unified_diff(filename.read_text().splitlines(), content.splitlines(), lineterm="")

    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(content)
    return f"{filename} updated, with diff:\n" + "\n".join(diff)


def main():
    mcp.run()
