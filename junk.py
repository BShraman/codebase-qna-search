
from core.state import CodebaseState

class StateGraph():
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.route = RouteState()

    def compiled_graph(self):
        # Create the graph
        from langgraph.graph import StateGraph, END, START
        code_base = StateGraph(CodebaseState)

        code_base.add_node("get_collection", self.vector_db.get_collection if hasattr(self.vector_db, 'get_collection') else None)
        code_base.add_node("get_collection", self.vector_db.get_collection)

        # Start the edges
        code_base.add_edge(START, "get_collection")
        # # Add conditional branching from 
        code_base.add_conditional_edges(
            "get_collection",
            self.route.route_invoke,
            {
                "exists": "query_vector_db",
                "does_not_exist": "document_loader"
            }
        )

        # Add edges - defining the flow
        code_base.add_edge("document_loader", END)

        # Compile the graph
        compiled_graph = code_base.compile()

        return compiled_graph
    

class RouteState(CodebaseState):
    def __init__(self):
        pass

    def route_invoke(self, state: CodebaseState) -> str:
        """Determine the next step based on document parsing"""
        if state["is_chromadb_exists"] is True:
            return "exists"
        else:
            return "does_not_exist"