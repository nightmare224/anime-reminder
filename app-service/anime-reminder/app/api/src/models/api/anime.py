import re
from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest


@dataclass
class Anime_Reminder():
    season: Optional[str] = None
    episode: Optional[str] = None
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)

@dataclass
class Anime():
    anime_id: Optional[str] = None
    anime_name: Optional[str] = None
    anime_reminder: Union[List[dict], List[Anime_Reminder]] = field(default_factory = list)
    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)

        reminders = []
        for r in self.anime_reminder:
            if type(r) is dict:
                reminders.append(Anime_Reminder(**r))
            else:
                reminders.append(r)
        self.anime_reminder = reminders
