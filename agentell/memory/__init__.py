import abc


class AgentMemory(abc.ABC):
    def init_memory(self, memory_set_id: str):
        pass

    def retrieve(self, memory_id: str) -> list[dict]:
        pass

    def query(self, memory_set_ids: list[str]) -> list[dict]:
        pass

    def add(self, memory_id: str, message: dict):
        pass
