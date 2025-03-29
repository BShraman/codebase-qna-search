

class StateGraph():
    def __init__(self):
        from core.nodes.document_embedding import DocumentEmbedding
        from core.nodes.vector_db import VectorDB
        from core.nodes.query import Query
        from core.route import RouteState
        
        self.doc_embedding = DocumentEmbedding()
        self.vector_db = VectorDB()
        self.query = Query()
        self.route = RouteState()

    def compiled_graph(self):
        """
        Generates and compiles a state graph for processing codebase operations.

        The graph defines the flow of operations, including conditional branching
        and sequential steps, starting from initializing the collection to querying
        and retrieving responses. It uses nodes and edges to represent the workflow
        and compiles the graph for execution.

        Returns:
            compiled_graph: The compiled state graph ready for execution.
        """
        from core.state import CodebaseState
        from langgraph.graph import StateGraph, END, START

        code_base = StateGraph(CodebaseState)

        # Add nodes
        code_base.add_node("check_collection", self.vector_db.check_collection)
        code_base.add_node("codebase_loader", self.doc_embedding.document_loader)
        code_base.add_node("codebase_embedding", self.doc_embedding.document_embedding)
        code_base.add_node("codebase_vdb", self.vector_db.vector_db)
        code_base.add_node("query_codebase_vdb", self.query.query_vector_db)
        code_base.add_node("get_response", self.query.get_response)

        # Start the edges
        code_base.add_edge(START, "check_collection")
        # Add conditional branching from 
        code_base.add_conditional_edges(
            "check_collection",
            self.route.route_invoke,
            {
                "exists": "query_codebase_vdb",
                "does_not_exist": "codebase_loader"
            })

        # # Add edges - defining the flow
        code_base.add_edge("codebase_loader", "codebase_embedding")

        # Add the final edges
        code_base.add_edge("codebase_embedding", "codebase_vdb")
        code_base.add_edge("codebase_vdb", "query_codebase_vdb")
        code_base.add_edge("query_codebase_vdb", "get_response")
        code_base.add_edge("get_response", END)

        # Compile the graph
        compiled_graph = code_base.compile()

        return compiled_graph