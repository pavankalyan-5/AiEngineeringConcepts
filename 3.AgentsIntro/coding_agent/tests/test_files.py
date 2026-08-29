import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coding_agent.tools.read_file import read_file
from coding_agent.tools.write_file import write_file
from coding_agent.tools import TOOL_FUNCTIONS


class FileToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.work = Path(self._tmp.name) / "workspace"
        self.work.mkdir()
        self.workspace_patch = patch(
            "coding_agent.tools.paths.WORKSPACE_DIR",
            self.work,
        )
        self.workspace_patch.start()

    def tearDown(self) -> None:
        self.workspace_patch.stop()
        self._tmp.cleanup()

    def test_write_then_read_roundtrip(self) -> None:
        status = write_file("hello.py", "print('hi')\n")
        self.assertIn("written", status.lower())
        self.assertEqual(read_file("hello.py"), "print('hi')\n")
        self.assertTrue((self.work / "hello.py").is_file())

    def test_write_creates_parent_directories(self) -> None:
        write_file("src/pkg/mod.py", "x = 1\n")
        self.assertEqual(read_file("src/pkg/mod.py"), "x = 1\n")

    def test_read_missing_file_returns_error_string(self) -> None:
        result = read_file("missing.py")
        self.assertIn("not found", result.lower())

    def test_read_escape_returns_error_string(self) -> None:
        result = read_file("../outside.txt")
        self.assertIn("workspace", result.lower())

    def test_registry_maps_names_to_functions(self) -> None:
        self.assertEqual(set(TOOL_FUNCTIONS), {"read_file", "write_file"})
        self.assertIs(TOOL_FUNCTIONS["read_file"], read_file)
        self.assertIs(TOOL_FUNCTIONS["write_file"], write_file)


if __name__ == "__main__":
    unittest.main()
