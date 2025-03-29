

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
        code_base.add_node("get_collection", self.vector_db.get_collection)
        code_base.add_node("document_loader", self.doc_embedding.document_loader)
        code_base.add_node("document_embedding", self.doc_embedding.document_embedding)
        code_base.add_node("vector_db", self.vector_db.vector_db)
        code_base.add_node("query_vector_db", self.query.query_vector_db)
        code_base.add_node("get_response", self.query.get_response)

        # Start the edges
        code_base.add_edge(START, "get_collection")
        #code_base.add_edge(START, "document_loader")
        # Add conditional branching from 
        code_base.add_conditional_edges(
            "get_collection",
            self.route.route_invoke,
            {
                "exists": "query_vector_db",
                "does_not_exist": "document_loader"
            })

        # # Add edges - defining the flow
        code_base.add_edge("document_loader", "document_embedding")

        # Add the final edges
        code_base.add_edge("document_embedding", "vector_db")
        code_base.add_edge("vector_db", "query_vector_db")
        code_base.add_edge("query_vector_db", "get_response")
        code_base.add_edge("get_response", END)

        # Compile the graph
        compiled_graph = code_base.compile()

        return compiled_graph