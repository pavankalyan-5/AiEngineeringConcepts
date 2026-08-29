import tempfile
import unittest
from pathlib import Path

from coding_agent.tools.paths import resolve_work_path


class ResolveWorkPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.work = Path(self._tmp.name) / "workspace"
        self.work.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_resolves_relative_file_inside_workspace(self) -> None:
        resolved = resolve_work_path("hello.py", work_dir=self.work)
        self.assertEqual(resolved, (self.work / "hello.py").resolve())

    def test_allows_nested_relative_path(self) -> None:
        resolved = resolve_work_path("src/app.py", work_dir=self.work)
        self.assertEqual(resolved, (self.work / "src" / "app.py").resolve())

    def test_rejects_empty_path(self) -> None:
        with self.assertRaises(ValueError):
            resolve_work_path("", work_dir=self.work)

    def test_rejects_parent_escape(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            resolve_work_path("../secret.txt", work_dir=self.work)
        self.assertIn("workspace", str(ctx.exception).lower())

    def test_rejects_absolute_path_outside_workspace(self) -> None:
        with self.assertRaises(ValueError):
            resolve_work_path("/etc/passwd", work_dir=self.work)


if __name__ == "__main__":
    unittest.main()
