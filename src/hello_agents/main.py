"""Application entry point for the travel assistant."""

import argparse
import os
from pathlib import Path

from .agent import TravelAgent
from .llm_client import OpenAICompatibleClient
from .tools import available_tools


DEFAULT_USER_PROMPT = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"


def _load_project_env() -> None:
    """Load KEY=VALUE entries from the project .env without overriding shell values."""
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if not env_file.is_file():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        name, separator, value = line.partition("=")
        name = name.strip()
        if not separator or not name or name in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        os.environ[name] = value


def main() -> None:
    """Load configuration and run the assistant."""
    parser = argparse.ArgumentParser(description="旅行助手")
    parser.add_argument(
        "prompt",
        nargs="?",
        default=DEFAULT_USER_PROMPT,
        help="要交给旅行助手处理的问题",
    )
    args = parser.parse_args()

    # Read project-local settings, without replacing values already exported
    # in the shell.
    _load_project_env()

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL")
    missing = [
        name
        for name, value in (
            ("OPENAI_API_KEY", api_key),
            ("OPENAI_BASE_URL", base_url),
            ("OPENAI_MODEL", model),
        )
        if not value
    ]
    if missing:
        raise SystemExit("请先设置环境变量: " + ", ".join(missing))

    llm = OpenAICompatibleClient(model=model, api_key=api_key, base_url=base_url)
    TravelAgent(llm, available_tools).run(args.prompt)
