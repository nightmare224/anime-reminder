import re
from dataclasses import dataclass, field
from typing import List, Union, Optional
from dataclass_type_validator import dataclass_type_validator
from lib.api.exceptions import OtherBadRequest
# from models.api.anime import Anime

@dataclass
class User():
    user_id: Optional[str] = None
    # email: Optional[str] = None
    # username: Optional[str] = None
    # department: Optional[str] = None
    # enabled: bool = True
    # email_verified: bool = False
    def __post_init__(self):
        # TODO: enabled = enabled & email_verified ?
        # self.enabled = self.enabled and self.email_verified
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise OtherBadRequest(e.errors)
        # email
        # try:
        #     if self.email and not re.match(r"^\S+@\S+$", self.email):
        #         raise ValueError
        # except:
        #     raise OtherBadRequest("invaild email format")

# @dataclass
# class User_Anime():
#     anime_id: Optional[str] = None
#     anime_reminder: Union[List[dict], List[Anime_Reminder]] = field(default_factory = list)
#     # email: Optional[str] = None
#     # username: Optional[str] = None
#     # department: Optional[str] = None
#     # enabled: bool = True
#     # email_verified: bool = False
#     def __post_init__(self):
#         # TODO: enabled = enabled & email_verified ?
#         # self.enabled = self.enabled and self.email_verified
#         try:
#             dataclass_type_validator(self)
#         except Exception as e:
#             raise OtherBadRequest(e.errors)
#         # email
#         # try:
#         #     if self.email and not re.match(r"^\S+@\S+$", self.email):
#         #         raise ValueError
#         # except:
#         #     raise OtherBadRequest("invaild email format")