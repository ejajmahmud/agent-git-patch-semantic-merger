"""Unit tests for agent-git-patch-semantic-merger."""
import unittest
from agent_git_patch_semantic_merger.core import GitPatchSemanticMerger

class TestGitPatchSemanticMerger(unittest.TestCase):
    def setUp(self):
        self.merger = GitPatchSemanticMerger()

    def test_clean_file_no_conflicts(self):
        text = "def hello(): pass"
        out, count = self.merger.resolve_file(text)
        self.assertEqual(count, 0)
        self.assertEqual(out, text)

    def test_conflict_resolution(self):
        conflict = "<<<<<<< HEAD" + chr(10) + "def a(): pass" + chr(10) + "=======" + chr(10) + "def b(): pass" + chr(10) + ">>>>>>> feat" + chr(10)
        out, count = self.merger.resolve_file(conflict)
        self.assertEqual(count, 1)
        self.assertTrue("def a(): pass" in out)
        self.assertTrue("def b(): pass" in out)
        self.assertFalse("<<<<<<<" in out)
