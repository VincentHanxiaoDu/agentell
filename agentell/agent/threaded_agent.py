from typing import Optional
from .agent_task import AgentTask, TaskStatus
from .base import BaseAgent
import threading
import queue
from datetime import datetime


class ThreadedAgent(BaseAgent):
    """Threaded agent class, run tasks in the background in a separate thread."""

    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id=agent_id)
        self._thread = None
        self._task_queue: queue.Queue[AgentTask] = queue.Queue()
        self._terminate_event = threading.Event()

    def start(self):
        self._thread = ProcessThread(self)
        self._thread.start()

    def submit(self, task: AgentTask):
        if self._terminate_event.is_set():
            raise RuntimeError("Cannot submit task to terminated agent")
        self._task_queue.put(task)

    def shutdown(self, timeout: float = 10):
        self._terminate_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)


class ProcessThread(threading.Thread):
    """Thread that processes tasks."""

    def __init__(self, agent: ThreadedAgent):
        super().__init__(f"{agent._agent_id}-thread", daemon=True)
        self._agent = agent

    def run(self):
        while not self._agent._terminate_event.is_set():
            try:
                task = self._agent._task_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self._agent._process(task)
                self._agent._task_queue.task_done()
            except Exception as e:
                task.exception = e
                task.error = str(e)
                task.status = TaskStatus.FAILED
            finally:
                task.completed_at = datetime.now()
