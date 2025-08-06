# Document Summarization 

The Document Summarization sample application demonstrates how to leverage the LlamaIndex framework, a powerful framework for building applications with large language models (LLMs), to generate concise and informative summaries from long-form documents. By integrating LlamaIndex framework, the application efficiently processes and understands textual content, enabling users to extract key information and insights from a variety of document types. This approach streamlines content review, enhances searchability, and supports advanced use cases such as knowledge management and automated reporting. 

## Get Started

To see the system requirements and other installation, see the following guides:

  - [System Requirements](docs/user-guide/system-requirements.md): Hardware and software requirements for running the sample application.
  - [Get Started](docs/user-guide/get-started.md): Step-by-step guide to get started with the sample application.

## Architecture

The Document Summarization sample application uses AI models to summarize documents. It offers a REST API and a web UI, built with scalable microservices.

The following figure shows the microservices required to implement the Document Summarization sample application.

![Technical Architecture Diagram of Document Summarization](.docs/user-guide/images/DocSum-Arch.png)

The components are as follows:

  -  **NGINX Web Server-based Reverse Proxy**
    - **Role:** Routes external requests to the appropriate backend service (API or UI).
    - **Configuration:** `nginx.conf`
    - **Port:** `8101` (external)

  -  **Gradio UI-based UI** (`docsum-ui`)
    - **Role:** Provides a web interface for users to upload documents and view summaries.
    - **Implementation:** `ui/gradio_app.py`
    - **Port:** `9998` (external, mapped to `7860` in container)
    - **Depends on:** `docsum-api`

  - **DocSum Backend Platform** (`docsum-api`)
    - **Role:** Handles REST API requests for document summarization and file uploads; and orchestrates the summarization pipeline.
    - **Implementation:** `app/server.py`
    - **Port:** `8090` (external, mapped to 8000 in container)
    - **Depends on:** OVMS Model Server (for LLM inference)

  -  **LLM on OpenVINO™ Model Server** (`ovms-service`)
    - **Role:** Serves AI models (e.g., LLMs) for inference.
    - **Configuration:** Loads models from a mounted volume.
    - **Ports:** `9300` (gRPC), `8300` (REST)

For more details on Architecture, see [How it works](docs/user-guide/how-it-works.md).

## Learn More

- **Overview**
  - [Overview](docs/user-guide/Overview.md): A high-level introduction.
  - [Overview Architecture](docs/user-guide/overview-architecture.md): Detailed architecture.
  - [How to Build from Source](docs/user-guide/build-from-source.md): Instructions for building from source code.
  - [How to Deploy with Helm Chart](docs/user-guide/deploy-with-helm.md): Guide for deploying using Helm chart.
  - [FAQ](docs/user-guide/faq.md): Answers for common questions.
  - [API Reference](docs/user-guide/api-reference.md): Comprehensive reference for the available REST API endpoints.
  - [Release Notes](docs/user-guide/release-notes.md): Information on the latest updates, improvements, and bug fixes.
