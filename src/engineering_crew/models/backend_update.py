from pydantic import BaseModel

class BackendImplementationUpdate(BaseModel):
    successfuly_executed: bool
    blocked_by_unimplemented_module: bool