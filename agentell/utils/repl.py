import sys
from typing import Iterator


class REPLHandler:
    @staticmethod
    def push(iterator: Iterator[str], end: str = ""):
        buffer = ""
        for chunk in iterator:
            buffer += chunk
            sys.stdout.write(chunk)
            sys.stdout.flush()
        sys.stdout.write(end)
        sys.stdout.flush()
        return buffer

    @staticmethod
    def get_input() -> str:
        return sys.stdin.readline()
