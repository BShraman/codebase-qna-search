from core.state import CodebaseState

class RouteState:
    """Handles routing decisions based on codebase state"""
    def __init__(self):
        pass

    def route_invoke(self, state: dict) -> dict:
        """Determine the next step based on document parsing"""
        if state.get("is_chromadb_exists", True):
            output = "exists"
        else:
            output = "does_not_exist"
        
        return output

    