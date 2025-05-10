from pydantic import BaseModel
from typing import List

class Field(BaseModel):
    """Field model for the engineering crew project."""
    name: str
    type: str
    description: str

class Method(BaseModel):
    """Method model for the engineering crew project."""
    name: str
    description: str
    parameters: List[str]
    return_type: str
    code_snippet: str

class Class(BaseModel):
    """Class model for the engineering crew project."""
    name: str
    description: str
    methods: List[Method]
    fields: List[Field]

class Module(BaseModel):
    """Module model for the engineering crew project."""
    name: str
    description: str
    file_path: str
    classes: List[Class]
    module_dependencies: List[str]

class Design(BaseModel):
    """Design model for the engineering crew project."""
    design: str
    modules: List[Module]
    required_libraries: List[str]