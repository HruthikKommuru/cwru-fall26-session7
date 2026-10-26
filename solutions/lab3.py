"""A deliberately small parser for the five supplied formats."""
import json


def parse_reply(text):
    """Read the first JSON object; return None for unusable input."""
    if not isinstance(text, str) or "{" not in text:
        return None
    try:
        data, _ = json.JSONDecoder().raw_decode(text[text.find("{"):])
        if not isinstance(data, dict):
            return None
        score = data.get("score", "not stated")
        if score != "not stated":
            score = int(score)
        return {"title": data.get("title", "not stated"), "score": score}
    except (json.JSONDecodeError, ValueError, TypeError, OverflowError):
        return None
