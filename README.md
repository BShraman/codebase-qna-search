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

## Compiled Graph
![Compiled Graph](docs/compiled_graph.png)


