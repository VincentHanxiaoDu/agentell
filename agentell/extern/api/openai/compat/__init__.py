from agentell.extern.chat import ChatLLM


class OpenAICompatAPI(ChatLLM):
    """OpenAI compat API."""

    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url
        self._auth_header = {"Authorization": f"Bearer {self._api_key}"}
        self._completions_url = f"{self._base_url}/chat/completions"
