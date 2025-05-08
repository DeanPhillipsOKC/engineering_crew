from typing import Optional, List, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pydantic import BaseModel

# Module‑level in‑memory storage
class EngineeringTask(BaseModel):
    """Schema for a task."""
    id: int
    description: str
    completed: bool = False

_tasks: List[EngineeringTask] = []
_next_id: int = 1


class AddTaskInput(BaseModel):
    """Schema for adding a new task."""
    description: str = Field(
        ..., description="Description of the task to add."
    )


class AddTaskTool(BaseTool):
    name: str = "add_task"
    description: str = (
        "Add a new user‑story‑style task to the tracker."
    )
    args_schema: Type[BaseModel] = AddTaskInput

    def _run(self, description: str) -> str:
        global _next_id, _tasks
        task  = EngineeringTask(
            id=_next_id,
            description=description,
            completed=False
        )
        _tasks.append(task)
        _next_id += 1
        return f"Task added: [ID {task.id}] {task.description}"

    async def _arun(self, description: str) -> str:
        return self._run(description)


class ListTasksInput(BaseModel):
    """Schema for listing tasks. No arguments currently needed."""
    pass


class ListTasksTool(BaseTool):
    name: str = "list_tasks"
    description: str = (
        "List all tasks and their completion status in the tracker."
    )
    args_schema: Type[BaseModel] = ListTasksInput

    def _run(self) -> List[EngineeringTask]:
        return _tasks

    async def _arun(self) -> str:
        return self._run()

class GetNextActiveTaskInput(BaseModel):
    """Schema for listing tasks. No arguments currently needed."""
    pass

class GetNextActiveTaskTool(BaseTool):
    name: str = "get_next_active_task"
    description: str = (
        "Get the next active task in the tracker."
    )
    args_schema: Type[BaseModel] = GetNextActiveTaskInput

    def _run(self) -> Optional[EngineeringTask]:
        for task in _tasks:
            if not task.completed:
                return task
        return None

    async def _arun(self) -> str:
        return self._run()

class CompleteTaskInput(BaseModel):
    """Schema for completing a task."""
    task_id: int = Field(
        ..., description="ID of the task to mark complete."
    )


class CompleteTaskTool(BaseTool):
    name: str = "complete_task"
    description: str = (
        "Mark an existing task as complete."
    )
    args_schema: Type[BaseModel] = CompleteTaskInput

    def _run(self, task_id: int) -> str:
        for task in _tasks:
            if task.id == task_id:
                if task.completed:
                    return f"Task ID {task_id} is already completed."
                task.completed = True
                return f"Task completed: [ID {task_id}]"
        return f"Error: No task found with ID {task_id}."

    async def _arun(self, task_id: int) -> str:
        return self._run(task_id)