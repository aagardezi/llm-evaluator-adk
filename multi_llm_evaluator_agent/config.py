import os
from dataclasses import dataclass


@dataclass
class EvaluatorAgentConfiguration:

    # gemini_model: str = "gemini-flash-latest"
    # gemini_model: str = "gemini-2.5-flash-preview-09-2025"
    gemini_model: str = "gemini-2.5-flash"
    claude_haiku: str = "claude-haiku-4-5"
    openai_litellm_model: str = "openai/gpt-4o"

    evaluator_model: str = "gemini-2.5-pro"


config = EvaluatorAgentConfiguration()