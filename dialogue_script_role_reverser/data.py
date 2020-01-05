"""Pythonic representation of dialogue data."""

from dataclasses import dataclass
from typing import List


@dataclass
class Choice:

    player: str
    target: str


@dataclass
class Node():

    id: str
    npc: str
    choices: List[Choice]

