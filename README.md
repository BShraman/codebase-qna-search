# Codebase QnA Search

## Overview
Codebase QnA Search is a developer tool designed to simplify searching and retrieving answers from codebases. It leverages advanced technologies such as the LlamaIndex for efficient indexing, a Llama Graph for structured data representation, and a robust ingestion pipeline to process and embed code repositories. The application integrates a powerful query engine to enable precise and context-aware searches. Additionally, the Llama workflow orchestrates the interaction between these components, ensuring seamless functionality. With support for OpenAI and Hugging Face APIs, the tool provides embedding, inference, and chat capabilities, making it an indispensable resource for navigating and understanding large codebases.

## Setup Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/codebase-qna-search.git
    cd codebase-qna-search
    ```

2. Create a Python virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt 
    ```

3. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add the following variables:
      ```
      SERVICE= # "openai" or "huggingface" chose 1 and setup rest
      HUGGING_FACE_HUB_TOKEN=<your-df_token>
      OPENAI_API_KEY=<your-openapi-key>
      HF_MODEL_NAME=<df-model-name>
      ```

4. Start the application:
    ```
    python3 main.py
    ```

## Overall Process
**1. Define State**  
    The state represents the current configuration and attributes of the codebase, focusing on document processing, query handling, and storage settings.

**2. Define Nodes**  
    Nodes in the LlamaGraph represent distinct components or entities within the codebase. Each node is responsible for a specific functionality or data, such as representing files, functions, or classes. These nodes are designed to interact with one another through well-defined edges, forming a structured graph. Key nodes include document embedding, vector database operations, and query handling to retrieve responses.

**3. Define Routes**  
    Routes in the LlamaGraph are responsible for determining the flow of processes based on the state .These routes check the existence and validity of collections within the chromadb and dynamically direct the workflow accordingly.

**4. Create State Graph**  
    The state graph is constructed by setting up the initial state, adding nodes, and defining edges to establish the flow of processes. This graph acts as the backbone of the application, connecting various components and ensuring smooth interaction between them. Nodes represent functionalities, while edges define the relationships and transitions, enabling efficient execution of workflows.

**5. Define Edges**  
    Edges in the state graph represent the connections and dependencies between nodes. They define how data flows and processes transition from one node to another.

**6. Run Application**  
    Once the state graph is fully defined, the application can be executed. Running the application initializes the state, processes the codebase, and enables query handling. This step brings together all components, allowing users to interact with the tool and retrieve insights from the codebase seamlessly.

## Compiled Graph
![Compiled Graph](docs/compiled_graph.png)


