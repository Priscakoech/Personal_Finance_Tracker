
import re

class MarkdownFormatter:
    def __init__(self):
        self.patterns = {
            r'^\#\s*(.*?)$': '[b]\\1[/b]',      # For handling titles...
            r'\*\*(.*?)\*\*': '[b]\\1[/b]',     # For handling subtitles...
            r'\*(.*?)\*': '[b][i]\\1[/i][/b]',  # For handling italics...
            r'^\-\s*(.*?)$': '    • \\1',       # For handling lists...
        }

    def format_text(self, text):
        """Formats the text by applying KivyMD-style markup replacements."""
        for (pattern, replacement) in self.patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        return text
