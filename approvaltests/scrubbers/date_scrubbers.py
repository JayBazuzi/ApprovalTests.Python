import re
from typing import Callable


def scrub_with_regex(regex: str, callable: Callable[[int], str]) -> Callable[[str],str]:
    def scrub(text: str) -> str:
        matches = []
        def find_index(string: str ) -> int:
            if not string in matches:
                matches.append(string)
            return matches.index(string)
        return re.sub(regex, lambda m: callable(find_index(m.group(0))), text)
    return scrub


def scrub_all_dates(d: str) -> str:
    return scrub_with_regex(r'\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}', lambda t: f'<date{t}>')(d)

