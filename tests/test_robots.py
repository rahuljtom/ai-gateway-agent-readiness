import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scan as s
ROBOTS = """User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
User-agent: CCBot
Disallow: /
Allow: /

User-agent: *
Disallow: /admin
"""
class T(unittest.TestCase):
    def setUp(self): self.g = s.parse_robots(ROBOTS)
    def test_named_block(self): self.assertTrue(s.blocked(self.g, "GPTBot"))
    def test_allow_root_beats_block(self): self.assertFalse(s.blocked(self.g, "ClaudeBot"))
    def test_star_group_used_when_unnamed(self): self.assertFalse(s.blocked(self.g, "PerplexityBot"))
    def test_blanket_block_applies(self): self.assertTrue(s.blocked(s.parse_robots("User-agent: *\nDisallow: /\n"), "GPTBot"))
    def test_html_is_not_a_text_file(self): self.assertFalse(s.valid_text_file(200, "text/html", "<!doctype html>"))
if __name__ == "__main__": unittest.main()
