#!/usr/bin/python3

from kill_comments import remove_comments
import unittest


class KillCommentsTest(unittest.TestCase):
    def test_single_line_comment_only(self):
        self.assertEqual(remove_comments("%foo"), "%")

    def test_double_comment_marks(self):
        self.assertEqual(remove_comments("%%foo"), "%")
        self.assertEqual(remove_comments("%bar%foo"), "%")

    def test_text_before_comments(self):
        self.assertEqual(remove_comments("foo%bar"), "foo%")
        self.assertEqual(remove_comments("  foo % bar"), "  foo %")

    def test_escaped_percentage(self):
        self.assertEqual(remove_comments("foo\\%bar"), "foo\\%bar")
        self.assertEqual(remove_comments("foo\\\\%bar"), "foo\\\\%")


if __name__ == "__main__":
    unittest.main()
