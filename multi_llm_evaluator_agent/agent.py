import datetime
import os
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, ParallelAgent, SequentialAgent, LlmAgent
from google.adk.tools import agent_tool, AgentTool
from google.adk.tools import google_search
from .config import config
import google.auth

from . import helpercode


from google.genai import types

from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode

from google.adk.models.lite_llm import LiteLlm

from google.adk.models.anthropic_llm import Claude
from google.adk.models.registry import LLMRegistry

PROJECT_ID = helpercode.get_project_id()

os.environ["OPENAI_API_KEY"] = helpercode.access_secret_version(PROJECT_ID, "OpenAIAccessKey")

agent_openai = LlmAgent(
    model=LiteLlm(model=config.openai_litellm_model), # LiteLLM model string format
    name="agent_openai",
    description=(
        "Agent to get answers to users queries via OpenAI"
    ),
    instruction="You are a helpful assistant powered by GPT-4o. You answer the users request to the best of your ability",
    output_key="openai_result"
)

LLMRegistry.register(Claude)

agent_claude_haiku_vertexai = LlmAgent(
    model=config.claude_haiku, # Pass the direct string after registration
    name="agent_claude_haiku_vertexai",
    description=(
        "Agent to get answers to users queries via Claude Haiku"
    ),
    instruction="You are a helpful assistant powered by Claude Haiku 4.5. You answer the users request to the best of your ability",
    output_key="claude_haiku_result"
)

agent_gemini_vertexai = LlmAgent(
    name="agent_gemini_vertexai",
    model=config.gemini_model,
    description=(
        "Agent to get answers to users queries via Claude Haiku"
    ),
    instruction="You are a helpful assistant powered by Claude Haiku 4.5. You answer the users request to the best of your ability",
    output_key="gemini_result"
)

data_retrieval_agent = ParallelAgent(
    name="data_retrieval_agent",
    description=(
        "You are an agent executes user queries against multiple sub agents in parallel"
    ),
    sub_agents=[agent_claude_haiku_vertexai, agent_gemini_vertexai, agent_openai]
)

evaluator_agent = LlmAgent(
    name="evaluator_agent",
    model=config.gemini_model,
    description=(
        "Agent to evaluate and compare answers from multiple LLM agents"
    ),
    instruction=(
        """
        You are an evaluator agent that compares answers from the multiple agents using different llms.
        You should evaluat the response on different criteria such as:
        Accuracy
        Completeness
        Conciseness
        Relevance
        Coherence
        Faithfulness
        Safety
        Efficiency
        Diversity

        The input responses are here:
        Gemini model version: Gemini-2.5-flash, Response: {gemini_result}
        Claude model version: Claude Haiku 4.5, Response: {claude_haiku_result}
        OpenAI model version: GPT-4o, Response: {openai_result}

        Create a detailed report with a table that gives are rating for each of the LLMs above against the criteira
        Give an explanation for your rating.
        Give an overall winner at the end.
        Be completely impratial when evaluating the response from the different LLMs
        Format the response in markdown
        """
    ),
    output_key="gemini_result"
)

sequential_agent = SequentialAgent(
    name="sequential_agent",
    description=(
        "you are the agent that runs the process for collecting the data and creating the response"
    ),
    sub_agents=[data_retrieval_agent, evaluator_agent]
)

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=config.gemini_model,
    description=(
        "Agent to evaluate and compare answers from multiple LLM agents"
    ),
    instruction=(
        """
        You are the orchistrator agent that takes the users queries and sends them to the sub agents to run against multiple LLMs.
        The data_retrieval_agent calls the sub agents in paralles. Make sure you pass the same query to each sub agent faithfully
        Do not answer the question your self, let the sub agents do the work.
        Every sub agent should execute the same query as the users input without any modification.
        Finally the evaluator_agent will evaluate the response.
        """
    ),
    sub_agents=[sequential_agent]
)

root_agent = orchestrator_agent