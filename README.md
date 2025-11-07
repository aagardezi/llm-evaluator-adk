# Multi-LLM Evaluator Agent

This project implements a multi-LLM evaluator agent that takes a user's query, sends it to multiple Large Language Models (LLMs) in parallel, and then evaluates their responses.

## Agent Architecture

The agent is built using the Google Agent Development Kit (ADK) and is composed of several sub-agents that work together in a sequential and parallel manner.

The agent architecture is as follows:

1.  **Orchestrator Agent**: This is the root agent that receives the user's query and orchestrates the entire process. It passes the query to the `sequential_agent`.

2.  **Sequential Agent**: This agent executes a sequence of two sub-agents:
    *   **Data Retrieval Agent**: This is a `ParallelAgent` that sends the user's query to three different LLM agents simultaneously:
        *   **OpenAI Agent**: An `LlmAgent` that uses OpenAI's GPT-4o model.
        *   **Claude Haiku Agent**: An `LlmAgent` that uses Anthropic's Claude Haiku 4.5 model.
        *   **Gemini Agent**: An `LlmAgent` that uses Google's Gemini-2.5-flash model.
    *   **Evaluator Agent**: This `LlmAgent` takes the responses from the three LLMs and generates a detailed report comparing them based on the following criteria:
        *   Accuracy
        *   Completeness
        *   Conciseness
        *   Relevance
        *   Coherence
        *   Faithfulness
        *   Safety
        *   Efficiency
        *   Diversity

The evaluator agent then provides an overall winner among the three LLMs.

![alt text](https://github.com/aagardezi/llm-evaluator-adk/blob/main/agent.png)

## Use Cases

This multi-LLM evaluator agent can be used for various purposes, including:

*   **LLM Performance Comparison**: Compare the performance of different LLMs for specific tasks or domains.
*   **Prompt Engineering**: Evaluate the effectiveness of different prompts for the same task.
*   **Quality Assurance**: Ensure the quality and consistency of LLM responses.
*   **Model Selection**: Choose the best LLM for a particular application based on its performance on a set of evaluation queries.

## Installation

To run this project, you need to have Python 3.12 or higher installed. You also need to install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r multi_llm_evaluator_agent/requirements.txt
```

You also need to have a Google Cloud project with the Vertex AI API enabled.

## Usage

To use the agent, you need to set the `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` environment variables. You also need to have the necessary permissions to access the Vertex AI API and the Secret Manager API.

The agent can be run locally or deployed to the Vertex AI Agent Engine.

## Deployment

The agent can be deployed to the Vertex AI Agent Engine using the `deploy.py` script. The `adk_deploy.sh` and `agentenginedeploy.sh` scripts can also be used for deployment.

### `adk_deploy.sh`

This script deploys the agent to the Agent Engine using the `adk deploy` command.

```bash
./adk_deploy.sh
```

### `agentenginedeploy.sh`

This script sends a POST request to the Discovery Engine API to create a new agent.

```bash
./agentenginedeploy.sh
```

## Dependencies

The project dependencies are listed in the `multi_llm_evaluator_agent/requirements.txt` file.
