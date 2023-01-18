import re
from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest

@dataclass
class Anime():
    anime_id: Optional[str] = None
    anime_name: Optional[str] = None
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)