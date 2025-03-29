## Overview
Codebase QnA Search is a powerful tool designed to help developers efficiently navigate and understand large codebases. It leverages the **LlamaIndex Framework** for advanced indexing and embedding, enabling the creation of a vector database that supports fast and accurate searches. Additionally, the **LangGraph Framework** is utilized to organize data into a structured state graph, defining workflows and interactions between various components of the codebase.

## Frameworks Used
The application leverages the following frameworks to deliver its functionality:

1. **LlamaIndex Framework**:
    - Provides advanced indexing and embedding capabilities.
    - Enables the creation of a vector database for fast and accurate searches.

2. **LangGraph Framework**:
    - Organizes data into a structured state graph.
    - Defines workflows and interactions between various components of the codebase.

3. **ChromaDB**:
    - Serves as a high-performance vector database.
    - Stores and retrieves embeddings for efficient query processing.

4. **OpenAI API**:
    - Powers natural language processing and understanding.
    - Facilitates query handling and response generation.

## Setup Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/codebase-qna-search.git
    cd codebase-qna-search
    ```

2. Set up a Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt 
    ```

3. Configure environment variables:
    - Create a `.env` file in the root directory.
    - Add these variables:
      ```
      SERVICE= # Choose "openai" or "huggingface"
      HUGGING_FACE_HUB_TOKEN=<your-token>
      OPENAI_API_KEY=<your-api-key>
      HF_MODEL_NAME=<model-name>
      ```

4. Run the application:
    ```bash
    python3 main.py
    ```
    *Update query inside the application before running*

## How It Works
1. **Define State**: Set up the configuration for processing documents, handling queries, and storing data.
2. **Define Nodes**: Nodes represent parts of the codebase like files, functions, or classes. They work together in a structured graph.
3. **Define Routes**: Routes guide the workflow by checking collections in the database and directing processes.
4. **Create State Graph**: Build a graph connecting nodes and edges to define workflows and interactions.
5. **Define Edges**: Edges show how nodes are connected and how data flows between them.
6. **Run Application**: Start the tool to process the codebase and handle queries.

## Compiled Graph
![Compiled Graph](docs/compiled_graph.png)

## Application Run and Output
As part of the application run, it will first check the collection name in the vector database (VectorDB). If the collection does not exist, the application will create it and output the query result. If the collection already exists, it will query the collection and return the result. Below is an example of the application's output:

**Collection Doesnt Exists**
![Collection Exists](docs/exists.png)

**Collection Exists**
![Collection Exists](docs/doesnotExists.png)




