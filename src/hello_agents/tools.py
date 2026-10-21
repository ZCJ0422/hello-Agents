"""External tools available to the travel assistant."""

import os

import requests
from tavily import TavilyClient


def get_weather(city: str) -> str:
    """Query current weather for a city through wttr.in."""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        current = response.json()["current_condition"][0]
        description = current["weatherDesc"][0]["value"]
        temperature = current["temp_C"]
        return f"{city}当前天气:{description}，气温{temperature}摄氏度"
    except requests.exceptions.RequestException as exc:
        return f"错误:查询天气时遇到网络问题 - {exc}"
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {exc}"


def get_attraction(city: str, weather: str) -> str:
    """Search for attractions suitable for a city's current weather."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "错误:未配置TAVILY_API_KEY环境变量。"

    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    try:
        response = TavilyClient(api_key=api_key).search(
            query=query, search_depth="basic", include_answer=True
        )
        if response.get("answer"):
            return response["answer"]

        results = [
            f"- {result.get('title', '无标题')}: {result.get('content', '')}"
            for result in response.get("results", [])
        ]
        if not results:
            return "抱歉，没有找到相关的旅游景点推荐。"
        return "根据搜索，为您找到以下信息:\n" + "\n".join(results)
    except Exception as exc:
        return f"错误:执行Tavily搜索时出现问题 - {exc}"


available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}
