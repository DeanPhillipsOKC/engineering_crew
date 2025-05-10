from pydantic import BaseModel

class TestImplementationUpdate(BaseModel):
    """Test implementation update model for the engineering crew project."""
    successfuly_executed: bool
    blocked_by_unimplemented_module: bool
    test_results: str  # Add a field to store test results or logs
    test_coverage: float  # Add a field to store test coverage percentage