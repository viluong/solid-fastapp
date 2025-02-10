from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenEntity:
    access_token: Optional[str] = None
    token_type: Optional[str] = None
