from core.state import CodebaseState

class RouteState(CodebaseState):
    """
    Represents the state of the codebase with various attributes related to
    routing and decision-making.
    """
    def __init__(self):
        # Initilizing CodebaseState
        super().__init__()

    def route_invoke(self, state: CodebaseState) -> str:
        """Determine the next step based on document parsing"""
        if state.get("is_chromadb_exists", True):
            return "exists"
        else:
            return "does_not_exist"