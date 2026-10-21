"""Agent loop and parsing for the travel assistant."""

import re
from typing import Callable, Dict, Optional

from .prompts import AGENT_SYSTEM_PROMPT


class TravelAgent:
    """Run the thought/action loop using an LLM and a tool registry."""

    def __init__(self, llm, tools: Dict[str, Callable], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps

    def run(self, user_prompt: str) -> Optional[str]:
        history = [f"用户请求: {user_prompt}"]
        print(f"用户输入: {user_prompt}\n" + "=" * 40)

        for step in range(self.max_steps):
            print(f"--- 循环 {step + 1} ---\n")
            output = self.llm.generate("\n".join(history), AGENT_SYSTEM_PROMPT)
            output = self._first_turn(output)
            print(f"模型输出:\n{output}\n")
            history.append(output)

            action_match = re.search(r"Action:\s*(.*)", output)
            if not action_match:
                observation = "错误: 未能解析到 Action 字段。请确保回复包含 Action。"
            else:
                action = action_match.group(1).strip()
                finish_match = re.fullmatch(r"Finish\[(.*)\]", action, re.DOTALL)
                if finish_match:
                    answer = finish_match.group(1)
                    print(f"任务完成，最终答案: {answer}")
                    return answer
                observation = self._run_tool(action)

            observation_line = f"Observation: {observation}"
            print(f"{observation_line}\n" + "=" * 40)
            history.append(observation_line)

        print("已达到最大执行轮数，任务未完成。")
        return None

    @staticmethod
    def _first_turn(output: str) -> str:
        match = re.search(
            r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
            output,
            re.DOTALL,
        )
        return match.group(1).strip() if match else output.strip()

    def _run_tool(self, action: str) -> str:
        call_match = re.fullmatch(r"(\w+)\((.*)\)", action)
        if not call_match:
            return "错误:无法解析 Action。请使用工具名(参数名=\"参数值\") 格式。"

        tool_name, args_text = call_match.groups()
        kwargs = dict(re.findall(r'(\w+)="([^\"]*)"', args_text))
        tool = self.tools.get(tool_name)
        if tool is None:
            return f"错误:未定义的工具 '{tool_name}'"
        try:
            return tool(**kwargs)
        except TypeError as exc:
            return f"错误:工具 '{tool_name}' 的参数不正确 - {exc}"
