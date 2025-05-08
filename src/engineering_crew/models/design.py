from pydantic import BaseModel

class DesignField(BaseModel):
    """Represents the design on how to implement a field in a class"""
    name: str
    description: str
    requirements: str

class DesignMethod(BaseModel):
    """Represents the design on how to implement a method in a class"""
    name: str
    description: str
    prototype: str
    requirements: str

class DesignClass(BaseModel):
    """Represents the design on how to implement a class"""
    name: str
    description: str
    requirements: str
    methods: list[DesignMethod]
    fields: list[DesignField]


class DesignModule(BaseModel):
    """Represents the design on how to implement a module"""
    name: str
    description: str
    file_path: str
    requirements: str
    classes: list[DesignClass]

class Design(BaseModel):
    """Represents the design on how to implement all modules in a system"""
    requirements: str
    folder_structure: str
    best_practices: str
    architecture_standards: str
    modules: list[DesignModule]