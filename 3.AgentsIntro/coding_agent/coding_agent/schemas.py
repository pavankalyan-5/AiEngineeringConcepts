read_file_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": (
            "Read a UTF-8 text file from the agent workspace. "
            "Use this before editing an existing file, or when the user asks what a file contains. "
            "Path must be relative to the workspace, e.g. 'hello.py' or 'src/app.py'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path of the file to read, e.g. 'hello.py'.",
                }
            },
            "required": ["path"],
        },
    },
}

write_file_schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Create or overwrite a UTF-8 text file in the agent workspace. "
            "`content` is the full file body with real newline characters. "
            "Do not wrap content in markdown fences. Do not encode newlines as the two-character sequence \\n."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path of the file to create or overwrite, e.g. 'hello.py'.",
                },
                "content": {
                    "type": "string",
                    "description": "Full file body with real newlines.",
                },
            },
            "required": ["path", "content"],
        },
    },
}

TOOL_MENU = [read_file_schema, write_file_schema]


def tool_catalog() -> list[dict[str, str]]:
    return [
        {
            "name": schema["function"]["name"],
            "description": schema["function"]["description"],
        }
        for schema in TOOL_MENU
    ]
