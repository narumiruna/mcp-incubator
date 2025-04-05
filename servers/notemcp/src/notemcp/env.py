import os
from functools import cache


@cache
def get_base_dir() -> str:
    base_dir = os.getenv("NOTEMCP_BASE_DIR")
    if base_dir is None:
        raise ValueError("NOTEMCP_BASE_DIR environment variable is not set")
    return base_dir
