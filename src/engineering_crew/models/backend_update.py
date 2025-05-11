from pydantic import BaseModel

class BackendImplementationUpdate(BaseModel):
    successfuly_executed: bool
    blocked_by_unimplemented_module: bool
    module_installs_required: list[str]  # List of modules that need to be installed