from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid
from agentell.agent.agent_msg import AgentMsg
import enum
from typing import Any, Optional

@enum.unique
class TaskStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    msgs: List[AgentMsg] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    exception: Optional[Exception] = None
    result: Any = None
