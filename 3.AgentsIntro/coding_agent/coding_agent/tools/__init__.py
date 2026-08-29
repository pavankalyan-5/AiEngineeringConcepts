from coding_agent.tools.read_file import read_file
from coding_agent.tools.write_file import write_file

TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
}

__all__ = ["TOOL_FUNCTIONS", "read_file", "write_file"]
