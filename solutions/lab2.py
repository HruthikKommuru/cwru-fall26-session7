"""Run before Lab 2's Check yourself cell; writes and imports a real module."""
from pathlib import Path
import importlib

MODULE = '\n'.join([
    'def clean_text(text):',
    '    lines = [line.strip() for line in text.splitlines() if line.strip()]',
    '    return "\\n".join(lines)',
    '',
    'def build_prompt(task, tone="plain", max_words=120):',
    '    return f"{task} ({tone}, max {max_words} words)"',
])
Path("lab_tools.py").write_text(MODULE + "\n")
import lab_tools
importlib.reload(lab_tools)
from lab_tools import clean_text, build_prompt
six_inputs = [" Paris ", "", "Lyon", " ", "  Boston", "\t"]
cleaned_inputs = [text.strip() for text in six_inputs if text.strip()]
