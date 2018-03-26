"""
Default export format styles.

"""
from enum import Enum


class Styles(Enum):
    DEFAULT = "{{ key | upper }}"
    IDENTITY = "{{ key }}"
    TERRAFORM = "TF_VAR_{{ key }}"
