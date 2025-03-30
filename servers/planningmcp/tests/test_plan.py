from planningmcp.server import Plan
from planningmcp.server import Subtask
from planningmcp.server import Task


def test_plan() -> None:
    plan = Plan(
        name="Test Plan",
        description="This is a test plan.",
        tasks=[
            Task(
                name="Test Task",
                description="This is a test task.",
                subtasks=[
                    Subtask(name="Test Subtask", description="This is a test subtask."),
                    Subtask(name="Test Subtask 2", description="This is another test subtask."),
                ],
            ),
            Task(
                name="Test Task 2",
                description="This is another test task.",
                subtasks=[
                    Subtask(name="Test Subtask 3", description="This is yet another test subtask."),
                ],
            ),
            Task(
                name="Test Task 3",
                description="This is a third test task.",
                subtasks=[
                    Subtask(name="Test Subtask 4", description="This is a fourth test subtask."),
                    Subtask(name="Test Subtask 5", description="This is a fifth test subtask."),
                ],
            ),
        ],
    )
    print(plan)
