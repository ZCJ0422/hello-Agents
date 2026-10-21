"""Backward-compatible entry point for the travel assistant.

Implementation lives in ``src/hello_agents``. Run this file directly to start
the example, or use ``hello-agents`` after installing the project.
"""

from hello_agents.agent import TravelAgent
from hello_agents.llm_client import OpenAICompatibleClient
from hello_agents.main import main
from hello_agents.prompts import AGENT_SYSTEM_PROMPT
from hello_agents.tools import available_tools, get_attraction, get_weather


if __name__ == "__main__":
    main()
