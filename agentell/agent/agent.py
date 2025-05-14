import abc
from .agent_task import AgentTask
from typing import Optional
import uuid


class BaseAgent(abc.ABC):
    """Base class for all agents."""

    def __init__(self, agent_id: Optional[str] = None):
        if agent_id is None:
            agent_id = str(uuid.uuid4())
        self._agent_id = agent_id

    @abc.abstractmethod
    def start(self):
        """Start the agent."""
        pass

    @abc.abstractmethod
    def _process(self, task: AgentTask):
        """Process a task."""
        pass

    @abc.abstractmethod
    def submit(self, task: AgentTask):
        """Submit a task to the agent."""
        pass

    @abc.abstractmethod
    def shutdown(self, timeout: float = 10):
        """Shutdown the agent."""
        pass

    def __enter__(self):
        """Enter the context of the agent."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context of the agent."""
        self.shutdown()


class AsyncBaseAgent(abc.ABC):
    def __init__(
        self,
        agent_id: Optional[str] = None,
    ):
        if agent_id is None:
            agent_id = str(uuid.uuid4())
        self._agent_id = agent_id

    @abc.abstractmethod
    async def start(self):
        pass

    @abc.abstractmethod
    async def submit(self, task: AgentTask):
        pass

    @abc.abstractmethod
    async def _process(self, task: AgentTask):
        pass

    @abc.abstractmethod
    async def shutdown(self, timeout: float = 10):
        pass

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.shutdown()


class SyncAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id=agent_id)

    def submit(self, task: AgentTask):
        self._process(task=task)
