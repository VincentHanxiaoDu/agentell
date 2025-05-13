from dataclasses import dataclass


@dataclass
class AgentMsg:
    role: str
    msg: str
