from __future__ import annotations

import json
from collections.abc import Callable

from coding_agent.client import get_client_and_model
from coding_agent.config import MAX_TURNS, MAX_TOKENS
from coding_agent.prompts import build_system_prompt
from coding_agent.schemas import TOOL_MENU
from coding_agent.tools import TOOL_FUNCTIONS

OnToolCall = Callable[[str, dict], None]


def parse_tool_arguments(arguments: str | dict | None) -> dict:
    if arguments is None or arguments == "":
        return {}
    if isinstance(arguments, dict):
        return arguments
    return json.loads(arguments)


def run_agent_turns(
    messages: list,
    max_turns: int = MAX_TURNS,
    on_tool_call: OnToolCall | None = None,
) -> str:
    client, model, _ = get_client_and_model()

    working = [
        {
            "role": "system",
            "content": build_system_prompt(),
        },
        *messages,
    ]

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=model,
            messages=working,
            tools=TOOL_MENU,
            max_tokens=MAX_TOKENS,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content or ""
            messages.append({"role": "assistant", "content": answer})
            return answer

        working.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": (
                                call.function.arguments
                                if isinstance(call.function.arguments, str)
                                else json.dumps(call.function.arguments)
                            ),
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        for call in message.tool_calls:
            name = call.function.name
            if name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {name}"
            else:
                arguments = parse_tool_arguments(call.function.arguments)
                if on_tool_call is not None:
                    on_tool_call(name, arguments)
                result = TOOL_FUNCTIONS[name](**arguments)

            working.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": call.id,
                }
            )

    fallback = "Stopped after hitting max_turns without a final answer"
    messages.append({"role": "assistant", "content": fallback})
    return fallback
