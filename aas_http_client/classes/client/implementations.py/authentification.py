from enum import Enum


class AuthMethod(Enum):
    basic_auto = 1
    o_auth2 = 2
    bearer = 3
