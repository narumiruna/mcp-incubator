from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from pydantic import Field

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP(
    "Planning MCP Server",
    instructions="You will do everything by using this tool.",
    log_level="ERROR",
)


class Subtask(BaseModel):
    name: str
    description: str

    def __str__(self) -> str:
        return f"{self.name}({self.description})"


class Task(BaseModel):
    name: str
    description: str
    subtasks: list[Subtask]

    def __str__(self) -> str:
        lines = [
            f"- {self.name}({self.description})",
        ]
        for subtask in self.subtasks:
            lines.append(f"  - {subtask}")
        return "\n".join(lines)


class Plan(BaseModel):
    name: str
    description: str
    tasks: list[Task]

    def __str__(self) -> str:
        lines = [
            f"# {self.name}",
            self.description,
            "## Tasks",
        ]
        for task in self.tasks:
            lines.append(f"{task}")
        return "\n".join(lines)


@mcp.tool()
def planning_tool(
    name: Annotated[str, Field(description="Name of the project")],
    description: Annotated[str, Field(description="Description of the project")],
    tasks: Annotated[list[Task], Field(description="List of tasks")],
) -> str:
    """You are a project manager. You need to plan a project. You have a list of tasks. Each task has a name, description, and subtasks. You need to create a plan for the project."""  # noqa: E501
    plan = Plan(name=name, description=description, tasks=tasks)
    return str(plan)


def main():
    mcp.run()
