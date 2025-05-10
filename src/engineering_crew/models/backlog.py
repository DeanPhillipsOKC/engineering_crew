from pydantic import BaseModel

class BackLogItem(BaseModel):
    """Backlog item model for the engineering crew project."""
    title: str
    module_name_no_extension: str
    description: str

class Backlog(BaseModel):
    """Backlog model for the engineering crew project."""
    items: list[BackLogItem]