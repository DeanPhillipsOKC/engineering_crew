from ..models.design import Design

class TaskManager:
    """TaskManager class to manage the design of a system"""

    def __init__(self, design: Design):
        self.design = design

    def get_design(self) -> Design:
        """Get the design of the system"""
        return self.design

    # Remove and return the next module from the design
    def pop_module(self):
        """Pop the next module from the design"""
        if self.design.modules:
            return self.design.modules.pop(0)
        return None