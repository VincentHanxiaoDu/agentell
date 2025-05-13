import asyncio
from datetime import datetime
from agentell.agent.agent_task import AgentTask, TaskStatus
from typing import Optional
from agentell.agent import AsyncBaseAgent


class AsyncAgent(AsyncBaseAgent):
    """Async agent class, run async tasks as async coroutines."""

    def __init__(
        self,
        agent_id: Optional[str] = None,
    ):
        super().__init__(agent_id)
        self._task_queue: asyncio.Queue[AgentTask] = asyncio.Queue()
        self._shutdown_event = asyncio.Event()
        self._loop_task = None

    async def start(self):
        self._loop_task = asyncio.create_task(self._run_loop())

    async def submit(self, task: AgentTask):
        if self._shutdown_event.is_set():
            raise RuntimeError("Cannot submit task to terminated agent")
        await self._task_queue.put(task)

    async def shutdown(self, timeout: float = 10):
        self._shutdown_event.set()
        if self._loop_task:
            try:
                await asyncio.wait_for(self._loop_task, timeout=timeout)
            except asyncio.TimeoutError:
                self._loop_task.cancel()

    async def _run_loop(self):
        while not self._shutdown_event.is_set():
            try:
                task = await asyncio.wait_for(self._task_queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            try:
                await self._process(task)
            except Exception as e:

                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.exception = e
            finally:
                task.completed_at = datetime.now()
